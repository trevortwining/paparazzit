# Implementation Plan - Concurrent Manifest Captures (018)

## Goal
Refactor `paparazzit` to support concurrent URL captures from manifests using `asyncio` and `playwright.async_api`.

## Proposed Changes

### Phase 1: Core Engine Refactor
*   **`src/paparazzit/capture/engine.py`**: Change `capture` to `async def`.
*   **`src/paparazzit/capture/playwright_engine.py`**: 
    *   Switch imports to `playwright.async_api`.
    *   Refactor `__enter__`/`__exit__` logic to `async __aenter__`/`async __aexit__`.
    *   Update `capture` and `_scroll_page` to be `async`.
*   **`src/paparazzit/capture/mss_engine.py`**:
    *   Update `capture` to be `async def`.
    *   Since MSS is sync, wrap the internal call in `asyncio.to_thread`.

### Phase 2: CLI Update
*   **`src/paparazzit/cli.py`**:
    *   Update `snap` command to be `async` (using `@click.command()` combined with `anyio` or manual `asyncio.run`).
    *   Add `--concurrency` / `-c` option.
    *   Implement concurrent processing logic using `asyncio.Semaphore` and `asyncio.gather`.

### Phase 3: Manifest Utility Update
*   **`src/paparazzit/utils/manifest.py`**: (If needed) update to ensure it doesn't block.

## Verification Plan

### Automated Tests
*   Update existing tests in `tests/test_storage.py` and `tests/test_cli.py` to handle the new `async` engine (using `pytest-asyncio`).
*   Create `tests/test_concurrency.py` to:
    *   Mock the capture process with a delay.
    *   Verify that multiple "captures" finish in less than `num * delay` time.

### Manual Verification
*   Run `uv run paparazzit snap --manifest sites.json --concurrency 4`.
*   Verify output logs show concurrent processing.
*   Check that images and metadata are saved correctly in the respective subdirectories.
