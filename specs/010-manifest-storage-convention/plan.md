# Technical Implementation Plan: Manifest Storage Convention

## Architecture
- Update `src/paparazzit/cli.py` to modify default output for `scout` and lookup logic for `snap`.
- Update `src/paparazzit/utils/storage.py` if necessary to handle the manifest directory path.

## Tasks
1. Update `scout` command: Change default `--output` value to `captures/manifests/manifest.json`.
2. Update `snap` command: Implement a lookup helper that checks `./` then `captures/manifests/`.
3. Add a unit test in `tests/test_cli.py` for the new lookup resolution.
