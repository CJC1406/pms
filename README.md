# Perishables Management System

A customisable desktop application for managing perishable inventory in retail stores, expanded toward retail billing and store operations.

## Product Scope

### Core inventory and perishables
- Product and batch management
- Expiry monitoring and alerts
- FEFO-based stock prioritisation
- Stock movement, low-stock alerts and wastage tracking
- Inventory dashboard and reports

### Retail billing and invoices
- Billing cart and checkout validation
- Unique invoice generation and printable/exportable invoices
- Customer mobile number and email capture according to the agreed invoice policy
- Stock deduction only after a successful sale; prevent overselling
- Email invoice delivery is a stretch goal and must not block invoice generation

### Employee and store operations
- Employee profiles and active/inactive/on-leave status
- Cashier attribution on invoices
- Role-based access and store dashboard summaries

## Planned Technology Stack

- Python
- PySide6
- SQLite
- SQLAlchemy
- pytest
- GitHub Actions for CI

## Project Structure

- `src/ui/` — Desktop interface
- `src/models/` — Data models
- `src/services/` — Inventory, expiry and billing business logic
- `src/database/` — Database configuration
- `tests/` — Automated tests
- `docs/` — Software engineering documentation
- `assets/` — UI assets

## Team Workflow

- Work from Jira stories and include the Jira issue key in branch names, commits and pull requests.
- Use feature branches and peer-reviewed pull requests.
- Run automated tests and build checks in GitHub Actions.
- Update Jira as work progresses; mark an issue Done only after acceptance criteria are met.
- Do not commit credentials, real customer contact details or production data.

See [Expanded Project Scope and Team Plan](docs/PROJECT_SCOPE_AND_TEAM_PLAN.md) for priorities, role split, sprint dates, Git workflow and Definition of Done.

## Sprint Schedule

- Sprint 1: 27–31 October 2026
- Sprint 2: 2–7 November 2026
- Presentation: 9 November 2026

## Status

Scope and initial Jira backlog defined. Implementation and CI validation are in progress.
