
from datetime import date, datetime, timezone
from decimal import Decimal
from typing import Any

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from src.models.batch import Batch
from src.models.product import Product


def create_product(
    session: Session,
    *,
    sku: str,
    name: str,
    category: str,
    cost_price: Decimal = Decimal("0.00"),
    selling_price: Decimal = Decimal("0.00"),
    supplier: str | None = None,
    low_stock_threshold: int = 0,
) -> Product:
    """Create a product after validating its input."""

    if not sku.strip():
        raise ValueError("SKU cannot be blank.")
    if not name.strip():
        raise ValueError("Product name cannot be blank.")
    if not category.strip():
        raise ValueError("Category cannot be blank.")
    if cost_price < 0 or selling_price < 0:
        raise ValueError("Prices cannot be negative.")
    if low_stock_threshold < 0:
        raise ValueError("Low-stock threshold cannot be negative.")

    product = Product(
        sku=sku.strip(),
        name=name.strip(),
        category=category.strip(),
        cost_price=cost_price,
        selling_price=selling_price,
        supplier=supplier.strip() if supplier and supplier.strip() else None,
        low_stock_threshold=low_stock_threshold,
    )

    session.add(product)
    try:
        session.commit()
        session.refresh(product)
    except IntegrityError as exc:
        session.rollback()
        raise ValueError(
            f"Could not create product. SKU '{sku}' may already exist."
        ) from exc

    return product


def get_product(
    session: Session,
    product_id: int,
    *,
    include_inactive: bool = False,
) -> Product | None:
    """Retrieve one product, including its batches."""

    statement = (
        select(Product)
        .options(selectinload(Product.batches))
        .where(Product.id == product_id)
    )

    if not include_inactive:
        statement = statement.where(Product.is_active.is_(True))

    return session.scalar(statement)


def list_products(
    session: Session,
    *,
    include_inactive: bool = False,
) -> list[Product]:
    """List products with their associated batches."""

    statement = select(Product).options(selectinload(Product.batches))

    if not include_inactive:
        statement = statement.where(Product.is_active.is_(True))

    statement = statement.order_by(Product.name, Product.id)
    return list(session.scalars(statement).all())


def update_product(
    session: Session,
    product_id: int,
    **changes: Any,
) -> Product:
    """Update permitted product fields."""

    product = session.get(Product, product_id)
    if product is None:
        raise ValueError(f"Product {product_id} does not exist.")

    allowed_fields = {
        "sku",
        "name",
        "category",
        "supplier",
        "cost_price",
        "selling_price",
        "low_stock_threshold",
    }

    unknown_fields = set(changes) - allowed_fields
    if unknown_fields:
        raise ValueError(
            f"Fields cannot be updated: {', '.join(sorted(unknown_fields))}"
        )

    for field in ("sku", "name", "category"):
        if field in changes:
            value = changes[field]
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field} cannot be blank.")
            changes[field] = value.strip()

    for field in ("cost_price", "selling_price"):
        if field in changes:
            value = changes[field]
            if not isinstance(value, Decimal):
                raise ValueError(f"{field} must be a Decimal value.")
            if value < 0:
                raise ValueError(f"{field} cannot be negative.")

    if "low_stock_threshold" in changes:
        value = changes["low_stock_threshold"]
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError("Low-stock threshold must be a non-negative integer.")

    if "supplier" in changes:
        value = changes["supplier"]
        if value is not None and not isinstance(value, str):
            raise ValueError("Supplier must be text or None.")
        changes["supplier"] = value.strip() or None if value else None

    for field, value in changes.items():
        setattr(product, field, value)

    try:
        session.commit()
        session.refresh(product)
    except IntegrityError as exc:
        session.rollback()
        raise ValueError(
            "Could not update product. Check that its SKU is unique "
            "and all values are valid."
        ) from exc

    return product


def deactivate_product(session: Session, product_id: int) -> Product:
    """Deactivate a product without deleting its inventory history."""

    product = session.get(Product, product_id)
    if product is None:
        raise ValueError(f"Product {product_id} does not exist.")

    product.is_active = False
    session.commit()
    session.refresh(product)
    return product


def add_batch(
    session: Session,
    *,
    product_id: int,
    batch_code: str,
    quantity_received: int,
    expiry_date: date,
    received_at: datetime | None = None,
) -> Batch:
    """Add a stock batch to an existing active product."""

    product = session.get(Product, product_id)

    if product is None or not product.is_active:
        raise ValueError("An existing active product is required.")
    if not batch_code.strip():
        raise ValueError("Batch code cannot be blank.")
    if (
        isinstance(quantity_received, bool)
        or not isinstance(quantity_received, int)
        or quantity_received <= 0
    ):
        raise ValueError("Received quantity must be a positive integer.")
    if not isinstance(expiry_date, date) or isinstance(expiry_date, datetime):
        raise ValueError("Expiry date must be a date.")
    if received_at is not None and not isinstance(received_at, datetime):
        raise ValueError("Received time must be a datetime.")

    batch = Batch(
        product_id=product_id,
        batch_code=batch_code.strip(),
        quantity_received=quantity_received,
        quantity_remaining=quantity_received,
        expiry_date=expiry_date,
        received_at=received_at or datetime.now(timezone.utc),
    )

    session.add(batch)
    try:
        session.commit()
        session.refresh(batch)
    except IntegrityError as exc:
        session.rollback()
        raise ValueError("Could not save the stock batch.") from exc

    return batch


def get_total_stock(session: Session, product_id: int) -> int:
    """Calculate a product's total stock from its batches."""

    product = session.get(Product, product_id)
    if product is None:
        raise ValueError(f"Product {product_id} does not exist.")

    return sum(
        batch.quantity_remaining
        for batch in session.scalars(
            select(Batch).where(Batch.product_id == product_id)
        ).all()
    )


def adjust_batch_stock(
    session: Session,
    batch_id: int,
    quantity_change: int,
) -> Batch:
    """Adjust a batch's remaining stock without allowing invalid quantities.

    quantity_change can be positive or negative, but cannot be zero.
    A positive adjustment cannot raise stock above the quantity received.
    """

    if (
        isinstance(quantity_change, bool)
        or not isinstance(quantity_change, int)
        or quantity_change == 0
    ):
        raise ValueError("Stock adjustment must be a non-zero integer.")

    batch = session.get(Batch, batch_id)
    if batch is None:
        raise ValueError(f"Batch {batch_id} does not exist.")

    new_quantity = batch.quantity_remaining + quantity_change

    if new_quantity < 0:
        raise ValueError("Insufficient stock: quantity cannot become negative.")
    if new_quantity > batch.quantity_received:
        raise ValueError("Stock cannot exceed the batch's received quantity.")

    batch.quantity_remaining = new_quantity
    session.commit()
    session.refresh(batch)
    return batch
