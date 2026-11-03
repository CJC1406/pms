
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QGridLayout,
    QStackedWidget,
)

from src.database.db import SessionLocal
from src.services.inventory_service import (
    list_products,
    get_total_stock,
)
from src.services.expiry_service import get_expiring_batches
from src.ui.inventory_page import InventoryPage
from src.ui.expiry_page import ExpiryPage
from src.ui.cart_page import CartPage


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("PMS | Perishables Management System")
        self.resize(1150, 750)
        self.dark_mode = False

        self.setStyleSheet(self.light_theme())

        central = QWidget()
        self.setCentralWidget(central)

        root_layout = QHBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # Sidebar
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(230)

        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(18, 25, 18, 20)
        sidebar_layout.setSpacing(12)

        logo = QLabel("PMS")
        logo.setObjectName("logo")
        sidebar_layout.addWidget(logo)

        subtitle = QLabel("Perishables Management")
        subtitle.setObjectName("sidebarSubtitle")
        subtitle.setWordWrap(True)
        sidebar_layout.addWidget(subtitle)

        sidebar_layout.addSpacing(25)

        self.pages = QStackedWidget()

        navigation = [
            ("Dashboard", self.create_dashboard),
            ("Inventory", InventoryPage),
            ("POS / Cart", CartPage),
            ("Expiry Tracking", ExpiryPage),
            ("Waste Management", self.create_placeholder),
            ("Reports", self.create_placeholder),
        ]

        self.nav_buttons = []

        for index, (name, page_creator) in enumerate(navigation):
            button = QPushButton(name)
            button.setObjectName("navButton")
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(
                lambda checked=False, i=index: self.change_page(i)
            )

            sidebar_layout.addWidget(button)
            self.nav_buttons.append(button)

            page = page_creator(name)
            self.pages.addWidget(page)

        sidebar_layout.addStretch()

        self.theme_button = QPushButton("Switch to Dark Mode")
        self.theme_button.setObjectName("themeButton")
        self.theme_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.theme_button.clicked.connect(self.toggle_theme)
        sidebar_layout.addWidget(self.theme_button)

        footer = QLabel("PMS • Inventory Control")
        footer.setObjectName("footer")
        sidebar_layout.addWidget(footer)

        root_layout.addWidget(self.sidebar)
        root_layout.addWidget(self.pages, 1)

        self.change_page(0)

    def create_dashboard(self, page_name):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(20)

        header = QHBoxLayout()

        title = QLabel("Dashboard")
        title.setObjectName("pageTitle")
        header.addWidget(title)

        header.addStretch()

        status = QLabel("STORE OVERVIEW")
        status.setObjectName("statusLabel")
        header.addWidget(status)

        layout.addLayout(header)

        description = QLabel(
            "Monitor stock levels, upcoming expiries, and product waste."
        )
        description.setObjectName("description")
        layout.addWidget(description)

        section_title = QLabel("Inventory Overview")
        section_title.setObjectName("sectionTitle")
        layout.addWidget(section_title)

        cards_layout = QGridLayout()
        cards_layout.setSpacing(16)

        self.dashboard_values = {}

        cards = [
            ("Total Products", "0", "Active products in catalogue"),
            ("Low Stock", "0", "Products needing attention"),
            ("Expiring Soon", "0", "Batches expiring within 7 days"),
            ("Waste This Month", "N/A", "Waste tracking not implemented"),
        ]

        for index, (heading, value, detail) in enumerate(cards):
            card = self.create_card(heading, value, detail)

            value_label = card.findChild(QLabel, "cardValue")
            self.dashboard_values[heading] = value_label

            cards_layout.addWidget(card, index // 2, index % 2)

        layout.addLayout(cards_layout)

        section_title = QLabel("Quick Actions")
        section_title.setObjectName("sectionTitle")
        layout.addWidget(section_title)

        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(12)

        actions = [
            ("View Inventory", 1),
            ("Check Expiry", 2),
            ("Record Waste", 3),
        ]

        for text, page_index in actions:
            button = QPushButton(text)
            button.setObjectName("actionButton")
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(
                lambda checked=False, i=page_index: self.change_page(i)
            )
            actions_layout.addWidget(button)

        layout.addLayout(actions_layout)
        layout.addStretch()

        self.refresh_dashboard()

        return page

    def refresh_dashboard(self):
        """Update dashboard statistics from the database."""

        try:
            with SessionLocal() as session:
                products = list_products(session)

                total_products = len(products)
                low_stock = 0

                for product in products:
                    stock = get_total_stock(session, product.id)

                    if stock <= product.low_stock_threshold:
                        low_stock += 1

                expiring_soon = len(
                    get_expiring_batches(session, days=7)
                )

            self.dashboard_values["Total Products"].setText(
                str(total_products)
            )

            self.dashboard_values["Low Stock"].setText(
                str(low_stock)
            )

            self.dashboard_values["Expiring Soon"].setText(
                str(expiring_soon)
            )

        except Exception as exc:
            for label in self.dashboard_values.values():
                label.setText("Error")

            print(f"Dashboard update failed: {exc}")

    def create_card(self, heading, value, detail):
        card = QFrame()
        card.setObjectName("dashboardCard")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(10)

        heading_label = QLabel(heading)
        heading_label.setObjectName("cardHeading")

        value_label = QLabel(value)
        value_label.setObjectName("cardValue")

        detail_label = QLabel(detail)
        detail_label.setObjectName("cardDetail")

        layout.addWidget(heading_label)
        layout.addWidget(value_label)
        layout.addWidget(detail_label)

        return card

    def create_placeholder(self, page_name):
        page = QWidget()

        layout = QVBoxLayout(page)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(16)

        title = QLabel(page_name)
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        message = QLabel(
            f"The {page_name.lower()} module will be implemented "
            "in a future development step."
        )
        message.setObjectName("description")
        message.setWordWrap(True)
        layout.addWidget(message)

        layout.addStretch()

        return page

    def change_page(self, index):
        self.pages.setCurrentIndex(index)

        for button_index, button in enumerate(self.nav_buttons):
            button.setProperty("active", button_index == index)
            button.style().unpolish(button)
            button.style().polish(button)

        if index == 0:
            self.refresh_dashboard()

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode

        if self.dark_mode:
            self.setStyleSheet(self.dark_theme())
            self.theme_button.setText("Switch to Light Mode")
        else:
            self.setStyleSheet(self.light_theme())
            self.theme_button.setText("Switch to Dark Mode")

    @staticmethod
    def light_theme():
        return """
        QMainWindow, QWidget {
            background-color: #FFF1F6;
            color: #422536;
            font-family: Arial;
            font-size: 13px;
        }

        QFrame#sidebar {
            background-color: #FFFFFF;
            border-right: 1px solid #F3D6E2;
        }

        QLabel#logo {
            color: #DB2777;
            font-size: 30px;
            font-weight: bold;
        }

        QLabel#sidebarSubtitle {
            color: #8D687A;
            font-size: 11px;
        }

        QPushButton#navButton {
            text-align: left;
            padding: 12px;
            border: none;
            border-radius: 8px;
            color: #765365;
            background-color: transparent;
        }

        QPushButton#navButton:hover {
            background-color: #FCE7F0;
            color: #BE185D;
        }

        QPushButton#navButton[active="true"] {
            background-color: #FBCFE0;
            color: #9D174D;
            font-weight: bold;
        }

        QPushButton#themeButton {
            padding: 11px;
            border: 1px solid #F0C4D6;
            border-radius: 8px;
            background-color: #FFFFFF;
            color: #9D174D;
        }

        QPushButton#themeButton:hover,
        QPushButton#actionButton:hover {
            background-color: #FCE7F0;
        }

        QLabel#footer {
            color: #9B7C8C;
            font-size: 11px;
        }

        QLabel#pageTitle {
            font-size: 27px;
            font-weight: bold;
            color: #4A1832;
        }

        QLabel#description {
            color: #876579;
            font-size: 13px;
        }

        QLabel#statusLabel {
            color: #BE185D;
            font-size: 11px;
            font-weight: bold;
        }

        QLabel#sectionTitle {
            font-size: 17px;
            font-weight: bold;
            color: #652342;
            padding-top: 8px;
        }

        QFrame#dashboardCard {
            background-color: #FFFFFF;
            border: 1px solid #F3D6E2;
            border-radius: 12px;
        }

        QLabel#cardHeading {
            color: #876579;
            font-size: 12px;
        }

        QLabel#cardValue {
            color: #9D174D;
            font-size: 28px;
            font-weight: bold;
        }

        QLabel#cardDetail {
            color: #9B7C8C;
            font-size: 11px;
        }

        QPushButton#actionButton {
            background-color: #FFFFFF;
            border: 1px solid #F0C4D6;
            border-radius: 8px;
            padding: 13px;
            color: #9D174D;
        }
        """

    @staticmethod
    def dark_theme():
        return """
        QMainWindow, QWidget {
            background-color: #21141D;
            color: #FCE7F0;
            font-family: Arial;
            font-size: 13px;
        }

        QFrame#sidebar {
            background-color: #2C1B28;
            border-right: 1px solid #493044;
        }

        QLabel#logo {
            color: #F9A8D4;
            font-size: 30px;
            font-weight: bold;
        }

        QLabel#sidebarSubtitle, QLabel#description,
        QLabel#cardHeading, QLabel#footer {
            color: #D5B8C8;
        }

        QPushButton#navButton {
            text-align: left;
            padding: 12px;
            border: none;
            border-radius: 8px;
            color: #E8D4E0;
            background-color: transparent;
        }

        QPushButton#navButton:hover,
        QPushButton#navButton[active="true"] {
            background-color: #493044;
            color: #F9A8D4;
        }

        QPushButton#navButton[active="true"] {
            font-weight: bold;
        }

        QPushButton#themeButton, QPushButton#actionButton {
            background-color: #3B2636;
            color: #FCE7F0;
            border: 1px solid #654057;
            border-radius: 8px;
            padding: 11px;
        }

        QPushButton#themeButton:hover,
        QPushButton#actionButton:hover {
            background-color: #593349;
        }

        QLabel#pageTitle, QLabel#sectionTitle,
        QLabel#cardValue {
            color: #FFE4F0;
        }

        QLabel#pageTitle {
            font-size: 27px;
            font-weight: bold;
        }

        QLabel#sectionTitle {
            font-size: 17px;
            font-weight: bold;
            padding-top: 8px;
        }

        QLabel#statusLabel {
            color: #F9A8D4;
            font-size: 11px;
            font-weight: bold;
        }

        QFrame#dashboardCard {
            background-color: #2C1B28;
            border: 1px solid #493044;
            border-radius: 12px;
        }

        QLabel#cardValue {
            font-size: 28px;
            font-weight: bold;
        }

        QLabel#cardDetail {
            color: #D5B8C8;
            font-size: 11px;
        }
        """


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
