
from datetime import date
from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from src.database.db import Base
from src.models.product import Product
from src.models.batch import Batch


@pytest.fixture
def session():
    """Provide an isolated in-memory SQLite database for each test."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(engine)

    with Session(engine) as db_session:
        yield db_session

    engine.dispose()


def make_product(sku="APPLE-001"):
    return Product(
        sku=sku,
        name="Apple",
        category="Fruit",
        cost_price=Decimal("10.00"),
        selling_price=Decimal("15.00"),
        low_stock_threshold=5,
    )


def test_product_can_be_created(session):
    product = make_product()

    session.add(product)
    session.commit()

    assert product.id is not None
    assert product.sku == "APPLE-001"
    assert product.is_active is True


def test_duplicate_product_sku_is_rejected(session):
    session.add_all([make_product(), make_product()])
    with pytest.raises(IntegrityError):
        session.commit()

    session.rollback()


@pytest.mark.parametrize(
    "field,value",
    [
        ("cost_price", Decimal("-1.00")),
        ("selling_price", Decimal("-1.00")),
        ("low_stock_threshold", -1),
    ],
)
def test_invalid_product_values_are_rejected(session, field, value):
    product = make_product()
    setattr(product, field, value)
    session.add(product)

    with pytest.raises(IntegrityError):
        session.commit()

    session.rollback()


def test_product_can_have_multiple_batches(session):
    product = make_product()

    product.batches.extend(
        [
            Batch(
                batch_code="LOT-001",
                quantity_received=20,
                quantity_remaining=15,
                expiry_date=date(2026, 11, 10),
            ),
            Batch(
                batch_code="LOT-002",
                quantity_received=30,
                quantity_remaining=30,
                expiry_date=date(2026, 11, 20),
            ),
        ]
    )

    session.add(product)
    session.commit()

    assert len(product.batches) == 2
    assert all(batch.product is product for batch in product.batches)


@pytest.mark.parametrize(
    "received,remaining",
    [
        (0, 0),
        (10, -1),
        (10, 11),
    ],
)
def test_invalid_batch_quantities_are_rejected(
    session,
    received,
    remaining,
):
    product = make_product()
    session.add(product)
    session.flush()

    batch = Batch(
        batch_code="LOT-INVALID",
        product_id=product.id,
        quantity_received=received,
        quantity_remaining=remaining,
        expiry_date=date(2026, 11, 10),
    )

    session.add(batch)

    with pytest.raises(IntegrityError):
        session.commit()

    session.rollback()


@pytest.mark.parametrize(
    "field,value",
    [
        ("sku", ""),
        ("name", "   "),
        ("category", ""),
    ],
)
def test_blank_product_text_is_rejected(session, field, value):
    product = make_product()
    setattr(product, field, value)
    session.add(product)

    with pytest.raises(IntegrityError):
        session.commit()

    session.rollback()


def test_batch_requires_expiry_date(session):
    product = make_product()
    session.add(product)
    session.flush()

    batch = Batch(
        batch_code="LOT-NO-EXPIRY",
        product_id=product.id,
        quantity_received=10,
        quantity_remaining=10,
        expiry_date=None,
    )
    session.add(batch)

    with pytest.raises(IntegrityError):
        session.commit()

    session.rollback()

