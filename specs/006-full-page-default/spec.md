# Feature Spec: Full-Page Web Captures by Default

## Overview
Update the Playwright capture engine to generate full-page screenshots by default instead of just capturing the visible viewport.

## User Story
As a QA engineer, I want to see the entire webpage in my screenshots, including content "below the fold," so that I can audit the full layout of a page in one capture.

## Functional Requirements
1. **Full-Page Default**: Set Playwright's `full_page` parameter to `True` for all URL-based captures.
2. **Auto-Resize**: Ensure the browser engine calculates the full height of the document before snapping.

## Acceptance Criteria
- Running `paparazzit snap --url https://example.com` produces a PNG that shows the entire vertical length of the page.
- No changes are made to the desktop (MSS) engine.
