# Requirements Traceability Matrix (RTM)
## Perishables Management System

| Field | Value |
|---|---|
| Version | 1.1 |
| Date | 6 November 2026 |
| Owner | Member 4 — Chiranth |
| Related documents | SRS.md, SAD.md, TEST_PLAN.md |
| Status | Draft for final review |

## 1. Purpose

This RTM maps each SRS requirement to its design component, test case and current implementation status. It identifies completed requirements, partial functionality, unimplemented features and requirements that have not yet been measured.

### Status definitions

- **Implemented / tested:** Implementation exists and relevant test evidence is reported.
- **Implemented / verification incomplete:** Functionality exists but complete verification is not established.
- **Partial:** Some aspects exist but the full requirement is not satisfied.
- **Not implemented:** No working implementation is confirmed.
- **Not measured:** A measurable target exists but no result is available.
- **Not confirmed:** Available evidence does not establish implementation.

## 2. Functional requirements traceability

| SRS ID | Requirement summary | Design component | Test case(s) | Current status | Evidence / gap |
|---|---|---|---|---|---|
| PMS-FR-001 | Create product with unique SKU and validated fields | Inventory Service, Product | TC-001, TC-002 | Implemented / tested | Automated regression suite passed. |
| PMS-FR-002 | View and update product | Inventory UI/Service | TC-001 | Implemented / tested | Inventory workflows included in release smoke testing. |
| PMS-FR-003 | Deactivate product while preserving history | Inventory Service, Product | TC-001 | Implemented / tested | Deactivation behaviour is covered by service functionality. |
| PMS-FR-004 | Receive stock as a batch with expiry | Inventory Service, Batch | TC-003 | Implemented / tested | Batch receiving validation exists. |
| PMS-FR-005 | Calculate available stock | Inventory Service | TC-003 | Implemented / tested | Based on remaining batch quantities. |
| PMS-FR-006 | Identify low-stock products | Dashboard Service | TC-013 | Partial | Dashboard summary exists; threshold behaviour should be verified against acceptance criteria. |
| PMS-FR-007 | Identify expired batches | Expiry Service | TC-004 | Implemented / tested | Expiry query filters expired batches with positive remaining stock. |
| PMS-FR-008 | Identify batches expiring within a horizon | Expiry Service | TC-004 | Implemented / tested | Dashboard uses a seven-day horizon. |
| PMS-FR-009 | FEFO stock allocation | Checkout Service | TC-005 | Implemented / tested | Eligible batches ordered by expiry date and batch ID. |
| PMS-FR-010 | Reject checkout above valid stock | Checkout Service | TC-006 | Implemented / tested | Insufficient stock raises an error; transaction rollback is tested. |
| PMS-FR-011 | Preserve stock movement/history | Inventory/stock history | TC-020 | Partial | Complete audit trail is not confirmed. |
| PMS-FR-012 | Manage billing cart | Cart UI/Service | TC-007 | Implemented / tested | Cart operations included in the reported functional workflows. |
| PMS-FR-013 | Calculate billing totals | Cart/Billing Service | TC-007 | Implemented / tested | Tax and discount policy should be stated separately if applicable. |
| PMS-FR-014 | Generate unique invoice and item snapshots | Invoice Service/Models | TC-008 | Implemented / tested | Invoice number and item snapshot fields are implemented. |
| PMS-FR-015 | Atomically create invoice and deduct stock | Checkout Service | TC-008, TC-009 | Implemented / tested | Checkout transaction commits or rolls back. |
| PMS-FR-016 | Record cashier identity on invoice | Invoice/Employee | TC-010 | Implemented / verification incomplete | Employee management and cashier-related changes are merged; avoid claiming unverified edge cases. |
| PMS-FR-017 | Store optional customer mobile/email | Checkout/Invoice | TC-011, TC-017 | Partial | Fields exist; contact policy and data-protection review remain. |
| PMS-FR-018 | Export or print invoice | Invoice Export/UI | TC-011 | Implemented / verification incomplete | Invoice output is included in project functionality; retain evidence of manual output verification. |
| PMS-FR-019 | Email invoice without undoing sale on delivery failure | Email Service/Cart UI | TC-011 | Partial | Email configuration and failure-path verification are not established by current release evidence. |
| PMS-FR-020 | Create employee profile | Employee Service/UI | TC-010 | Implemented / verification incomplete | Employee management changes merged in PR #17; manual workflow reported passed. |
| PMS-FR-021 | Edit employee profile | Employee Service/UI | TC-010 | Implemented / verification incomplete | Included in merged employee-management functionality. |
| PMS-FR-022 | Activate/deactivate employee | Employee Service/UI | TC-010 | Implemented / verification incomplete | Included in merged employee-management functionality. |
| PMS-FR-023 | Restrict cashier selection to active employees | Checkout/Employee Service | TC-010 | Implemented / verification incomplete | Cashier-related workflow included in merged release; retain direct test evidence. |
| PMS-FR-024 | Maintain distinct on-leave status | Employee model/UI | TC-010 | Not implemented | Current employee status is active/inactive; distinct leave state is not confirmed. |
| PMS-FR-025 | Record waste event linked to product/batch | Waste UI/Service/Model | TC-012 | Not implemented | Waste-management functionality is not operational. |
| PMS-FR-026 | Capture waste quantity, date, reason, actor and notes | Waste Service/Model | TC-012 | Not implemented | Proposed WasteRecord data contract only. |
| PMS-FR-027 | Validate waste quantity | Waste Service | TC-012 | Not implemented | Positive and not-over-remaining validation requires implementation. |
| PMS-FR-028 | Atomically persist waste and reduce batch stock | Waste Service/DB | TC-012 | Not implemented | Transaction and rollback tests cannot run before implementation. |
| PMS-FR-029 | Generate waste reports by period/product/reason/value | Dashboard/Reports | TC-012, TC-013 | Not implemented | Waste reporting is not part of the current operational release. |
| PMS-FR-030 | Prevent sale of written-off stock | Checkout/Batch | TC-005, TC-012 | Partial | FEFO excludes expired/depleted batches; waste write-off workflow is absent. |
| PMS-FR-031 | Display inventory, expiry and sales summary | Dashboard Service/UI | TC-013 | Implemented / tested | Dashboard smoke test passed. |
| PMS-FR-032 | Display waste summary | Dashboard/Reports | TC-013 | Not implemented | Waste metric is explicitly unavailable/not implemented. |
| PMS-FR-033 | Refresh summary from persisted data | Dashboard Service/UI | TC-013 | Implemented / tested | Dashboard summary refreshes from database records. |

