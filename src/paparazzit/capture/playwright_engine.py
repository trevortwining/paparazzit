from playwright.sync_api import sync_playwright
from paparazzit.capture.engine import CaptureEngine
from PIL import Image
import io
import subprocess
import sys
import time

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

    def _scroll_page(self, page):
        """
        Scrolls the page from top to bottom to trigger lazy loading.
        """
        # Python-driven scroll for better control and reliability
        last_height = page.evaluate("document.body.scrollHeight")
        
        while True:
            # Scroll down to bottom
            page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
            
            # Wait to load page
            page.wait_for_timeout(2000)
            
            # Calculate new scroll height and compare with last scroll height
            new_height = page.evaluate("document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        # Scroll back to top
        page.evaluate("window.scrollTo(0, 0)")
        # Wait for network idle again as new resources might be loading
        try:
            page.wait_for_load_state("networkidle", timeout=5000)
        except Exception:
            # If network doesn't idle, just proceed
            pass

    def capture(self, url: str, wait: int = 0, scroll: bool = False):
        if self.browser:
            # Context management handled externally or via __enter__
            page = self.browser.new_page()
            try:
                page.goto(url)
                page.wait_for_load_state("networkidle")
                
                if scroll:
                    self._scroll_page(page)

                if wait > 0:
                    page.wait_for_timeout(wait)
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
                    
                    if scroll:
                        self._scroll_page(page)
                        
                    if wait > 0:
                        page.wait_for_timeout(wait)
                    screenshot_bytes = page.screenshot(full_page=True)
                    return Image.open(io.BytesIO(screenshot_bytes))
                finally:
                    browser.close()
