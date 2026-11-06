import math
import statistics
import time
from datetime import date, timedelta
from decimal import Decimal

from sqlalchemy import create_engine
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
from src.services.dashboard_service import get_dashboard_summary
from src.services.inventory_service import list_products


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
            sku=f"PERF-{i:04d}",
            name=f"Test Product {i:04d}",
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
                    batch_code=f"B-{product.id}-{j}",
                    product_id=product.id,
                    quantity_received=100,
                    quantity_remaining=80,
                    expiry_date=date.today() + timedelta(days=60 + j),
                )
            )

    session.add_all(batches)
    session.commit()

    print("Seeded 1,000 products and 2,000 batches.")

    def measure(label, operation, runs=30):
        timings = []

        for _ in range(runs):
            start = time.perf_counter()
            operation()
            timings.append((time.perf_counter() - start) * 1000)

        ordered = sorted(timings)
        p95 = ordered[math.ceil(0.95 * len(ordered)) - 1]

        print(f"\n{label}")
        print(f"Runs: {runs}")
        print(f"Average: {statistics.mean(timings):.2f} ms")
        print(f"Median: {statistics.median(timings):.2f} ms")
        print(f"P95: {p95:.2f} ms")
        print(f"Maximum: {max(timings):.2f} ms")

    measure(
        "Dashboard summary (1,000 products, 2,000 batches)",
        lambda: get_dashboard_summary(session, as_of=date.today()),
    )

    measure(
        "Product listing (1,000 products)",
        lambda: list_products(session),
    )

engine.dispose()
