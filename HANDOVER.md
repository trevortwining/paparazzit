# Handover: paparazzit

## Status
Core functionality is stable and tested. The tool supports URL/window snaps, sitemap scouting, and batch processing.

## Current Specs
- `001-core-snap`: Basic engine logic.
- `002-batch-snap`: Batch processing logic.
- `003-sitemap-scout`: Sitemap to manifest generation.
- `004-dynamic-output-paths`: Folder organization.
- `005-strict-sitemap-parsing`: Targeted `<url><loc>` scraping.
- `006-full-page-default`: Vertical capture for web.
- `007-unified-manifest-metadata`: JSON consolidation for batches.
- `008-test-suite`: Pytest foundation.
- `009-quality-assurance-foundation`: Pre-commit hooks & `doctor` command.
- `010-manifest-storage-convention`: `captures/manifests` folder.
- `011-smart-loading`: Network idle & `--wait` flag.

## Next Steps
- **Desktop Scroll & Stitch:** Implement a mechanism to capture long desktop windows (PDFs, Slack) by scrolling and merging.
- **GUI Selector:** Add a feature to interactively select a window/region if `--window` is ambiguous.
- **Cloud Upload:** Add an optional feature to upload captures to a S3/GCS bucket for team sharing.
- **CI/CD Integration:** Set up a GitHub Action to run the test suite on every PR.
