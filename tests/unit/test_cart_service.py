from decimal import Decimal
from datetime import date

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.database.db import Base
from src.services.inventory_service import create_product, add_batch
from src.services.cart_service import (
    add_cart_item,
    update_cart_quantity,
    remove_cart_item,
    calculate_cart_totals,
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


def create_stocked_product(session, quantity=10):
    product = create_product(
        session,
        sku="CART-001",
        name="Apple",
        category="Fruit",
        selling_price=Decimal("15.00"),
    )

    add_batch(
        session,
        product_id=product.id,
        batch_code="CART-BATCH-001",
        quantity_received=quantity,
        expiry_date=date(2027, 12, 31),
    )

    return product


def test_add_cart_item(session):
    product = create_stocked_product(session)
    cart = {}

    item = add_cart_item(session, cart, product.id, 3)

    assert item["quantity"] == 3
    assert item["unit_price"] == Decimal("15.00")
    assert item["line_total"] == Decimal("45.00")


def test_add_same_product_increases_quantity(session):
    product = create_stocked_product(session)
    cart = {}

    add_cart_item(session, cart, product.id, 2)
    item = add_cart_item(session, cart, product.id, 3)

    assert item["quantity"] == 5
    assert item["line_total"] == Decimal("75.00")


def test_add_cart_item_rejects_quantity_above_stock(session):
    product = create_stocked_product(session)
    cart = {}

    with pytest.raises(ValueError):
        add_cart_item(session, cart, product.id, 11)


@pytest.mark.parametrize("quantity", [0, -1, True, 1.5])
def test_add_cart_item_rejects_invalid_quantity(session, quantity):
    product = create_stocked_product(session)
    cart = {}

    with pytest.raises(ValueError):
        add_cart_item(session, cart, product.id, quantity)


def test_update_cart_quantity(session):
    product = create_stocked_product(session)
    cart = {}

    add_cart_item(session, cart, product.id, 2)
    item = update_cart_quantity(session, cart, product.id, 4)

    assert item["quantity"] == 4
    assert item["line_total"] == Decimal("60.00")


def test_update_quantity_rejects_above_stock(session):
    product = create_stocked_product(session)
    cart = {}

    add_cart_item(session, cart, product.id, 2)

    with pytest.raises(ValueError):
        update_cart_quantity(session, cart, product.id, 11)


def test_remove_cart_item(session):
    product = create_stocked_product(session)
    cart = {}

    add_cart_item(session, cart, product.id, 2)
    remove_cart_item(cart, product.id)

    assert product.id not in cart


def test_calculate_cart_totals():
    items = [
        {"quantity": 2, "unit_price": Decimal("15.00")},
        {"quantity": 1, "unit_price": Decimal("20.00")},
    ]

    totals = calculate_cart_totals(
        items,
        tax_rate=Decimal("10"),
        discount_rate=Decimal("5"),
    )

    assert totals["subtotal"] == Decimal("50.00")
    assert totals["discount_amount"] == Decimal("2.50")
    assert totals["tax_amount"] == Decimal("4.75")
    assert totals["total"] == Decimal("52.25")


@pytest.mark.parametrize(
    "tax,discount",
    [
        (-1, 0),
        (101, 0),
        (0, -1),
        (0, 101),
    ],
)
def test_calculate_cart_totals_rejects_invalid_rates(tax, discount):
    with pytest.raises(ValueError):
        calculate_cart_totals([], tax_rate=tax, discount_rate=discount)


def test_calculate_cart_totals_rejects_invalid_quantity():
    with pytest.raises(ValueError):
        calculate_cart_totals([
            {"quantity": 0, "unit_price": Decimal("15.00")}
        ])
