
from datetime import date, timedelta
from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.database.db import Base
from src.services.inventory_service import create_product, add_batch
from src.services.expiry_service import (
    get_expired_batches,
    get_expiring_batches,
    get_fefo_batches,
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
    )


def create_test_batch(session, product_id, code, quantity, expiry):
    return add_batch(
        session,
        product_id=product_id,
        batch_code=code,
        quantity_received=quantity,
        expiry_date=expiry,
    )


def test_get_expired_batches(session, product):
    today = date(2026, 10, 30)

    expired = create_test_batch(
        session, product.id, "OLD-001", 10, today - timedelta(days=1)
    )

    create_test_batch(
        session, product.id, "FUTURE-001", 10, today + timedelta(days=5)
    )

    result = get_expired_batches(session, as_of=today)

    assert len(result) == 1
    assert result[0].id == expired.id


def test_get_expired_batches_excludes_depleted_stock(session, product):
    today = date(2026, 10, 30)

    depleted = create_test_batch(
        session, product.id, "EMPTY-001", 10, today - timedelta(days=1)
    )

    depleted.quantity_remaining = 0
    session.commit()

    assert get_expired_batches(session, as_of=today) == []


def test_get_expiring_batches(session, product):
    today = date(2026, 10, 30)

    today_batch = create_test_batch(
        session, product.id, "TODAY-001", 10, today
    )

    future_batch = create_test_batch(
        session, product.id, "SOON-001", 10, today + timedelta(days=5)
    )

    create_test_batch(
        session, product.id, "LATER-001", 10, today + timedelta(days=10)
    )

    result = get_expiring_batches(session, days=7, as_of=today)

    assert [batch.id for batch in result] == [
        today_batch.id,
        future_batch.id,
    ]


def test_get_expiring_batches_rejects_invalid_days(session):
    with pytest.raises(ValueError):
        get_expiring_batches(session, days=-1)

    with pytest.raises(ValueError):
        get_expiring_batches(session, days=1.5)


def test_fefo_orders_batches_by_expiry(session, product):
    today = date(2026, 10, 30)

    later = create_test_batch(
        session, product.id, "LATER-001", 10, today + timedelta(days=5)
    )

    earlier = create_test_batch(
        session, product.id, "EARLIER-001", 10, today + timedelta(days=2)
    )

    result = get_fefo_batches(session, product.id, as_of=today)

    assert [batch.id for batch in result] == [
        earlier.id,
        later.id,
    ]


def test_fefo_excludes_expired_and_depleted_batches(session, product):
    today = date(2026, 10, 30)

    create_test_batch(
        session, product.id, "EXPIRED-001", 10, today - timedelta(days=1)
    )

    depleted = create_test_batch(
        session, product.id, "EMPTY-001", 10, today + timedelta(days=2)
    )
    depleted.quantity_remaining = 0
    session.commit()

    valid = create_test_batch(
        session, product.id, "VALID-001", 10, today + timedelta(days=3)
    )

    result = get_fefo_batches(session, product.id, as_of=today)

    assert len(result) == 1
    assert result[0].id == valid.id


def test_fefo_returns_empty_for_unknown_product(session):
    assert get_fefo_batches(session, 9999) == []


def test_expiry_functions_ignore_inactive_products(session, product):
    today = date(2026, 10, 30)

    create_test_batch(
        session, product.id, "EXPIRED-002", 10, today - timedelta(days=1)
    )

    product.is_active = False
    session.commit()

    assert get_expired_batches(session, as_of=today) == []
    assert get_expiring_batches(session, as_of=today) == []
    assert get_fefo_batches(session, product.id, as_of=today) == []
