from datetime import date

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QPushButton,
    QComboBox, QSpinBox, QLineEdit, QPlainTextEdit, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox,
)

from src.database.db import SessionLocal
from src.models.batch import Batch
from src.models.product import Product
from src.services.waste_service import (
    WASTE_REASONS, get_waste_summary, list_waste_records, record_waste,
)
from sqlalchemy import select
from sqlalchemy.orm import joinedload


class WastePage(QWidget):
    """Record stock write-offs and review waste history and totals."""

    def __init__(self, page_name="Waste Management", parent=None):
        super().__init__(parent)
        root = QVBoxLayout(self)
        root.setContentsMargins(32, 28, 32, 28)
        root.setSpacing(14)

        title = QLabel("Waste Management")
        title.setObjectName("pageTitle")
        root.addWidget(title)
        description = QLabel(
            "Record expired, damaged or spoiled stock. Every write-off is linked "
            "to a batch and immediately deducted from available inventory."
        )
        description.setObjectName("description")
        description.setWordWrap(True)
        root.addWidget(description)

        form = QFormLayout()
        self.batch_combo = QComboBox()
        self.batch_combo.currentIndexChanged.connect(self.update_batch_stock)
        self.stock_label = QLabel("Available: —")
        batch_row = QHBoxLayout()
        batch_row.addWidget(self.batch_combo, 1)
        batch_row.addWidget(self.stock_label)
        form.addRow("Product / batch", batch_row)

        self.quantity_input = QSpinBox()
        self.quantity_input.setRange(1, 1_000_000)
        self.quantity_input.setValue(1)
        form.addRow("Waste quantity", self.quantity_input)

        self.reason_combo = QComboBox()
        self.reason_combo.addItems(WASTE_REASONS)
        form.addRow("Reason", self.reason_combo)

        self.recorded_by_input = QLineEdit()
        self.recorded_by_input.setPlaceholderText("Name of employee recording waste")
        form.addRow("Recorded by", self.recorded_by_input)

        self.notes_input = QPlainTextEdit()
        self.notes_input.setPlaceholderText("Optional details (maximum 500 characters)")
        self.notes_input.setMaximumHeight(65)
        form.addRow("Notes", self.notes_input)
        root.addLayout(form)

        actions = QHBoxLayout()
        self.record_button = QPushButton("Record Waste")
        self.record_button.setObjectName("actionButton")
        self.record_button.clicked.connect(self.submit_waste)
        actions.addWidget(self.record_button)
        refresh_button = QPushButton("Refresh History")
        refresh_button.setObjectName("actionButton")
        refresh_button.clicked.connect(self.refresh)
        actions.addWidget(refresh_button)
        actions.addStretch()
        root.addLayout(actions)

        self.summary_label = QLabel("Waste summary: 0 units | Estimated cost: 0.00")
        self.summary_label.setObjectName("sectionTitle")
        root.addWidget(self.summary_label)

        self.table = QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels([
            "Date / Time", "Product", "Batch", "Quantity", "Reason",
            "Recorded By", "Estimated Cost", "Notes",
        ])
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        root.addWidget(self.table, 1)

        self.load_batches()
        self.refresh()

    def load_batches(self):
        self.batch_combo.clear()
        with SessionLocal() as session:
            batches = session.scalars(
                select(Batch).options(joinedload(Batch.product))
                .where(Batch.quantity_remaining > 0)
                .order_by(Product.name, Batch.expiry_date, Batch.id)
                .join(Product)
            ).unique().all()
            for batch in batches:
                label = (f"{batch.product.name} — {batch.batch_code} "
                         f"(expiry {batch.expiry_date.isoformat()})")
                self.batch_combo.addItem(label, batch.id)
                self.batch_combo.setItemData(
                    self.batch_combo.count() - 1, batch.quantity_remaining,
                    Qt.ItemDataRole.UserRole + 1,
                )
        self.update_batch_stock()

    def update_batch_stock(self, *_):
        available = self.batch_combo.currentData(Qt.ItemDataRole.UserRole + 1)
        if available is None:
            self.stock_label.setText("Available: 0")
            self.record_button.setEnabled(False)
        else:
            self.stock_label.setText(f"Available: {available}")
            self.record_button.setEnabled(True)
            self.quantity_input.setMaximum(max(1, int(available)))

    def submit_waste(self):
        batch_id = self.batch_combo.currentData()
        if batch_id is None:
            QMessageBox.warning(self, "No stock", "There are no batches with remaining stock.")
            return
        try:
            with SessionLocal() as session:
                record = record_waste(
                    session,
                    batch_id=int(batch_id),
                    quantity=self.quantity_input.value(),
                    reason=self.reason_combo.currentText(),
                    recorded_by=self.recorded_by_input.text(),
                    notes=self.notes_input.toPlainText(),
                )
                cost = record.estimated_cost
            QMessageBox.information(
                self, "Waste recorded",
                f"Waste of {record.quantity} unit(s) recorded. Estimated cost: {cost:.2f}",
            )
            self.recorded_by_input.clear()
            self.notes_input.clear()
            self.load_batches()
            self.refresh()
        except ValueError as exc:
            QMessageBox.warning(self, "Cannot record waste", str(exc))
        except Exception as exc:
            QMessageBox.critical(self, "Waste recording failed", str(exc))

    def refresh(self):
        try:
            with SessionLocal() as session:
                records = list_waste_records(session)
                summary = get_waste_summary(session)
                rows = []
                for item in records:
                    rows.append((
                        item.recorded_at.strftime("%Y-%m-%d %H:%M"),
                        item.batch.product.name,
                        item.batch.batch_code,
                        item.quantity,
                        item.reason,
                        item.recorded_by,
                        f"{item.estimated_cost:.2f}",
                        item.notes or "—",
                    ))
            self.summary_label.setText(
                f"All-time waste: {summary['total_quantity']} units  |  "
                f"Records: {summary['record_count']}  |  "
                f"Estimated cost: {summary['estimated_cost']:.2f}"
            )
            self.table.setRowCount(0)
            for values in rows:
                row = self.table.rowCount()
                self.table.insertRow(row)
                for column, value in enumerate(values):
                    self.table.setItem(row, column, QTableWidgetItem(str(value)))
        except Exception as exc:
            QMessageBox.warning(self, "Waste history error", str(exc))
