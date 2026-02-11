import click
from paparazzit.capture.playwright_engine import PlaywrightEngine
from paparazzit.capture.mss_engine import MSSEngine
from paparazzit.utils.storage import save_capture, PROJECT_ROOT, DEFAULT_CAPTURES_DIR
from paparazzit.utils.manifest import parse_manifest
from paparazzit.utils.sitemap import fetch_sitemap
import json
import sys
import os
from urllib.parse import urlparse
import asyncio

MANIFESTS_DIR = os.path.join(PROJECT_ROOT, "captures", "manifests")

@click.group()
def cli():
    """paparazzit - A CLI tool for capturing screenshots with metadata."""
    pass

async def async_snap(url, window, manifest, wait, scroll, concurrency):
    try:
        subdir = None
        if manifest:
            # Manifest lookup logic
            manifest_path = manifest
            if not os.path.exists(manifest_path):
                # Check absolute manifest dir
                default_path = os.path.join(MANIFESTS_DIR, manifest)
                if os.path.exists(default_path):
                    manifest_path = default_path
                else:
                    click.echo(f"Error: Manifest file not found: {manifest}")
                    click.echo(f"Searched in: {os.getcwd()} and {MANIFESTS_DIR}")
                    sys.exit(1)

            subdir = os.path.basename(manifest_path).replace(".", "-")
            urls = parse_manifest(manifest_path)
            click.echo(f"Processing manifest: {manifest_path} ({len(urls)} URLs) with concurrency {concurrency}")
            
            all_metadata = []
            sem = asyncio.Semaphore(concurrency)
            
            async with PlaywrightEngine() as engine:
                async def capture_task(target_url):
                    async with sem:
                        try:
                            click.echo(f"Capturing URL: {target_url} ...")
                            image = await engine.capture(target_url, wait=wait, scroll=scroll)
                            # save_capture uses DEFAULT_CAPTURES_DIR by default
                            # save_capture is sync but it does file I/O. For now keeping it sync is okay as it's fast enough or we could wrap it.
                            # But since we are inside an async function, strictly speaking we should probably wrap it if it blocks.
                            # However, file writing is usually fast. Let's leave it sync for now unless we want to wrap it.
                            image_path, _, metadata = await asyncio.to_thread(save_capture, image, "playwright", target_url, subdir=subdir, save_json=False)
                            all_metadata.append(metadata)
                            click.echo(f"  Success: {image_path}")
                        except Exception as e:
                            click.echo(f"  Failed: {target_url} - {e}", err=True)

                tasks = [capture_task(u) for u in urls]
                await asyncio.gather(*tasks)
            
            # Save consolidated metadata
            if all_metadata:
                metadata_file = os.path.join(DEFAULT_CAPTURES_DIR, subdir, "metadata.json")
                os.makedirs(os.path.dirname(metadata_file), exist_ok=True)
                with open(metadata_file, "w") as f:
                    json.dump(all_metadata, f, indent=2)
                click.echo(f"Unified metadata saved to: {metadata_file}")
                
            click.echo("Batch processing complete.")
            return

        if url:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc or parsed_url.path.split('/')[0]
            subdir = domain.replace(".", "-")
            click.echo(f"Capturing URL: {url} ...")
            engine = PlaywrightEngine()
            # One-off capture also needs to be awaited
            image = await engine.capture(url, wait=wait, scroll=scroll)
            engine_name = "playwright"
            target = url
        else:
            subdir = "desktop"
            click.echo(f"Capturing Window: {window} ...")
            engine = MSSEngine()
            image = await engine.capture(window, wait=wait)
            engine_name = "mss"
            target = window
        
        image_path, json_path, _ = await asyncio.to_thread(save_capture, image, engine_name, target, subdir=subdir)
        click.echo(f"Capture saved successfully!")
        click.echo(f"Image: {image_path}")
        click.echo(f"Metadata: {json_path}")
        
    except Exception as e:
        click.echo(f"Error during capture: {e}", err=True)
        sys.exit(1)

