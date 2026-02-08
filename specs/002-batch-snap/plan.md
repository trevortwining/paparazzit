# Technical Implementation Plan: Batch Snap

## Architecture
- Update `cli.py` to handle the new `--manifest` option.
- Implement a `ManifestParser` utility to handle different JSON structures (simple list vs. objects).
- Modify the execution flow to loop through targets while reusing the Playwright browser instance for efficiency.

## Tasks
1. Create `src/paparazzit/utils/manifest.py` to parse input files.
2. Update `cli.py` logic to support the new flag and loop execution.
3. Optimize Playwright engine to stay open during batch runs (avoiding browser restart per URL).
4. Verify error isolation (try/except block within the loop).
