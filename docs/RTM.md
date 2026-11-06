# Requirements Traceability Matrix (RTM)
## Perishables Management System — Expanded Scope

| Field | Value |
|---|---|
| Version | 1.0 |
| Date | 5 November 2026 |
| Owner | Member 4 — Chiranth |
| Related documents | SRS.md, SAD.md, TEST_PLAN.md |
| Status | Draft; update after peer review and final release tests |

## 1. Purpose
This RTM maps each SRS requirement to its implementation area and one or more test cases. It is used to identify missing tests, unimplemented requirements and scope deviations.

**Status meanings**
- **Implemented:** evidence found in inspected code or reported test run; still requires final release-branch verification.
- **Pending PR:** implementation exists on a feature branch but has not been confirmed merged.
- **Partial:** some related functionality exists, but requirement is not fully met.
- **Not implemented:** no working implementation was found; tests remain blocked.
- **Not measured:** measurable NFR is defined but performance/usability evidence has not been collected.

## 2. Functional requirements traceability

| SRS ID | Requirement summary | Design component | Test case(s) | Current status | Evidence / gap |
|---|---|---|---|---|---|
| PMS-FR-001 | Create product with unique SKU and validated fields | Inventory Service, Product | TC-001, TC-002 | Implemented | Inventory service validates required fields and duplicate SKU. |
| PMS-FR-002 | View/update product | Inventory UI/Service | TC-001 | Implemented | Verify final UI workflow. |
| PMS-FR-003 | Deactivate product preserving history | Inventory Service, Product | TC-001 | Implemented | Service deactivates rather than deletes. |
| PMS-FR-004 | Receive stock as batch with expiry | Inventory Service, Batch | TC-003 | Implemented | Batch receiving validation exists. |
| PMS-FR-005 | Calculate available stock | Inventory Service | TC-003 | Implemented | Based on remaining batch quantities. |
| PMS-FR-006 | Identify low-stock products | Dashboard Service | TC-013 | Partial | Summary count exists; verify threshold/UI. |
| PMS-FR-007 | Identify expired batches | Expiry Service | TC-004 | Implemented | Query filters expiry before current date and positive remaining stock. |
| PMS-FR-008 | Identify batches expiring within horizon | Expiry Service | TC-004 | Implemented | Default dashboard horizon 7 days. |
| PMS-FR-009 | FEFO allocation | Checkout Service | TC-005 | Implemented | Batches ordered by expiry date then ID. |
| PMS-FR-010 | Reject checkout above valid stock | Checkout Service | TC-006 | Implemented | Insufficient stock raises error and transaction rolls back. |
| PMS-FR-011 | Preserve stock movement/history | Inventory/stock history | TC-020 | Partial | Full audit trail not confirmed. |
| PMS-FR-012 | Manage billing cart | Cart UI/Cart Service | TC-007 | Implemented | Verify complete UI path. |
| PMS-FR-013 | Calculate billing totals | Cart/Billing Service | TC-007 | Implemented | Tax/discount rules require team confirmation. |
| PMS-FR-014 | Unique invoice and item snapshots | Invoice Service/Models | TC-008 | Implemented | Unique invoice number and item snapshot fields. |
| PMS-FR-015 | Atomic invoice and stock deduction | Checkout Service | TC-008, TC-009 | Implemented | Commit/rollback transaction in checkout service. |
| PMS-FR-016 | Cashier identity on invoice | Invoice/Employee | TC-010 | Pending PR | Employee FK attribution on SCRUM-48 branch; cashier text snapshot exists on main. |
| PMS-FR-017 | Optional customer mobile/email | Checkout/Invoice | TC-011, TC-017 | Partial | Fields exist; contact policy needs approval. |
| PMS-FR-018 | Export/print invoice | Invoice Export/UI | TC-011 | Implemented | Verify file output during manual system test. |
| PMS-FR-019 | Email invoice; failure does not undo sale | Email Service/Cart UI | TC-011 | Partial | Feature exists in project work; verify mail configuration and failure path. |
| PMS-FR-020 | Create employee profile | Employee Service/UI | TC-010 | Pending PR | SCRUM-48 branch; verify after peer-reviewed merge. |
| PMS-FR-021 | Edit employee profile | Employee Service/UI | TC-010 | Pending PR | SCRUM-48 branch. |
| PMS-FR-022 | Activate/deactivate employee | Employee Service/UI | TC-010 | Pending PR | Duplicate activation definition fixed; branch tests pass (100 reported). |
| PMS-FR-023 | Only active employee can be cashier | Checkout/Employee Service | TC-010 | Pending PR | Branch implementation; manual verification still required. |
| PMS-FR-024 | Explicit on-leave status | Employee model/UI | TC-010 | Not implemented | Current employee model uses active/inactive; separate leave state not confirmed. |
| PMS-FR-025 | Record waste event linked to product/batch | Waste UI/Service/Model | TC-012 | Not implemented | Waste Management navigation is placeholder. |
| PMS-FR-026 | Capture waste quantity, date, reason, actor, notes | Waste Service/Model | TC-012 | Not implemented | Proposed WasteRecord data contract. |
| PMS-FR-027 | Validate waste quantity | Waste Service | TC-012 | Not implemented | Requires positive and not-over-remaining validation. |
| PMS-FR-028 | Atomically persist waste and reduce batch stock | Waste Service/DB | TC-012 | Not implemented | Requires transaction and rollback tests. |
| PMS-FR-029 | Waste reports by period/product/reason/value | Dashboard/Reports | TC-012, TC-013 | Not implemented | Dashboard currently returns `waste_status: Not implemented`. |
| PMS-FR-030 | Prevent sale of written-off stock | Checkout/Batch | TC-005, TC-012 | Partial | FEFO excludes expired/depleted batches; waste write-off flow absent. |
| PMS-FR-031 | Display inventory/expiry/sales summary | Dashboard Service/UI | TC-013 | Implemented | Current dashboard summary includes product, low stock, expiry, sales and invoice count. |
| PMS-FR-032 | Display waste summary | Dashboard/Reports | TC-013 | Not implemented | UI displays N/A; service says not implemented. |
| PMS-FR-033 | Refresh summary from persisted data | Dashboard Service/UI | TC-013 | Implemented | Refresh action queries database. |

