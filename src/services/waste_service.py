from datetime import date, datetime, time, timedelta, timezone
from decimal import Decimal

from sqlalchemy import func, select, update
from sqlalchemy.orm import Session, joinedload

from src.models.batch import Batch
from src.models.product import Product
from src.models.waste import WasteRecord

WASTE_REASONS = (
    "Expired", "Damaged", "Spoiled", "Contaminated", "Quality Issue", "Other",
)


def record_waste(
    session: Session,
    *,
    batch_id: int,
    quantity: int,
    reason: str,
    recorded_by: str,
    notes: str | None = None,
    recorded_at: datetime | None = None,
) -> WasteRecord:
    """Write off stock and persist its waste record atomically."""
    if isinstance(batch_id, bool) or not isinstance(batch_id, int) or batch_id <= 0:
        raise ValueError("Batch ID must be a positive integer.")
    if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
        raise ValueError("Waste quantity must be a positive integer.")
    if reason not in WASTE_REASONS:
        raise ValueError("Select a valid waste reason.")
    if not isinstance(recorded_by, str) or not recorded_by.strip():
        raise ValueError("Recorded-by name cannot be blank.")
    if notes is not None and (not isinstance(notes, str) or len(notes) > 500):
        raise ValueError("Notes must be 500 characters or fewer.")
    if recorded_at is not None and not isinstance(recorded_at, datetime):
        raise ValueError("Recorded time must be a datetime.")

    try:
        batch = session.scalar(
            select(Batch).where(Batch.id == batch_id).with_for_update()
        )
        if batch is None:
            raise ValueError("Selected batch does not exist.")
        product = session.get(Product, batch.product_id)
        if product is None:
            raise ValueError("The batch product does not exist.")
        if quantity > batch.quantity_remaining:
            raise ValueError(
                f"Insufficient batch stock. Requested {quantity}, "
                f"available {batch.quantity_remaining}."
            )

        result = session.execute(
            update(Batch)
            .where(Batch.id == batch_id, Batch.quantity_remaining >= quantity)
            .values(quantity_remaining=Batch.quantity_remaining - quantity)
        )
        if result.rowcount != 1:
            raise ValueError("Stock changed while recording waste. Please retry.")

        record = WasteRecord(
            batch_id=batch_id,
            quantity=quantity,
            reason=reason,
            recorded_by=recorded_by.strip(),
            notes=notes.strip() or None if notes else None,
            unit_cost=Decimal(str(product.cost_price)),
            recorded_at=recorded_at or datetime.now(timezone.utc),
        )
        session.add(record)
        session.commit()
        session.refresh(record)
        return record
    except Exception:
        session.rollback()
        raise


def list_waste_records(
    session: Session, *, start_date: date | None = None,
    end_date: date | None = None, product_id: int | None = None,
    reason: str | None = None,
) -> list[WasteRecord]:
    statement = select(WasteRecord).options(
        joinedload(WasteRecord.batch).joinedload(Batch.product)
    )
    if start_date:
        statement = statement.where(
            WasteRecord.recorded_at >= datetime.combine(start_date, time.min, timezone.utc)
        )
    if end_date:
        statement = statement.where(
            WasteRecord.recorded_at < datetime.combine(
                end_date + timedelta(days=1), time.min, timezone.utc
            )
        )
    if product_id is not None:
        statement = statement.join(WasteRecord.batch).where(Batch.product_id == product_id)
    if reason:
        statement = statement.where(WasteRecord.reason == reason)
    return list(session.scalars(statement.order_by(WasteRecord.recorded_at.desc(), WasteRecord.id.desc())).unique())


def get_waste_summary(session: Session, *, start_date: date | None = None,
                      end_date: date | None = None) -> dict:
    records = list_waste_records(session, start_date=start_date, end_date=end_date)
    by_reason: dict[str, int] = {}
    by_product: dict[str, int] = {}
    for record in records:
        by_reason[record.reason] = by_reason.get(record.reason, 0) + record.quantity
        name = record.batch.product.name
        by_product[name] = by_product.get(name, 0) + record.quantity
    return {
        "record_count": len(records),
        "total_quantity": sum(r.quantity for r in records),
        "estimated_cost": sum((r.estimated_cost for r in records), Decimal("0.00")),
        "by_reason": by_reason,
        "by_product": by_product,
    }
