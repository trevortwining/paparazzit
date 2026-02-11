# Feature Spec: Concurrent Manifest Captures (Async)

## Overview
Currently, the `snap` command processes manifest files sequentially, waiting for each URL to complete before starting the next. This specification defines the refactor of the capture engine and CLI to support concurrent captures using Python's `asyncio` and Playwright's `async_api`.

## User Story
As a user, I want to capture multiple URLs from a manifest concurrently so that I can significantly reduce the total time required for large batch jobs.

## Functional Requirements

### 1. Async Engine Refactor
*   **Requirement:** `PlaywrightEngine` MUST be refactored to use `playwright.async_api`.
*   **Requirement:** The base `CaptureEngine.capture` method MUST be redefined as an `async def`.
*   **Requirement:** `MSSEngine` (Desktop Snaps) MUST be updated to work within an async context (wrapped or run in a thread/executor).

### 2. Concurrency Control
*   **Requirement:** The `snap` command MUST accept a new `--concurrency` (alias `-c`) option.
*   **Requirement:** Default concurrency MUST be set to `2`.
*   **Requirement:** The application MUST use a semaphore or similar mechanism to limit the number of active browser pages to the specified concurrency level.

### 3. CLI Integration
*   **Requirement:** The `snap` command MUST use `asyncio.run` to execute the capture loop when processing manifests.
*   **Requirement:** Progress reporting MUST remain clear and indicate which URLs are being processed.

## Implementation Details

### `src/paparazzit/capture/engine.py` (Base Class)
```python
class CaptureEngine:
    async def capture(self, target: str, **kwargs):
        raise NotImplementedError
```

### `src/paparazzit/cli.py`
*   Refactor the `manifest` processing block in `snap` to create a list of tasks and use `asyncio.gather` (with a `Semaphore`).

## Testing Requirements
1.  **Concurrent Execution:** Verify that multiple URLs are loading at the same time (checked via logs or network monitoring).
2.  **Concurrency Limit:** Verify that setting `--concurrency 1` results in sequential behavior.
3.  **Error Isolation:** Verify that a failure in one concurrent capture does not stop other active or pending captures.
4.  **MSSEngine Regression:** Verify that `paparazzit snap --window "Title"` still works correctly.

## Acceptance Criteria
-   `paparazzit snap --manifest sites.json --concurrency 5` launches up to 5 concurrent capture tasks.
-   Overall capture time for a manifest is significantly lower than sequential processing.
-   Application maintains a single browser instance while opening multiple pages/contexts for concurrency.
