# Feature Spec: Unified Manifest Metadata

## Overview
Change the metadata storage behavior for manifest-based captures. Instead of individual JSON sidecars for every screenshot, all metadata for a batch run should be consolidated into a single `metadata.json` file within the output subdirectory.

## User Story
As a QA engineer, I want my batch capture results to have a single, clean summary file instead of dozens of individual JSON files, making it easier to parse and share the results of a full-site audit.

## Functional Requirements
1. **Consolidated Storage**: When running `snap --manifest`, suppress the creation of individual `.json` files for each capture.
2. **Unified JSON**: Create a single `metadata.json` in the target `captures/<manifest-name-json>/` folder.
3. **Content Schema**: The unified file should contain an array of objects, where each object represents one capture (including timestamp, URL, file path, and system info).
4. **Single-Snap Persistence**: Individual `--url` and `--window` captures should continue to use individual sidecars as they do now.

## Acceptance Criteria
- Running `paparazzit snap --manifest sites.json` creates one folder with multiple PNGs and exactly ONE `metadata.json`.
- The `metadata.json` contains the full history of the batch run.
- Running `paparazzit snap --url https://google.com` still creates a single PNG and a single JSON sidecar.
