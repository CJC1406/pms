
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
    QDialog,
    QFormLayout,
    QLineEdit,
    QComboBox,
    QDialogButtonBox,
)

from src.database.db import SessionLocal
from src.services.employee_service import (
    create_employee,
    list_employees,
    update_employee,
    deactivate_employee,
    activate_employee,
)


class EmployeeDialog(QDialog):
    def __init__(self, employee=None, parent=None):
        super().__init__(parent)

        self.setWindowTitle(
            "Edit Employee" if employee else "Add Employee"
        )
        self.setMinimumWidth(380)

        layout = QFormLayout(self)

        self.code_input = QLineEdit()
        self.name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.phone_input = QLineEdit()

        self.role_input = QComboBox()
        self.role_input.addItems([
            "Cashier",
            "Manager",
            "Admin",
        ])

        layout.addRow("Employee Code:", self.code_input)
        layout.addRow("Full Name:", self.name_input)
        layout.addRow("Email:", self.email_input)
        layout.addRow("Phone:", self.phone_input)
        layout.addRow("Role:", self.role_input)

        if employee:
            self.code_input.setText(employee.employee_code)
            self.name_input.setText(employee.full_name)
            self.email_input.setText(employee.email or "")
            self.phone_input.setText(employee.phone or "")

            index = self.role_input.findText(employee.role)
            if index >= 0:
                self.role_input.setCurrentIndex(index)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addRow(buttons)

    def get_data(self):
        return {
            "employee_code": self.code_input.text().strip(),
            "full_name": self.name_input.text().strip(),
            "email": self.email_input.text().strip() or None,
            "phone": self.phone_input.text().strip() or None,
            "role": self.role_input.currentText(),
        }


class EmployeePage(QWidget):
    def __init__(self, page_name="Employee Management", parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(14)

        title = QLabel("Employee Management")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

        description = QLabel(
            "Create employee profiles and manage cashier accounts."
        )
        description.setObjectName("description")
        layout.addWidget(description)

        button_row = QHBoxLayout()

        add_button = QPushButton("Add Employee")
        add_button.setObjectName("actionButton")
        add_button.clicked.connect(self.add_employee)
        button_row.addWidget(add_button)

        edit_button = QPushButton("Edit Selected")
        edit_button.setObjectName("actionButton")
        edit_button.clicked.connect(self.edit_employee)
        button_row.addWidget(edit_button)

        deactivate_button = QPushButton("Deactivate Selected")
        deactivate_button.setObjectName("actionButton")
        deactivate_button.clicked.connect(self.deactivate_employee)
        button_row.addWidget(deactivate_button)

        activate_button = QPushButton("Activate Selected")
        activate_button.setObjectName("actionButton")
        activate_button.clicked.connect(
            self.activate_selected_employee
        )
        button_row.addWidget(activate_button)

        refresh_button = QPushButton("Refresh")
        refresh_button.setObjectName("actionButton")
        refresh_button.clicked.connect(self.load_employees)
        button_row.addWidget(refresh_button)

        layout.addLayout(button_row)

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels([
            "Employee Code",
            "Full Name",
            "Email",
            "Phone",
            "Role",
            "Status",
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.table.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )

        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        layout.addWidget(self.table)

        self.load_employees()

    def load_employees(self):
        self.table.setRowCount(0)

        try:
            with SessionLocal() as session:
                employees = list_employees(
                    session,
                    active_only=False,
                )

                for employee in employees:
                    row = self.table.rowCount()
                    self.table.insertRow(row)

                    values = [
                        employee.employee_code,
                        employee.full_name,
                        employee.email or "",
                        employee.phone or "",
                        employee.role,
                        "Active" if employee.is_active else "Inactive",
                    ]

                    for column, value in enumerate(values):
                        cell = QTableWidgetItem(str(value))

                        if column == 0:
                            cell.setData(
                                Qt.ItemDataRole.UserRole,
                                employee.id,
                            )

                        self.table.setItem(row, column, cell)

        except Exception as exc:
            QMessageBox.critical(
                self,
                "Employee Error",
                str(exc),
            )

    def selected_employee_id(self):
        row = self.table.currentRow()

        if row < 0:
            return None

        item = self.table.item(row, 0)

        if item is None:
            return None

        return item.data(Qt.ItemDataRole.UserRole)

    def add_employee(self):
        dialog = EmployeeDialog(parent=self)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        data = dialog.get_data()

        try:
            with SessionLocal() as session:
                create_employee(session, **data)

            self.load_employees()

            QMessageBox.information(
                self,
                "Success",
                "Employee created successfully.",
            )

        except Exception as exc:
            QMessageBox.warning(
                self,
                "Could Not Create Employee",
                str(exc),
            )

    def edit_employee(self):
        employee_id = self.selected_employee_id()

        if employee_id is None:
            QMessageBox.warning(
                self,
                "No Selection",
                "Select an employee first.",
            )
            return

        try:
            with SessionLocal() as session:
                employees = list_employees(session)
                employee = next(
                    (
                        item for item in employees
                        if item.id == employee_id
                    ),
                    None,
                )

            if employee is None:
                QMessageBox.warning(
                    self,
                    "Not Found",
                    "Employee could not be found.",
                )
                return

            dialog = EmployeeDialog(employee, self)

            if dialog.exec() != QDialog.DialogCode.Accepted:
                return

            data = dialog.get_data()

            with SessionLocal() as session:
                update_employee(session, employee_id, **data)

            self.load_employees()

            QMessageBox.information(
                self,
                "Success",
                "Employee updated successfully.",
            )

        except Exception as exc:
            QMessageBox.warning(
                self,
                "Update Failed",
                str(exc),
            )

    def deactivate_employee(self):
        employee_id = self.selected_employee_id()

        if employee_id is None:
            QMessageBox.warning(
                self,
                "No Selection",
                "Select an employee first.",
            )
            return

        answer = QMessageBox.question(
            self,
            "Confirm Deactivation",
            "Are you sure you want to deactivate this employee?",
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        try:
            with SessionLocal() as session:
                deactivate_employee(session, employee_id)

            self.load_employees()

            QMessageBox.information(
                self,
                "Success",
                "Employee deactivated successfully.",
            )

        except Exception as exc:
            QMessageBox.warning(
                self,
                "Deactivation Failed",
                str(exc),
            )

    def activate_selected_employee(self):
        employee_id = self.selected_employee_id()

        if employee_id is None:
            QMessageBox.warning(
                self,
                "No Selection",
                "Select an employee first.",
            )
            return

        try:
            with SessionLocal() as session:
                activate_employee(session, employee_id)

            self.load_employees()

            QMessageBox.information(
                self,
                "Success",
                "Employee activated successfully.",
            )

        except Exception as exc:
            QMessageBox.warning(
                self,
                "Activation Failed",
                str(exc),
            )
