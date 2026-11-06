# Software Test Plan
## Perishables Management System

| Field | Value |
|---|---|
| Version | 1.2 |
| Date | 6 November 2026 |
| Authors | PMS Team — Deeksha, Chris, Janhavi, Chiranth |
| Test plan owner | Member 3 — QA and CI |
| Status | Updated draft — pending team sign-off |
| Application | Python 3 / PySide6 / SQLAlchemy / SQLite |

## Revision history

| Version | Date | Summary |
|---|---|---|
| 1.0 | 5 Nov 2026 | Initial expanded-scope test plan |
| 1.1 | 6 Nov 2026 | Updated release test evidence, employee feature status and outstanding test gaps |
| 1.2 | 6 Nov 2026 | Aligned scope and invoice behaviour; added performance, checkout and usability results; updated regression and coverage metrics |

## 1. Introduction

### 1.1 Purpose

This document defines the testing approach for the Perishables Management System (PMS). It identifies the features to be tested, test methods, test environment, test cases, responsibilities, execution evidence and release criteria.

### 1.2 Scope

Testing covers the current implemented desktop application:

- Product creation, viewing, updating and deactivation.
- Batch receiving and stock calculations.
- Low-stock and expiry information.
- Expiry tracking and FEFO stock allocation.
- POS cart and checkout.
- Invoice generation, item snapshots and stock deduction.
- Employee management and cashier-related workflows.
- Dashboard summaries.
- Application launch, persistence and regression behaviour.

Waste management is excluded from the final project scope and is not part of this release's acceptance criteria. Authentication and role-based access control are reported by the team as implemented; security validation and permission testing remain deferred and are not claimed as passed.

### 1.3 References

- `SRS.md`
- `SAD.md`
- `RTM.md`
- `README.md`
- `PROJECT_SCOPE_AND_TEAM_PLAN.md`
- Repository source code and automated tests
- Project evaluation checklist

### 1.4 Definitions

- FEFO: First Expired, First Out.
- POS: Point of Sale.
- CI: Continuous Integration.
- UAT: User Acceptance Testing.
- RTM: Requirements Traceability Matrix.
- Regression testing: Re-running tests to detect unintended changes.

## 2. Test items

The following application components are included:

1. Product and inventory services.
2. Batch and stock management.
3. Expiry tracking and FEFO allocation.
4. POS cart and checkout.
5. Invoice generation and provision.
6. Employee management.
7. Dashboard summaries.
8. SQLite persistence and database transactions.
9. PySide6 user interface.
10. Automated test suite and GitHub Actions workflow.

## 3. Features to be tested

| Requirement group | Features | Test references |
|---|---|---|
| Product management | Product validation, unique SKU, update and deactivation | TC-001, TC-002 |
| Batch and inventory | Batch receiving, quantity validation and available stock | TC-003 |
| Expiry tracking | Expired and near-expiry batch identification | TC-004 |
| FEFO and stock validation | Correct batch allocation and insufficient-stock rejection | TC-005, TC-006 |
| POS and billing | Cart operations and total calculation | TC-007 |
| Invoice and transaction | Invoice snapshots, stock deduction and rollback | TC-008, TC-009 |
| Employee management | Employee lifecycle and cashier-related workflows | TC-010 |
| Invoice output | Invoice generation/provision and optional customer contact fields; printing is not a required feature | TC-011 |
| Waste management | Excluded from final project scope | TC-012 — out of scope |
| Dashboard | Inventory, expiry and sales summaries | TC-013 |
| Performance | Dashboard summary, product listing and checkout response targets | TC-014, TC-015 |
| Usability | First-time checkout usability | TC-016 |
| Data protection | Customer contact handling and configuration review | TC-017 |
| Security | Authentication and role permissions | TC-018 — implementation not confirmed |
| Validation | Invalid input and boundary cases | TC-019 |
| Auditability | Stock and employee change history | TC-020 — partial/unverified |

## 4. Features not to be tested in this release

The following are outside the verified operational release:

- Waste recording, write-off and waste reporting (excluded from final project scope).
- Security validation, including authentication/RBAC permission testing, is deferred; implementation is reported by the team but is not security-verified.
- Multi-store or cloud deployment.
- Multi-workstation concurrency.
- External email-provider delivery under live credentials.
- Production-scale performance and load behaviour.
- Formal accessibility certification.

These items must not be reported as passed merely because they are described in the SRS or SAD.

## 5. Test approach and strategy

### 5.1 Test levels

- **Unit testing:** Validate individual service functions and business rules.
- **Integration testing:** Verify interactions between services, SQLAlchemy models and SQLite.
- **System testing:** Run complete application workflows through the UI.
- **Regression testing:** Re-run the automated suite after changes.
- **Acceptance testing:** Verify the agreed core workflows and release criteria.

### 5.2 Test types

- Functional testing.
- Boundary and invalid-input testing.
- Database transaction and rollback testing.
- UI smoke testing.
- Regression testing.
- Clean-checkout installation and launch verification.
- Security-oriented configuration and data-handling review (deferred for this evaluation cycle).
- Performance and usability testing.

