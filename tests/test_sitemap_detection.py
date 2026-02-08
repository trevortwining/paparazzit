import pytest
from paparazzit.utils.sitemap import fetch_sitemap
import httpx

def test_fetch_sitemap_direct_xml(mocker):
    # Setup
    url = "https://example.com/sitemap.xml"
    content = b"""<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        <url><loc>https://example.com/page1</loc></url>
    </urlset>"""
    
    # Mock httpx
    mock_get = mocker.patch("httpx.get")
    mock_get.return_value.status_code = 200
    mock_get.return_value.content = content
    mock_get.return_value.headers = {}
    
    # Execute
    urls = fetch_sitemap(url)
    
    # Verify
    mock_get.assert_called_with("https://example.com/sitemap.xml", follow_redirects=True)
    assert len(urls) == 1
    assert urls[0] == "https://example.com/page1"

def test_fetch_sitemap_domain_root(mocker):
    # Setup
    url = "https://example.com"
    content = b"""<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        <url><loc>https://example.com/root</loc></url>
    </urlset>"""
    
    # Mock httpx
    mock_get = mocker.patch("httpx.get")
    mock_get.return_value.status_code = 200
    mock_get.return_value.content = content
    mock_get.return_value.headers = {}
    
    # Execute
    urls = fetch_sitemap(url)
    
    # Verify: Should have appended /sitemap.xml
    mock_get.assert_called_with("https://example.com/sitemap.xml", follow_redirects=True)
    assert len(urls) == 1
    assert urls[0] == "https://example.com/root"

def test_fetch_sitemap_not_found(mocker):
    # Setup
    url = "https://missing.com"
    
    # Mock httpx 404
    mock_get = mocker.patch("httpx.get")
    mock_response = mocker.Mock()
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError("Not Found", request=None, response=mock_response)
    mock_get.return_value = mock_response

    # Execute & Verify
    with pytest.raises(FileNotFoundError) as excinfo:
        fetch_sitemap(url)
    
    assert "sitemap.xml not found at https://missing.com/sitemap.xml" in str(excinfo.value)
