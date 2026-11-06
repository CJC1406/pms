
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from src.models.employee import Employee
from src.models.invoice import Invoice, InvoiceItem
from src.models.product import Product


CENT = Decimal("0.01")


def _money(value: Decimal) -> Decimal:
    """Round monetary values to two decimal places."""
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


def create_invoice_record(
    session: Session,
    *,
    cashier: str,
    items: list[dict],
    customer_mobile: str | None = None,
    customer_email: str | None = None,
    employee_id: int | None = None,
) -> Invoice:
    """
    Create and persist an invoice from checkout items.

    Each item must contain:
        product_id: int
        quantity: positive int

    Prices and product details are captured at invoice time.
    This function does not deduct stock or send email.
    """

    if not isinstance(cashier, str) or not cashier.strip():
        raise ValueError("Cashier cannot be blank.")

    if not isinstance(items, list) or not items:
        raise ValueError("Invoice must contain at least one item.")

    if customer_mobile is not None and not isinstance(customer_mobile, str):
        raise ValueError("Customer mobile must be text or None.")

    if customer_email is not None and not isinstance(customer_email, str):
        raise ValueError("Customer email must be text or None.")

    employee = None

    if employee_id is not None:
        if (
            isinstance(employee_id, bool)
            or not isinstance(employee_id, int)
            or employee_id <= 0
        ):
            raise ValueError("Employee ID must be a positive integer.")

        employee = session.get(Employee, employee_id)

        if employee is None:
            raise ValueError("Employee does not exist.")

        if not employee.is_active:
            raise ValueError("Inactive employees cannot process sales.")

        cashier = employee.full_name

    invoice_items: list[InvoiceItem] = []
    subtotal = Decimal("0.00")

    for item in items:
        if not isinstance(item, dict):
            raise ValueError("Each invoice item must be a dictionary.")

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

        product = session.scalar(
            select(Product).where(
                Product.id == product_id,
                Product.is_active.is_(True),
            )
        )

        if product is None:
            raise ValueError(
                f"Active product {product_id} does not exist."
            )

        unit_price = _money(Decimal(product.selling_price))
        line_total = _money(unit_price * quantity)
        subtotal += line_total

        invoice_items.append(
            InvoiceItem(
                product_id=product.id,
                product_name=product.name,
                sku=product.sku,
                quantity=quantity,
                unit_price=unit_price,
                line_total=line_total,
            )
        )

    subtotal = _money(subtotal)

    invoice = Invoice(
        invoice_number=(
            f"PMS-{datetime.now(timezone.utc):%Y%m%d}-"
            f"{uuid4().hex[:12].upper()}"
        ),
        created_at=datetime.now(timezone.utc),
        cashier=cashier.strip(),
        employee_id=employee.id if employee else None,
        customer_mobile=(
            customer_mobile.strip()
            if customer_mobile and customer_mobile.strip()
            else None
        ),
        customer_email=(
            customer_email.strip()
            if customer_email and customer_email.strip()
            else None
        ),
        subtotal=subtotal,
        total=subtotal,
        items=invoice_items,
    )

    session.add(invoice)
    session.flush()

    return invoice


def generate_invoice(
    session: Session,
    *,
    cashier: str,
    items: list[dict],
    customer_mobile: str | None = None,
    customer_email: str | None = None,
    employee_id: int | None = None,
) -> Invoice:
    """Create and persist an invoice independently of inventory."""

    try:
        invoice = create_invoice_record(
            session,
            cashier=cashier,
            items=items,
            customer_mobile=customer_mobile,
            customer_email=customer_email,
            employee_id=employee_id,
        )

        session.commit()
        session.refresh(invoice)

        return invoice

    except Exception:
        session.rollback()
        raise


def get_invoice(
    session: Session,
    invoice_id: int,
) -> Invoice | None:
    """Retrieve an invoice and its persisted line items."""

    statement = (
        select(Invoice)
        .options(
            selectinload(Invoice.items),
            selectinload(Invoice.employee),
        )
        .where(Invoice.id == invoice_id)
    )

    return session.scalar(statement)


def get_invoice_by_number(
    session: Session,
    invoice_number: str,
) -> Invoice | None:
    """Retrieve an invoice using its unique invoice number."""

    statement = (
        select(Invoice)
        .options(
            selectinload(Invoice.items),
            selectinload(Invoice.employee),
        )
        .where(Invoice.invoice_number == invoice_number)
    )

    return session.scalar(statement)
