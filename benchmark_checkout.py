import math
import statistics
import time
from datetime import date, timedelta
from decimal import Decimal

from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.database.db import Base
import src.models.batch
import src.models.employee
import src.models.invoice
import src.models.product
import src.models.waste

from src.models.product import Product
from src.models.batch import Batch
from src.models.invoice import Invoice
from src.services.checkout_service import complete_checkout


engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

with Session() as session:
    products = [
        Product(
            sku=f"CHECKOUT-{i:04d}",
            name=f"Checkout Product {i:04d}",
            category="Benchmark",
            supplier="Test Supplier",
            cost_price=Decimal("10.00"),
            selling_price=Decimal("15.00"),
            low_stock_threshold=10,
            is_active=True,
        )
        for i in range(1000)
    ]

    session.add_all(products)
    session.flush()

    batches = []
    for product in products:
        for j in range(2):
            batches.append(
                Batch(
                    batch_code=f"CB-{product.id}-{j}",
                    product_id=product.id,
                    quantity_received=100,
                    quantity_remaining=100,
                    expiry_date=date.today() + timedelta(days=60 + j * 30),
                )
            )

    session.add_all(batches)
    session.commit()

    checkout_items = [
        {"product_id": product.id, "quantity": 1}
        for product in products[:20]
    ]

    print("Seeded 1,000 products and 2,000 batches.")
    print("Each checkout contains 20 distinct products.")

    timings = []

    for run in range(30):
        start = time.perf_counter()

        invoice = complete_checkout(
            session,
            cashier="Performance Test",
            items=checkout_items,
            as_of=date.today(),
        )

        elapsed = (time.perf_counter() - start) * 1000
        timings.append(elapsed)

        if len(invoice.items) != 20:
            raise RuntimeError("Checkout did not create 20 invoice items.")

    ordered = sorted(timings)
    p95 = ordered[math.ceil(0.95 * len(ordered)) - 1]

    invoice_count = session.scalar(
        select(func.count(Invoice.id))
    )

    print("\nComplete checkout performance")
    print("Runs:", len(timings))
    print("Invoices created:", invoice_count)
    print(f"Average: {statistics.mean(timings):.2f} ms")
    print(f"Median: {statistics.median(timings):.2f} ms")
    print(f"P95: {p95:.2f} ms")
    print(f"Maximum: {max(timings):.2f} ms")

engine.dispose()