### 5.3 Entry criteria

- A testable application build is available.
- Required dependencies can be installed.
- Test database and test data are available.
- Relevant requirements and test cases are documented.
- The test environment is accessible.

### 5.4 Exit criteria

- Planned executable tests have been run or explicitly marked blocked/not measured.
- No known critical defect prevents the core demonstration workflows.
- Automated tests pass.
- CI checks pass for the release merge.
- Manual smoke and functional workflows are recorded.
- Known deviations and unimplemented requirements are documented.
- Release documentation is reviewed.

### 5.5 Security validation

Security validation covers:

1. Check that customer contact details and secrets are not written to ordinary logs.
2. Review repository and configuration files for committed credentials.
3. Verify service-layer validation for untrusted inputs.
4. Review whether employee and customer data is unnecessarily exposed.
5. Confirm whether authentication and role-based permissions are implemented.
6. Verify that privileged operations cannot be performed without the required role, if RBAC is implemented.
7. Review audit records for invoice and stock changes.

**Current limitation:** Full authentication/RBAC and complete audit-trail coverage have not been confirmed. These checks must be recorded as not confirmed or pending, not passed.

## 6. Test environment

| Item | Environment |
|---|---|
| Language | Python 3 |
| UI framework | PySide6 |
| ORM | SQLAlchemy |
| Database | SQLite |
| Test framework | pytest and pytest-qt where applicable |
| CI | GitHub Actions |
| Version control | Git and GitHub |
| Operating environment | Local development; Windows and macOS usage reported |
| Test data | Local test database and synthetic records |

The application launch command is:

`python -m src.main`

The automated test command is:

`python -m pytest -q`

## 7. Test schedule

| Activity | Planned / recorded date | Status |
|---|---|---|
| Test planning and case design | Sprint 1–2 | Completed |
| Automated regression | 6 Nov 2026 | 111 tests passed |
| Clean-checkout verification | 6 Nov 2026 | Completed |
| Manual smoke testing | 6 Nov 2026 | Six areas passed |
| Functional workflow verification | 6 Nov 2026 | Six workflows passed |
| Final documentation review | 6 Nov 2026 onward | In progress |
| Final evaluation demonstration | 9 Nov 2026 | Scheduled |

## 8. Test cases

| Test ID | Test scenario | Expected result | Current result/status |
|---|---|---|---|
| TC-001 | Create, view, update and deactivate a product | Valid product changes persist; deactivation preserves history | Automated suite passed; mapped test |
| TC-002 | Submit blank, duplicate or invalid product fields | Invalid values are rejected with clear errors | Automated suite passed; mapped test |
| TC-003 | Receive a batch and calculate available stock | Valid batch is stored and stock is calculated from remaining quantities | Automated suite passed; mapped test |
| TC-004 | Identify expired and near-expiry batches | Correct batches are returned according to expiry date and horizon | Automated suite passed; mapped test |
| TC-005 | Checkout with multiple eligible batches | Stock is allocated in FEFO order | Automated suite passed; mapped test |
| TC-006 | Checkout with insufficient valid stock | Checkout is rejected and stock remains unchanged | Automated suite passed; mapped test |
| TC-007 | Add, update and remove cart items; calculate total | Cart quantities and totals are correct | Automated suite passed; mapped test |
| TC-008 | Complete checkout and generate invoice | Invoice and item snapshots are persisted with stock deduction | Automated suite passed; mapped test |
| TC-009 | Force checkout failure during persistence | Transaction rolls back without partial invoice/stock changes | Automated suite passed; mapped test |
| TC-010 | Create, edit, activate/deactivate employee and use cashier workflow | Employee state and cashier-related behaviour are correct | Release manual workflow reported passed; see evidence |
| TC-011 | Generate/provide invoice and handle optional customer fields | Invoice is generated and provided; optional fields are handled. Printing is not a required feature. | Mapped to automated/manual verification; email delivery requires separate configuration verification |
| TC-012 | Waste management | Not applicable to the final project scope | Out of scope — excluded from final release |
| TC-013 | Open and refresh dashboard | Summary reflects persisted inventory, expiry and sales data | Manual smoke passed; waste summary not implemented |
| TC-014 | Measure dashboard summary and product-listing response time | 95% of defined runs complete within 3 seconds | Pass — 30 runs; 1,000 products and 2,000 batches. Dashboard P95 140.11 ms (maximum 189.75 ms); product listing P95 20.61 ms (maximum 22.98 ms). Synthetic in-memory SQLite benchmark. |
| TC-015 | Measure complete checkout processing time for 20 distinct products | 95% of defined runs complete within 3 seconds | Pass — 30 successful checkouts; 1,000 products and 2,000 batches. Average 26.90 ms, median 26.88 ms, P95 28.93 ms, maximum 31.44 ms. Synthetic in-memory SQLite benchmark. |
| TC-016 | Observe first-time users completing checkout | At least 4 of 5 users complete without assistance | Pass — 5 of 5 completed without assistance (100%); acceptance threshold met. |
| TC-017 | Inspect logs and repository configuration for sensitive data | No secrets or full customer contact details appear in ordinary logs or committed configuration | Review required; not claimed passed |
| TC-018 | Verify authentication and role permissions | Unauthenticated or unauthorised operations are denied | Implementation reported by team; security/permission validation deferred and not tested for this evaluation. |
| TC-019 | Submit invalid quantities, prices, dates and identifiers | Invalid input is rejected safely | Automated suite passed; mapped test |
| TC-020 | Review audit history for stock and employee changes | Actor/time history is available for required operations | Partial/unverified; further review required |

