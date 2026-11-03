from datetime import date

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from src.models.batch import Batch
from src.models.product import Product
from src.services.invoice_service import create_invoice_record


def complete_checkout(
    session: Session,
    *,
    cashier: str,
    items: list[dict],
    customer_mobile: str | None = None,
    customer_email: str | None = None,
    as_of: date | None = None,
):
    """Create an invoice and deduct valid stock in one transaction."""

    if not isinstance(items, list) or not items:
        raise ValueError("Checkout must contain at least one item.")

    quantities: dict[int, int] = {}

    for item in items:
        if not isinstance(item, dict):
            raise ValueError("Each checkout item must be a dictionary.")

        product_id = item.get("product_id")
        quantity = item.get("quantity")

        if (
            isinstance(product_id, bool)
            or not isinstance(product_id, int)
            or product_id <= 0
        ):
            raise ValueError("Product ID must be a positive integer.")

        if (
            isinstance(quantity, bool)
            or not isinstance(quantity, int)
            or quantity <= 0
        ):
            raise ValueError("Quantity must be a positive integer.")

        quantities[product_id] = quantities.get(product_id, 0) + quantity

    try:
        product_ids = sorted(quantities)

        products = list(
            session.scalars(
                select(Product)
                .where(
                    Product.id.in_(product_ids),
                    Product.is_active.is_(True),
                )
                .order_by(Product.id)
                .with_for_update()
            ).all()
        )

        if len(products) != len(product_ids):
            raise ValueError("Checkout contains a missing or inactive product.")

        batch_allocations: list[tuple[int, int]] = []
        today = as_of or date.today()

        # Validate stock and allocate batches using FEFO.
        for product_id in product_ids:
            requested = quantities[product_id]

            batches = list(
                session.scalars(
                    select(Batch)
                    .where(
                        Batch.product_id == product_id,
                        Batch.quantity_remaining > 0,
                        Batch.expiry_date >= today,
                    )
                    .order_by(Batch.expiry_date, Batch.id)
                    .with_for_update()
                ).all()
            )

            available = sum(batch.quantity_remaining for batch in batches)

            if requested > available:
                raise ValueError(
                    f"Insufficient valid stock for product {product_id}. "
                    f"Requested {requested}, available {available}."
                )

            remaining = requested

            for batch in batches:
                if remaining <= 0:
                    break

                deduction = min(batch.quantity_remaining, remaining)
                batch_allocations.append((batch.id, deduction))
                remaining -= deduction

        # Create invoice within the same transaction.
        invoice = create_invoice_record(
            session,
            cashier=cashier,
            items=[
                {
                    "product_id": product_id,
                    "quantity": quantities[product_id],
                }
                for product_id in product_ids
            ],
            customer_mobile=customer_mobile,
            customer_email=customer_email,
        )

        # Conditional updates protect against stock changing after validation.
        for batch_id, deduction in batch_allocations:
            result = session.execute(
                update(Batch)
                .where(
                    Batch.id == batch_id,
                    Batch.quantity_remaining >= deduction,
                )
                .values(
                    quantity_remaining=Batch.quantity_remaining - deduction
                )
            )

            if result.rowcount != 1:
                raise ValueError(
                    "Stock changed during checkout. Please retry the sale."
                )

        session.commit()
        session.refresh(invoice)

        return invoice

    except Exception:
        session.rollback()
        raise