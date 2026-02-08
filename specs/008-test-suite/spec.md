# Feature Spec: Test Suite Implementation

## Overview
Implement a comprehensive test suite for paparazzit using pytest to ensure reliability across all features (snap, scout, batch processing).

## Functional Requirements
1. **Unit Tests**:
    - Manifest parsing (src/paparazzit/utils/manifest.py)
    - Sitemap parsing (src/paparazzit/utils/sitemap.py)
    - Path sanitization and storage logic (src/paparazzit/utils/storage.py)
2. **Integration Tests**:
    - CLI command wiring (src/paparazzit/cli.py)
    - Metadata collection and consolidation logic
3. **Mocks**:
    - Use mocks for external dependencies (httpx, playwright, mss) to ensure tests run reliably in CI/WSL environments without requiring a GUI or live internet.

## Acceptance Criteria
- Running `pytest` from the project root executes all tests.
- Minimum 70% code coverage for core utilities.
- All tests pass on the current codebase.