### 8.1 Execution summary

Reported release evidence as of 6 November 2026:

- Automated regression suite: 131 tests passed.
- Coverage report: 37% statement coverage with branch measurement enabled; HTML report generated.
- Fresh clone: dependencies installed and application launched.
- Clean-checkout automated suite: 111 tests passed at the time of the clean-checkout verification; the later local regression suite passed 131 tests.
- Manual smoke testing: six listed areas passed.
- Functional workflow testing: six listed workflows passed.
- PR #21 merged into `main`; all reported PR checks passed.
- Demo video playback verified.
- TC-014 dashboard and product-listing performance benchmark passed: 30 runs against 1,000 products and 2,000 batches; P95 values 140.11 ms and 20.61 ms respectively.
- TC-015 complete 20-item checkout benchmark passed: 30 successful checkouts; P95 28.93 ms.
- TC-016 usability observation passed: all five first-time users completed checkout without assistance.

The 131-test result is a suite-level result. It does not mean every deferred, out-of-scope or unverified test in this plan passed. The performance results are synthetic in-memory SQLite measurements, not production-scale or concurrent-user load tests.

## 9. Test deliverables

- Software Test Plan.
- Automated test source files.
- Test execution results.
- Manual test evidence.
- Screenshots under `docs/evidence/screenshots/`.
- Demo video under `docs/evidence/demo.mov`.
- Release checklist.
- Requirements Traceability Matrix.
- CI workflow results.

## 10. Roles and responsibilities

| Role | Team member | Responsibility |
|---|---|---|
| Backend and data | Deeksha | Data models, database and service implementation |
| UI and workflows | Chris | PySide6 screens and application workflows |
| QA and CI/CD | Janhavi | Test automation, regression and CI validation |
| Integration and documentation | Chiranth | Integration coordination, Jira, documentation and release evidence |

All team members are responsible for testing and documenting their own changes and participating in peer review.

## 11. Risks and mitigation

| Risk | Mitigation |
|---|---|
| Unstable application build | Run regression suite and CI before merge |
| Missing or invalid test data | Use repeatable synthetic data and isolated test databases |
| Database state affects test results | Use temporary test databases and fixtures |
| Waste management excluded from scope | Keep waste-related tests out of release acceptance criteria |
| Email service unavailable | Test invoice persistence independently of delivery |
| Platform differences | Verify installation and launch on supported environments |
| Security controls not confirmed | Document limitations and avoid claiming security acceptance |
| Synthetic performance data may not represent production use | Disclose in-memory SQLite test conditions and avoid production-scale claims |

## 12. Assumptions and dependencies

- Python and required packages are available.
- SQLite can create and access the local database.
- The test environment has the necessary UI dependencies.
- Test records use synthetic data.
- GitHub Actions is available for repository CI.
- External email delivery depends on valid provider configuration.
- Waste and RBAC tests depend on those features being implemented.

## 13. Suspension and resumption criteria

Suspend testing if:

- The application cannot launch.
- The database is unavailable or corrupted.
- A blocking defect prevents execution of core workflows.
- The test environment is unstable.
- Test results cannot be reproduced.

Resume when:

- Blocking defects are resolved.
- The environment is stable.
- Test data and dependencies are restored.
- The relevant build is available.

## 14. Test metrics and reporting

Metrics to report:

- Number of automated tests passed, failed and skipped.
- Manual smoke-test completion.
- Functional workflow completion.
- Open critical and high-priority defects.
- Requirement-to-test coverage.
- Performance results when measured.
- CI pass/fail status.

Current reported metrics:

| Metric | Result |
|---|---|
| Automated tests | 131 passed |
| Clean-checkout tests | 111 passed at clean-checkout verification; later local suite: 131 passed |
| Manual smoke areas | 6 passed |
| Functional workflows | 6 passed |
| PR #21 checks | Passed |
| TC-014 performance | Pass — dashboard P95 140.11 ms; product listing P95 20.61 ms |
| TC-015 checkout performance | Pass — 20-item checkout P95 28.93 ms |
| TC-016 usability | Pass — 5/5 first-time users completed without assistance |
| Waste-management tests | Out of scope — removed from final project scope |
| Authentication/RBAC tests | Implementation reported; security validation deferred and not tested |

## 15. Approvals

| Role | Name | Approval / date |
|---|---|---|
| QA / CI lead | Janhavi | Pending |
| Development representative | Deeksha / Chris | Pending |
| Integration and documentation owner | Chiranth | Pending |
| Project/evaluation authority | To be confirmed | Pending |

Approval must be recorded by the relevant team members. This draft does not imply formal sign-off.