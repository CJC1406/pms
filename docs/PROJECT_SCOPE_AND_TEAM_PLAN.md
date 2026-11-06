# Perishables Management System
## Project Scope, Team Plan and Delivery Record

## 1. Project direction

The project expands the initial perishables inventory desktop application into a Retail Perishables and Store Operations Management System.

The application remains a Python desktop application using PySide6, SQLite, SQLAlchemy and pytest.

This document preserves the original expanded scope and records the implementation state at the end of Sprint 2. Planned requirements are not automatically treated as delivered features.

## 2. Original project scope

### P0 — Core release requirements

- Product and batch inventory management, including SKU, category, quantity, supplier, cost and selling price.
- Expiry-date tracking and FEFO stock prioritisation.
- Stock movements, stock validation and low-stock/near-expiry alerts.
- Wastage tracking.
- POS billing cart, quantity and price calculations.
- Invoice number and printable/downloadable invoice.
- Inventory deduction only after a successful sale.
- Rejection of sales exceeding available stock.
- Automated tests, CI build and usable working demonstration.

### P1 — Should-have requirements

- Customer mobile number and email for invoice delivery, with an agreed optional/required policy.
- Employee profiles and status, including active, inactive and on leave.
- Cashier association with each invoice.
- Role-based access for administrator, inventory manager and cashier.
- Dashboard for inventory, expiry, sales and waste summaries.
- Supplier and stock-receiving records.
- Audit trail for stock adjustments and completed sales.

### P2 — Stretch goals

- Email invoices.
- Attendance and shifts.
- Richer analytics and configurable dashboard widgets.
- Deployment to a test environment after CI succeeds.

## 3. Current implementation and scope deviations

The following table records the known release state as of 6 November 2026.

| Feature area | Original scope | Current release state |
|---|---|---|
| Product management | P0 | Implemented |
| Batch and stock management | P0 | Implemented |
| Expiry tracking | P0 | Implemented |
| FEFO checkout allocation | P0 | Implemented |
| POS cart and billing | P0 | Implemented |
| Invoice generation/output | P0 | Implemented; external email delivery requires separate verification |
| Waste recording and reports | P0 | Not implemented; documented scope deviation |
| Employee profiles | P1 | Implemented and merged |
| Cashier attribution | P1 | Included in merged release; retain verification evidence |
| Distinct employee on-leave state | P1 | Not confirmed; current active/inactive status does not establish a separate leave state |
| Role-based access control | P1 | Not confirmed implemented |
| Dashboard inventory/expiry/sales summaries | P1 | Implemented |
| Dashboard waste summary | P1 | Not implemented |
| Supplier and stock-receiving records | P1 | Batch receiving exists; full supplier-management scope is not confirmed |
| Complete audit trail | P1 | Not confirmed |
| Email invoice delivery | P2 | Requires configuration and failure-path verification |
| Attendance/shifts | P2 | Not confirmed implemented |
| Rich analytics/configurable widgets | P2 | Not confirmed implemented |
| Test-environment deployment | P2 | Local development and clean-checkout verification completed; remote deployment not confirmed |

The final evaluation must explain the waste-management deviation and any other requirements that remain unimplemented or unverified.

## 4. Billing rules

The agreed billing design includes:

- Generate a unique invoice identifier.
- Validate positive quantities and current selling prices.
- Apply tax/discount only according to the project rules configured by the team.
- Prevent overselling.
- Ensure inventory changes and sale records are consistent.
- Keep invoice persistence independent of email delivery failure.
- Avoid storing customer contact details in ordinary logs.
- Restrict customer data access where access controls exist.

## 5. Four-person team roles

| Member | Role | Responsibilities |
|---|---|---|
| Deeksha | Backend and data | SQLAlchemy models, database schema, inventory/sales business rules and service layer |
| Chris | UI and workflows | PySide6 screens, inventory forms, billing cart, invoice UI and dashboard |
| Janhavi | QA and CI/CD | pytest, integration/regression tests, GitHub Actions and build checks |
| Chiranth | Integration, Jira and documentation | Backlog/sprint coordination, cross-module integration, SRS/SAD/Test Plan/RTM, demo and release checklist |

Shared responsibilities:

- Each member writes tests for their changes.
- Each member updates Jira for assigned work.
- Each member opens focused pull requests.
- Team members review another member's changes.
- Deviations are documented.
- The integration/documentation owner coordinates rather than replacing the work of other members.

## 6. Git workflow

- Branch naming follows the team's agreed feature/test/CI/docs convention.
- Commits use clear prefixes such as `feat:`, `fix:`, `test:`, `ci:`, `docs:` and `refactor:`.
- Pull requests link to the relevant Jira issue.
- Pull requests describe acceptance criteria and test results.
- CI must pass before merge.
- Peer review should be recorded according to repository/team rules.
- Secrets, real customer contact data and production database files must not be committed.

Example workflow:

```bash
git switch main
git pull origin main
git switch -c feature/ISSUE-ID-short-description
```

## 7. Sprint dates and objectives

| Period | Objective | Planned outcome |
|---|---|---|
| Sprint 1: 27–31 October 2026 | Working inventory baseline and CI | Initial application, inventory workflows, first demo |
| Sprint 2: 2–7 November 2026 | Billing/invoice integration, staff/dashboard essentials, regression and documentation | Integrated application, second demo and release evidence |
| Feature freeze target: 7 November 2026 | Stop new feature development | Critical fixes only after freeze, with review |
| Final presentation: 9 November 2026 | Demonstrate and explain the project | Working demo, documentation and SDLC evidence |

## 8. Delivery and release evidence

Reported on 6 November 2026:

- 111 automated tests passed locally.
- 111 automated tests passed on a clean clone.
- Application launched successfully from a clean checkout.
- Six manual smoke-test areas passed.
- Six functional workflows passed.
- PR #21 checks passed and PR #21 merged into `main`.
- Demo video saved at `docs/evidence/demo.mov` and verified to play.
- Screenshots saved under `docs/evidence/screenshots/`.

These results do not establish that unimplemented waste management, authentication/RBAC, performance targets or usability targets have passed.

## 9. Definition of Done

A task is Done when:

- Acceptance criteria are met.
- Code is integrated into the target branch.
- Relevant automated tests pass.
- CI is green.
- Pull request review requirements are satisfied.
- Jira status, estimate and comments reflect reality.
- Documentation and RTM are updated where relevant.
- The feature can be demonstrated from the documented setup.

A requirement that is not implemented must be recorded as a deviation, not marked Done.

## 10. Jira discipline

- Estimate issues before sprint execution.
- Use story points consistently.
- Assign backlog items to the responsible team member.
- Move issues through the configured workflow based on actual progress.
- Link issues to pull requests and test evidence.
- Mark Done only after acceptance criteria and verification are complete.
- Do not alter estimates or statuses solely to improve the burndown chart.

## 11. Final evaluation preparation

Each team member should be prepared to explain:

- Their assigned Jira issues and story points.
- Their code contribution and relevant pull requests.
- The architecture and why a layered modular monolith was selected.
- The testing strategy and actual automated test results.
- The sprint workflow and collaboration process.
- Deviations between original scope and final implementation.
- The limitations that remain in the release.

The final demonstration should focus on working functionality and clearly identify features that remain planned or unimplemented.