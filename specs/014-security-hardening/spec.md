# Spec: Security Hardening

## Overview
This specification defines the security improvements for `paparazzit` to mitigate Local File Inclusion (LFI), Path Traversal, and XML External Entity (XXE) vulnerabilities.

## Requirements

### 1. Input Validation (CLI)
*   **Requirement:** The `snap` command MUST reject URLs with the `file://` scheme.
*   **Requirement:** The `snap` command MUST only accept `http://` and `https://` schemes.
*   **Error Handling:** If a forbidden scheme is detected, the CLI MUST exit with a status code of 1 and print a clear error message (e.g., "Error: Only HTTP/HTTPS URLs are supported.").

### 2. Output Path Sanitization (CLI)
*   **Requirement:** The `scout` command MUST resolve the `--output` path.
*   **Requirement:** The `scout` command MUST NOT allow writing files outside the current working directory or the `captures/` directory without explicit user confirmation (or a force flag).
*   **Logic:**
    *   If the resolved path is outside `os.getcwd()`, prompt the user: "Warning: You are writing outside the project directory. Continue? [y/N]"
    *   If `--force` is provided, skip the prompt.
    *   If not interactive (e.g., CI/CD), default to N (abort) unless `--force` is used.

### 3. Secure XML Parsing (Sitemap Utils)
*   **Requirement:** The `fetch_sitemap` function MUST use `defusedxml.ElementTree` instead of `xml.etree.ElementTree`.
*   **Requirement:** The parser MUST be configured to forbid external entity expansion (default behavior of `defusedxml`).
*   **Dependency:** The project MUST depend on `defusedxml`.

## Testing
*   **Test Case 1:** `paparazzit snap --url file:///etc/passwd` -> Assert exit code 1 and error message.
*   **Test Case 2:** `paparazzit scout --url ... --output /tmp/evil.json` -> Assert prompt or error.
*   **Test Case 3:** `paparazzit scout --url ... --output /tmp/evil.json --force` -> Assert success (if valid sitemap).
*   **Test Case 4:** Unit test `parse_sitemap_xml` with a malicious XML string (containing DTD/Entity) -> Assert `defusedxml` raises an error or ignores the entity safely.
