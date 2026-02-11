import pytest
from click.testing import CliRunner
from paparazzit.cli import cli, MANIFESTS_DIR
import json
import os
import asyncio
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def mock_playwright_engine(mocker):
    # Mock PlaywrightEngine class
    mock_engine_cls = mocker.patch("paparazzit.cli.PlaywrightEngine")
    
    # Create a mock instance
    mock_instance = MagicMock()
    
    # Make __aenter__ return the instance (async)
    mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
    mock_instance.__aexit__ = AsyncMock(return_value=None)
    
    # Make capture an async method
    mock_instance.capture = AsyncMock()
    
    # Make the class return this instance
    mock_engine_cls.return_value = mock_instance
    return mock_instance

@pytest.fixture
def mock_mss_engine(mocker):
    mock_engine_cls = mocker.patch("paparazzit.cli.MSSEngine")
    mock_instance = MagicMock()
    mock_instance.capture = AsyncMock()
    mock_engine_cls.return_value = mock_instance
    return mock_instance

def test_cli_snap_no_args():
    runner = CliRunner()
    result = runner.invoke(cli, ['snap'])
    assert result.exit_code == 1
    assert "Error: You must provide either --url, --window, or --manifest." in result.output

def test_cli_scout_mocked(mocker, tmp_path):
    # Mock PROJECT_ROOT to allow writing to tmp_path
    mocker.patch("paparazzit.cli.PROJECT_ROOT", str(tmp_path))

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

def test_cli_snap_url_mocked(mock_playwright_engine, mocker):
    mock_save = mocker.patch("paparazzit.cli.save_capture")
    mock_save.return_value = ("img.png", "meta.json", {})
    
    runner = CliRunner()
    result = runner.invoke(cli, ['snap', '--url', 'https://example.com'])
    
    assert result.exit_code == 0
    assert "Capturing URL: https://example.com ..." in result.output
    assert "Capture saved successfully!" in result.output
    
    # Check if capture was called
    mock_playwright_engine.capture.assert_called_with('https://example.com', wait=0, scroll=False)

def test_cli_snap_url_wait_flag(mock_playwright_engine, mocker):
    mock_save = mocker.patch("paparazzit.cli.save_capture")
    mock_save.return_value = ("img.png", "meta.json", {})
    
    runner = CliRunner()
    # Test --wait flag
    result = runner.invoke(cli, ['snap', '--url', 'https://example.com', '--wait', '2000'])
    
    assert result.exit_code == 0
    # Verify capture was called with the wait parameter
    mock_playwright_engine.capture.assert_called_with('https://example.com', wait=2000, scroll=False)

def test_cli_snap_url_scroll_flag(mock_playwright_engine, mocker):
    mock_save = mocker.patch("paparazzit.cli.save_capture")
    mock_save.return_value = ("img.png", "meta.json", {})
    
    runner = CliRunner()
    # Test --scroll flag
    result = runner.invoke(cli, ['snap', '--url', 'https://example.com', '--scroll'])
    
    assert result.exit_code == 0
    # Verify capture was called with the scroll parameter
    mock_playwright_engine.capture.assert_called_with('https://example.com', wait=0, scroll=True)

def test_cli_snap_manifest_mocked(mock_playwright_engine, mocker, tmp_path):
    # Create a dummy manifest
    manifest_file = tmp_path / "manifest.json"
    manifest_file.write_text(json.dumps(["https://a.com", "https://b.com"]))
    
    mock_save = mocker.patch("paparazzit.cli.save_capture")
    mock_save.return_value = ("img.png", None, {"target": "mocked"})
    
    runner = CliRunner()
    # Invoke
    result = runner.invoke(cli, ['snap', '--manifest', str(manifest_file)])
    
    assert result.exit_code == 0
    assert "Processing manifest" in result.output
    # Check for both URLs
    assert "Capturing URL: https://a.com ..." in result.output
    assert "Capturing URL: https://b.com ..." in result.output
    assert "Batch processing complete." in result.output
    
    # Check calls
    assert mock_playwright_engine.capture.call_count == 2

def test_cli_snap_window(mock_mss_engine, mocker):
    mock_save = mocker.patch("paparazzit.cli.save_capture")
    mock_save.return_value = ("img.png", "meta.json", {})
    
    runner = CliRunner()
    result = runner.invoke(cli, ['snap', '--window', 'My Window'])
    
    assert result.exit_code == 0
    mock_mss_engine.capture.assert_called_with('My Window', wait=0)

def test_cli_snap_concurrency(mock_playwright_engine, mocker, tmp_path):
    # This test verifies that the concurrency flag is accepted and used.
    # To truly test concurrency, we'd need a delay in capture and check timing, 
    # but for CLI unit test, just checking it runs without error is a good start.
    manifest_file = tmp_path / "manifest.json"
    manifest_file.write_text(json.dumps(["https://a.com", "https://b.com", "https://c.com"]))
    
    mock_save = mocker.patch("paparazzit.cli.save_capture")
    mock_save.return_value = ("img.png", None, {"target": "mocked"})
    
    runner = CliRunner()
    result = runner.invoke(cli, ['snap', '--manifest', str(manifest_file), '--concurrency', '3'])
    
    assert result.exit_code == 0
    assert "with concurrency 3" in result.output
