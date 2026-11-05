# Software Test Plan (STP)
## Perishables Management System — Expanded Retail Operations Scope

| Field | Value |
|---|---|
| Version | 1.0 — Expanded-scope draft |
| Date | 5 November 2026 |
| Authors | PMS Team |
| Test plan owner | Member 4 — Chiranth, with all members testing their changes |
| Status | Draft for peer review |
| Test framework | pytest; pytest-qt where GUI tests are available |

## 1. Introduction

### 1.1 Purpose
Define test scope, strategy, environment, responsibilities, entry/exit criteria, test cases, security validation, metrics and traceability for the expanded PMS.

### 1.2 Scope
Testing covers product/batch inventory, expiry and FEFO, billing/checkout, invoices, employee profiles/cashier attribution, dashboard summaries and the planned waste-management workflow. Waste tests are design/acceptance cases until the feature is implemented.

### 1.3 References
SRS.md, SAD.md, RTM.md, project scope/team plan, repository tests and the supplied evaluation checklist.

### 1.4 Definitions
FEFO, POS, SKU, NFR, RTM, UAT, PII, RBAC.

## 2. Test items
- Product and batch inventory services/UI.
- Expiry tracking and FEFO allocation.
- Cart and checkout service/UI.
- Invoice creation, export and optional email delivery.
- Employee management and cashier attribution (SCRUM-48 branch pending PR).
- Waste management (not implemented; planned test target).
- Dashboard and reports.
- Database transaction handling, input validation and security controls.
- CI workflow and full pytest suite.

## 3. Features to be tested

| Requirement IDs | Feature | Primary verification |
|---|---|---|
| PMS-FR-001–006 | Product/batch inventory and low-stock | Unit, integration and UI tests |
| PMS-FR-007–011 | Expiry, FEFO and stock history | Unit and integration tests |
| PMS-FR-012–019 | Cart, checkout, invoices and email | Unit, integration and end-to-end tests |
| PMS-FR-020–024 | Employee profiles/status/attribution | Service and UI tests after SCRUM-48 merge |
| PMS-FR-025–030 | Waste records and stock write-off | Planned tests; cannot pass until implemented |
| PMS-FR-031–033 | Dashboard/report summaries | Service and UI tests |
| PMS-NFR-001–008 | Performance, reliability, usability, maintainability, portability and durability | Timed runs, failure injection, UAT and review |
| PMS-SEC-001–006 | Authentication, authorisation, privacy, validation and audit | Negative tests, log inspection and code review |

## 4. Features not to be tested / exclusions
- External supplier systems, ERP integrations and payment gateway processing (not in current scope).
- Barcode scanner, weighing scale and physical receipt-printer hardware unless added to the release.
- Multi-store synchronisation, cloud hosting and production-scale load.
- Real customer data and real payment information; use synthetic test data.
- Email provider internals; test only PMS integration behaviour and failure handling.
- Full authentication/RBAC behaviour cannot be accepted as implemented until those controls exist.

## 5. Test approach / strategy

### 5.1 Test levels
1. **Unit testing:** service validation, calculations, FEFO ordering, employee operations and waste calculations.
2. **Integration testing:** checkout with invoice and batch deductions; employee-to-invoice attribution; proposed waste record with batch deduction.
3. **System testing:** launch application and complete core user workflows through the UI.
4. **Regression testing:** run full pytest suite after changes to shared inventory, checkout, employee or database code.
5. **Acceptance testing:** team member acting as store user verifies agreed user stories and demo workflows.

### 5.2 Test types
- Functional and boundary-value testing.
- Database integrity and transaction rollback testing.
- Regression testing.
- UI usability and cross-platform smoke testing.
- Performance checks against SRS NFR thresholds.
- Security/privacy validation.
- Compatibility checks on supported Windows and macOS environments.

### 5.3 Entry criteria
- Feature branch is available and dependencies install.
- Database test fixtures or isolated temporary SQLite database are available.
- Requirements and acceptance criteria are identified.
- Test data uses synthetic products, employees and customer contact values.
- CI workflow is available for automated tests.

### 5.4 Exit criteria
- All release-critical planned tests executed.
- 100% of P0 test cases pass; no open critical/high severity defects.
- All implemented requirements in the RTM have test evidence.
- Full pytest suite and CI pass on the release candidate.
- Failed/not-implemented requirements are documented as deviations; no planned feature is falsely marked accepted.
- Peer review completed and demo workflow verified.

