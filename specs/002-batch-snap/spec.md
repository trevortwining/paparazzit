# Feature Spec: Batch Snap Functionality

## Overview
Extends paparazzit to support batch processing of multiple URLs from a JSON manifest file.

## User Story
As a QA lead, I want to provide a list of URLs in a single file so that I can automatically generate screenshots for an entire site or a set of test environments without manual intervention.

## Functional Requirements
1. **Manifest Support**: Add a `--manifest <path>` flag to the `snap` command.
2. **JSON Format**: The manifest should be a simple JSON array of strings or objects containing a `url` key.
3. **Sequential Processing**: The tool should iterate through the list and capture each URL using the existing Playwright engine.
4. **Resilience**: If one URL fails to load, the tool should log the error and continue to the next one.
5. **Output**: Every capture should still follow the standard PNG + JSON sidecar storage pattern.

## Acceptance Criteria
- Running `paparazzit snap --manifest sites.json` processes all URLs in the file.
- Error handling prevents a single bad URL from crashing the entire batch.
- Metadata for each snap correctly reflects the specific URL captured.
