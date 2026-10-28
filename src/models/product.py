
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.db import Base


class Product(Base):
    """A product sold by the store."""

    __tablename__ = "products"

    __table_args__ = (
        CheckConstraint("length(trim(sku)) > 0", name="ck_product_sku_not_blank"),
        CheckConstraint("length(trim(name)) > 0", name="ck_product_name_not_blank"),
        CheckConstraint(
            "length(trim(category)) > 0",
            name="ck_product_category_not_blank",
        ),
        CheckConstraint("cost_price >= 0", name="ck_product_cost_nonnegative"),
        CheckConstraint(
            "selling_price >= 0",
            name="ck_product_selling_price_nonnegative",
        ),
        CheckConstraint(
            "low_stock_threshold >= 0",
            name="ck_product_low_stock_threshold_nonnegative",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    sku: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(String(150), nullable=False)

    category: Mapped[str] = mapped_column(String(100), nullable=False)

    supplier: Mapped[str | None] = mapped_column(String(150), nullable=True)

    cost_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=Decimal("0.00"),
    )

    selling_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=Decimal("0.00"),
    )

    low_stock_threshold: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    batches: Mapped[list["Batch"]] = relationship(
        "Batch",
        back_populates="product",
        cascade="all, delete-orphan",
    )
