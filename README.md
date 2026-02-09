# paparazzit 📸

paparazzit is a robust CLI tool designed for automated screenshot capture and QA. It supports both web-based captures (via Playwright) and desktop window captures (via MSS), making it a versatile companion for visual regression testing and documentation.

## Features

- **Web Snapshots**: Capture full-page or viewport screenshots of URLs using Playwright.
- **Window Snapshots**: Capture specific desktop windows by title using MSS.
- **Sitemap Scouting**: Automatically fetch and parse `sitemap.xml` files to generate capture manifests.
- **Smart Loading**: Waits for "Network Idle" states by default to ensure pages are fully rendered.
- **QA Foundation**: Built-in `doctor` command to verify your environment and dependencies.

## Installation

paparazzit is managed using [uv](https://github.com/astral-sh/uv).

1. **Clone the repository**:
   ```bash
   git clone https://github.com/trevortwining/paparazzit.git
   cd paparazzit
   ```

2. **Setup the environment**:
   ```bash
   uv venv
   source .venv/bin/activate
   uv sync
   ```

3. **Install Browser Dependencies**:
   ```bash
   playwright install chromium
   ```

4. **Verify Installation**:
   ```bash
   paparazzit doctor
   ```

## Quick Start

### 1. Scout a Site
Generate a manifest of URLs from a sitemap:
```bash
paparazzit scout --url https://example.com --output manifests/example.json
```

### 2. Snap a Single URL
Capture a quick screenshot:
```bash
paparazzit snap --url https://example.com
```

### 3. Batch Capture from Manifest
Capture everything in your scouted manifest:
```bash
paparazzit snap --manifest captures/manifests/example.json
```

### 4. Capture a Desktop Window
Capture an open application by its window title:
```bash
paparazzit snap --window "Visual Studio Code"
```

## Storage Convention

Captures are organized into a strict directory structure for easy navigation:
- **Manifests**: `captures/manifests/*.json`
- **Screenshots**: `captures/snaps/[manifest-name]/`

## Development

Run tests to ensure everything is working:
```bash
pytest
```

---
*Created with dry wit and high competence by TBot.*
