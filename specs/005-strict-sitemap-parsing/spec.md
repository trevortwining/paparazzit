# Feature Spec: Strict Sitemap Parsing

## Overview
Refine the sitemap parsing logic to strictly extract URLs that are contained within `<url><loc>...</loc></url>` tags.

## User Story
As a QA engineer, I want to ensure that my manifest only contains actual page URLs from the sitemap, avoiding any other `<loc>` tags that might be present (such as those in sitemap index files).

## Functional Requirements
1. **Strict Tag Matching**: Update the parser to specifically look for the `<loc>` tag inside a `<url>` parent tag.
2. **Namespace Support**: Maintain existing support for XML namespaces (e.g., the standard sitemaps.org schema).
3. **Index Handling**: By strictly looking for `<url><loc>`, this naturally avoids `<sitemap><loc>` patterns used in sitemap index files, which is the desired behavior for a leaf-node manifest.

## Acceptance Criteria
- Running `paparazzit scout` on a standard sitemap correctly extracts all page URLs.
- URLs inside `<sitemap>` tags (sitemap indexes) are ignored.
- The output manifest format remains unchanged.
