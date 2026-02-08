from playwright.sync_api import sync_playwright
from paparazzit.capture.engine import CaptureEngine
from PIL import Image
import io
import subprocess
import sys

class PlaywrightEngine(CaptureEngine):
    def __init__(self):
        self._ensure_browser()
        self.playwright = None
        self.browser = None

    def _ensure_browser(self):
        # Basic check/install for chromium
        try:
            # We try to launch, if it fails we might need to install
            with sync_playwright() as p:
                try:
                    p.chromium.launch()
                except Exception:
                    print("Chromium not found. Installing...")
                    subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
        except Exception as e:
            print(f"Warning: Playwright browser check failed: {e}")

    def __enter__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def capture(self, url: str):
        if self.browser:
            # Context management handled externally or via __enter__
            page = self.browser.new_page()
            try:
                page.goto(url)
                page.wait_for_load_state("networkidle")
                screenshot_bytes = page.screenshot(full_page=True)
                return Image.open(io.BytesIO(screenshot_bytes))
            finally:
                page.close()
        else:
            # Fallback for one-off captures if not used as context manager
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                try:
                    page.goto(url)
                    page.wait_for_load_state("networkidle")
                    screenshot_bytes = page.screenshot(full_page=True)
                    return Image.open(io.BytesIO(screenshot_bytes))
                finally:
                    browser.close()
