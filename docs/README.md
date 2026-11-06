# Perishables Management System (PMS)

A desktop application for managing perishable retail inventory, batches, expiry dates, point-of-sale billing, invoices and employee information.

## 1. Project overview

The Perishables Management System helps a retail store manage products and perishable stock while supporting billing and invoice generation.

The application is designed as a local desktop system using Python, PySide6, SQLAlchemy and SQLite.

## 2. Current release features

- Product creation, viewing, updating and deactivation.
- Batch-based stock receiving and quantity tracking.
- Expiry tracking for expired and near-expiry stock.
- FEFO (First Expired, First Out) stock allocation during checkout.
- POS cart and invoice generation.
- Stock deduction during successful checkout.
- Employee profile management and cashier-related workflows.
- Dashboard summaries for inventory, expiry and sales.
- Light and dark UI themes.

## 3. Known limitations

The following expanded-scope requirements are not confirmed as implemented in the current release:

- Waste recording, batch write-off and waste reports.
- Full authentication and role-based access control.
- A complete audit trail for all stock and employee changes.
- Formal performance and usability acceptance measurements.
- Production multi-user or multi-store deployment.

These limitations are documented in `docs/SRS.md`, `docs/SAD.md` and `docs/RTM.md`.

## 4. Technology stack

| Component | Technology |
|---|---|
| Programming language | Python 3 |
| Desktop UI | PySide6 |
| ORM | SQLAlchemy |
| Database | SQLite |
| Automated testing | pytest |
| UI testing | pytest-qt where applicable |
| CI | GitHub Actions |
| Version control | Git and GitHub |

## 5. Prerequisites

Install:

- Python 3.
- Git.
- pip.
- A supported desktop environment for PySide6.

## 6. Clone the repository

```bash
git clone https://github.com/CJC1406/pms.git
cd pms
```

## 7. Create and activate a virtual environment

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows PowerShell

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use the appropriate local execution-policy procedure permitted on your machine, or activate the environment using Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

## 8. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 9. Run the application

From the repository root, with the virtual environment activated:

```bash
python -m src.main
```

The application uses its configured SQLite database. Use synthetic/test records during evaluation; do not commit real customer data or local database files containing sensitive information.

## 10. Run automated tests

Run the full test suite:

```bash
python -m pytest -q
```

To run a specific test file:

```bash
python -m pytest tests/unit/test_invoice_service.py -q
```

The reported release regression result on 6 November 2026 was **111 tests passed**. A clean-checkout run also reported 111 passing tests.

## 11. Repository structure

The main project areas are:

```text
pms/
├── src/
│   ├── database/
│   ├── models/
│   ├── services/
│   ├── ui/
│   └── main.py
├── tests/
│   ├── unit/
│   └── ...
├── docs/
│   ├── evidence/
│   │   ├── screenshots/
│   │   └── demo.mov
│   ├── SRS.md
│   ├── SAD.md
│   ├── TEST_PLAN.md
│   ├── RTM.md
│   ├── RELEASE_CHECKLIST.md
│   └── MANUAL_TEST_EVIDENCE.md
├── .github/
│   └── workflows/
├── requirements.txt
└── README.md
```

Some local or generated files may not be committed. The repository contents on `main` are authoritative.

## 12. Development workflow

1. Pull the latest changes from `main`.
2. Create a feature branch for the assigned Jira issue.
3. Implement the change and add relevant tests.
4. Run the test suite locally.
5. Commit and push the feature branch.
6. Open a pull request linked to the Jira issue.
7. Obtain review and pass CI checks.
8. Merge only after acceptance criteria are verified.
9. Update relevant documentation and Jira status.

Example:

```bash
git switch main
git pull origin main
git switch -c feature/ISSUE-ID-short-description
```

Use the actual Jira issue ID and agreed branch naming convention.

## 13. Release verification evidence

Reported on 6 November 2026:

- 111 automated tests passed locally.
- 111 automated tests passed on a clean clone.
- Application launched successfully from a clean checkout.
- Six manual smoke-test areas passed.
- Six functional workflows passed.
- PR #21 merged into `main`, with all reported PR checks passing.
- Demo recording stored at `docs/evidence/demo.mov`.
- Screenshots stored at `docs/evidence/screenshots/`.

See `docs/RELEASE_CHECKLIST.md` and `docs/MANUAL_TEST_EVIDENCE.md` for release evidence.

## 14. Project documentation

| Document | Purpose |
|---|---|
| `docs/SRS.md` | Software requirements and acceptance criteria |
| `docs/SAD.md` | Architecture, components, data and design decisions |
| `docs/TEST_PLAN.md` | Test strategy, cases and execution evidence |
| `docs/RTM.md` | Requirement-to-design and test traceability |
| `docs/RELEASE_CHECKLIST.md` | Release readiness and evidence |
| `PROJECT_SCOPE_AND_TEAM_PLAN.md` | Original scope, roles and sprint plan |

## 15. Team

| Member | Responsibility |
|---|---|
| Deeksha | Backend and data |
| Chris | UI and workflows |
| Janhavi | QA and CI/CD |
| Chiranth | Integration, Jira and documentation |

## 16. Repository

GitHub: https://github.com/CJC1406/pms