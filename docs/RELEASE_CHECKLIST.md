# PMS Release Checklist

**Project:** Perishables Management System  
**Jira:** SCRUM-53 — Final regression, release checklist and Sprint 2 demo  
**Sprint:** Sprint 2  
**Release evaluation:** 9 November 2026

## 1. Regression testing

- [x] Run the complete automated test suite locally.
- [x] Confirm 111 tests passed on 6 November 2026.
- [ ] Re-run tests after the final release changes.
- [ ] Investigate and resolve any critical defects.
- [ ] Perform a manual application smoke test.

## 2. Continuous integration

- [x] GitHub Actions workflow is configured.
- [x] Latest five main-branch workflow runs passed on 6 November 2026.
- [ ] Push the SCRUM-53 feature branch.
- [ ] Confirm its GitHub Actions workflow passes.
- [ ] Confirm the final pull request checks pass.

## 3. Clean checkout verification

- [ ] Clone the repository into a fresh directory.
- [ ] Create and activate a virtual environment.
- [ ] Install dependencies from requirements.txt.
- [ ] Launch the application using python -m src.main.
- [ ] Confirm the database initialises successfully.
- [ ] Verify the main application screens work.

## 4. Manual smoke testing

- [ ] Dashboard opens and displays correctly.
- [ ] Inventory screens load and product operations work.
- [ ] Billing cart and checkout behave correctly.
- [ ] Expiry tracking displays the expected information.
- [ ] Employee management screens work.
- [ ] Light and dark themes work correctly.
- [ ] No critical errors occur during normal navigation.

## 5. Documentation and project records

- [ ] README setup instructions are accurate.
- [ ] SRS reflects the agreed requirements.
- [ ] SAD reflects the implemented architecture.
- [ ] Test Plan reflects the actual testing approach.
- [ ] RTM maps requirements to tests.
- [ ] Jira acceptance criteria and issue status are updated.

## 6. Sprint 2 demo and release

- [ ] Record a demonstration of approximately two minutes.
- [ ] Save the video in the repository.
- [ ] Verify the video plays correctly.
- [ ] Freeze feature changes by 7 November 2026.
- [ ] Push the final feature branch.
- [ ] Open a pull request targeting main.
- [ ] Obtain peer review and address feedback.
- [ ] Merge only after acceptance criteria and CI checks pass.

## Evidence recorded

| Check | Evidence |
|---|---|
| Local regression | 111 tests passed, reported 6 November 2026 |
| Main-branch CI | Latest five runs passed, checked 6 November 2026 |
| SCRUM-53 branch CI | Pending |
| Clean checkout | Pending |
| Manual smoke test | Pending |
| Demo video | Pending |
| Peer review and merge | Pending |

**Release decision:** Not yet approved. Complete the pending checks before declaring the release ready.
