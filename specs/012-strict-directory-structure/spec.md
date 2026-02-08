# Feature Spec: Strict Directory Structure

## Overview
Enforce a strict, project-root-based directory hierarchy for all output files (snaps and manifests). Regardless of the current working directory, all artifacts must be saved to absolute paths derived from the project root (`~/projects/utils/paparazzit`).

## User Story
As a user, I want my captures and manifests to be saved to a consistent, predictable location within the project structure, regardless of where I execute the `paparazzit` command, so that I can easily find my files and avoid cluttering random directories.

## Functional Requirements
1.  **Project Root Anchor**: All paths must be resolved relative to `~/projects/utils/paparazzit`.
2.  **Dedicated Snap Directory**: All screenshots (snaps) must be saved to `captures/snaps/` (e.g., `captures/snaps/<domain>/`).
3.  **Dedicated Manifest Directory**: All manifest files must be saved to `captures/manifests/`.
4.  **No Double-Nesting**: Prevent recursive directory creation (e.g., `captures/manifests/captures` or `captures/captures`).
5.  **CWD Independence**: The tool must behave identically whether run from the project root, a subdirectory, or an external path.

## Testing Requirements
1.  **Path Verification**: Verify that `save_capture` uses the absolute `DEFAULT_CAPTURES_DIR`.
2.  **Manifest Lookup**: Verify that `snap --manifest` correctly locates files in the absolute `MANIFESTS_DIR`.
3.  **Cross-Directory Execution**: (Manual/Integration) Verify that running `paparazzit` from `/tmp` or `$HOME` correctly targets the project folder.

## Acceptance Criteria
-   `scout` saves manifests to `~/projects/utils/paparazzit/captures/manifests/` by default.
-   `snap` saves images/metadata to `~/projects/utils/paparazzit/captures/snaps/` by default.
-   The structure `captures/manifests/captures` is never created.
