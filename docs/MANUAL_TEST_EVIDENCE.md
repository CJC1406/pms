# Manual Test Evidence — PMS

**Project:** Perishables Management System  
**Test date:** 6 November 2026  
**Result:** All listed manual test cases passed.

## 1. Application Smoke Tests

| ID | Test area | Result |
|---|---|---|
| MT-01 | Dashboard loads and displays store overview | PASS |
| MT-02 | Inventory page loads and displays products | PASS |
| MT-03 | POS / Cart page loads and supports cart operations | PASS |
| MT-04 | Expiry Tracking page loads | PASS |
| MT-05 | Employee Management page loads | PASS |
| MT-06 | Light and dark themes work correctly | PASS |

## 2. Functional Workflow Tests

| ID | Test case | Result |
|---|---|---|
| FT-01 | Create a product | PASS |
| FT-02 | Edit product details | PASS |
| FT-03 | Update stock quantity | PASS |
| FT-04 | Complete checkout and generate invoice | PASS |
| FT-05 | Verify stock deduction after checkout | PASS |
| FT-06 | Verify expiry tracking | PASS |

## 3. Automated and Clean-Checkout Verification

| Verification | Result |
|---|---|
| Fresh GitHub clone | PASS |
| Dependency installation | PASS |
| Automated test suite | PASS — 111 tests |
| Application launch from clean clone | PASS |
| GitHub pull request CI | PASS |

## 4. Evidence Files

- Screenshots: `docs/evidence/screenshots/`
- Sprint 2 demo recording: `docs/evidence/demo.mov`

## 5. Overall Result

All 12 listed manual test cases passed. The automated test suite passed with 111 tests in the clean checkout. The application launched successfully from the clean checkout.

**Note:** Screenshot filenames are retained as captured. Refer to the screenshots folder for visual evidence.
