# Spec: Portable Project Root Detection

## Overview
Currently, `PROJECT_ROOT` is hardcoded to a specific path in `storage.py`. This specification defines a portable method to detect the project root dynamically, allowing the application to run correctly regardless of its installation location or system user.

## Requirements

### 1. Dynamic Root Resolution
*   **Requirement:** The application MUST resolve the project root path dynamically.
*   **Logic:**
    1.  Check for an environment variable `PAPARAZZIT_ROOT`.
    2.  If `PAPARAZZIT_ROOT` is set, use its value as the `PROJECT_ROOT`.
    3.  If NOT set, calculate the root relative to the location of `storage.py`.
    4.  Since `storage.py` is at `src/paparazzit/utils/storage.py`, the project root is three levels up.

### 2. Implementation Details
*   **File:** `src/paparazzit/utils/storage.py`
*   **Implementation:**
    ```python
    import os

    # Resolve PROJECT_ROOT
    PROJECT_ROOT = os.environ.get("PAPARAZZIT_ROOT")
    if not PROJECT_ROOT:
        # Move up 3 levels from src/paparazzit/utils/storage.py to get to project root
        PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    ```

### 3. Verification
*   **Requirement:** The `doctor` command MUST display the resolved `PROJECT_ROOT` to aid in debugging.
*   **Requirement:** All existing capture and manifest paths MUST remain relative to the new dynamic `PROJECT_ROOT`.

## Testing Requirements
1.  **Default Detection:** Verify `PROJECT_ROOT` correctly identifies the directory containing `pyproject.toml` when no environment variable is set.
2.  **Environment Variable Override:** Set `PAPARAZZIT_ROOT=/tmp/paparazzit_test` and verify that `DEFAULT_CAPTURES_DIR` updates to `/tmp/paparazzit_test/captures/snaps`.
3.  **Cross-Platform Pathing:** Ensure `os.path.abspath` and `os.path.join` are used to maintain compatibility with Windows and Unix-like systems.

## Acceptance Criteria
-   Hardcoded home directory path is removed from `storage.py`.
-   Application successfully creates `captures/` inside its own directory structure when run without overrides.
-   Providing `PAPARAZZIT_ROOT` successfully redirects all output.
