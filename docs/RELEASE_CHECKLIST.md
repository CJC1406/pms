# PMS Release Checklist

**Project:** Perishables Management System  
**Jira:** SCRUM-53 — Final regression, release checklist and Sprint 2 demo  
**Sprint:** Perishables Sprint 2  
**Release evaluation:** 9 November 2026  
**Evidence review date:** 6 November 2026  
**Frozen release commit:** `054dd59` — `docs: declare PMS feature freeze for final evaluation`

## 1. Regression testing

- [x] Run the complete automated test suite locally.
- [x] Confirm the latest full local suite: **131 tests passed**.
- [x] Re-run tests after release-evidence changes.
- [x] No critical defects reported during the completed manual tests.
- [x] Perform manual application smoke testing.
- [x] Verify the six reported functional workflows.
- [x] Record the measured statement coverage: **37%**, with branch coverage enabled.

**Historical result:** The earlier clean-checkout verification recorded 111 passing tests. This is retained as a historical result and is not the latest full-suite count.

## 2. Continuous integration

- [x] GitHub Actions workflow configured.
- [x] PR #21 checks passed and PR #21 merged into `main`.
- [x] GitHub Actions passed for the frozen commit `054dd59`.
- [x] Verify that no failing workflow is reported for the frozen commit.

## 3. Clean-checkout verification

- [x] Clone repository into a fresh directory.
- [x] Create and activate a virtual environment.
- [x] Install dependencies from `requirements.txt`.
- [x] Run `python -m pytest -q`.
- [x] Confirm **111 tests passed** in the recorded clean-checkout run.
- [x] Launch using `python -m src.main`.
- [x] Confirm application starts successfully with its database.
- [x] Verify main application screens.

The 111-test clean-checkout result is an earlier verification. The later local full-suite result is 131 passed.

## 4. Manual smoke testing

- [x] Dashboard opens and displays correctly.
- [x] Inventory screens load and product operations work.
- [x] Billing cart and checkout behave correctly.
- [x] Expiry tracking displays expected information.
- [x] Employee management screens work.
- [x] Light and dark themes work correctly.
- [x] No critical errors reported during normal navigation.

## 5. Functional workflow testing

- [x] Product and inventory workflow.
- [x] Batch receiving and stock workflow.
- [x] Expiry tracking and FEFO workflow.
- [x] POS cart and checkout workflow.
- [x] Invoice generation/output workflow.
- [x] Employee management and cashier-related workflow.

Refer to `docs/MANUAL_TEST_EVIDENCE.md` for the recorded manual results.

## 6. Documentation and project records

- [x] README setup instructions reviewed against a clean checkout.
- [x] SRS updated to reflect agreed requirements and current implementation status.
- [x] SAD updated to reflect merged architecture and current implementation status.
- [x] Test Plan updated against actual execution evidence.
- [ ] Final cross-check of README, SRS, SAD, Test Plan, RTM and project scope completed together.
- [ ] Jira acceptance criteria and issue status checked against final evidence.
- [x] Team approval of final deliverables confirmed: all four team members approved.

Team approval is not represented as external evaluator approval or as a separate formal peer-review record.

## 7. Sprint 2 demo and release

- [x] Record a demonstration.
- [x] Save the video in the repository at `docs/evidence/demo.mov`.
- [x] Verify the video plays correctly.
- [x] Confirm the required demo duration and content against the evaluation checklist.
- [x] Feature-freeze declaration committed and pushed in `054dd59`.
- [ ] Feature freeze becomes effective on the declared date: **7 November 2026**.
- [x] PR #21 checks passed and PR #21 merged into `main`.
- [x] GitHub Actions passed for the frozen commit `054dd59`.
- [ ] Confirm whether a separate formal peer-review record is required and, if so, record it.

## 8. Evidence recorded

