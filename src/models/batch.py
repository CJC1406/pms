
from datetime import date, datetime, timezone

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.db import Base
from src.models.product import Product


class Batch(Base):
    """A specific lot of stock belonging to a product."""

    __tablename__ = "batches"

    __table_args__ = (
        CheckConstraint(
            "length(trim(batch_code)) > 0",
            name="ck_batch_code_not_blank",
        ),
        CheckConstraint(
            "quantity_received > 0",
            name="ck_batch_quantity_received_positive",
        ),
        CheckConstraint(
            "quantity_remaining >= 0",
            name="ck_batch_quantity_remaining_nonnegative",
        ),
        CheckConstraint(
            "quantity_remaining <= quantity_received",
            name="ck_batch_remaining_lte_received",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    batch_code: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
        index=True,
    )

    quantity_received: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    quantity_remaining: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    expiry_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    received_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="batches",
    )
