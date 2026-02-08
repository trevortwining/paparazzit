# Technical Implementation Plan: Unified Manifest Metadata

## Architecture
- Update `src/paparazzit/utils/storage.py` to support returning metadata objects without saving them to disk.
- Update the batch loop in `src/paparazzit/cli.py` to collect these objects and perform a single write at the end of the run.

## Implementation Details
1. **Storage Utility**: Add a flag or separate method to `storage.py` that handles "batch" metadata (gathering vs. writing).
2. **CLI Logic**: 
   - Initialize a `batch_results` list.
   - For each snap in the manifest loop, append the metadata to the list.
   - After the loop finishes, save the list as `metadata.json` in the target subdirectory.

## Tasks
1. Refactor `storage.py` to make JSON writing optional/separable from PNG writing.
2. Update the manifest processing logic in `cli.py` to accumulate results.
3. Verify that the final `metadata.json` is valid and contains all entries.
