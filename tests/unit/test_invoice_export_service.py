
from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.database.db import Base
from src.services.inventory_service import create_product
from src.services.invoice_service import generate_invoice
from src.services.invoice_export_service import (
    export_invoice_html,
    render_invoice_html,
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


def test_render_invoice_html(session, product):
    invoice = generate_invoice(
        session,
        cashier="Chris",
        customer_mobile="9876543210",
        customer_email="customer@example.com",
        items=[{"product_id": product.id, "quantity": 2}],
    )

    html = render_invoice_html(invoice)

    assert invoice.invoice_number in html
    assert "Chris" in html
    assert "Apple" in html
    assert "₹30.00" in html
    assert "Print / Save as PDF" in html


def test_export_invoice_html_creates_file(tmp_path, session, product):
    invoice = generate_invoice(
        session,
        cashier="Chris",
        items=[{"product_id": product.id, "quantity": 1}],
    )

    output_file = tmp_path / "invoice.html"

    returned_path = export_invoice_html(invoice, output_file)

    assert returned_path == output_file
    assert output_file.exists()

    content = output_file.read_text(encoding="utf-8")
    assert invoice.invoice_number in content
    assert "Apple" in content
