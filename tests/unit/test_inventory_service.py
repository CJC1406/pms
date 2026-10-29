
from datetime import date
from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.database.db import Base
from src.models.batch import Batch
from src.models.product import Product
from src.services.inventory_service import (
    add_batch,
    adjust_batch_stock,
    create_product,
    deactivate_product,
    get_product,
    get_total_stock,
    list_products,
    update_product,
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
        cost_price=Decimal("10.00"),
        selling_price=Decimal("15.00"),
        low_stock_threshold=5,
    )


def test_create_product(session):
    item = create_product(
        session,
        sku="MILK-001",
        name="Milk",
        category="Dairy",
    )

    assert item.id is not None
    assert item.sku == "MILK-001"
    assert item.is_active is True


def test_create_product_rejects_duplicate_sku(session, product):
    with pytest.raises(ValueError, match="SKU"):
        create_product(
            session,
            sku="APPLE-001",
            name="Another Apple",
            category="Fruit",
        )


@pytest.mark.parametrize(
    "kwargs",
    [
        {"sku": " ", "name": "Apple", "category": "Fruit"},
        {"sku": "A2", "name": " ", "category": "Fruit"},
        {"sku": "A3", "name": "Apple", "category": ""},
        {"sku": "A4", "name": "Apple", "category": "Fruit",
         "cost_price": Decimal("-1")},
        {"sku": "A5", "name": "Apple", "category": "Fruit",
         "selling_price": Decimal("-1")},
        {"sku": "A6", "name": "Apple", "category": "Fruit",
         "low_stock_threshold": -1},
    ],
)
def test_create_product_rejects_invalid_input(session, kwargs):
    with pytest.raises(ValueError):
        create_product(session, **kwargs)


def test_list_and_get_products(session, product):
    assert [item.sku for item in list_products(session)] == ["APPLE-001"]
    assert get_product(session, product.id).sku == "APPLE-001"
    assert get_product(session, 9999) is None


def test_update_product(session, product):
    updated = update_product(
        session,
        product.id,
        name="Green Apple",
        selling_price=Decimal("16.00"),
    )

    assert updated.name == "Green Apple"
    assert updated.selling_price == Decimal("16.00")


def test_update_rejects_invalid_fields_and_values(session, product):
    with pytest.raises(ValueError, match="cannot be updated"):
        update_product(session, product.id, is_active=False)

    with pytest.raises(ValueError, match="cannot be negative"):
        update_product(
            session,
            product.id,
            selling_price=Decimal("-5.00"),
        )


def test_deactivate_product_preserves_record(session, product):
    deactivated = deactivate_product(session, product.id)

    assert deactivated.is_active is False
    assert get_product(session, product.id) is None
    assert get_product(
        session, product.id, include_inactive=True
    ).is_active is False


def test_add_batch_and_calculate_total_stock(session, product):
    first = add_batch(
        session,
        product_id=product.id,
        batch_code="BATCH-001",
        quantity_received=20,
        expiry_date=date(2027, 1, 31),
    )
    add_batch(
        session,
        product_id=product.id,
        batch_code="BATCH-002",
        quantity_received=10,
        expiry_date=date(2027, 2, 28),
    )

    assert first.quantity_remaining == 20
    assert get_total_stock(session, product.id) == 30


@pytest.mark.parametrize(
    "quantity, expiry, code",
    [
        (0, date(2027, 1, 31), "B1"),
        (-1, date(2027, 1, 31), "B2"),
        (5, None, "B3"),
        (5, date(2027, 1, 31), " "),
    ],
)
def test_add_batch_rejects_invalid_values(
    session, product, quantity, expiry, code
):
    with pytest.raises(ValueError):
        add_batch(
            session,
            product_id=product.id,
            batch_code=code,
            quantity_received=quantity,
            expiry_date=expiry,
        )


def test_stock_adjustment(session, product):
    batch = add_batch(
        session,
        product_id=product.id,
        batch_code="STOCK-001",
        quantity_received=10,
        expiry_date=date(2027, 3, 31),
    )

    adjust_batch_stock(session, batch.id, -4)
    assert get_total_stock(session, product.id) == 6

    adjust_batch_stock(session, batch.id, 2)
    assert get_total_stock(session, product.id) == 8


def test_stock_adjustment_rejects_invalid_quantities(session, product):
    batch = add_batch(
        session,
        product_id=product.id,
        batch_code="STOCK-002",
        quantity_received=10,
        expiry_date=date(2027, 3, 31),
    )

    with pytest.raises(ValueError, match="Insufficient stock"):
        adjust_batch_stock(session, batch.id, -11)

    with pytest.raises(ValueError, match="cannot exceed"):
        adjust_batch_stock(session, batch.id, 1)

    with pytest.raises(ValueError, match="non-zero integer"):
        adjust_batch_stock(session, batch.id, 0)


def test_cannot_add_batch_to_inactive_product(session, product):
    deactivate_product(session, product.id)

    with pytest.raises(ValueError, match="active product"):
        add_batch(
            session,
            product_id=product.id,
            batch_code="BATCH-INACTIVE",
            quantity_received=5,
            expiry_date=date(2027, 1, 31),
        )