## 3. Non-functional requirements traceability

| SRS ID | NFR | Test case(s) | Status |
|---|---|---|---|
| PMS-NFR-001 | 95% dashboard/search runs within 3s on defined dataset | TC-014 | Not measured |
| PMS-NFR-002 | 95% 20-line checkout DB processing within 3s | TC-015 | Not measured |
| PMS-NFR-003 | 100 checkout attempts preserve invoice/stock consistency | TC-006, TC-008, TC-009 | Partial; targeted tests required |
| PMS-NFR-004 | 4/5 first-time users complete checkout unaided | TC-016 | Not measured |
| PMS-NFR-005 | Service-layer rules, tests and CI pass | TC-001–TC-013 | Partial; full suite last reported 100 passed on SCRUM-48 branch |
| PMS-NFR-006 | Install/launch on supported Windows/macOS | Manual smoke test | Not measured |
| PMS-NFR-007 | Data survives restart | System persistence test | Not measured |
| PMS-NFR-008 | Failed checkout/waste transaction fully rolls back | TC-006, TC-009, TC-012 | Checkout implemented; waste blocked |

## 4. Security requirements traceability

| SRS ID | Security requirement | Test case(s) | Status |
|---|---|---|---|
| PMS-SEC-001 | Authenticate before privileged operations | TC-018 | Not confirmed implemented |
| PMS-SEC-002 | Enforce role-based permissions | TC-018 | Not confirmed implemented |
| PMS-SEC-003 | Do not log customer contact/secrets | TC-017 | Requires log inspection |
| PMS-SEC-004 | Keep credentials out of source control | TC-017 | Requires repository/config review |
| PMS-SEC-005 | Validate untrusted input in service layer | TC-002, TC-006, TC-019 | Partial; expand negative tests |
| PMS-SEC-006 | Audit invoices, employee changes, stock adjustments and waste | TC-020 | Partial; full audit trail not confirmed |

## 5. Coverage summary

| Category | Requirement count | Mapped to test? | Key outstanding work |
|---|---:|---|---|
| Functional | 33 | Yes | Waste feature and employee merge/manual verification |
| Non-functional | 8 | Yes | Performance, usability, portability and durability evidence |
| Security | 6 | Yes | Authentication/RBAC decision and audit/log verification |
| Security objectives | 3 | Addressed by SEC requirements | Verify implementation and risk acceptance |

## 6. Known deviations and release blockers

| Deviation | Expected by expanded scope | Observed state | Action |
|---|---|---|---|
| Waste management | Waste records, batch write-off, reason capture and reports | Placeholder UI; dashboard says not implemented | Implement PMS-FR-025–030 or obtain explicit scope deferral approval. |
| Employee profiles | Create/edit/activate/deactivate and invoice attribution | SCRUM-48 feature branch; not yet confirmed merged | Peer review PR, merge, run full tests and manual checkout verification. |
| Employee on-leave status | Distinct on-leave state | Active/inactive status only confirmed | Implement if required; otherwise document as P2 deferred. |
| RBAC/authentication | Admin, inventory manager and cashier permissions | Not confirmed in inspected code | Decide whether required for current demo; implement or record approved deviation. |
| Audit trail | Actor/time history for stock and waste changes | Full coverage not confirmed | Verify existing records; implement missing audit events. |
| Performance and usability targets | Measured NFR acceptance | No measurements supplied | Run defined test protocols and attach results. |

## 7. RTM maintenance rules
1. Add a requirement ID before implementing a new feature.
2. Link each Jira issue and PR to the relevant requirement ID.
3. Add/adjust test cases whenever a requirement changes.
4. Update implementation status only after code review and test evidence.
5. Do not mark blocked or unimplemented requirements as passed.
6. Review the RTM after each sprint and before final evaluation.
