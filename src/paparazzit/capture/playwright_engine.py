from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright
from paparazzit.capture.engine import CaptureEngine
from PIL import Image
import io
import subprocess
import sys
import asyncio

class PlaywrightEngine(CaptureEngine):
    def __init__(self):
        self._ensure_browser()
        self.playwright = None
        self.browser = None

    def _ensure_browser(self):
        # Basic check/install for chromium
        try:
            with sync_playwright() as p:
                try:
                    browser = p.chromium.launch()
                    browser.close()
                except Exception:
                    print("Chromium not found. Installing...")
                    subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
        except Exception as e:
            print(f"Warning: Playwright browser check failed: {e}")

    async def __aenter__(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    async def _scroll_page(self, page):
        """
        Incrementally scrolls the page from top to bottom to trigger lazy loading.
        """
        # Get total scroll height
        scroll_height = await page.evaluate("document.body.scrollHeight")
        viewport_height = await page.evaluate("window.innerHeight")
        current_scroll = 0

        while current_scroll < scroll_height:
            # Scroll down by viewport height
            await page.evaluate(f"window.scrollTo(0, {current_scroll + viewport_height});")
            current_scroll += viewport_height
            
            # Wait for content to load
            await page.wait_for_timeout(500)
            
            # Recalculate scroll height in case it grew (infinite scroll)
            new_scroll_height = await page.evaluate("document.body.scrollHeight")
            if new_scroll_height > scroll_height:
                scroll_height = new_scroll_height

        # Scroll back to top
        await page.evaluate("window.scrollTo(0, 0)")
        # Wait for network idle again as new resources might be loading
        try:
            await page.wait_for_load_state("networkidle", timeout=5000)
        except Exception:
            # If network doesn't idle, just proceed
            pass

    async def capture(self, url: str, wait: int = 0, scroll: bool = False):
        if self.browser:
            # Context management handled externally or via __aenter__
            page = await self.browser.new_page()
            try:
                await page.goto(url)
                try:
                    await page.wait_for_load_state("networkidle", timeout=10000) # Add timeout to avoid hanging
                except Exception:
                    pass # Proceed even if networkidle times out
                
                if scroll:
                    await self._scroll_page(page)

                if wait > 0:
                    await page.wait_for_timeout(wait)
                screenshot_bytes = await page.screenshot(full_page=True)
                return Image.open(io.BytesIO(screenshot_bytes))
            finally:
                await page.close()
        else:
            # Fallback for one-off captures if not used as context manager
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                try:
                    await page.goto(url)
                    try:
                        await page.wait_for_load_state("networkidle", timeout=10000)
                    except Exception:
                        pass
                    
                    if scroll:
                        await self._scroll_page(page)
                        
                    if wait > 0:
                        await page.wait_for_timeout(wait)
                    screenshot_bytes = await page.screenshot(full_page=True)
                    return Image.open(io.BytesIO(screenshot_bytes))
                finally:
                    await browser.close()
