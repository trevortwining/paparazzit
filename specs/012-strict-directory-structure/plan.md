# Implementation Plan: Strict Directory Structure

## Overview
Refactor storage utilities and CLI logic to enforce a strict, project-root-based directory hierarchy for all output files.

## Steps
- [x] **Refactor Storage Logic**: Update `src/paparazzit/utils/storage.py` to use `DEFAULT_CAPTURES_DIR` based on `PROJECT_ROOT`.
- [x] **Update CLI Defaults**: Modify `src/paparazzit/cli.py` to use `MANIFESTS_DIR` and `DEFAULT_CAPTURES_DIR` for default paths.
- [x] **Fix Path Resolution**: Ensure `scout` and `snap --manifest` use absolute paths correctly and prevent double-nesting.
- [x] **Clean Up**: Remove the incorrectly created nested directories (e.g., `captures/manifests/captures`).
- [x] **Verify Tests**: Update and run `pytest` to ensure all tests pass with the new absolute path logic.

## Acceptance Criteria
- [x] Running `scout` saves manifests to `~/projects/utils/paparazzit/captures/manifests/` by default.
- [x] Running `snap` saves images/metadata to `~/projects/utils/paparazzit/captures/snaps/` by default.
- [x] The structure `captures/manifests/captures` is never created.
