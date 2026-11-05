from datetime import date
from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.database.db import Base
from src.models.batch import Batch
from src.models.waste import WasteRecord
from src.services.inventory_service import add_batch, create_product
from src.services.waste_service import (
    WASTE_REASONS, get_waste_summary, list_waste_records, record_waste,
)


@pytest.fixture
def session():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    factory = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    Base.metadata.create_all(engine)
    with factory() as db:
        yield db
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def stock(session):
    product = create_product(
        session, sku="WASTE-001", name="Apple", category="Fruit",
        cost_price=Decimal("12.50"), selling_price=Decimal("20.00"),
    )
    batch = add_batch(
        session, product_id=product.id, batch_code="APPLE-B1",
        quantity_received=10, expiry_date=date(2027, 1, 1),
    )
    return product, batch


def test_record_waste_deducts_batch_and_snapshots_cost(session, stock):
    product, batch = stock
    record = record_waste(
        session, batch_id=batch.id, quantity=3, reason="Spoiled", recorded_by="CJ"
    )
    session.refresh(batch)
    assert batch.quantity_remaining == 7
    assert record.batch_id == batch.id
    assert record.recorded_by == "CJ"
    assert record.estimated_cost == Decimal("37.50")


def test_waste_record_and_stock_rollback_together(session, stock):
    _, batch = stock
    with pytest.raises(ValueError, match="Insufficient"):
        record_waste(
            session, batch_id=batch.id, quantity=11,
            reason="Expired", recorded_by="CJ",
        )
    session.refresh(batch)
    assert batch.quantity_remaining == 10
    assert session.query(WasteRecord).count() == 0


@pytest.mark.parametrize("quantity", [0, -1, True, 1.5, "2"])
def test_rejects_invalid_quantity(session, stock, quantity):
    _, batch = stock
    with pytest.raises(ValueError, match="positive integer"):
        record_waste(
            session, batch_id=batch.id, quantity=quantity,
            reason="Expired", recorded_by="CJ",
        )


def test_rejects_invalid_reason_and_blank_recorder(session, stock):
    _, batch = stock
    with pytest.raises(ValueError, match="reason"):
        record_waste(session, batch_id=batch.id, quantity=1, reason="Other reason", recorded_by="CJ")
    with pytest.raises(ValueError, match="cannot be blank"):
        record_waste(session, batch_id=batch.id, quantity=1, reason="Other", recorded_by=" ")


def test_rejects_missing_batch(session):
    with pytest.raises(ValueError, match="does not exist"):
        record_waste(session, batch_id=999, quantity=1, reason="Expired", recorded_by="CJ")


def test_history_and_summary_group_by_reason_and_product(session, stock):
    product, batch = stock
    record_waste(session, batch_id=batch.id, quantity=2, reason="Expired", recorded_by="CJ")
    record_waste(session, batch_id=batch.id, quantity=1, reason="Damaged", recorded_by="CJ")
    records = list_waste_records(session)
    summary = get_waste_summary(session)
    assert len(records) == 2
    assert summary["total_quantity"] == 3
    assert summary["estimated_cost"] == Decimal("37.50")
    assert summary["by_reason"] == {"Expired": 2, "Damaged": 1}
    assert summary["by_product"] == {product.name: 3}


def test_waste_is_no_longer_available_for_checkout(session, stock):
    _, batch = stock
    record_waste(session, batch_id=batch.id, quantity=10, reason="Expired", recorded_by="CJ")
    session.refresh(batch)
    assert batch.quantity_remaining == 0
