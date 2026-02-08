import httpx
import pytest
from paparazzit.utils.sitemap import fetch_sitemap

def test_parse_sitemap_xml_basic():
    from paparazzit.utils.sitemap import parse_sitemap_xml
    xml = b"""<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
       <url>
          <loc>http://www.example.com/</loc>
          <lastmod>2005-01-01</lastmod>
       </url>
       <url>
          <loc>http://www.example.com/about</loc>
       </url>
    </urlset>"""
    urls = parse_sitemap_xml(xml)
    assert urls == ["http://www.example.com/", "http://www.example.com/about"]

def test_fetch_sitemap_mocked(mocker):
    mock_get = mocker.patch("httpx.get")
    mock_response = mocker.Mock()
    mock_response.content = b"""<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
       <url><loc>https://test.com/1</loc></url>
    </urlset>"""
    mock_response.headers = {"content-type": "text/xml"}
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    urls = fetch_sitemap("https://test.com/sitemap.xml")
    assert urls == ["https://test.com/1"]
    mock_get.assert_called_once_with("https://test.com/sitemap.xml", follow_redirects=True)

def test_fetch_sitemap_gzipped(mocker):
    import gzip
    mock_get = mocker.patch("httpx.get")
    
    xml_content = b"""<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
       <url><loc>https://test.com/gz</loc></url>
    </urlset>"""
    gz_content = gzip.compress(xml_content)
    
    mock_response = mocker.Mock()
    mock_response.content = gz_content
    mock_response.headers = {"content-type": "application/x-gzip"}
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    urls = fetch_sitemap("https://test.com/sitemap.xml.gz")
    assert urls == ["https://test.com/gz"]
