# Technical Implementation Plan: Core Snap (Option B)

## Architecture Overview
The tool will be a Python-based CLI using `click` for command-line parsing. It will use a factory pattern to select between two capture engines:
1. **Desktop Engine (`mss`)**: For window-based captures.
2. **Web Engine (`playwright`)**: For URL-based captures.

## Tech Stack
- **CLI**: `click`
- **Capture**: `mss` (Desktop), `playwright` (Web)
- **Metadata**: `pygetwindow` (Windows/Linux) or `pyobjc` (macOS) for window titles.
- **Image Processing**: `Pillow` (for any necessary resizing or padding).

## Implementation Details

### 1. Project Structure
```
paparazzit/
├── captures/          # Output directory
├── src/
│   ├── cli.py         # Entry point
│   ├── capture/
│   │   ├── engine.py  # Base class
│   │   ├── mss_engine.py
│   │   └── playwright_engine.py
│   └── utils/
│       ├── metadata.py
│       └── storage.py
├── pyproject.toml
└── README.md
```

### 2. Workflow Logic
- If `--url` is provided with a value:
    - Use Playwright to navigate to the URL.
    - Capture the viewport.
    - Save metadata with the provided URL.
- If `--window` is provided:
    - Find window handle by title.
    - Use mss to capture that specific bounding box.
    - Save metadata with window info.

### 3. Metadata Schema
```json
{
  "timestamp": "2026-02-08T10:23:00Z",
  "engine": "playwright|mss",
  "target": "URL or Window Title",
  "files": {
    "image": "snap_20260208_1023.png"
  },
  "system": {
    "os": "...",
    "resolution": "..."
  }
}
```

## Research Tasks
- [ ] Verify `mss` window-specific cropping logic across OSs.
- [ ] Determine best way to handle Playwright browser installation in a "lightweight" CLI context (e.g., `playwright install chromium`).

## Tasks Breakdown (High Level)
1. Setup Python environment with `uv`.
2. Implement storage and metadata utilities.
3. Implement the Playwright capture engine.
4. Implement the MSS capture engine.
5. Wire everything into the `click` CLI.
