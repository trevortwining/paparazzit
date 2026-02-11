import pytest
import asyncio
import time
from unittest.mock import AsyncMock, MagicMock
from paparazzit.cli import async_snap

@pytest.mark.asyncio
async def test_concurrent_manifest_processing(mocker, tmp_path):
    # Setup
    urls = ["https://site.com/1", "https://site.com/2", "https://site.com/3", "https://site.com/4"]
    manifest_file = tmp_path / "manifest.json"
    import json
    manifest_file.write_text(json.dumps(urls))
    
    # Mock PlaywrightEngine
    mock_engine_cls = mocker.patch("paparazzit.cli.PlaywrightEngine")
    mock_instance = MagicMock()
    mock_engine_cls.return_value = mock_instance
    mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
    mock_instance.__aexit__ = AsyncMock(return_value=None)
    
    # Mock capture with a delay
    async def delayed_capture(url, **kwargs):
        await asyncio.sleep(0.1) # 100ms delay
        return MagicMock() # Return a mock image
    
    mock_instance.capture = AsyncMock(side_effect=delayed_capture)
    
    # Mock save_capture to be fast
    mocker.patch("paparazzit.cli.save_capture", return_value=("img.png", None, {}))
    
    # Mock OS ops
    mocker.patch("paparazzit.cli.os.makedirs")
    mocker.patch("paparazzit.cli.open", mocker.mock_open())
    mocker.patch("paparazzit.cli.json.dump")

    # Run with concurrency 4
    start_time = time.time()
    await async_snap(url=None, window=None, manifest=str(manifest_file), wait=0, scroll=False, concurrency=4)
    end_time = time.time()
    
    duration = end_time - start_time
    
    # If sequential, it would take > 0.4s (4 * 0.1s).
    # With concurrency 4, it should take slightly more than 0.1s.
    # Allow some overhead, say 0.25s.
    assert duration < 0.35, f"Expected < 0.35s, got {duration}s"
    assert mock_instance.capture.call_count == 4

@pytest.mark.asyncio
async def test_sequential_processing_limit(mocker, tmp_path):
    # Verify that concurrency=1 behaves sequentially
    urls = ["https://site.com/1", "https://site.com/2"]
    manifest_file = tmp_path / "manifest.json"
    import json
    manifest_file.write_text(json.dumps(urls))
    
    mock_engine_cls = mocker.patch("paparazzit.cli.PlaywrightEngine")
    mock_instance = MagicMock()
    mock_engine_cls.return_value = mock_instance
    mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
    mock_instance.__aexit__ = AsyncMock(return_value=None)
    
    async def delayed_capture(url, **kwargs):
        await asyncio.sleep(0.1)
        return MagicMock()
    
    mock_instance.capture = AsyncMock(side_effect=delayed_capture)
    mocker.patch("paparazzit.cli.save_capture", return_value=("img.png", None, {}))
    mocker.patch("paparazzit.cli.os.makedirs")
    mocker.patch("paparazzit.cli.open", mocker.mock_open())
    mocker.patch("paparazzit.cli.json.dump")
    
    start_time = time.time()
    await async_snap(url=None, window=None, manifest=str(manifest_file), wait=0, scroll=False, concurrency=1)
    end_time = time.time()
    
    duration = end_time - start_time
    # Sequential: 2 * 0.1s = 0.2s + overhead. Should be > 0.2s.
    assert duration >= 0.2, f"Expected >= 0.2s, got {duration}s"
