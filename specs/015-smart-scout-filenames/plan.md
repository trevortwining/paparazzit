# Plan: Smart Scout Filenaming

## Goal
Update `paparazzit scout` to automatically generate the output manifest filename based on the target domain when no `--output` is provided.

## Current Behavior
*   If `--output` is missing, defaults to `captures/manifests/manifest.json`.

## New Behavior
*   If `--output` is missing:
    1.  Parse the domain from `--url` (e.g., `https://google.ca/sitemap.xml` -> `google.ca`).
    2.  Sanitize the domain (replace dots `.` with hyphens `-`).
    3.  Set output to `captures/manifests/[domain-slug].json`.
    *   Example: `https://google.ca` -> `captures/manifests/google-ca.json`.

## Implementation Details
1.  **Modify `src/paparazzit/cli.py`**:
    *   Import `urlparse` (already there).
    *   In `scout` function:
        *   Extract domain: `urlparse(url).netloc` (or path logic if scheme missing).
        *   Slugify: `domain.replace(".", "-")`.
        *   Construct default path: `os.path.join(MANIFESTS_DIR, f"{slug}.json")`.

## Verification Plan
*   **Test Case 1:** `paparazzit scout --url https://google.ca` -> Assert file created at `captures/manifests/google-ca.json`.
*   **Test Case 2:** `paparazzit scout --url https://sub.example.com/sitemap.xml` -> Assert `sub-example-com.json`.
*   **Test Case 3:** Explicit `--output` still overrides default.
