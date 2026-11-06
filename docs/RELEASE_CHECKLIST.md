# PMS Release Checklist

**Project:** Perishables Management System  
**Jira:** SCRUM-53 — Final regression, release checklist and Sprint 2 demo  
**Sprint:** Sprint 2  
**Release evaluation:** 9 November 2026

## 1. Regression testing

- [x] Run the complete automated test suite locally.
- [x] Confirm 111 tests passed on 6 November 2026.
- [x] Re-run tests after the final release documentation and evidence changes.
- [x] No critical defects reported during the completed manual tests.
- [x] Perform a manual application smoke test.

## 2. Continuous integration

- [x] GitHub Actions workflow is configured.
- [x] Latest five main-branch workflow runs passed on 6 November 2026.
- [ ] Push the SCRUM-53 release-evidence branch.
- [ ] Confirm its GitHub Actions workflow passes.
- [ ] Confirm the final pull request checks pass.

## 3. Clean checkout verification

- [x] Clone the repository into a fresh directory.
- [x] Create and activate a virtual environment.
- [x] Install dependencies from requirements.txt.
- [x] Launch the application using python -m src.main.
- [x] Confirm the application starts successfully with its database.
- [x] Verify the main application screens work.

## 4. Manual smoke testing

- [x] Dashboard opens and displays correctly.
- [x] Inventory screens load and product operations work.
- [x] Billing cart and checkout behave correctly.
- [x] Expiry tracking displays the expected information.
- [x] Employee management screens work.
- [x] Light and dark themes work correctly.
- [x] No critical errors reported during normal navigation.

## 5. Documentation and project records

- [ ] README setup instructions are reviewed.
- [ ] SRS reflects the agreed requirements.
- [ ] SAD reflects the implemented architecture.
- [ ] Test Plan reflects the actual testing approach.
- [ ] RTM maps requirements to tests.
- [ ] Jira acceptance criteria and issue status are updated.

## 6. Sprint 2 demo and release

- [x] Record a demonstration.
- [x] Save the video in the repository at docs/evidence/demo.mov.
- [ ] Verify the video plays correctly.
- [ ] Freeze feature changes by 7 November 2026.
- [ ] Push the final feature branch.
- [ ] Open a pull request targeting main.
- [ ] Obtain peer review and address feedback.
- [ ] Merge only after acceptance criteria and CI checks pass.

## Evidence recorded

| Check | Evidence |
|---|---|
| Local regression | 111 tests passed |
| Main-branch CI | Latest five runs passed, checked 6 November 2026 |
| Clean checkout | Fresh clone, dependencies installed, tests passed, app launched |
| Clean checkout tests | 111 tests passed |
| Manual smoke test | All 6 smoke-test areas passed |
| Functional workflows | All 6 listed workflows passed |
| Screenshots | docs/evidence/screenshots/ |
| Demo video | docs/evidence/demo.mov, approximately 20 MB |
| SCRUM-53 branch CI | Pending |
| Final PR checks | Pending |
| Peer review and merge | Pending |

**Release decision:** Pending final branch CI, pull request review, documentation review, and demo playback verification.
