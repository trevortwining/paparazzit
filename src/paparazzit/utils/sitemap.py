import httpx
import defusedxml.ElementTree as ET
import gzip
from typing import List
from urllib.parse import urljoin, urlparse

def fetch_sitemap(url: str) -> List[str]:
    """
    Fetches and parses a sitemap.xml (or .xml.gz) file.
    If a domain root is provided (e.g., https://example.com), 
    it automatically checks for /sitemap.xml.
    Returns a list of URLs extracted from <loc> tags.
    """
    
    # 1. Resolve URL
    sitemap_url = url
    parsed = urlparse(url)
    
    # If path is empty or just "/", assume domain root and append sitemap.xml
    if not parsed.path or parsed.path == "/":
        sitemap_url = urljoin(url, "sitemap.xml")
    elif not url.endswith('.xml') and not url.endswith('.xml.gz'):
         # If path exists but doesn't look like an XML file, check if it's a directory
         # that might contain a sitemap? For now, stick to the spec: 
         # "If not ending in .xml, treat as domain root/base and append"
         # But maybe user provided "example.com/blog/"? 
         # Spec implies: "If not ends in .xml ... automatically append /sitemap.xml"
         # Let's use a slightly smarter heuristic: 
         if not parsed.path.endswith('.xml') and not parsed.path.endswith('.gz'):
             sitemap_url = urljoin(url if url.endswith('/') else url + '/', "sitemap.xml")

    # 2. Check Existence (HEAD request or GET if server forbids HEAD)
    try:
        response = httpx.get(sitemap_url, follow_redirects=True)
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
             raise FileNotFoundError(f"sitemap.xml not found at {sitemap_url}")
        raise e
    except httpx.RequestError as e:
        raise ConnectionError(f"Failed to connect to {sitemap_url}: {e}")
    
    content = response.content
    
    # Handle Gzipped sitemaps
    if sitemap_url.endswith('.gz') or response.headers.get('content-type') == 'application/x-gzip':
        try:
            content = gzip.decompress(content)
        except Exception as e:
            # If decompression fails, maybe it's not actually gzipped
            pass
            
    return parse_sitemap_xml(content)

def parse_sitemap_xml(xml_content: bytes) -> List[str]:
    """
    Parses XML content and extracts URLs from <loc> tags.
    Handles namespaces commonly found in sitemaps.
    Uses defusedxml to prevent XXE attacks.
    """
    try:
        root = ET.fromstring(xml_content)
    except ET.ParseError as e:
        raise ValueError(f"Failed to parse sitemap XML: {e}")

    # Sitemaps usually have a namespace: http://www.sitemaps.org/schemas/sitemap/0.9
    # We can use wildcard or explicit namespace handling
    urls = []
    
    # NEW LOGIC: Strictly look for <url><loc> to avoid sitemap index and image locs
    for loc in root.findall(".//{*}url/{*}loc"):
        if loc.text:
            urls.append(loc.text.strip())
            
    return urls
