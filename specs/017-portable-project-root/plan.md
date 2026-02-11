# Implementation Plan - Portable Project Root (017)

## Goal
Implement dynamic `PROJECT_ROOT` detection in `src/paparazzit/utils/storage.py` and update `doctor` command for visibility.

## Proposed Changes

### `src/paparazzit/utils/storage.py`
- Remove hardcoded `PROJECT_ROOT`.
- Implement environment variable check (`PAPARAZZIT_ROOT`).
- Implement fallback using `__file__` to traverse up 3 levels.

### `src/paparazzit/cli.py`
- Update `doctor` command to print the resolved `PROJECT_ROOT`.

## Verification Plan

### Automated Tests
- Create `tests/test_portable_root.py` to:
    - Verify default detection (no env var).
    - Verify env var override.
- Run `uv run pytest tests/test_portable_root.py`.
- Run all existing tests to ensure no regressions in pathing.

### Manual Verification
- Run `uv run paparazzit doctor` and check output.
- Run `PAPARAZZIT_ROOT=/tmp/pap_test uv run paparazzit doctor` and verify the override.
