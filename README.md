# Perishables Management System (PMS)

A customisable desktop application for managing perishable inventory in retail stores. The system aims to reduce wastage, monitor expiry dates, improve stock rotation, and provide useful inventory reports.

## Technology Stack

- **Language:** Python 3
- **GUI:** PySide6
- **Database:** SQLite
- **ORM:** SQLAlchemy
- **Testing:** pytest and pytest-qt
- **CI:** GitHub Actions
- **Version Control:** Git and GitHub

## Getting Started

### Prerequisites

Install Python 3.10 or newer. Python 3.12 is the version configured in the current GitHub Actions workflow.

Install Git and ensure you have access to the private GitHub repository.

### 1. Clone the repository

Open Terminal and run:

```bash
git clone https://github.com/CJC1406/pms.git
cd pms
```

### 2. Create a virtual environment

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run tests

```bash
python -m pytest
```

### 5. Run the desktop application

Once the application entry point and GUI module have been committed:

```bash
python -m src.main
```

If these modules are not yet present in the branch you cloned, continue with the setup and development tasks assigned to your team.

## Project Structure

```text
pms/
├── .github/
│   └── workflows/
│       └── ci.yml             # Automated testing workflow
├── assets/                    # Icons, images, and other UI assets
├── docs/
│   └── diagrams/              # UML and architecture diagrams
├── src/
│   ├── main.py                # Application entry point
│   ├── ui/                    # Windows, pages, and themes
│   ├── models/                # SQLAlchemy data models
│   ├── services/              # Inventory and business logic
│   └── database/              # Database configuration
├── tests/
│   ├── unit/                  # Unit tests
│   └── integration/           # Integration tests
├── .gitignore
├── README.md
└── requirements.txt
```

Some modules may still be under development. The structure above describes the intended organisation; check the actual files on your current branch before assuming a feature is implemented.

### Folder Responsibilities

| Folder | Purpose |
|---|---|
| `src/ui/` | PySide6 interface, navigation, dashboard, and themes |
| `src/models/` | Product, batch, and stock-movement models |
| `src/services/` | Inventory, expiry, FEFO, waste, and reporting logic |
| `src/database/` | SQLite connection and database setup |
| `tests/unit/` | Tests for individual functions and business rules |
| `tests/integration/` | Tests across connected modules |
| `docs/` | SRS, SAD, test plan, design decisions, and other project documentation |
| `assets/` | Icons, images, and interface resources |
| `.github/workflows/` | GitHub Actions CI configuration |

## Planned Features

1. Product and batch management.
2. Stock quantity and stock-movement tracking.
3. Expiry-date monitoring and alerts.
4. FEFO (First Expired, First Out) stock prioritisation.
5. Waste recording and analysis.
6. Low-stock monitoring and reorder suggestions.
7. Inventory dashboard and reports.
8. Customisable themes and dashboard widgets.

## Team Development Workflow

### Branching

Do not commit feature work directly to `main`.

Create a feature branch from the latest `main` branch:

```bash
git switch main
git pull origin main
git switch -c feature/your-feature-name
```

Use a descriptive branch name, such as:

- `feature/ui-dashboard`
- `feature/inventory-database`
- `feature/expiry-waste`
- `feature/reports-testing`

### Commit conventions

Use meaningful commit messages that describe the change:

```text
feat(ui): add dashboard navigation
feat(inventory): implement batch management
fix(expiry): correct expiry status calculation
test(inventory): test stock validation
docs(readme): document local setup
```

Each change must have appropriate documentation. Add or update tests when behaviour changes, and update project documentation when requirements, interfaces, or design decisions change. Avoid artificial commits created solely to increase commit counts.

### Pull requests

1. Push your feature branch to GitHub.
2. Open a pull request targeting `main`.
3. Describe the changes and testing performed.
4. Request a review from another team member.
5. Ensure CI checks pass before merging.

**Important:** Chiranth is the only team member authorised to use the pull-request bypass when necessary. All other team members must follow the pull-request process. Chiranth should also use pull requests by default.

### Documentation

Maintain the project documents in `docs/`, including:

- Software Requirements Specification (SRS)
- Software Architecture and Design (SAD)
- Software Test Plan
- Requirements Traceability Matrix (RTM)
- UML diagrams and relevant design decisions

Keep documentation consistent with the features actually implemented.

## Current Project Status

The repository setup and initial CI workflow are established. The application is being developed incrementally, beginning with the desktop dashboard and project structure.

Features described as planned are not necessarily implemented yet.

## Repository

GitHub: https://github.com/CJC1406/pms