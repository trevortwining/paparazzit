# Technical Implementation Plan: Smart Loading

## Architecture
- Update `src/paparazzit/capture/playwright_engine.py` to use Playwright's network idle wait state.
- Update `src/paparazzit/cli.py` to support the new `--wait` flag.

## Implementation Details
1. **Engine**: Add `page.wait_for_load_state("networkidle")` after the `goto` call.
2. **Additional Sleep**: If a `wait_ms` value is passed to the engine, implement a `time.sleep()` or `page.wait_for_timeout()` before the screenshot.
3. **CLI**: Add `--wait` as an integer option to the `snap` command.

## Tasks
1. Modify `PlaywrightEngine.capture` to include the wait state logic.
2. Add the `--wait` option to the `snap` command in `cli.py`.
3. Update tests to verify the flag is accepted.
