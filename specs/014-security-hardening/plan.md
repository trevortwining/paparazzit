# Plan: Security Hardening

## Goal
Harden `paparazzit` against common local vulnerabilities including Local File Inclusion (LFI), Path Traversal, and XML External Entity (XXE) attacks.

## Vulnerabilities to Address
1.  **Local File Disclosure (LFI):** `snap --url` currently accepts `file://` schemes, allowing users to snapshot sensitive local files.
2.  **Path Traversal/Arbitrary Write:** `scout --output` allows writing files to absolute paths or via `../`, potentially overwriting critical system files.
3.  **XML External Entity (XXE):** `sitemap.py` uses `xml.etree.ElementTree` which is vulnerable to malicious XML payloads.

## Proposed Changes

### 1. URL Validation (`cli.py`, `capture/playwright_engine.py`)
*   **Logic:**
    *   Inspect `url` argument in `snap`.
    *   Raise an error if the scheme is not `http` or `https`.
    *   Allow an override flag (e.g., `--unsafe-allow-file`) if this is a desired power-user feature, otherwise block entirely. **Decision: Block entirely for now.**

### 2. Output Path Sanitization (`cli.py`, `utils/storage.py`)
*   **Logic:**
    *   In `scout`, resolve the `--output` path.
    *   Ensure the resolved path is within the `paparazzit` project root (or a specific `captures/` allowlist).
    *   If the user explicitly provides an absolute path outside the project, prompt for confirmation (if interactive) or error out.

### 3. Secure XML Parsing (`utils/sitemap.py`)
*   **Dependency:** Add `defusedxml` to `pyproject.toml` (and `uv`).
*   **Logic:**
    *   Replace `xml.etree.ElementTree` with `defusedxml.ElementTree`.
    *   This automatically prevents XXE and billion laughs attacks.

## Verification Plan
*   **Test LFI:** Attempt `paparazzit snap --url file:///etc/passwd` -> Should fail.
*   **Test Traversal:** Attempt `paparazzit scout --url ... --output ../../../system_file` -> Should fail/warn.
*   **Test XXE:** Create a malicious sitemap with an external entity and attempt to `scout` it -> Should fail safely.
