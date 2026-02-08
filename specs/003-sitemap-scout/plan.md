# Technical Implementation Plan: Sitemap Scout

## Architecture
- Add the `scout` command to `src/paparazzit/cli.py`.
- Use `httpx` or `requests` to fetch sitemaps.
- Use `lxml` or standard `xml.etree.ElementTree` for parsing `<loc>` tags.

## Tasks
1. Add `httpx` to project dependencies.
2. Implement `src/paparazzit/utils/sitemap.py` to handle fetching and XML parsing.
3. Update `cli.py` to include the `scout` command group/logic.
4. Verify the output format matches the manifest expectations from Feature 002.
