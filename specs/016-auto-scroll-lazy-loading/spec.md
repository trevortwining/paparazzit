# Spec: Auto-Scroll for Lazy Loading

## Overview
This specification introduces an auto-scrolling mechanism to trigger lazy-loaded resources (images, iframes, scripts) before capturing a screenshot.

## Requirements

### 1. CLI Changes
*   **Flag:** Add `--scroll / --no-scroll` flag to `snap`.
*   **Default:** `False` (for speed).

### 2. Engine Logic (`PlaywrightEngine`)
*   **Method:** `_scroll_page(page)`
*   **Behavior:**
    1.  Start at `(0, 0)`.
    2.  Scroll down in chunks of `viewport.height` (e.g., `window.innerHeight`).
    3.  Wait `100ms` between chunks (or user `wait` setting?). Let's stick to a fixed `100ms` per chunk for responsiveness.
    4.  Continue until `document.body.scrollHeight`.
    5.  Wait `100ms` at the bottom.
    6.  Scroll back to `(0, 0)`.
    7.  Wait for `networkidle` again (critical: resources triggered by scroll need time to load).

### 3. Engine Interface
*   Update `capture(url, wait, scroll=False)` signature.
*   Update `CaptureEngine` base class if necessary (make `scroll` a kwarg).

## Testing
*   **Mocking:** Use `pytest-mock` to spy on `page.evaluate` calls to verify the scroll JS was executed.
*   **Integration:** Ideally, capture a page with `loading="lazy"` images.
