
from decimal import Decimal
from pathlib import Path
import tempfile

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QSpinBox, QDoubleSpinBox, QTableWidget,
    QTableWidgetItem, QHeaderView, QLineEdit, QMessageBox,
)

from src.database.db import SessionLocal
from src.services.inventory_service import list_products, get_total_stock
from src.services.cart_service import (
    add_cart_item,
    update_cart_quantity,
    remove_cart_item,
    calculate_cart_totals,
)
from src.services.invoice_service import generate_invoice
from src.services.invoice_export_service import export_invoice_html
from src.services.email_service import send_invoice_email


class CartPage(QWidget):
    def __init__(self, page_name="POS / Cart", parent=None):
        super().__init__(parent)
        self.cart = {}
        self.products = {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(14)

        title = QLabel("POS / Shopping Cart")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        description = QLabel("Select products, edit quantities and checkout.")
        description.setObjectName("description")
        layout.addWidget(description)

        product_row = QHBoxLayout()

        self.product_combo = QComboBox()
        self.product_combo.setMinimumWidth(260)
        product_row.addWidget(self.product_combo)

        self.add_quantity = QSpinBox()
        self.add_quantity.setRange(1, 999999)
        self.add_quantity.setValue(1)
        product_row.addWidget(self.add_quantity)

        add_button = QPushButton("Add to Cart")
        add_button.setObjectName("actionButton")
        add_button.clicked.connect(self.add_selected_product)
        product_row.addWidget(add_button)

        refresh_button = QPushButton("Refresh Products")
        refresh_button.setObjectName("actionButton")
        refresh_button.clicked.connect(self.load_products)
        product_row.addWidget(refresh_button)

        layout.addLayout(product_row)

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels([
            "Product", "SKU", "Quantity", "Unit Price", "Line Total", "Action"
        ])
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        layout.addWidget(self.table)

        settings_row = QHBoxLayout()

        settings_row.addWidget(QLabel("Cashier:"))
        self.cashier_input = QLineEdit()
        self.cashier_input.setPlaceholderText("Enter cashier name")
        self.cashier_input.setText("Cashier")
        settings_row.addWidget(self.cashier_input)

        settings_row.addWidget(QLabel("Tax (%):"))
        self.tax_input = QDoubleSpinBox()
        self.tax_input.setRange(0, 100)
        self.tax_input.setDecimals(2)
        self.tax_input.setValue(0)
        self.tax_input.valueChanged.connect(self.update_totals)
        settings_row.addWidget(self.tax_input)

        settings_row.addWidget(QLabel("Discount (%):"))
        self.discount_input = QDoubleSpinBox()
        self.discount_input.setRange(0, 100)
        self.discount_input.setDecimals(2)
        self.discount_input.setValue(0)
        self.discount_input.valueChanged.connect(self.update_totals)
        settings_row.addWidget(self.discount_input)

        layout.addLayout(settings_row)

        # Optional customer email for invoice delivery.
        email_row = QHBoxLayout()
        email_row.addWidget(QLabel("Customer Email:"))

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText(
            "Enter customer email (optional)"
        )
        email_row.addWidget(self.email_input)

        layout.addLayout(email_row)

        self.subtotal_label = QLabel("Subtotal: 0.00")
        self.discount_label = QLabel("Discount: 0.00")
        self.tax_label = QLabel("Tax: 0.00")
        self.total_label = QLabel("Total: 0.00")
        self.total_label.setObjectName("sectionTitle")

        layout.addWidget(self.subtotal_label)
        layout.addWidget(self.discount_label)
        layout.addWidget(self.tax_label)
        layout.addWidget(self.total_label)

        checkout_row = QHBoxLayout()

        clear_button = QPushButton("Clear Cart")
        clear_button.setObjectName("actionButton")
        clear_button.clicked.connect(self.clear_cart)
        checkout_row.addWidget(clear_button)

        checkout_button = QPushButton("Checkout")
        checkout_button.setObjectName("actionButton")
        checkout_button.clicked.connect(self.checkout)
        checkout_row.addWidget(checkout_button)

        layout.addLayout(checkout_row)
        layout.addStretch()

        self.load_products()

    def load_products(self):
        self.product_combo.clear()
        self.products = {}

        try:
            with SessionLocal() as session:
                products = list_products(session)

                for product in products:
                    if not product.is_active:
                        continue

                    stock = get_total_stock(session, product.id)
                    if stock <= 0:
                        continue

                    self.products[product.id] = product
                    self.product_combo.addItem(
                        f"{product.name} ({product.sku}) - Stock: {stock}",
                        product.id,
                    )

        except Exception as exc:
            QMessageBox.critical(self, "Product Error", str(exc))

    def add_selected_product(self):
        product_id = self.product_combo.currentData()

        if product_id is None:
            QMessageBox.warning(self, "No Product", "Select an available product.")
            return

        try:
            with SessionLocal() as session:
                add_cart_item(
                    session,
                    self.cart,
                    product_id,
                    self.add_quantity.value(),
                )

            self.refresh_table()
            self.update_totals()

        except ValueError as exc:
            QMessageBox.warning(self, "Invalid Quantity", str(exc))
        except Exception as exc:
            QMessageBox.critical(self, "Cart Error", str(exc))

    def refresh_table(self):
        self.table.setRowCount(0)

        for product_id, item in self.cart.items():
            row = self.table.rowCount()
            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(item["product_name"]))
            self.table.setItem(row, 1, QTableWidgetItem(item["sku"]))

            quantity = QSpinBox()
            quantity.setRange(1, 999999)
            quantity.setValue(item["quantity"])
            quantity.valueChanged.connect(
                lambda value, pid=product_id: self.change_quantity(pid, value)
            )
            self.table.setCellWidget(row, 2, quantity)

            self.table.setItem(
                row, 3, QTableWidgetItem(f'{item["unit_price"]:.2f}')
            )
            self.table.setItem(
                row, 4, QTableWidgetItem(f'{item["line_total"]:.2f}')
            )

            remove_button = QPushButton("Remove")
            remove_button.clicked.connect(
                lambda checked=False, pid=product_id: self.remove_item(pid)
            )
            self.table.setCellWidget(row, 5, remove_button)

    def change_quantity(self, product_id, quantity):
        try:
            with SessionLocal() as session:
                update_cart_quantity(
                    session, self.cart, product_id, quantity
                )

            self.refresh_table()
            self.update_totals()

        except ValueError as exc:
            QMessageBox.warning(self, "Invalid Quantity", str(exc))
            self.refresh_table()

    def remove_item(self, product_id):
        try:
            remove_cart_item(self.cart, product_id)
            self.refresh_table()
            self.update_totals()
        except ValueError as exc:
            QMessageBox.warning(self, "Cart Error", str(exc))

    def update_totals(self):
        try:
            totals = calculate_cart_totals(
                list(self.cart.values()),
                tax_rate=Decimal(str(self.tax_input.value())),
                discount_rate=Decimal(str(self.discount_input.value())),
            )

            self.subtotal_label.setText(
                f'Subtotal: {totals["subtotal"]:.2f}'
            )
            self.discount_label.setText(
                f'Discount: {totals["discount_amount"]:.2f}'
            )
            self.tax_label.setText(
                f'Tax: {totals["tax_amount"]:.2f}'
            )
            self.total_label.setText(
                f'Total: {totals["total"]:.2f}'
            )

        except ValueError as exc:
            QMessageBox.warning(self, "Calculation Error", str(exc))

    def clear_cart(self):
        self.cart.clear()
        self.refresh_table()
        self.update_totals()

    def checkout(self):
        if not self.cart:
            QMessageBox.warning(self, "Empty Cart", "Add products before checkout.")
            return

        cashier = self.cashier_input.text().strip()
        if not cashier:
            QMessageBox.warning(self, "Missing Cashier", "Enter the cashier name.")
            return

        customer_email = self.email_input.text().strip()

        try:
            with SessionLocal() as session:
                # Recheck stock immediately before checkout.
                for product_id, item in self.cart.items():
                    current_stock = get_total_stock(session, product_id)
                    if item["quantity"] > current_stock:
                        raise ValueError(
                            f'Insufficient stock for {item["product_name"]}. '
                            f"Available: {current_stock}."
                        )

                totals = calculate_cart_totals(
                    list(self.cart.values()),
                    tax_rate=Decimal(str(self.tax_input.value())),
                    discount_rate=Decimal(str(self.discount_input.value())),
                )

                invoice = generate_invoice(
                    session,
                    cashier=cashier,
                    customer_email=customer_email or None,
                    items=[
                        {
                            "product_id": item["product_id"],
                            "quantity": item["quantity"],
                        }
                        for item in self.cart.values()
                    ],
                )

                # Store the final amount including tax and discount.
                invoice.total = totals["total"]
                session.commit()

                invoice_number = invoice.invoice_number

                # Export the invoice before closing the database session.
                invoice_dir = Path(tempfile.gettempdir()) / "pms_invoices"
                invoice_dir.mkdir(parents=True, exist_ok=True)

                invoice_path = export_invoice_html(
                    invoice,
                    invoice_dir / f"{invoice_number}.html",
                )

            # The invoice is already saved. Email failure must not undo checkout.
            self.clear_cart()
            self.load_products()

            email_message = ""

            if customer_email:
                try:
                    send_invoice_email(
                        customer_email,
                        invoice_number,
                        invoice_path,
                    )
                    email_message = (
                        f"\nEmail delivery: accepted for {customer_email}."
                    )
                except Exception as email_error:
                    email_message = (
                        "\nInvoice was saved, but email delivery failed: "
                        f"{email_error}\n"
                        "The invoice remains available in the system."
                    )

            QMessageBox.information(
                self,
                "Checkout Successful",
                f"Invoice: {invoice_number}\n"
                f"Subtotal: {totals['subtotal']:.2f}\n"
                f"Discount: {totals['discount_amount']:.2f}\n"
                f"Tax: {totals['tax_amount']:.2f}\n"
                f"Total: {totals['total']:.2f}"
                f"{email_message}",
            )

        except ValueError as exc:
            QMessageBox.warning(self, "Checkout Blocked", str(exc))
        except Exception as exc:
            QMessageBox.critical(self, "Checkout Error", str(exc))
