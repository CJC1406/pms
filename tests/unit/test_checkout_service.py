from datetime import date, timedelta
from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.database.db import Base
from src.models.batch import Batch
from src.models.invoice import Invoice
from src.services.inventory_service import create_product
from src.services.checkout_service import complete_checkout


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
        sku="MILK-001",
        name="Milk",
        category="Dairy",
        selling_price=Decimal("10.00"),
    )


def create_batch(session, product, quantity, expiry_date, batch_code):
    batch = Batch(
        product_id=product.id,
        batch_code=batch_code,
        quantity_received=quantity,
        quantity_remaining=quantity,
        expiry_date=expiry_date,
    )
    session.add(batch)
    session.commit()
    session.refresh(batch)
    return batch


def test_checkout_deducts_stock_and_creates_invoice(session, product):
    batch = create_batch(
        session, product, 10, date.today() + timedelta(days=10), "B1"
    )

    invoice = complete_checkout(
        session,
        cashier="Chris",
        items=[{"product_id": product.id, "quantity": 3}],
    )

    session.refresh(batch)

    assert invoice.id is not None
    assert batch.quantity_remaining == 7


def test_checkout_uses_fefo(session, product):
    early_batch = create_batch(
        session, product, 2, date.today() + timedelta(days=2), "EARLY"
    )
    later_batch = create_batch(
        session, product, 5, date.today() + timedelta(days=10), "LATER"
    )

    complete_checkout(
        session,
        cashier="Chris",
        items=[{"product_id": product.id, "quantity": 3}],
    )

    session.refresh(early_batch)
    session.refresh(later_batch)

    assert early_batch.quantity_remaining == 0
    assert later_batch.quantity_remaining == 4


def test_insufficient_stock_rejected_without_changes(session, product):
    batch = create_batch(
        session, product, 2, date.today() + timedelta(days=10), "B1"
    )

    with pytest.raises(ValueError, match="Insufficient valid stock"):
        complete_checkout(
            session,
            cashier="Chris",
            items=[{"product_id": product.id, "quantity": 5}],
        )

    session.refresh(batch)

    assert batch.quantity_remaining == 2
    assert session.query(Invoice).count() == 0


def test_expired_stock_is_not_sold(session, product):
    batch = create_batch(
        session, product, 5, date.today() - timedelta(days=1), "EXPIRED"
    )

    with pytest.raises(ValueError, match="Insufficient valid stock"):
        complete_checkout(
            session,
            cashier="Chris",
            items=[{"product_id": product.id, "quantity": 1}],
        )

    session.refresh(batch)

    assert batch.quantity_remaining == 5
    assert session.query(Invoice).count() == 0


def test_inactive_product_checkout_rejected(session, product):
    product.is_active = False
    session.commit()

    create_batch(
        session, product, 5, date.today() + timedelta(days=10), "B1"
    )

    with pytest.raises(ValueError, match="missing or inactive"):
        complete_checkout(
            session,
            cashier="Chris",
            items=[{"product_id": product.id, "quantity": 1}],
        )

    assert session.query(Invoice).count() == 0


def test_duplicate_product_lines_are_combined(session, product):
    batch = create_batch(
        session, product, 10, date.today() + timedelta(days=10), "B1"
    )

    invoice = complete_checkout(
        session,
        cashier="Chris",
        items=[
            {"product_id": product.id, "quantity": 2},
            {"product_id": product.id, "quantity": 3},
        ],
    )

    session.refresh(batch)

    assert batch.quantity_remaining == 5
    assert len(invoice.items) == 1
    assert invoice.items[0].quantity == 5


@pytest.mark.parametrize("quantity", [0, -1, 1.5, True, "2"])
def test_invalid_quantity_rejected(session, product, quantity):
    with pytest.raises(ValueError, match="Quantity must be a positive integer"):
        complete_checkout(
            session,
            cashier="Chris",
            items=[{"product_id": product.id, "quantity": quantity}],
        )

    assert session.query(Invoice).count() == 0