# Spec: Smart Scout Filenaming

## Overview
This specification updates the `scout` command to automatically generate an output manifest filename based on the target domain when the `--output` argument is omitted.

## Requirements

### 1. Default Filename Logic
*   **Trigger:** The `--output` argument is `None`.
*   **Logic:**
    1.  Parse the `--url` argument using `urllib.parse.urlparse`.
    2.  Extract the `netloc` (domain) or the first path component if `netloc` is missing.
    3.  Replace all dots `.` with hyphens `-` in the extracted domain.
    4.  Create a filename: `[domain-slug].json`.
    5.  Full path: `os.path.join(MANIFESTS_DIR, [domain-slug].json)`.

### 2. Output Override
*   **Requirement:** If `--output` is provided by the user, the automatic filenaming logic MUST be skipped, and the user-provided path used instead.

## Example Scenarios
*   `--url https://google.ca` -> `captures/manifests/google-ca.json`
*   `--url https://sub.example.com/sitemap.xml` -> `captures/manifests/sub-example-com.json`
*   `--url example.com` -> `captures/manifests/example-com.json`

## Testing
*   **Test Case 1:** Scout with no `--output` -> Assert file name matches sanitized domain.
*   **Test Case 2:** Scout with specific `--output` -> Assert specific file name used.
