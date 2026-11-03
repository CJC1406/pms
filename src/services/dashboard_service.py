from datetime import date, datetime, time, timedelta, timezone
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.models.invoice import Invoice
from src.models.product import Product
from src.services.expiry_service import get_expiring_batches
from src.services.inventory_service import get_total_stock, list_products


def get_dashboard_summary(
    session: Session,
    *,
    as_of: date | None = None,
) -> dict:
    """Calculate dashboard figures directly from stored database records."""

    today = as_of or date.today()

    products = list_products(session)
    total_products = len(products)

    low_stock = sum(
        1
        for product in products
        if get_total_stock(session, product.id)
        <= product.low_stock_threshold
    )

    expiring_batches = get_expiring_batches(
        session,
        days=7,
        as_of=today,
    )

    expiring_quantity = sum(
        batch.quantity_remaining for batch in expiring_batches
    )

    start = datetime.combine(today, time.min, tzinfo=timezone.utc)
    end = start + timedelta(days=1)

    daily_sales = session.scalar(
        select(func.coalesce(func.sum(Invoice.total), 0)).where(
            Invoice.created_at >= start,
            Invoice.created_at < end,
        )
    )

    invoice_count = session.scalar(
        select(func.count(Invoice.id)).where(
            Invoice.created_at >= start,
            Invoice.created_at < end,
        )
    )

    return {
        "total_products": total_products,
        "low_stock": low_stock,
        "expiring_batches": len(expiring_batches),
        "expiring_quantity": expiring_quantity,
        "daily_sales": Decimal(str(daily_sales or 0)),
        "invoice_count": invoice_count or 0,
        "waste_status": "Not implemented",
    }
