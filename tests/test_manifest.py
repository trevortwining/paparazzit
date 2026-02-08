import json
import pytest
import os
from paparazzit.utils.manifest import parse_manifest

def test_parse_manifest_string_list(tmp_path):
    manifest_file = tmp_path / "manifest.json"
    data = ["https://google.com", "https://github.com"]
    manifest_file.write_text(json.dumps(data))
    
    urls = parse_manifest(str(manifest_file))
    assert urls == data

def test_parse_manifest_object_list(tmp_path):
    manifest_file = tmp_path / "manifest.json"
    data = [{"url": "https://google.com"}, {"url": "https://github.com"}]
    manifest_file.write_text(json.dumps(data))
    
    urls = parse_manifest(str(manifest_file))
    assert urls == ["https://google.com", "https://github.com"]

def test_parse_manifest_mixed_list(tmp_path):
    manifest_file = tmp_path / "manifest.json"
    data = ["https://google.com", {"url": "https://github.com"}, "invalid", {"no_url": "here"}]
    manifest_file.write_text(json.dumps(data))
    
    urls = parse_manifest(str(manifest_file))
    # 'invalid' is a string, so it should be included as a URL (even if not a valid URL format)
    # The current implementation includes all strings.
    assert urls == ["https://google.com", "https://github.com", "invalid"]

def test_parse_manifest_not_found():
    with pytest.raises(FileNotFoundError):
        parse_manifest("non_existent.json")

def test_parse_manifest_invalid_json(tmp_path):
    manifest_file = tmp_path / "invalid.json"
    manifest_file.write_text("not json")
    
    with pytest.raises(json.JSONDecodeError):
        parse_manifest(str(manifest_file))

def test_parse_manifest_not_array(tmp_path):
    manifest_file = tmp_path / "obj.json"
    manifest_file.write_text(json.dumps({"key": "value"}))
    
    with pytest.raises(ValueError, match="Manifest must be a JSON array"):
        parse_manifest(str(manifest_file))
