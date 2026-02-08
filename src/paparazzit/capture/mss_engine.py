import mss
from paparazzit.capture.engine import CaptureEngine
from PIL import Image

class MSSEngine(CaptureEngine):
    def capture(self, window_title: str, **kwargs):
        with mss.mss() as sct:
            if window_title == "all" or window_title == "active":
                # For Linux, we default to primary monitor as window title targeting is limited without X11 libs
                monitor = sct.monitors[1] # Primary monitor
                sct_img = sct.grab(monitor)
                return Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            
            # Simple fallback: if title specified but not supported, capture full screen
            print(f"Warning: Window targeting for '{window_title}' not fully supported on this platform. Capturing primary monitor.")
            monitor = sct.monitors[1]
            sct_img = sct.grab(monitor)
            return Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
