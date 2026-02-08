# Technical Implementation Plan: Strict Sitemap Parsing

## Architecture
- Modify the XPath/search logic in `src/paparazzit/utils/sitemap.py`.

## Implementation Details
1. Update `parse_sitemap_xml` to use a more specific path: `.//{*}url/{*}loc`.
2. This ensures we only match `loc` when it is a direct child of `url`.

## Tasks
1. Edit `src/paparazzit/utils/sitemap.py`.
2. Test with a sample sitemap that includes both `<url>` and other tags (like `<sitemap>` or metadata).
