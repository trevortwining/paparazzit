# paparazzit 📸

A high-performance CLI screenshot capture tool designed for QA teams. It collects screenshots along with rich system and context metadata, supporting both web (Playwright) and desktop (MSS) capture engines.

## 🚀 Features

- **Web Engine:** Full-page captures using Playwright.
- **Desktop Engine:** Fast screen/window captures using MSS.
- **Context-Rich:** Every capture generates a matching JSON metadata sidecar (timestamp, URL, window title, system info).
- **Sitemap Scouting:** Automatically generate capture manifests from website sitemaps.
- **Batch Processing:** Snap dozens of URLs at once from a JSON manifest.
- **Full-Page by Default:** Web captures automatically include the entire vertical length of the page.
- **Smart Organization:** Captures are automatically sorted into folders by domain or manifest name.
- **Smart Loading:** Automatic waiting for network idle plus an optional `--wait` buffer.

## 📦 Installation

This project uses `uv` for lightning-fast dependency management.

```bash
git clone <repository-url>
cd paparazzit
uv sync
```

## 🛠 Usage

### 1. Scouting a Site
Generate a manifest of URLs from a website's sitemap.
```bash
uv run paparazzit scout --url https://example.com/sitemap.xml --output manifest.json
```

### 2. Capturing Screenshots

#### Snap a Single URL
```bash
uv run paparazzit snap --url https://google.com
```

#### Snap a Specific Window
```bash
uv run paparazzit snap --window "Chrome"
```

#### Batch Snap from a Manifest
```bash
uv run paparazzit snap --manifest manifest.json
```

**Manifest Format (`manifest.json`):**
The manifest can be a simple list of URLs or a list of objects containing a `url` key.
```json
[
  "https://google.com",
  "https://github.com",
  { "url": "https://wikipedia.org" }
]
```

## 📁 Output Structure

All captures are saved to the `captures/` directory and organized into subfolders:

- **Single Snaps:** Saved to `captures/<domain-name>/` (e.g., `google-com/`) with individual PNG and JSON sidecars.
- **Batch Snaps:** Saved to `captures/<manifest-name>/` (e.g., `sites-json/`) with multiple PNGs and a single unified `metadata.json` for the entire run.
- **Desktop Snaps:** Saved to `captures/desktop/`.

**Files:**
- `snap_YYYYMMDD_HHMMSS.png`: The screenshot (full-page for web).
- `snap_YYYYMMDD_HHMMSS.json`: Metadata (for single snaps).
- `metadata.json`: Consolidated metadata (for batch snaps).

## 🛠 Development

Built with the **GitHub Spec Kit** framework.
- **Language:** Python 3.11+
- **Core Libs:** Playwright, MSS, Click, HTTPX.

---
*Maintained by Trevor Twining
