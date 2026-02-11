import json
import os
from datetime import datetime
import platform

# Resolve PROJECT_ROOT
PROJECT_ROOT = os.environ.get("PAPARAZZIT_ROOT")
if not PROJECT_ROOT:
    # Move up 3 levels from src/paparazzit/utils/storage.py to get to project root
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

DEFAULT_CAPTURES_DIR = os.path.join(PROJECT_ROOT, "captures", "snaps")

def get_system_info():
    return {
        "os": platform.system(),
        "os_release": platform.release(),
        "machine": platform.machine(),
    }

def save_capture(image, engine_name, target, captures_dir=None, subdir=None, save_json=True):
    if captures_dir is None:
        captures_dir = DEFAULT_CAPTURES_DIR

    output_dir = captures_dir
    if subdir:
        output_dir = os.path.join(captures_dir, subdir)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = f"snap_{timestamp}"
    image_path = os.path.join(output_dir, f"{base_name}.png")
    
    image.save(image_path)
    
    metadata = {
        "timestamp": datetime.now().isoformat(),
        "engine": engine_name,
        "target": target,
        "files": {
            "image": os.path.basename(image_path)
        },
        "system": get_system_info()
    }
    
    json_path = None
    if save_json:
        json_path = os.path.join(output_dir, f"{base_name}.json")
        with open(json_path, "w") as f:
            json.dump(metadata, f, indent=2)
    
    return image_path, json_path, metadata
