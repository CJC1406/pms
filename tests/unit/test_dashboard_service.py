from datetime import date, timedelta
from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.database.db import Base
from src.services.dashboard_service import get_dashboard_summary
from src.services.inventory_service import create_product, add_batch
from src.services.invoice_service import generate_invoice


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
        sku="DASH-001",
        name="Dashboard Apple",
        category="Fruit",
        selling_price=Decimal("15.00"),
        low_stock_threshold=5,
    )


def test_empty_dashboard_summary(session):
    summary = get_dashboard_summary(session)

    assert summary["total_products"] == 0
    assert summary["low_stock"] == 0
    assert summary["expiring_batches"] == 0
    assert summary["expiring_quantity"] == 0
    assert summary["daily_sales"] == Decimal("0")
    assert summary["invoice_count"] == 0
    assert summary["monthly_waste_cost"] == Decimal("0")

def test_dashboard_counts_products_and_low_stock(session, product):
    summary = get_dashboard_summary(session)

    assert summary["total_products"] == 1
    assert summary["low_stock"] == 1


def test_dashboard_counts_expiring_batches(session, product):
    add_batch(
        session,
        product_id=product.id,
        batch_code="DASH-EXPIRY",
        quantity_received=8,
        expiry_date=date.today() + timedelta(days=3),
    )

    summary = get_dashboard_summary(session)

    assert summary["expiring_batches"] == 1
    assert summary["expiring_quantity"] == 8


def test_dashboard_counts_daily_sales_and_invoices(session, product):
    invoice = generate_invoice(
        session,
        cashier="Dashboard Test",
        items=[{"product_id": product.id, "quantity": 2}],
    )

    summary = get_dashboard_summary(session)

    assert summary["daily_sales"] == invoice.total
    assert summary["invoice_count"] == 1


def test_dashboard_summary_uses_requested_date(session):
    summary = get_dashboard_summary(
        session,
        as_of=date(2027, 1, 15),
    )

    assert summary["total_products"] == 0
    assert summary["daily_sales"] == Decimal("0")
    assert summary["invoice_count"] == 0
