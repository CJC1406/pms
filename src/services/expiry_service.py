
from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.batch import Batch
from src.models.product import Product


def get_expired_batches(
    session: Session,
    *,
    as_of: date | None = None,
) -> list[Batch]:
    """
    Return batches that have expired and still contain stock.

    A batch is expired when its expiry date is earlier than today.
    """

    today = as_of or date.today()

    statement = (
        select(Batch)
        .join(Product, Batch.product_id == Product.id)
        .where(
            Batch.expiry_date < today,
            Batch.quantity_remaining > 0,
            Product.is_active.is_(True),
        )
        .order_by(Batch.expiry_date, Batch.id)
    )

    return list(session.scalars(statement).all())


def get_expiring_batches(
    session: Session,
    *,
    days: int = 7,
    as_of: date | None = None,
) -> list[Batch]:
    """
    Return batches expiring today or within the next N days.
    """

    if isinstance(days, bool) or not isinstance(days, int) or days < 0:
        raise ValueError("Days must be a non-negative integer.")

    today = as_of or date.today()
    last_day = today + timedelta(days=days)

    statement = (
        select(Batch)
        .join(Product, Batch.product_id == Product.id)
        .where(
            Batch.expiry_date >= today,
            Batch.expiry_date <= last_day,
            Batch.quantity_remaining > 0,
            Product.is_active.is_(True),
        )
        .order_by(Batch.expiry_date, Batch.id)
    )

    return list(session.scalars(statement).all())


def get_fefo_batches(
    session: Session,
    product_id: int,
    *,
    as_of: date | None = None,
) -> list[Batch]:
    """
    Return available batches in First Expiring, First Out order.

    Excludes expired batches, depleted batches, and inactive products.
    """

    today = as_of or date.today()

    statement = (
        select(Batch)
        .join(Product, Batch.product_id == Product.id)
        .where(
            Batch.product_id == product_id,
            Batch.expiry_date >= today,
            Batch.quantity_remaining > 0,
            Product.is_active.is_(True),
        )
        .order_by(Batch.expiry_date, Batch.id)
    )

    return list(session.scalars(statement).all())