## 3. Non-functional requirements traceability

| SRS ID | Requirement | Test case(s) | Status | Evidence / gap |
|---|---|---|---|---|
| PMS-NFR-001 | 95% of dashboard/search runs complete within 3 seconds on defined dataset | TC-014 | Not measured | No benchmark results supplied. |
| PMS-NFR-002 | 95% of 20-line checkout DB processing completes within 3 seconds | TC-015 | Not measured | No benchmark results supplied. |
| PMS-NFR-003 | 100 checkout attempts preserve invoice/stock consistency | TC-006, TC-008, TC-009 | Partial | Transaction tests exist; 100-attempt stress protocol not evidenced. |
| PMS-NFR-004 | Four of five first-time users complete checkout unaided | TC-016 | Not measured | No usability study supplied. |
| PMS-NFR-005 | Service-layer rules, tests and CI pass | TC-001–TC-013 | Implemented / tested | 111 automated tests passed; PR #21 checks passed. |
| PMS-NFR-006 | Install and launch on supported Windows/macOS environments | Manual smoke test | Partial | Local use reported; a formal cross-platform test matrix is not supplied. |
| PMS-NFR-007 | Data survives application restart | System persistence test | Implemented / verification incomplete | SQLite persistence exists; retain explicit restart test evidence. |
| PMS-NFR-008 | Failed checkout/waste transaction fully rolls back | TC-006, TC-009, TC-012 | Partial | Checkout rollback implemented and tested; waste path blocked. |

