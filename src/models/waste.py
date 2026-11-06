from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.db import Base


class WasteRecord(Base):
    """A recorded write-off from a specific inventory batch."""

    __tablename__ = "waste_records"
    __table_args__ = (
        CheckConstraint("quantity > 0", name="ck_waste_quantity_positive"),
        CheckConstraint("unit_cost >= 0", name="ck_waste_unit_cost_nonnegative"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    batch_id: Mapped[int] = mapped_column(
        ForeignKey("batches.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    reason: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    recorded_by: Mapped[str] = mapped_column(String(120), nullable=False)
    notes: Mapped[str | None] = mapped_column(String(500), nullable=True)
    unit_cost: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False,
        default=lambda: datetime.now(timezone.utc), index=True,
    )

    batch = relationship("Batch")

    @property
    def estimated_cost(self) -> Decimal:
        return self.unit_cost * self.quantity
