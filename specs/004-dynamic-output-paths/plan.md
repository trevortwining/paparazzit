# Technical Implementation Plan: Dynamic Output Paths

## Architecture
- Update `src/paparazzit/utils/storage.py` to support optional subdirectories.
- Update `src/paparazzit/cli.py` to calculate the folder name based on the input type (URL or Manifest).

## Implementation Details
1. **Domain Parsing**: Use `urllib.parse` to extract the netloc from URLs.
2. **String Sanitization**: Implement a utility function to replace `.` with `-`.
3. **Storage Logic**:
   - For single `--url`: Folder = sanitized domain.
   - For `--manifest`: Folder = sanitized filename.
   - For `--window`: Default to `captures/desktop/` or similar to maintain organization.

## Tasks
1. Update `storage.py` to accept a `subdir` argument in the save methods.
2. Update `cli.py` to compute the `subdir` name:
   - Extract domain from URL.
   - Extract filename from manifest path.
   - Apply the period-to-hyphen replacement.
3. Verify that directory creation (`mkdir -p`) is handled correctly before saving.
