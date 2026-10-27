# Perishables Management System — Expanded Scope and Team Plan

## Project direction
Expand the initial perishables inventory desktop application into a Retail Perishables and Store Operations Management System. The application remains a Python desktop application using PySide6, SQLite, SQLAlchemy and pytest unless the team agrees on a documented change.

## Scope
### P0 — Core release
- Product and batch inventory management (SKU, category, quantity, supplier, cost and selling price).
- Expiry-date tracking and FEFO (First Expired, First Out) stock prioritisation.
- Stock movements, stock validation, low-stock/near-expiry alerts and wastage tracking.
- Point-of-sale billing cart, quantity and price calculations, invoice number and printable/downloadable invoice.
- Inventory deduction only after a successful sale; reject sales exceeding available stock.
- Automated tests, CI build and usable working demo.

### P1 — Should have
- Capture customer mobile number and email for invoice delivery, with clear optional/required policy set by the team.
- Employee profiles and status (active, inactive, on leave); associate a cashier with each invoice.
- Role-based access for administrator, inventory manager and cashier.
- Dashboard for inventory, expiry, sales and waste summaries.
- Supplier and stock-receiving records.
- Audit trail for stock adjustments and completed sales.

### P2 — Stretch goals
- Email invoices, attendance/shifts, richer analytics and configurable dashboard widgets.
- Deployment to a test environment after CI succeeds.

## Billing rules
- Generate a unique invoice identifier.
- Validate positive quantities and current selling prices.
- Apply tax/discount only according to the project rules configured by the team.
- Prevent overselling and ensure inventory changes and sale records are consistent.
- Invoice generation must still work if email delivery fails.
- Do not store customer contact details in ordinary logs; restrict access to customer data.

## Four-person team roles (replace placeholders with actual names)
1. **Member 1 — Backend and data:** SQLAlchemy models, database migrations/schema, inventory/sales business rules and APIs/service layer.
2. **Member 2 — UI and workflows:** PySide6 screens, inventory forms, billing cart, invoice UI and dashboard.
3. **Member 3 — QA and CI/CD:** pytest, integration/regression tests, GitHub Actions, build checks and deployment workflow.
4. **Member 4 — Integration, Jira and documentation:** backlog/sprint coordination, cross-module integration, SRS/SAD/Test Plan/RTM compilation, demo and release checklist.

Shared responsibilities: each member writes tests for their changes, updates Jira, opens small pull requests, reviews another member's PR, and documents deviations. Member 4 coordinates rather than doing all documentation alone.

## Git workflow
- Branch naming: `feature/PMS-<issue>-short-name`, `test/PMS-<issue>-short-name`, `ci/PMS-<issue>-short-name`, `docs/PMS-<issue>-short-name`.
- Commit prefixes: `feat:`, `fix:`, `test:`, `ci:`, `docs:`, `refactor:`.
- PRs must link a Jira issue, state acceptance criteria/test results and receive a peer review before merge.
- Protect `main` where repository settings allow; run CI on PRs and pushes to main.
- Never commit secrets, real customer contact data, or production data.

## Sprint dates
- Sprint 1: 27–31 October 2026 — working inventory baseline, CI checks, first demo.
- Sprint 2: 2–7 November 2026 — billing/invoice integration, staff and dashboard essentials, regression tests, final documentation and second demo.
- Presentation: 9 November 2026.
- Freeze feature development on 7 November; only critical fixes afterwards with review.

## Definition of Done
- Acceptance criteria are met and the code is integrated.
- Relevant automated tests pass; CI is green.
- Pull request is reviewed and merged.
- Jira status, estimate and comments reflect reality.
- Documentation and RTM are updated where relevant.
- Demo can be run from a clean checkout using the documented instructions.

## Jira discipline
- Estimate issues before sprint start; use story points consistently.
- Move issues through the team's configured workflow as work progresses.
- Mark Done only after acceptance criteria and verification are complete.
- Never alter estimates or statuses solely to improve the burndown chart.
