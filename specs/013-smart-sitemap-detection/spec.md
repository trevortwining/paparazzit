# Feature Spec: Smart Sitemap Detection

## Overview
Enhance the `scout` command to automatically detect `sitemap.xml` when provided with a base domain URL, improving usability by removing the need to manually append the filename.

## User Story
As a user, I want to provide a simple domain (e.g., `https://example.com`) to the `scout` command so that the tool automatically finds and parses `https://example.com/sitemap.xml` without me having to type the full path.

## Functional Requirements
1.  **Input Handling**:
    *   If the `--url` argument ends in `.xml`, treat it as a direct link to the sitemap (preserve existing behavior).
    *   If the `--url` argument does *not* end in `.xml`, automatically append `/sitemap.xml` to the URL.
2.  **Existence Check**:
    *   Before attempting to parse, verify that the constructed sitemap URL exists (return status 200).
    *   If the sitemap is not found (404), exit with a clear error message: `sitemap.xml not found at <url>`.
3.  **Redirection**: Follow standard HTTP redirects (e.g., `http` -> `https`, `non-www` -> `www`) when resolving the sitemap location.

## Testing Requirements
1.  **Direct XML**: Verify `scout --url https://site.com/custom-map.xml` still works.
2.  **Domain Root**: Verify `scout --url https://site.com` resolves to `https://site.com/sitemap.xml`.
3.  **Missing Sitemap**: Verify `scout --url https://site.com` returns a specific error if the sitemap doesn't exist.

## Acceptance Criteria
-   `paparazzit scout --url https://google.com` successfully finds and parses `https://google.com/sitemap.xml`.
-   `paparazzit scout --url https://google.com/sitemap.xml` still works.
-   `paparazzit scout --url https://example.com` (where no sitemap exists) prints `Error: sitemap.xml not found`.