@cli.command()
@click.option("--url", help="Capture a screenshot of a URL using Playwright.")
@click.option("--window", help="Capture a screenshot of a window by title using MSS.")
@click.option("--manifest", help="Capture multiple URLs from a JSON manifest file.")
@click.option("--wait", type=int, default=0, help="Additional wait time in milliseconds before capture.")
@click.option("--scroll", is_flag=True, help="Auto-scroll the page to trigger lazy-loaded resources.")
@click.option("--concurrency", "-c", type=int, default=2, help="Number of concurrent captures for manifests.")
def snap(url, window, manifest, wait, scroll, concurrency):
    """Capture a screenshot and save it with metadata."""
    if not url and not window and not manifest:
        click.echo("Error: You must provide either --url, --window, or --manifest.")
        sys.exit(1)
    
    # Security: Validate URL scheme
    if url:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            click.echo(f"Error: Invalid URL scheme '{parsed.scheme}'. Only 'http' and 'https' are supported.")
            sys.exit(1)

    asyncio.run(async_snap(url, window, manifest, wait, scroll, concurrency))

@cli.command()
@click.option("--url", required=True, help="URL of the sitemap.xml file or domain root.")
@click.option("--output", help="Output filename for the manifest (default: captures/manifests/manifest.json).")
@click.option("--limit", type=int, help="Limit the number of URLs to extract.")
@click.option("--force", is_flag=True, help="Force writing to output path even if outside project directory.")
def scout(url, output, limit, force):
    """Fetch and parse a sitemap.xml file into a JSON manifest."""
    try:
        # Default output path convention
        if output is None:
            parsed = urlparse(url)
            domain = parsed.netloc or parsed.path.split('/')[0]
            domain_slug = domain.replace(".", "-")
            output = os.path.join(MANIFESTS_DIR, f"{domain_slug}.json")
            os.makedirs(os.path.dirname(output), exist_ok=True)
        else:
            if not os.path.isabs(output) and "/" not in output and "\\" not in output:
                 output = os.path.join(MANIFESTS_DIR, output)
            
            # Security: Path Traversal Check
            abs_output = os.path.abspath(output)
            abs_root = os.path.abspath(PROJECT_ROOT)
            
            try:
                if os.path.commonpath([abs_output, abs_root]) != abs_root:
                    if not force:
                        click.echo(f"Error: Output path '{output}' is outside the project directory.")
                        click.echo("Use --force to override this safety check.")
                        sys.exit(1)
            except ValueError:
                 if not force:
                    click.echo(f"Error: Output path '{output}' is on a different drive/root than the project.")
                    click.echo("Use --force to override this safety check.")
                    sys.exit(1)

            parent = os.path.dirname(output)
            if parent:
                os.makedirs(parent, exist_ok=True)
            else:
                os.makedirs(os.path.dirname(output), exist_ok=True)

        click.echo(f"Scouting sitemap: {url} ...")
        urls = fetch_sitemap(url)
        
        if limit:
            urls = urls[:limit]
            click.echo(f"Limited to {len(urls)} URLs.")
        else:
            click.echo(f"Extracted {len(urls)} URLs.")

        with open(output, 'w') as f:
            json.dump(urls, f, indent=2)
            
        click.echo(f"Manifest saved to: {output}")
        
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error during scout: {e}", err=True)
        sys.exit(1)

@cli.command()
def doctor():
    """Check the health of the paparazzit environment."""
    click.echo("Running paparazzit health check...")
    click.echo(f"Project Root: {PROJECT_ROOT}")
    
    # 1. Check Python dependencies
    missing = []
    for dep in ["playwright", "mss", "PIL", "click", "httpx"]:
        try:
            __import__(dep)
        except ImportError:
            missing.append(dep)
    
    if not missing:
        click.echo("✅ Core dependencies found.")
    else:
        click.echo(f"❌ Missing dependencies: {', '.join(missing)}", err=True)

    # 2. Check Playwright browsers
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch()
            browser.close()
        click.echo("✅ Playwright browsers are functional.")
    except Exception as e:
        click.echo(f"❌ Playwright check failed: {e}", err=True)

    # 3. Check for capture directories
    if os.path.exists(DEFAULT_CAPTURES_DIR):
        click.echo(f"✅ Snaps directory exists: {DEFAULT_CAPTURES_DIR}")
    else:
        click.echo(f"ℹ️ Snaps directory not yet created: {DEFAULT_CAPTURES_DIR}")

    if os.path.exists(MANIFESTS_DIR):
        click.echo(f"✅ Manifests directory exists: {MANIFESTS_DIR}")
    else:
        click.echo(f"ℹ️ Manifests directory not yet created: {MANIFESTS_DIR}")

    click.echo("\nDoctor check complete. Take two of these and call me in the morning! ")

if __name__ == "__main__":
    cli()
