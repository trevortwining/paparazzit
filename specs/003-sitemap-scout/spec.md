# Feature Spec: Sitemap Manifest Generation (scout)

## Overview
Adds a new command `paparazzit scout` that fetches a website's `sitemap.xml` and generates a JSON manifest file compatible with the `snap --manifest` command.

## User Story
As a QA engineer, I want to quickly generate a list of all pages on a site so that I can perform a full-site visual audit without manually creating a manifest.

## Functional Requirements
1. **New Command**: Implement `paparazzit scout --url <sitemap_url>`.
2. **Sitemap Parsing**:
    - Fetch the XML from the provided URL.
    - Extract all `<loc>` tags.
    - Handle standard `sitemap.xml` and Gzipped sitemaps (`.xml.gz`) if possible.
3. **Output**: Save the extracted URLs into a `manifest.json` (default name) in the current directory.
4. **Options**:
    - `--output <filename>`: Specify a custom name for the generated manifest.
    - `--limit <number>`: (Optional) Limit the number of URLs extracted for quick testing.

## Acceptance Criteria
- Running `paparazzit scout --url https://example.com/sitemap.xml` creates a `manifest.json`.
- The generated file is a valid JSON array of strings.
- The output file can be immediately used with `paparazzit snap --manifest manifest.json`.