## 4. Security requirements traceability

| SRS ID | Security requirement | Test case(s) | Status | Evidence / gap |
|---|---|---|---|---|
| PMS-SEC-001 | Authenticate before privileged operations | TC-018 | Not confirmed | Authentication implementation not established. |
| PMS-SEC-002 | Enforce role-based permissions | TC-018 | Not confirmed | RBAC implementation not established. |
| PMS-SEC-003 | Do not log customer contact data or secrets | TC-017 | Verification required | Requires log inspection. |
| PMS-SEC-004 | Keep credentials out of source control | TC-017 | Verification required | Requires repository/configuration review. |
| PMS-SEC-005 | Validate untrusted input in service layer | TC-002, TC-006, TC-019 | Implemented / verification incomplete | Service validation and automated tests exist; complete negative-test coverage should be checked. |
| PMS-SEC-006 | Audit invoices, employee changes, stock adjustments and waste | TC-020 | Partial | Invoice and employee information exists; complete audit trail is not confirmed; waste is unimplemented. |

## 5. Coverage summary

| Category | Requirement count | Test mapping | Outstanding work |
|---|---:|---|---|
| Functional | 33 | Mapped to TC-001–TC-013 and TC-020 | Waste requirements, on-leave status and remaining verification gaps |
| Non-functional | 8 | Mapped to TC-014–TC-016 and system tests | Performance, usability, portability and durability evidence |
| Security | 6 | Mapped to TC-017–TC-020 | Authentication/RBAC decision, log/config review and audit verification |

All listed requirements have a test reference or an identified verification activity. Mapping a requirement to a test does not mean that the test has passed.

## 6. Known deviations and release gaps

| Deviation | Expected by expanded scope | Observed state | Action |
|---|---|---|---|
| Waste management | Waste records, batch write-off, reason capture and reports | Not implemented in current release | Implement or obtain explicit scope deferral approval. |
| Employee profiles | Create/edit/activate/deactivate and invoice attribution | Included in merged release | Retain PR #17 and manual verification evidence. |
| Employee on-leave status | Distinct on-leave state | Active/inactive status only confirmed | Implement if required; otherwise document as deferred. |
| Authentication/RBAC | Admin, inventory manager and cashier permissions | Not confirmed implemented | Decide whether required; implement or record approved deviation. |
| Audit trail | Actor/time history for stock and waste changes | Complete coverage not confirmed | Verify existing records and implement missing events. |
| Performance and usability | Measured NFR acceptance | No measurements supplied | Execute the defined test protocols and attach results. |
| Email delivery | Reliable invoice email and failure handling | Configuration/failure path not fully verified | Test with controlled provider configuration. |

## 7. Release evidence

Reported evidence as of 6 November 2026:

- 111 automated tests passed locally.
- 111 automated tests passed on a fresh clone.
- Application launched successfully from the clean checkout.
- Six manual smoke-test areas passed.
- Six functional workflows passed.
- PR #21 merged into `main`; all reported PR checks passed.
- Demo video saved at `docs/evidence/demo.mov` and verified to play.
- Screenshots saved under `docs/evidence/screenshots/`.

## 8. RTM maintenance rules

1. Add a requirement ID before implementing a new feature.
2. Link each Jira issue and PR to the relevant requirement ID.
3. Add or adjust test cases whenever a requirement changes.
4. Update implementation status only after code review and test evidence.
5. Do not mark blocked, unimplemented or unmeasured requirements as passed.
6. Review the RTM after each sprint and before final evaluation.
7. Keep the SRS, SAD, Test Plan and RTM consistent with the merged release.