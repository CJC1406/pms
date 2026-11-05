
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.db import Base


class Invoice(Base):
    """Persisted invoice generated from a checkout."""

    __tablename__ = "invoices"

    __table_args__ = (
        CheckConstraint("length(trim(invoice_number)) > 0"),
        CheckConstraint("length(trim(cashier)) > 0"),
        CheckConstraint("subtotal >= 0"),
        CheckConstraint("total >= 0"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    invoice_number: Mapped[str] = mapped_column(
        String(40),
        unique=True,
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    cashier: Mapped[str] = mapped_column(String(150), nullable=False)

    employee_id: Mapped[int | None] = mapped_column(
        ForeignKey("employees.id"),
        nullable=True,
        index=True,
    )

    employee: Mapped["Employee | None"] = relationship(
        "Employee",
        back_populates="invoices",
    )

    customer_mobile: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    customer_email: Mapped[str | None] = mapped_column(
        String(254),
        nullable=True,
    )

    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    total: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    items: Mapped[list["InvoiceItem"]] = relationship(
        "InvoiceItem",
        back_populates="invoice",
        cascade="all, delete-orphan",
    )


class InvoiceItem(Base):
    """A product line stored as a historical invoice snapshot."""

    __tablename__ = "invoice_items"

    __table_args__ = (
        CheckConstraint("quantity > 0"),
        CheckConstraint("unit_price >= 0"),
        CheckConstraint("line_total >= 0"),
        CheckConstraint("length(trim(product_name)) > 0"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    invoice_id: Mapped[int] = mapped_column(
        ForeignKey("invoices.id"),
        nullable=False,
        index=True,
    )

    product_id: Mapped[int | None] = mapped_column(
        ForeignKey("products.id"),
        nullable=True,
    )

    product_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    sku: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    line_total: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    invoice: Mapped["Invoice"] = relationship(
        "Invoice",
        back_populates="items",
    )
