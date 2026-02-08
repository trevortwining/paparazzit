# paparazzit Constitution

## Core Principles

### I. Local-First & Privacy
paparazzit is a tool for capturing internal QA data. Screenshots and metadata are stored locally by default. Any transmission of data (e.g., to a central server or bug tracker) must be explicit, authenticated, and logged.

### II. Context-Rich Captures
A screenshot without context is just a picture. Every capture must automatically gather relevant system metadata: active window title, process name, timestamp, screen resolution, and OS version.

### III. Lightweight & Portable
The tool should be easy to distribute to team members. It should favor libraries that don't require heavy external dependencies (like full browser engines) unless absolutely necessary for the specific capture mode.

### IV. Structured Metadata
Metadata should be stored in a standard JSON format alongside image files (sidecar files) to allow for easy ingestion by other QA tools or automated analysis.

### V. Developer-Centric CLI
The primary interface is a CLI that follows Unix philosophy: simple commands, pipeable output, and clear error messages.

## Technology Stack
- **Language:** Python 3.11+
- **Capture Engines:** Multi-engine support (mss for speed, Playwright for web, etc.)
- **Storage:** Local filesystem with JSON metadata sidecars.

## Governance
This constitution guides all implementation plans and tasks. Changes to core principles require an update to this document and a review of existing features for alignment.

**Version**: 1.0.0 | **Ratified**: 2026-02-08
