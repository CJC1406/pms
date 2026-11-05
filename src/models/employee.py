from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.db import Base


class Employee(Base):
    """A store employee who can be assigned as a cashier."""

    __tablename__ = "employees"

    __table_args__ = (
        CheckConstraint(
            "length(trim(employee_code)) > 0",
            name="ck_employee_code_not_blank",
        ),
        CheckConstraint(
            "length(trim(full_name)) > 0",
            name="ck_employee_name_not_blank",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    employee_code: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
        index=True,
    )

    full_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    email: Mapped[str | None] = mapped_column(
        String(254),
        unique=True,
        nullable=True,
    )

    phone: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    role: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="Cashier",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    invoices: Mapped[list["Invoice"]] = relationship(
        "Invoice",
        back_populates="employee",
    )