# PMS Release Checklist

**Project:** Perishables Management System
**Jira:** SCRUM-53 — Final regression, release checklist and Sprint 2 demo
**Sprint:** Perishables Sprint 2
**Release evaluation:** 9 November 2026
**Evidence review date:** 6 November 2026

## 1. Regression testing

- [x] Run the complete automated test suite locally.
- [x] Confirm 111 tests passed on 6 November 2026.
- [x] Re-run tests after release evidence changes.
- [x] No critical defects reported during completed manual tests.
- [x] Perform manual application smoke testing.
- [x] Verify the six reported functional workflows.

## 2. Continuous integration

- [x] GitHub Actions workflow configured.
- [x] Latest five main-branch workflow runs reported as passed on 6 November 2026.
- [x] Final release PR #21 checks passed.
- [x] PR #21 merged into `main`.
- [x] Verify that no new failing workflow has appeared since the recorded check.

## 3. Clean-checkout verification

- [x] Clone repository into a fresh directory.
- [x] Create and activate a virtual environment.
- [x] Install dependencies from `requirements.txt`.
- [x] Run `python -m pytest -q`.
- [x] Confirm 111 tests passed on clean checkout.
- [x] Launch using `python -m src.main`.
- [x] Confirm application starts successfully with its database.
- [x] Verify main application screens.

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
- [x] Test Plan reviewed against actual execution evidence.
- [x] RTM reviewed against the SRS and Test Plan.
- [x] Project scope and team plan reviewed for deviations.
- [x] Jira acceptance criteria and issue status reviewed.
- [x] Team approval/sign-off recorded where required.

## 7. Sprint 2 demo and release

- [x] Record a demonstration.
- [x] Save the video in the repository at `docs/evidence/demo.mov`.
- [x] Verify the video plays correctly.
- [x] Confirm the required demo duration and content against the evaluation checklist.
- [ ] Confirm feature freeze by 7 November 2026.
- [x] Push final release-evidence changes through PR #21.
- [x] Open pull request targeting `main`.
- [x] Confirm PR #21 checks passed.
- [x] Merge PR #21 into `main`.
- [x] Confirm any required formal peer-review evidence is recorded.

## 8. Evidence recorded

| Check                | Evidence                                                  | Status                         |
| -------------------- | --------------------------------------------------------- | ------------------------------ |
| Local regression     | 111 tests passed                                          | Complete                       |
| Main-branch CI       | Latest five runs reported passed on 6 Nov                 | Complete at time checked       |
| Clean checkout       | Fresh clone, dependencies installed, application launched | Complete                       |
| Clean-checkout tests | 111 tests passed                                          | Complete                       |
| Manual smoke test    | Six smoke-test areas passed                               | Complete                       |
| Functional workflows | Six listed workflows passed                               | Complete                       |
| Screenshots          | `docs/evidence/screenshots/`                              | Recorded                       |
| Demo video           | `docs/evidence/demo.mov`, approximately 20 MB             | Recorded and playback verified |
| PR #21 checks        | All reported checks passed                                | Complete                       |
| PR #21 merge         | Merged into `main`                                        | Complete                       |
| Documentation review | SRS and SAD corrected; remaining docs under review        | In progress                    |
| Formal peer review   | No complete evidence recorded here                        | Pending verification           |

## 9. Known limitations and deviations

- Waste management is not implemented in the current release.
- Full authentication and RBAC are not confirmed as implemented.
- A distinct employee on-leave status is not confirmed.
- Complete stock-adjustment and waste audit trails are not confirmed.
- Performance and usability targets have not been formally measured.
- Email delivery configuration and failure-path verification require separate evidence.

These limitations must be disclosed during the final demonstration if they are relevant to the agreed requirements.

## 10. Release decision

**Current state:** Release evidence is substantially complete, but final documentation review and Jira acceptance review remain outstanding.

Do not mark SCRUM-53 Done until:

1. README, Test Plan, RTM and project scope documentation have been reviewed.
2. Remaining acceptance criteria have been checked against actual evidence.
3. Any required peer-review/sign-off evidence has been recorded.
4. The final Jira status and comments accurately reflect the result.

The release evidence above records the state reported on 6 November 2026. Recheck the repository and CI before final submission.
