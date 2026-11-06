
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.database.db import Base
from src.models import batch, employee, invoice, product
from src.services.employee_service import (
    activate_employee,
    create_employee,
    deactivate_employee,
    get_employee,
    list_employees,
    update_employee,
)


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    TestingSession = sessionmaker(bind=engine)

    with TestingSession() as db:
        yield db

    Base.metadata.drop_all(engine)
    engine.dispose()


def add_employee(session, code="EMP001", name="Test Employee",
                 email="test@example.com"):
    return create_employee(
        session,
        employee_code=code,
        full_name=name,
        email=email,
    )


def test_create_employee(session):
    employee = create_employee(
        session,
        employee_code=" EMP001 ",
        full_name=" Test Employee ",
        email=" TEST@EXAMPLE.COM ",
        phone=" 1234567890 ",
    )

    assert employee.employee_code == "EMP001"
    assert employee.full_name == "Test Employee"
    assert employee.email == "test@example.com"
    assert employee.phone == "1234567890"
    assert employee.role == "Cashier"
    assert employee.is_active is True


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("employee_code", "   ", "Employee code cannot be blank."),
        ("full_name", "   ", "Employee name cannot be blank."),
        ("role", "   ", "Employee role cannot be blank."),
    ],
)
def test_create_employee_rejects_blank_required_fields(
    session, field, value, message
):
    data = {
        "employee_code": "EMP001",
        "full_name": "Test Employee",
        "role": "Cashier",
    }
    data[field] = value

    with pytest.raises(ValueError, match=message):
        create_employee(session, **data)


def test_create_employee_rejects_duplicate_code(session):
    add_employee(session)

    with pytest.raises(ValueError, match="Employee code already exists."):
        add_employee(session, email="other@example.com")


def test_create_employee_rejects_duplicate_email(session):
    add_employee(session)

    with pytest.raises(ValueError, match="Email address already exists."):
        add_employee(session, code="EMP002")


def test_create_employee_normalizes_optional_blank_fields(session):
    employee = create_employee(
        session,
        employee_code="EMP001",
        full_name="Test Employee",
        email="   ",
        phone="   ",
    )

    assert employee.email is None
    assert employee.phone is None


def test_get_employee(session):
    employee = add_employee(session)

    result = get_employee(session, employee.id)

    assert result is not None
    assert result.id == employee.id


def test_get_employee_returns_none_for_missing_id(session):
    assert get_employee(session, 999) is None


def test_list_employees_returns_sorted_employees(session):
    add_employee(session, "EMP002", "Zara")
    add_employee(session, "EMP001", "Adam", "adam@example.com")

    employees = list_employees(session)

    assert [employee.full_name for employee in employees] == ["Adam", "Zara"]


def test_list_employees_active_only(session):
    first = add_employee(session, "EMP001", "Adam")
    second = add_employee(session, "EMP002", "Zara", "zara@example.com")
    deactivate_employee(session, second.id)

    employees = list_employees(session, active_only=True)

    assert [employee.id for employee in employees] == [first.id]


def test_update_employee(session):
    employee = add_employee(session)

    updated = update_employee(
        session,
        employee.id,
        employee_code="EMP010",
        full_name="Updated Name",
        email=" UPDATED@EXAMPLE.COM ",
        phone=" 9876543210 ",
        role="Manager",
    )

    assert updated.employee_code == "EMP010"
    assert updated.full_name == "Updated Name"
    assert updated.email == "updated@example.com"
    assert updated.phone == "9876543210"
    assert updated.role == "Manager"


def test_update_employee_rejects_missing_employee(session):
    with pytest.raises(ValueError, match="Employee does not exist."):
        update_employee(
            session,
            999,
            employee_code="EMP001",
            full_name="Test",
        )


def test_update_employee_rejects_duplicate_code(session):
    first = add_employee(session, "EMP001", "Adam")
    second = add_employee(session, "EMP002", "Zara", "zara@example.com")

    with pytest.raises(ValueError, match="Employee code already exists."):
        update_employee(
            session,
            second.id,
            employee_code=first.employee_code,
            full_name="Zara",
        )


def test_update_employee_rejects_duplicate_email(session):
    first = add_employee(session, "EMP001", "Adam")
    second = add_employee(session, "EMP002", "Zara", "zara@example.com")

    with pytest.raises(ValueError, match="Email address already exists."):
        update_employee(
            session,
            second.id,
            employee_code="EMP002",
            full_name="Zara",
            email=first.email,
        )


def test_update_employee_rejects_blank_required_fields(session):
    employee = add_employee(session)

    with pytest.raises(ValueError, match="Employee name cannot be blank."):
        update_employee(
            session,
            employee.id,
            employee_code="EMP001",
            full_name="   ",
        )


def test_deactivate_employee(session):
    employee = add_employee(session)

    result = deactivate_employee(session, employee.id)

    assert result.is_active is False


def test_deactivate_employee_rejects_missing_employee(session):
    with pytest.raises(ValueError, match="Employee does not exist."):
        deactivate_employee(session, 999)


def test_activate_employee(session):
    employee = add_employee(session)
    deactivate_employee(session, employee.id)

    result = activate_employee(session, employee.id)

    assert result.is_active is True


def test_activate_employee_rejects_missing_employee(session):
    with pytest.raises(ValueError, match="Employee not found."):
        activate_employee(session, 999)
