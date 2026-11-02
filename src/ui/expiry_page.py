
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
    QSpinBox,
)

from src.database.db import SessionLocal
from src.services.expiry_service import (
    get_expired_batches,
    get_expiring_batches,
    get_fefo_batches,
)


class ExpiryPage(QWidget):
    """Database-backed expiry monitoring and FEFO page."""

    def __init__(self, page_name="Expiry Tracking", parent=None):
        super().__init__(parent)

        self.current_filter = "all"

        root = QVBoxLayout(self)
        root.setContentsMargins(32, 28, 32, 28)
        root.setSpacing(16)

        title = QLabel("Expiry Tracking")
        title.setObjectName("pageTitle")
        root.addWidget(title)

        description = QLabel(
            "Monitor expired stock, upcoming expiries and FEFO priorities."
        )
        description.setObjectName("description")
        root.addWidget(description)

        # Summary
        summary = QHBoxLayout()

        self.expired_label = QLabel("Expired batches: 0")
        self.expiring_label = QLabel("Expiring soon: 0")

        for label in (self.expired_label, self.expiring_label):
            label.setObjectName("sectionTitle")
            summary.addWidget(label)

        summary.addStretch()
        root.addLayout(summary)

        # Filters
        filters = QHBoxLayout()

        self.all_button = QPushButton("All Batches")
        self.expired_button = QPushButton("Expired")
        self.expiring_button = QPushButton("Expiring Soon")
        self.fefo_button = QPushButton("FEFO View")

        for button in (
            self.all_button,
            self.expired_button,
            self.expiring_button,
            self.fefo_button,
        ):
            button.setObjectName("actionButton")
            filters.addWidget(button)

        root.addLayout(filters)

        self.all_button.clicked.connect(
            lambda: self.load_batches("all")
        )
        self.expired_button.clicked.connect(
            lambda: self.load_batches("expired")
        )
        self.expiring_button.clicked.connect(
            lambda: self.load_batches("expiring")
        )
        self.fefo_button.clicked.connect(
            lambda: self.load_batches("fefo")
        )

        # Expiry window
        days_layout = QHBoxLayout()

        days_layout.addWidget(QLabel("Upcoming expiry window:"))

        self.days_input = QSpinBox()
        self.days_input.setRange(0, 365)
        self.days_input.setValue(7)
        days_layout.addWidget(self.days_input)

        days_layout.addWidget(QLabel("days"))

        apply_button = QPushButton("Apply")
        apply_button.setObjectName("actionButton")
        apply_button.clicked.connect(
            lambda: self.load_batches("expiring")
        )
        days_layout.addWidget(apply_button)

        days_layout.addStretch()
        root.addLayout(days_layout)

        # Batch table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Product",
            "Batch Code",
            "Quantity Remaining",
            "Expiry Date",
            "Days Until Expiry",
            "Status",
        ])

        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        root.addWidget(self.table)

        refresh_button = QPushButton("Refresh")
        refresh_button.setObjectName("actionButton")
        refresh_button.clicked.connect(
            lambda: self.load_batches(self.current_filter)
        )
        root.addWidget(refresh_button)

        self.load_batches("all")

    def load_batches(self, filter_type="all"):
        """Load batch records according to the selected expiry filter."""

        self.current_filter = filter_type

        try:
            with SessionLocal() as session:

                expired = get_expired_batches(session)
                expiring = get_expiring_batches(
                    session,
                    days=self.days_input.value(),
                )

                if filter_type == "expired":
                    batches = expired

                elif filter_type == "expiring":
                    batches = expiring

                elif filter_type == "fefo":
                    from src.services.inventory_service import list_products

                    batches = []
                    for product in list_products(session):
                        batches.extend(
                            get_fefo_batches(session, product.id)
                        )

                else:
                    batches = (
                        expired
                        + expiring
                    )

                # Capture values while the database session is open.
                rows = []
                from datetime import date

                today = date.today()

                for batch in batches:
                    product_name = (
                        batch.product.name if batch.product else "Unknown"
                    )
                    days_left = (batch.expiry_date - today).days

                    if days_left < 0:
                        status = "Expired"
                    elif days_left == 0:
                        status = "Expires Today"
                    elif days_left <= 7:
                        status = "Expiring Soon"
                    else:
                        status = "Safe"

                    rows.append((
                        product_name,
                        batch.batch_code,
                        batch.quantity_remaining,
                        batch.expiry_date.isoformat(),
                        days_left,
                        status,
                    ))

                self.expired_label.setText(
                    f"Expired batches: {len(expired)}"
                )
                self.expiring_label.setText(
                    f"Expiring soon: {len(expiring)}"
                )

            self.table.setRowCount(0)

            for values in rows:
                row = self.table.rowCount()
                self.table.insertRow(row)

                for column, value in enumerate(values):
                    item = QTableWidgetItem(str(value))
                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignCenter
                    )
                    self.table.setItem(row, column, item)

        except Exception as exc:
            QMessageBox.warning(
                self,
                "Expiry Tracking Error",
                str(exc),
            )