| Check | Evidence | Status |
|---|---|---|
| Latest local regression | 131 tests passed | Complete |
| Historical clean checkout | Fresh clone, dependencies installed, application launched; 111 tests passed | Complete |
| Main-branch CI | GitHub Actions passed for `054dd59` | Complete |
| Manual smoke test | Six smoke-test areas passed | Complete |
| Functional workflows | Six listed workflows passed | Complete |
| Statement coverage | 37%; branch coverage enabled | Recorded |
| Screenshots | `docs/evidence/screenshots/` | Recorded |
| Demo video | `docs/evidence/demo.mov`, approximately 20 MB; playback verified | Complete |
| PR #21 | Checks passed; merged into `main` | Complete |
| Team approval | All four team members approved final deliverables | Confirmed |
| Formal peer review | Separate formal peer-review evidence not confirmed | Pending verification |
| Final documentation/Jira cross-check | Still to be completed | Pending |

## 9. Performance and usability evidence

### TC-014 — Dashboard summary and product listing

Representative synthetic in-memory SQLite data: 1,000 products and 2,000 batches; 30 runs.

| Operation | Average | P95 | Maximum | Result |
|---|---:|---:|---:|---|
| Dashboard summary | 126.19 ms | 140.11 ms | 189.75 ms | Pass |
| Product listing | 14.59 ms | 20.61 ms | 22.98 ms | Pass |

Both operations were below the 3,000 ms target.

### TC-015 — Complete 20-item checkout

- 1,000 products and 2,000 batches seeded in synthetic in-memory SQLite.
- 20 distinct products per checkout, quantity 1 each.
- 30 runs; 30 invoices created.
- Average: **26.90 ms**; median: **26.88 ms**; P95: **28.93 ms**; maximum: **31.44 ms**.
- Result: **Pass** against the 3,000 ms target.

### TC-016 — First-time checkout usability

- 5 of 5 first-time testers completed checkout without assistance.
- Success rate: **100%**.
- Acceptance threshold: 4 of 5 (80%).
- Result: **Pass**.

**Benchmark limitation:** Performance results use synthetic data and in-memory SQLite. They are not production-scale or concurrent multi-user load-test results. The usability result records the reported five-user observation.

## 10. Known limitations and deviations

- Waste management is **out of scope** for the final release.
- Authentication/RBAC implementation is reported complete by the team; security and permission validation are deferred. Do not describe security validation as passed.
- A distinct employee on-leave status is not confirmed.
- Complete stock-adjustment audit-trail behavior is not confirmed.
- Waste audit trails are not applicable to the final release scope.
- Email delivery configuration and failure-path verification require separate evidence.
- The application supports offline/local use. Multi-workstation concurrent use has not been validated.
- Invoice generation is included. Invoice printing is not a required user-facing feature and must not be presented as one.

Disclose relevant limitations during the final demonstration.

## 11. Feature freeze declaration

**Declaration commit:** `054dd59`  
**Declared effective date:** 7 November 2026  
**Purpose:** Final evaluation preparation for 9 November 2026.

- No new features or scope expansion after the effective date.
- No unnecessary architectural or dependency changes.
- Only critical bug fixes are permitted.
- Any critical fix must be tested, reviewed and documented.
- Existing demo video, test evidence and release documentation are preserved.
- The final evaluation will use the frozen release from the `main` branch.

**Team approval:** All four team members have approved the final deliverables.

## 12. Release decision

**Current state:** The frozen commit is synchronized with `origin/main`, the working tree was verified clean, and GitHub Actions passed for `054dd59`. The final local test suite reports 131 passed. Performance and usability test results are recorded above.

Do not mark SCRUM-53 Done until:

1. The final cross-check of README, SRS, SAD, Test Plan, RTM and project scope is complete.
2. Remaining Jira acceptance criteria are checked against actual evidence.
3. Any separately required formal peer-review evidence is confirmed and recorded.
4. The final Jira status and comments accurately reflect the verified result.

Recheck repository status and CI before final submission if any critical fix is made after the freeze.
