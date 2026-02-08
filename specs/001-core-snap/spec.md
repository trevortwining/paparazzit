# Feature Spec: Core Snap Functionality

## Overview
paparazzit is a CLI-based screenshot capture tool designed for QA teams. This feature implements the core "snap" command which captures a screenshot and associated metadata.

## User Story
As a QA engineer, I want to run a simple command to capture a screenshot of a specific window or URL so that I can document bugs with full system context.

## Functional Requirements
1. **Command Interface**: Provide a CLI command `paparazzit snap`.
2. **Window Targeting**: Support a `--window` flag to target a specific application by title (e.g., "Chrome").
3. **URL Metadata**: Support a `--url` flag. If the target window is a browser (like Chrome), the tool should attempt to extract the current URL.
4. **Storage**:
    - Save the image as a PNG file in a `captures/` directory.
    - Generate a matching `json` sidecar file.
5. **Metadata Content**: The JSON file must include:
    - `timestamp`: ISO 8601 format.
    - `window_title`: The title of the captured window.
    - `url`: The URL (if `--url` was provided and successful).
    - `system_info`: Basic OS and resolution data.
6. **Naming Convention**: Files should be named using a timestamp or UUID to avoid collisions (e.g., `snap_20260208_1022.png`).

## Technical Constraints
- **Language**: Python 3.11+
- **Primary Engine**: `mss` for screenshotting.
- **Metadata Extraction**: Use `pygetwindow` or similar for window titles; research mechanism for URL extraction from active browsers.

## Acceptance Criteria
- Running `paparazzit snap --window "Chrome" --url` creates two files in `captures/`.
- The PNG shows the Chrome window.
- The JSON contains the correct timestamp and metadata.
