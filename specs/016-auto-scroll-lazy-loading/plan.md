# Plan: Auto-Scroll for Lazy Loading

## Goal
Implement an auto-scroll mechanism to trigger lazy-loaded images before capturing a screenshot. This addresses issues where `networkidle` and timeouts are insufficient.

## Strategy
Add a `--scroll` flag to the `snap` command. When enabled, `paparazzit` will:
1.  Navigate to the page.
2.  Perform a "smooth scroll" from top to bottom.
3.  Wait briefly at the bottom (optional buffer).
4.  Scroll back to top.
5.  Wait for network idle again (to let triggered resources finish loading).
6.  Capture the screenshot.

## Implementation Details
1.  **CLI Update (`src/paparazzit/cli.py`):**
    *   Add `--scroll/--no-scroll` flag to `snap` (default: `False`? Or maybe `True` if we want robust defaults?). Let's make it opt-in for now to keep things fast, or maybe a `--lazy` flag. Let's stick with `--scroll`.

2.  **Engine Update (`src/paparazzit/capture/playwright_engine.py`):**
    *   Update `capture` method signature to accept `scroll: bool`.
    *   Implement `_scroll_page(page)` helper:
        *   Execute JS to scroll by viewport height chunks.
        *   Wait small delay between chunks (e.g., 100ms).
        *   Once at bottom, scroll back to `(0, 0)`.

## Verification Plan
*   **Test Case:** Create a dummy HTML page with lazy-loaded images (using `loading="lazy"` and placement below fold).
*   **Action:** Snap with `--scroll`.
*   **Assertion:** Verify the bottom image is loaded (mock checking `naturalWidth` or just visual check if we had visual regression testing). For unit tests, we can just assert the scroll JS was executed.
