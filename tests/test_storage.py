import os
import json
from PIL import Image
from paparazzit.utils.storage import save_capture

def test_save_capture_basic(tmp_path):
    # Mock image
    img = Image.new('RGB', (100, 100), color='red')
    captures_dir = tmp_path / "captures"
    
    img_path, json_path, metadata = save_capture(
        img, "test_engine", "https://example.com", 
        captures_dir=str(captures_dir)
    )
    
    assert os.path.exists(img_path)
    assert os.path.exists(json_path)
    assert metadata["engine"] == "test_engine"
    assert metadata["target"] == "https://example.com"
    assert "system" in metadata
    
    with open(json_path, 'r') as f:
        saved_metadata = json.load(f)
    assert saved_metadata == metadata

def test_save_capture_with_subdir(tmp_path):
    img = Image.new('RGB', (10, 10))
    captures_dir = tmp_path / "captures"
    subdir = "my-site"
    
    img_path, _, _ = save_capture(
        img, "test", "target", 
        captures_dir=str(captures_dir), subdir=subdir
    )
    
    assert str(captures_dir / subdir) in img_path
    assert os.path.exists(img_path)

def test_save_capture_no_json(tmp_path):
    img = Image.new('RGB', (10, 10))
    captures_dir = tmp_path / "captures"
    
    _, json_path, _ = save_capture(
        img, "test", "target", 
        captures_dir=str(captures_dir), save_json=False
    )
    
    assert json_path is None
