# Technical Implementation Plan: Full-Page Default

## Architecture
- Modify the `PlaywrightEngine` call in `src/paparazzit/capture/playwright_engine.py`.

## Implementation Details
1. Locate the `page.screenshot()` call.
2. Update the arguments to include `full_page=True`.

## Tasks
1. Edit `src/paparazzit/capture/playwright_engine.py`.
2. Verify that long pages (like Wikipedia or news sites) result in vertically long PNG files.
