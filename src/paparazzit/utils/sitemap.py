import httpx
import xml.etree.ElementTree as ET
import gzip
from typing import List

def fetch_sitemap(url: str) -> List[str]:
    """
    Fetches and parses a sitemap.xml (or .xml.gz) file.
    Returns a list of URLs extracted from <loc> tags.
    """
    response = httpx.get(url, follow_redirects=True)
    response.raise_for_status()
    
    content = response.content
    
    # Handle Gzipped sitemaps
    if url.endswith('.gz') or response.headers.get('content-type') == 'application/x-gzip':
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
