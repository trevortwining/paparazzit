# Feature Spec: Dynamic Output Paths

## Overview
Organize captures into subdirectories based on the domain or manifest name.

## User Story
As a QA engineer, I want my captures to be automatically organized into folders by domain so that I can easily browse screenshots from different sites without them getting mixed together in one big folder.

## Functional Requirements
1. **Domain-Based Folders**: When capturing a URL (via `--url`), create a subdirectory inside `captures/` named after the domain.
    - Example: `https://github.com/openclaw` -> `captures/github-com/`.
    - Rule: Replace all periods (`.`) in the domain with hyphens (`-`).
2. **Manifest-Based Folders**: When using a manifest (via `--manifest`), use the manifest filename as the subdirectory name.
    - Example: `internal-sites.json` -> `captures/internal-sites-json/`.
    - Rule: Replace all periods (`.`) in the filename with hyphens (`-`).
3. **Consistency**: Ensure both the PNG and the JSON metadata are saved into these new subdirectories.

## Acceptance Criteria
- Running `paparazzit snap --url https://google.com` saves files to `captures/google-com/`.
- Running `paparazzit snap --manifest sites.json` saves all snaps into `captures/sites-json/`.
- All periods in folder names are successfully converted to hyphens.
