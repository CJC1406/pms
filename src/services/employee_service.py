from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.employee import Employee


def create_employee(
    session: Session,
    *,
    employee_code: str,
    full_name: str,
    email: str | None = None,
    phone: str | None = None,
    role: str = "Cashier",
) -> Employee:
    """Create a new employee profile."""

    employee_code = employee_code.strip() if employee_code else ""
    full_name = full_name.strip() if full_name else ""
    email = email.strip().lower() if email and email.strip() else None
    phone = phone.strip() if phone and phone.strip() else None
    role = role.strip() if role else ""

    if not employee_code:
        raise ValueError("Employee code cannot be blank.")

    if not full_name:
        raise ValueError("Employee name cannot be blank.")

    if not role:
        raise ValueError("Employee role cannot be blank.")

    existing_code = session.scalar(
        select(Employee).where(
            Employee.employee_code == employee_code
        )
    )
    if existing_code:
        raise ValueError("Employee code already exists.")

    if email:
        existing_email = session.scalar(
            select(Employee).where(Employee.email == email)
        )
        if existing_email:
            raise ValueError("Email address already exists.")

    employee = Employee(
        employee_code=employee_code,
        full_name=full_name,
        email=email,
        phone=phone,
        role=role,
        is_active=True,
    )

    session.add(employee)
    session.commit()
    session.refresh(employee)

    return employee


def get_employee(session: Session, employee_id: int) -> Employee | None:
    return session.get(Employee, employee_id)


def list_employees(
    session: Session,
    *,
    active_only: bool = False,
) -> list[Employee]:
    statement = select(Employee).order_by(Employee.full_name)

    if active_only:
        statement = statement.where(Employee.is_active.is_(True))

    return list(session.scalars(statement).all())


def update_employee(
    session: Session,
    employee_id: int,
    *,
    employee_code: str,
    full_name: str,
    email: str | None = None,
    phone: str | None = None,
    role: str = "Cashier",
) -> Employee:
    employee = session.get(Employee, employee_id)

    if employee is None:
        raise ValueError("Employee does not exist.")

    employee_code = employee_code.strip() if employee_code else ""
    full_name = full_name.strip() if full_name else ""
    email = email.strip().lower() if email and email.strip() else None
    phone = phone.strip() if phone and phone.strip() else None
    role = role.strip() if role else ""

    if not employee_code:
        raise ValueError("Employee code cannot be blank.")

    if not full_name:
        raise ValueError("Employee name cannot be blank.")

    if not role:
        raise ValueError("Employee role cannot be blank.")

    duplicate_code = session.scalar(
        select(Employee).where(
            Employee.employee_code == employee_code,
            Employee.id != employee_id,
        )
    )
    if duplicate_code:
        raise ValueError("Employee code already exists.")

    if email:
        duplicate_email = session.scalar(
            select(Employee).where(
                Employee.email == email,
                Employee.id != employee_id,
            )
        )
        if duplicate_email:
            raise ValueError("Email address already exists.")

    employee.employee_code = employee_code
    employee.full_name = full_name
    employee.email = email
    employee.phone = phone
    employee.role = role

    session.commit()
    session.refresh(employee)

    return employee


def deactivate_employee(
    session: Session,
    employee_id: int,
) -> Employee:
    employee = session.get(Employee, employee_id)

    if employee is None:
        raise ValueError("Employee does not exist.")

    employee.is_active = False

    session.commit()
    session.refresh(employee)

    return employee