import pytest
from click.testing import CliRunner
from paparazzit.cli import cli
import json
import os

def test_cli_snap_no_args():
    runner = CliRunner()
    result = runner.invoke(cli, ['snap'])
    assert result.exit_code == 1
    assert "Error: You must provide either --url, --window, or --manifest." in result.output

def test_cli_scout_mocked(mocker, tmp_path):
    # Mock fetch_sitemap to avoid network calls
    mock_fetch = mocker.patch("paparazzit.cli.fetch_sitemap")
    mock_fetch.return_value = ["https://site.com/1", "https://site.com/2"]
    
    output_file = tmp_path / "manifest.json"
    
    runner = CliRunner()
    result = runner.invoke(cli, ['scout', '--url', 'https://site.com/sitemap.xml', '--output', str(output_file)])
    
    assert result.exit_code == 0
    assert f"Manifest saved to: {output_file}" in result.output
    
    # Verify content
    with open(output_file, 'r') as f:
        data = json.load(f)
    assert data == ["https://site.com/1", "https://site.com/2"]

def test_cli_scout_default_path(mocker):
    # Mock fetch_sitemap
    mock_fetch = mocker.patch("paparazzit.cli.fetch_sitemap")
    mock_fetch.return_value = ["https://site.com/1"]
    
    # Mock os.makedirs and open to avoid real filesystem side effects
    mock_makedirs = mocker.patch("paparazzit.cli.os.makedirs")
    mock_open_func = mocker.patch("paparazzit.cli.open", mocker.mock_open())
    
    runner = CliRunner()
    result = runner.invoke(cli, ['scout', '--url', 'https://site.com/sitemap.xml'])
    
    assert result.exit_code == 0
    expected_path = os.path.join("captures", "manifests", "manifest.json")
    assert f"Manifest saved to: {expected_path}" in result.output
    mock_makedirs.assert_called_with(os.path.join("captures", "manifests"), exist_ok=True)
    mock_open_func.assert_called_with(expected_path, 'w')

def test_cli_snap_manifest_lookup(mocker, tmp_path):
    # 1. Test finding manifest in captures/manifests/
    mock_parse = mocker.patch("paparazzit.cli.parse_manifest")
    mock_parse.return_value = ["https://site.com/1"]
    
    # Mock os.path.exists: first call for manifest path (False), second for default path (True)
    mock_exists = mocker.patch("paparazzit.cli.os.path.exists")
    mock_exists.side_effect = [False, True]
    
    # Mock engines and save_capture
    mocker.patch("paparazzit.cli.PlaywrightEngine")
    mocker.patch("paparazzit.cli.save_capture", return_value=("img.png", None, {}))
    mocker.patch("paparazzit.cli.os.makedirs")
    mocker.patch("paparazzit.cli.open", mocker.mock_open())
    
    runner = CliRunner()
    result = runner.invoke(cli, ['snap', '--manifest', 'my_manifest.json'])
    
    assert result.exit_code == 0
    expected_path = os.path.join("captures", "manifests", "my_manifest.json")
    assert f"Processing manifest: {expected_path}" in result.output

def test_cli_snap_manifest_not_found(mocker):
    # Mock os.path.exists: return False for both checks
    mock_exists = mocker.patch("paparazzit.cli.os.path.exists")
    mock_exists.return_value = False
    
    runner = CliRunner()
    result = runner.invoke(cli, ['snap', '--manifest', 'missing.json'])
    
    assert result.exit_code == 1
    assert "Error: Manifest file not found: missing.json" in result.output


def test_cli_scout_limit(mocker, tmp_path):
    mock_fetch = mocker.patch("paparazzit.cli.fetch_sitemap")
    mock_fetch.return_value = ["https://site.com/1", "https://site.com/2", "https://site.com/3"]
    
    output_file = tmp_path / "limit.json"
    
    runner = CliRunner()
    result = runner.invoke(cli, ['scout', '--url', 'https://site.com/sitemap.xml', '--output', str(output_file), '--limit', '2'])
    
    assert result.exit_code == 0
    assert "Limited to 2 URLs." in result.output
    
    with open(output_file, 'r') as f:
        data = json.load(f)
    assert len(data) == 2
    assert data == ["https://site.com/1", "https://site.com/2"]

def test_cli_snap_url_mocked(mocker):
    # Mock engines to avoid playwright/mss issues
    mock_pw = mocker.patch("paparazzit.cli.PlaywrightEngine")
    mock_save = mocker.patch("paparazzit.cli.save_capture")
    mock_save.return_value = ("img.png", "meta.json", {})
    
    runner = CliRunner()
    result = runner.invoke(cli, ['snap', '--url', 'https://example.com'])
    
    assert result.exit_code == 0
    assert "Capturing URL: https://example.com ..." in result.output
    assert "Capture saved successfully!" in result.output

def test_cli_snap_manifest_mocked(mocker, tmp_path):
    # Create a dummy manifest
    manifest_file = tmp_path / "manifest.json"
    manifest_file.write_text(json.dumps(["https://a.com", "https://b.com"]))
    
    mock_pw = mocker.patch("paparazzit.cli.PlaywrightEngine")
    # Mocking context manager __enter__
    mock_pw.return_value.__enter__.return_value.capture.return_value = mocker.Mock()
    
    mock_save = mocker.patch("paparazzit.cli.save_capture")
    mock_save.return_value = ("img.png", None, {"target": "mocked"})
    
    # Mock open to avoid writing the unified metadata to real captures/ dir
    # Use mocker.patch for specific modules if possible, but builtins.open is tricky.
    # Instead of patching open, let's patch the file operations in paparazzit.cli
    mocker.patch("paparazzit.cli.json.dump")
    mocker.patch("paparazzit.cli.open", mocker.mock_open(read_data=json.dumps(["https://a.com", "https://b.com"])))
    
    runner = CliRunner()
    # We need to be careful about the 'captures' dir path in the real CLI code
    # For this test, we just want to see if it processes the manifest
    result = runner.invoke(cli, ['snap', '--manifest', str(manifest_file)])
    
    assert result.exit_code == 0
    assert "Processing manifest" in result.output
    assert "Capturing URL: https://a.com ..." in result.output
    assert "Capturing URL: https://b.com ..." in result.output
    assert "Batch processing complete." in result.output
