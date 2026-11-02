
from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.database.db import Base
from src.models.invoice import Invoice, InvoiceItem
from src.services.inventory_service import create_product
from src.services.invoice_service import (
    generate_invoice,
    get_invoice,
    get_invoice_by_number,
)


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    TestingSession = sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
    )

    Base.metadata.create_all(engine)

    with TestingSession() as db:
        yield db

    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def product(session):
    return create_product(
        session,
        sku="APPLE-001",
        name="Apple",
        category="Fruit",
        selling_price=Decimal("15.00"),
    )


def test_generate_invoice_and_calculate_total(session, product):
    invoice = generate_invoice(
        session,
        cashier="Chris",
        customer_mobile="9876543210",
        customer_email="customer@example.com",
        items=[
            {"product_id": product.id, "quantity": 3},
        ],
    )

    assert invoice.id is not None
    assert invoice.invoice_number.startswith("PMS-")
    assert invoice.cashier == "Chris"
    assert invoice.customer_mobile == "9876543210"
    assert invoice.customer_email == "customer@example.com"
    assert invoice.subtotal == Decimal("45.00")
    assert invoice.total == Decimal("45.00")

    assert len(invoice.items) == 1
    assert invoice.items[0].product_name == "Apple"
    assert invoice.items[0].quantity == 3
    assert invoice.items[0].unit_price == Decimal("15.00")
    assert invoice.items[0].line_total == Decimal("45.00")


def test_invoice_number_is_unique(session, product):
    first = generate_invoice(
        session,
        cashier="Cashier A",
        items=[{"product_id": product.id, "quantity": 1}],
    )

    second = generate_invoice(
        session,
        cashier="Cashier B",
        items=[{"product_id": product.id, "quantity": 1}],
    )

    assert first.invoice_number != second.invoice_number


def test_invoice_can_be_retrieved_by_id_and_number(session, product):
    invoice = generate_invoice(
        session,
        cashier="Chris",
        items=[{"product_id": product.id, "quantity": 2}],
    )

    by_id = get_invoice(session, invoice.id)
    by_number = get_invoice_by_number(session, invoice.invoice_number)

    assert by_id is not None
    assert by_number is not None
    assert by_id.invoice_number == invoice.invoice_number
    assert by_number.id == invoice.id
    assert len(by_id.items) == 1


@pytest.mark.parametrize(
    "cashier,items",
    [
        ("", [{"product_id": 1, "quantity": 1}]),
        ("Chris", []),
        ("Chris", [{"product_id": 1, "quantity": 0}]),
        ("Chris", [{"product_id": 1, "quantity": -1}]),
        ("Chris", [{"product_id": 9999, "quantity": 1}]),
        ("Chris", [{"product_id": True, "quantity": 1}]),
        ("Chris", [{"product_id": 1, "quantity": True}]),
    ],
)
def test_invoice_rejects_invalid_input(session, cashier, items):
    with pytest.raises(ValueError):
        generate_invoice(
            session,
            cashier=cashier,
            items=items,
        )


def test_invoice_without_customer_contact(session, product):
    invoice = generate_invoice(
        session,
        cashier="Chris",
        items=[{"product_id": product.id, "quantity": 1}],
    )

    assert invoice.customer_mobile is None
    assert invoice.customer_email is None


def test_invoice_does_not_change_inventory(session, product):
    from src.services.inventory_service import add_batch, get_total_stock
    from datetime import date

    add_batch(
        session,
        product_id=product.id,
        batch_code="TEST-BATCH",
        quantity_received=10,
        expiry_date=date(2027, 12, 31),
    )

    stock_before = get_total_stock(session, product.id)

    generate_invoice(
        session,
        cashier="Chris",
        items=[{"product_id": product.id, "quantity": 2}],
    )

    stock_after = get_total_stock(session, product.id)

    assert stock_before == stock_after == 10
