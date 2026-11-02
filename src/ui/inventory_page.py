
from datetime import date
from decimal import Decimal

from PySide6.QtCore import Qt, QDate
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
    QDialog,
    QFormLayout,
    QDialogButtonBox,
    QDoubleSpinBox,
    QSpinBox,
    QDateEdit,
    QInputDialog,
)

from src.database.db import SessionLocal
from src.services.inventory_service import (
    list_products,
    create_product,
    update_product,
    deactivate_product,
    add_batch,
    adjust_batch_stock,
    get_total_stock,
)


class ProductDialog(QDialog):
    """Dialog for adding or editing a product."""

    def __init__(self, parent=None, product=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Product" if product else "Add Product")
        self.setMinimumWidth(350)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.sku = QLineEdit()
        self.name = QLineEdit()
        self.category = QLineEdit()
        self.supplier = QLineEdit()

        self.cost_price = QDoubleSpinBox()
        self.cost_price.setMaximum(9999999)
        self.cost_price.setDecimals(2)

        self.selling_price = QDoubleSpinBox()
        self.selling_price.setMaximum(9999999)
        self.selling_price.setDecimals(2)

        self.threshold = QSpinBox()
        self.threshold.setMaximum(1000000)

        form.addRow("SKU:", self.sku)
        form.addRow("Product Name:", self.name)
        form.addRow("Category:", self.category)
        form.addRow("Supplier:", self.supplier)
        form.addRow("Cost Price:", self.cost_price)
        form.addRow("Selling Price:", self.selling_price)
        form.addRow("Low Stock Threshold:", self.threshold)

        layout.addLayout(form)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        if product:
            self.sku.setText(product.sku)
            self.name.setText(product.name)
            self.category.setText(product.category)
            self.supplier.setText(product.supplier or "")
            self.cost_price.setValue(float(product.cost_price))
            self.selling_price.setValue(float(product.selling_price))
            self.threshold.setValue(product.low_stock_threshold)

    def get_data(self):
        return {
            "sku": self.sku.text().strip(),
            "name": self.name.text().strip(),
            "category": self.category.text().strip(),
            "supplier": self.supplier.text().strip() or None,
            "cost_price": Decimal(str(self.cost_price.value())),
            "selling_price": Decimal(str(self.selling_price.value())),
            "low_stock_threshold": self.threshold.value(),
        }


class BatchDialog(QDialog):
    """Dialog for adding a stock batch."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Stock Batch")
        self.setMinimumWidth(350)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.batch_code = QLineEdit()

        self.quantity = QSpinBox()
        self.quantity.setMinimum(1)
        self.quantity.setMaximum(1000000)

        self.expiry_date = QDateEdit()
        self.expiry_date.setCalendarPopup(True)
        self.expiry_date.setDate(QDate.currentDate().addDays(7))

        form.addRow("Batch Code:", self.batch_code)
        form.addRow("Quantity Received:", self.quantity)
        form.addRow("Expiry Date:", self.expiry_date)

        layout.addLayout(form)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)


class InventoryPage(QWidget):
    """Database-backed inventory management page."""

    def __init__(self, page_name="Inventory", parent=None):
        super().__init__(parent)

        self.selected_product_id = None
        self.selected_batch_id = None

        root = QVBoxLayout(self)
        root.setContentsMargins(32, 28, 32, 28)
        root.setSpacing(14)

        title = QLabel("Inventory Management")
        title.setObjectName("pageTitle")
        root.addWidget(title)

        description = QLabel(
            "Manage products, stock batches and inventory quantities."
        )
        description.setObjectName("description")
        root.addWidget(description)

        # Search and product actions
        toolbar = QHBoxLayout()

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search by SKU, name or category...")
        self.search.textChanged.connect(self.filter_products)
        toolbar.addWidget(self.search, 1)

        add_button = QPushButton("Add Product")
        add_button.setObjectName("actionButton")
        add_button.clicked.connect(self.add_product)
        toolbar.addWidget(add_button)

        edit_button = QPushButton("Edit Product")
        edit_button.setObjectName("actionButton")
        edit_button.clicked.connect(self.edit_product)
        toolbar.addWidget(edit_button)

        deactivate_button = QPushButton("Deactivate")
        deactivate_button.setObjectName("actionButton")
        deactivate_button.clicked.connect(self.deactivate_selected_product)
        toolbar.addWidget(deactivate_button)

        root.addLayout(toolbar)

        products_heading = QLabel("Products")
        products_heading.setObjectName("sectionTitle")
        root.addWidget(products_heading)

        self.product_table = QTableWidget()
        self.product_table.setColumnCount(7)
        self.product_table.setHorizontalHeaderLabels([
            "ID",
            "SKU",
            "Product Name",
            "Category",
            "Selling Price",
            "Available Stock",
            "Low Stock At",
        ])
        self.product_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.product_table.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )
        self.product_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self.product_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.product_table.setColumnHidden(0, True)
        self.product_table.itemSelectionChanged.connect(
            self.on_product_selected
        )
        root.addWidget(self.product_table, 3)

        # Batch section
        batch_toolbar = QHBoxLayout()

        batch_heading = QLabel("Stock Batches")
        batch_heading.setObjectName("sectionTitle")
        batch_toolbar.addWidget(batch_heading)
        batch_toolbar.addStretch()

        add_batch_button = QPushButton("Add Batch")
        add_batch_button.setObjectName("actionButton")
        add_batch_button.clicked.connect(self.add_stock_batch)
        batch_toolbar.addWidget(add_batch_button)

        adjust_button = QPushButton("Adjust Selected Batch")
        adjust_button.setObjectName("actionButton")
        adjust_button.clicked.connect(self.adjust_stock)
        batch_toolbar.addWidget(adjust_button)

        root.addLayout(batch_toolbar)

        self.batch_table = QTableWidget()
        self.batch_table.setColumnCount(5)
        self.batch_table.setHorizontalHeaderLabels([
            "Batch ID",
            "Batch Code",
            "Quantity Received",
            "Remaining Quantity",
            "Expiry Date",
        ])
        self.batch_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.batch_table.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )
        self.batch_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self.batch_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.batch_table.setColumnHidden(0, True)
        self.batch_table.itemSelectionChanged.connect(
            self.on_batch_selected
        )
        root.addWidget(self.batch_table, 2)

        refresh_button = QPushButton("Refresh Inventory")
        refresh_button.setObjectName("actionButton")
        refresh_button.clicked.connect(self.refresh)
        root.addWidget(refresh_button)

        self.products = []
        self.refresh()

    def show_error(self, message):
        QMessageBox.warning(self, "Inventory Error", str(message))

    def refresh(self):
        """Reload active products and their stock batches."""
        try:
            with SessionLocal() as session:
                self.products = list_products(session)

                rows = []
                for product in self.products:
                    stock = get_total_stock(session, product.id)
                    rows.append((product, stock))

            self.product_table.setRowCount(0)

            for product, stock in rows:
                row = self.product_table.rowCount()
                self.product_table.insertRow(row)

                values = [
                    product.id,
                    product.sku,
                    product.name,
                    product.category,
                    f"₹{product.selling_price:.2f}",
                    stock,
                    product.low_stock_threshold,
                ]

                for column, value in enumerate(values):
                    item = QTableWidgetItem(str(value))
                    if column in (0, 4, 5, 6):
                        item.setTextAlignment(
                            Qt.AlignmentFlag.AlignCenter
                        )
                    self.product_table.setItem(row, column, item)

                if stock <= product.low_stock_threshold:
                    for column in range(7):
                        self.product_table.item(row, column).setToolTip(
                            "Low stock: available quantity is at or below "
                            "the configured threshold."
                        )

            self.filter_products(self.search.text())

            if self.selected_product_id is not None:
                self.select_product_row(self.selected_product_id)
            else:
                self.batch_table.setRowCount(0)

        except Exception as exc:
            self.show_error(exc)

    def filter_products(self, text):
        """Filter the product table using SKU, name or category."""
        search_text = text.strip().lower()

        for row in range(self.product_table.rowCount()):
            searchable = " ".join(
                self.product_table.item(row, column).text().lower()
                for column in (1, 2, 3)
            )
            self.product_table.setRowHidden(
                row, search_text not in searchable
            )

    def select_product_row(self, product_id):
        for row in range(self.product_table.rowCount()):
            if int(self.product_table.item(row, 0).text()) == product_id:
                self.product_table.selectRow(row)
                return

        self.selected_product_id = None
        self.batch_table.setRowCount(0)

    def on_product_selected(self):
        row = self.product_table.currentRow()

        if row < 0:
            return

        self.selected_product_id = int(
            self.product_table.item(row, 0).text()
        )
        self.load_batches()

    def on_batch_selected(self):
        row = self.batch_table.currentRow()

        if row < 0:
            self.selected_batch_id = None
            return

        self.selected_batch_id = int(
            self.batch_table.item(row, 0).text()
        )

    def load_batches(self):
        """Display batches belonging to the selected product."""
        self.batch_table.setRowCount(0)

        if self.selected_product_id is None:
            return

        try:
            with SessionLocal() as session:
                product = next(
                    (
                        item for item in list_products(session)
                        if item.id == self.selected_product_id
                    ),
                    None,
                )

                if product is None:
                    return

                batches = sorted(
                    product.batches,
                    key=lambda batch: (batch.expiry_date, batch.id),
                )

                batch_rows = [
                    (
                        batch.id,
                        batch.batch_code,
                        batch.quantity_received,
                        batch.quantity_remaining,
                        batch.expiry_date.isoformat(),
                    )
                    for batch in batches
                ]

            for values in batch_rows:
                row = self.batch_table.rowCount()
                self.batch_table.insertRow(row)

                for column, value in enumerate(values):
                    self.batch_table.setItem(
                        row, column, QTableWidgetItem(str(value))
                    )

        except Exception as exc:
            self.show_error(exc)

    def add_product(self):
        dialog = ProductDialog(self)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        try:
            data = dialog.get_data()

            with SessionLocal() as session:
                create_product(session, **data)

            QMessageBox.information(
                self, "Success", "Product added successfully."
            )
            self.refresh()

        except Exception as exc:
            self.show_error(exc)

    def edit_product(self):
        if self.selected_product_id is None:
            self.show_error("Select a product to edit.")
            return

        try:
            with SessionLocal() as session:
                from src.services.inventory_service import get_product
                product = get_product(session, self.selected_product_id)

                if product is None:
                    raise ValueError("Selected product was not found.")

                dialog = ProductDialog(self, product)

                if dialog.exec() != QDialog.DialogCode.Accepted:
                    return

                data = dialog.get_data()
                update_product(session, self.selected_product_id, **data)

            QMessageBox.information(
                self, "Success", "Product updated successfully."
            )
            self.refresh()

        except Exception as exc:
            self.show_error(exc)

    def deactivate_selected_product(self):
        if self.selected_product_id is None:
            self.show_error("Select a product to deactivate.")
            return

        answer = QMessageBox.question(
            self,
            "Confirm Deactivation",
            "Deactivate this product? Its inventory history will be kept.",
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        try:
            with SessionLocal() as session:
                deactivate_product(session, self.selected_product_id)

            self.selected_product_id = None
            self.selected_batch_id = None
            self.refresh()

        except Exception as exc:
            self.show_error(exc)

    def add_stock_batch(self):
        if self.selected_product_id is None:
            self.show_error("Select a product before adding a batch.")
            return

        dialog = BatchDialog(self)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        try:
            batch_code = dialog.batch_code.text().strip()
            if not batch_code:
                raise ValueError("Batch code cannot be blank.")

            with SessionLocal() as session:
                add_batch(
                    session,
                    product_id=self.selected_product_id,
                    batch_code=batch_code,
                    quantity_received=dialog.quantity.value(),
                    expiry_date=dialog.expiry_date.date().toPython(),
                )

            self.refresh()
            self.load_batches()

        except Exception as exc:
            self.show_error(exc)

    def adjust_stock(self):
        if self.selected_batch_id is None:
            self.show_error("Select a batch to adjust its stock.")
            return

        quantity, accepted = QInputDialog.getInt(
            self,
            "Adjust Stock",
            "Enter quantity change (negative to remove stock):",
            1,
            -1000000,
            1000000,
        )

        if not accepted:
            return

        if quantity == 0:
            self.show_error("Adjustment cannot be zero.")
            return

        try:
            with SessionLocal() as session:
                adjust_batch_stock(
                    session,
                    self.selected_batch_id,
                    quantity,
                )

            self.refresh()
            self.load_batches()

        except Exception as exc:
            self.show_error(exc)
