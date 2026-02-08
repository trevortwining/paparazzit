import click
from paparazzit.capture.playwright_engine import PlaywrightEngine
from paparazzit.capture.mss_engine import MSSEngine
from paparazzit.utils.storage import save_capture
from paparazzit.utils.manifest import parse_manifest
from paparazzit.utils.sitemap import fetch_sitemap
import json
import sys
import os
from urllib.parse import urlparse

@click.group()
def cli():
    """paparazzit - A CLI tool for capturing screenshots with metadata."""
    pass

@cli.command()
@click.option("--url", help="Capture a screenshot of a URL using Playwright.")
@click.option("--window", help="Capture a screenshot of a window by title using MSS.")
@click.option("--manifest", help="Capture multiple URLs from a JSON manifest file.")
def snap(url, window, manifest):
    """Capture a screenshot and save it with metadata."""
    if not url and not window and not manifest:
        click.echo("Error: You must provide either --url, --window, or --manifest.")
        sys.exit(1)
    
    try:
        subdir = None
        if manifest:
            # Manifest lookup logic
            manifest_path = manifest
            if not os.path.exists(manifest_path):
                default_path = os.path.join("captures", "manifests", manifest)
                if os.path.exists(default_path):
                    manifest_path = default_path
                else:
                    click.echo(f"Error: Manifest file not found: {manifest}")
                    sys.exit(1)

            subdir = os.path.basename(manifest_path).replace(".", "-")
            urls = parse_manifest(manifest_path)
            click.echo(f"Processing manifest: {manifest_path} ({len(urls)} URLs)")
            
            all_metadata = []
            with PlaywrightEngine() as engine:
                for target_url in urls:
                    try:
                        click.echo(f"Capturing URL: {target_url} ...")
                        image = engine.capture(target_url)
                        image_path, _, metadata = save_capture(image, "playwright", target_url, subdir=subdir, save_json=False)
                        all_metadata.append(metadata)
                        click.echo(f"  Success: {image_path}")
                    except Exception as e:
                        click.echo(f"  Failed: {target_url} - {e}", err=True)
            
            # Save consolidated metadata
            if all_metadata:
                metadata_file = os.path.join("captures", subdir, "metadata.json")
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
            image = engine.capture(url)
            engine_name = "playwright"
            target = url
        else:
            subdir = "desktop"
            click.echo(f"Capturing Window: {window} ...")
            engine = MSSEngine()
            image = engine.capture(window)
            engine_name = "mss"
            target = window
        
        image_path, json_path, _ = save_capture(image, engine_name, target, subdir=subdir)
        click.echo(f"Capture saved successfully!")
        click.echo(f"Image: {image_path}")
        click.echo(f"Metadata: {json_path}")
        
    except Exception as e:
        click.echo(f"Error during capture: {e}", err=True)
        sys.exit(1)

@cli.command()
@click.option("--url", required=True, help="URL of the sitemap.xml file.")
@click.option("--output", help="Output filename for the manifest (default: captures/manifests/manifest.json).")
@click.option("--limit", type=int, help="Limit the number of URLs to extract.")
def scout(url, output, limit):
    """Fetch and parse a sitemap.xml file into a JSON manifest."""
    try:
        # Default output path convention
        if output is None:
            output_dir = os.path.join("captures", "manifests")
            os.makedirs(output_dir, exist_ok=True)
            output = os.path.join(output_dir, "manifest.json")
        else:
            # If user provides a path, ensure parent directory exists
            parent = os.path.dirname(output)
            if parent:
                os.makedirs(parent, exist_ok=True)

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
        
    except Exception as e:
        click.echo(f"Error during scout: {e}", err=True)
        sys.exit(1)

@cli.command()
def doctor():
    """Check the health of the paparazzit environment."""
    click.echo("Running paparazzit health check...")
    
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

    # 3. Check for capture directory
    if os.path.exists("captures"):
        click.echo("✅ 'captures' directory exists.")
    else:
        click.echo("ℹ️ 'captures' directory not yet created (this is normal if no snaps have been taken).")

    # 4. Check for pre-commit hooks
    if os.path.exists(".git/hooks/pre-commit"):
        click.echo("✅ Git pre-commit hooks are installed.")
    else:
        click.echo("❌ Git pre-commit hooks are NOT installed.")

    click.echo("\nDoctor check complete. Take two of these and call me in the morning! ")

if __name__ == "__main__":
    cli()