### 5.5 Security validation
- Confirm sensitive fields are not logged.
- Confirm email credentials are not stored in source code.
- Test service-layer validation with invalid quantities, identifiers, dates and monetary inputs.
- Attempt privileged actions using each role once authentication/RBAC exists.
- Verify cashier cannot select an inactive employee.
- Verify invoice/customer data visibility follows approved role permissions.
- Verify stock, invoice and waste transactions roll back completely on failure.
- Inspect audit records for actor and timestamp after employee, stock and waste changes.

## 6. Test environment

| Item | Environment |
|---|---|
| OS | Windows and macOS development machines |
| Runtime | Python 3.10+; CI currently configured for Python 3.12 |
| GUI | PySide6 |
| Database | Temporary SQLite database for tests; local SQLite for manual demo |
| ORM | SQLAlchemy |
| Test tools | pytest, pytest-qt where applicable |
| CI | GitHub Actions |
| Test data | Synthetic products, batches, employees, invoices and customer contact details |
| Reporting | pytest output, CI run, defect log and test summary |

## 7. Test schedule and milestones
Dates are planning targets and should be updated to the actual team calendar.

| Milestone | Target |
|---|---|
| SRS/SAD/Test Plan/RTM review | 5 Nov 2026 |
| Employee branch peer review and integration | Before release freeze |
| Waste scope decision and implementation/deviation approval | Before final evaluation |
| Regression and system testing | After feature freeze |
| Final UAT and demo rehearsal | Before 9 Nov 2026 presentation |
| Final test summary and document sign-off | Before submission |

## 8. Test deliverables
- SRS, SAD, Test Plan and RTM.
- Automated unit/integration test suite.
- Test execution logs and CI run evidence.
- Defect list with severity, owner and resolution.
- Manual system/UAT checklist.
- Code coverage and branch coverage reports if configured.
- Documented deviations and final test summary.

## 9. Roles and responsibilities

| Member | Role / responsibility |
|---|---|
| Deeksha | UI and billing/dashboard workflow tests for assigned features |
| Chris | Inventory, invoice and stock-deduction service tests |
| Janhavi | Regression test design and execution |
| Chiranth (Member 4) | Integration, documentation, RTM, test coordination and release checklist |

All contributors are responsible for tests covering their own code and for peer review of at least one other contribution.

## 10. Risks and mitigation

| Risk | Mitigation |
|---|---|
| Waste feature is a placeholder | Keep its test cases marked blocked/not implemented; do not report them as passed. |
| Employee branch not merged | Test on feature branch, obtain peer review, then rerun tests on merged release branch. |
| Local DB differs from test DB | Use isolated SQLite fixtures and document schema initialisation. |
| Email/network unavailable | Test invoice persistence separately; simulate email failure and ensure invoice remains committed. |
| Expiry date boundary errors | Test yesterday, today, horizon boundary and day after horizon. |
| Stock race or partial update | Use transaction/conditional update tests and failure injection. |
| Cross-platform UI differences | Run smoke test on Windows and macOS before final demo. |

## 11. Assumptions and dependencies
- Product and batch fixtures can be generated without production data.
- The workstation date/time is valid.
- Test environment uses same dependency versions as documented project setup.
- Email tests can use a mock/stub rather than a real recipient.
- Waste acceptance tests depend on completion of PMS-FR-025–030.

## 12. Suspension and resumption criteria
Suspend a test run if the application cannot initialise its database, the test environment is unavailable, or a blocking defect invalidates more than 30% of planned tests. Resume after the environment is restored and blocking defects are fixed or isolated.

## 13. Test case management and traceability

The authoritative mapping is in `RTM.md`. Each test case uses IDs `TC-###`; each SRS requirement maps to at least one verification reference. Test status must be recorded as Not Run, Pass, Fail or Blocked. A test for an unimplemented feature is Blocked, not Pass.

## 14. Test cases

