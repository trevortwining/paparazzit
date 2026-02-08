# Implementation Plan: Smart Sitemap Detection

## Overview
Update `scout` logic to check for `sitemap.xml` automatically when provided with a base domain.

## Steps
- [ ] **Define Spec**: Create `specs/013-smart-sitemap-detection/spec.md`.
- [ ] **Refactor `fetch_sitemap`**: Update `src/paparazzit/utils/sitemap.py` to handle URL resolution.
    -   If URL ends in `.xml`, use as is.
    -   If not, append `/sitemap.xml`.
    -   Verify existence (HTTP HEAD/GET).
- [ ] **Update CLI Logic**: Ensure `src/paparazzit/cli.py` handles the potential `FileNotFound` or `HTTPError` gracefully.
- [ ] **Add Tests**: Create `tests/test_sitemap_detection.py` to cover:
    -   Direct XML input.
    -   Domain root input.
    -   Missing sitemap (404).
- [ ] **Verify**: Run `pytest` to confirm all existing and new tests pass.

## Acceptance Criteria
- [ ] `paparazzit scout --url https://google.com` works.
- [ ] `paparazzit scout --url https://google.com/sitemap.xml` works.
- [ ] `paparazzit scout --url https://missing.com` fails with `Error: sitemap.xml not found`.