| Test ID | Requirement(s) | Scenario / steps | Expected result | Type / status |
|---|---|---|---|---|
| TC-001 | FR-001, FR-002 | Create valid product; retrieve and update it. | Product persists and updated fields are returned. | Unit/integration — execute |
| TC-002 | FR-001 | Create two products with same SKU and submit blank required fields. | Service rejects duplicate/invalid product; no invalid row persists. | Negative — execute |
| TC-003 | FR-004, FR-005 | Add a valid batch and query available stock. | Batch stores received/remaining quantity; stock total equals sum of remaining batches. | Integration — execute |
| TC-004 | FR-007, FR-008 | Create expired, today, within-7-day and beyond-7-day batches. | Expired list and expiring list contain only correct boundary records. | Unit — execute |
| TC-005 | FR-009 | Add two valid batches with different expiry dates; sell quantity spanning both. | Earlier-expiring batch is consumed first; no expired batch is used. | Integration — execute |
| TC-006 | FR-010, NFR-003, NFR-008 | Attempt checkout above valid available stock. | Checkout fails; no invoice is persisted and all batch quantities remain unchanged. | Negative/integration — execute |
| TC-007 | FR-012, FR-013 | Add, change and remove cart lines; calculate totals. | Positive quantities accepted; line/subtotal/tax/discount/total follow approved rules. | Unit/UI — execute |
| TC-008 | FR-014, FR-015 | Complete valid checkout and inspect invoice and batches. | Unique invoice and item snapshots persist; exact stock deduction commits once. | Integration — execute |
| TC-009 | FR-015, NFR-003, NFR-008 | Force an exception after invoice creation but before stock update/commit. | Transaction rolls back invoice and stock changes. | Failure injection — execute |
| TC-010 | FR-016, FR-020–023 | Create employee, select as cashier, checkout; then deactivate employee and retry. | Active employee is attributed; inactive employee cannot be selected/used. | Integration/UI — blocked until SCRUM-48 merge |
| TC-011 | FR-018, FR-019 | Export invoice; simulate email provider failure. | Export contains correct invoice; email failure does not undo sale. | Integration — execute |
| TC-012 | FR-025–030 | Record valid waste against a batch; attempt zero, negative and excessive quantity. | Valid event persists and reduces stock; invalid/excess entries are rejected atomically. | Planned — blocked (waste not implemented) |
| TC-013 | FR-031–033 | Compare dashboard values with seeded database records, refresh after checkout. | Displayed product, low-stock, expiry, sales and invoice metrics match query results. | Integration/UI — execute |
| TC-014 | NFR-001 | Load agreed dataset; run product search and dashboard refresh 20 times. | At least 95% of runs complete within 3 seconds. | Performance — not measured |
| TC-015 | NFR-002 | Run 20-line checkout 20 times using repeatable fixture data. | At least 95% of DB processing runs complete within 3 seconds. | Performance — not measured |
| TC-016 | NFR-004 | Observe five first-time users completing basic checkout after 5-minute orientation. | At least four complete without assistance. | UAT — not run |
| TC-017 | SEC-003, SEC-004 | Seed fake customer contact values and fake credentials; inspect logs and repository diff. | Sensitive values absent from logs and secrets absent from tracked files. | Security — execute |
| TC-018 | SEC-001, SEC-002 | Attempt inventory/employee/waste actions using each role. | Each action is permitted/denied according to approved role matrix. | Security — blocked until RBAC exists |
| TC-019 | SEC-005 | Submit malformed IDs, blank strings, invalid dates and invalid numeric values directly to services. | Service rejects invalid data without corrupting database. | Security/unit — execute |
| TC-020 | SEC-006, FR-011 | Perform stock adjustment, employee status change and waste event; inspect history. | Actor and timestamp are retained for each auditable action. | Audit — partial / waste blocked |

## 15. Test metrics and reporting
Collect:
- Number of planned, executed, passed, failed and blocked tests.
- Pass rate = passed / executed × 100.
- Requirement coverage = requirements with at least one executed test / total requirements × 100.
- Defect count by severity and age.
- CI result and duration.
- Performance percentile for NFR-001/002.
- Waste feature readiness (blocked until implemented).

Do not count Blocked or Not Run cases as passing.

## 16. Approvals

| Role | Name | Status |
|---|---|---|
| Documentation owner | Chiranth | Draft prepared |
| Developer peer reviewer | Team member to be assigned | Pending |
| QA reviewer | Janhavi / team decision | Pending |
| Team approval | All members | Pending |
