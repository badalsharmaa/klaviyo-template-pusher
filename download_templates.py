#!/usr/bin/env python3
import os
import sys
import requests
from pathlib import Path
from push_template import load_environment, get_templates, get_template

def make_safe_filename(name):
    """Generate a clean, safe filename from a template name."""
    safe = "".join([c if (c.isalnum() or c in " -_") else "" for c in name]).strip()
    safe = safe.replace(" ", "_")
    # Collapse multiple underscores
    while "__" in safe:
        safe = safe.replace("__", "_")
    return safe or "template"

def main():
    # Load configuration
    load_environment()
    api_key = os.getenv("KLAVIYO_API_KEY")
    if not api_key:
        print("[!] Error: KLAVIYO_API_KEY environment variable not found.", file=sys.stderr)
        sys.exit(1)

    print("[*] Fetching template list from Klaviyo...")
    # Fetch templates. Limit is 10 per page, get_templates handles pagination up to 3 pages (30 templates).
    response = get_templates(api_key, limit=10)
    if response is None or response.status_code != 200:
        status = response.status_code if response else "Unknown"
        print(f"[!] Error fetching template list: {status}", file=sys.stderr)
        sys.exit(1)

    templates_list = response.json().get("data", [])
    total_found = len(templates_list)
    print(f"[+] Found {total_found} templates on the server.")

    # We want to download the 25 latest
    to_download = templates_list[:25]
    count_to_download = len(to_download)
    print(f"[*] Starting download of the {count_to_download} latest templates...")

    # Create destination directory
    output_dir = Path("downloaded_templates")
    output_dir.mkdir(exist_ok=True)
    print(f"[*] Saving templates to directory: {output_dir.resolve()}")

    successful_downloads = 0

    for idx, item in enumerate(to_download):
        template_id = item.get("id")
        attrs = item.get("attributes", {})
        template_name = attrs.get("name", "Untitled Template")
        editor_type = attrs.get("editor_type", "UNKNOWN")
        
        print(f"\n[{idx+1}/{count_to_download}] Fetching details for '{template_name}' (ID: {template_id}, Editor: {editor_type})...")
        
        detail_response = get_template(api_key, template_id)
        if detail_response is None or detail_response.status_code != 200:
            print(f"    [!] Failed to fetch template {template_id} detail.")
            continue

        try:
            detail_data = detail_response.json()
        except ValueError:
            print(f"    [!] Failed to parse JSON response for template {template_id}.")
            continue

        if "data" not in detail_data:
            print(f"    [!] Template data not found in response for template {template_id}.")
            continue

        detail_attrs = detail_data["data"].get("attributes", {})
        html_content = detail_attrs.get("html")
        if not html_content:
            print(f"    [!] Template '{template_name}' does not contain HTML content.")
            continue

        # Create safe filename
        safe_name = make_safe_filename(template_name)
        # We format filename as: index_safename_id.html (using 1-based index with zero padding)
        filename = f"{idx+1:02d}_{safe_name}_{template_id}.html"
        filepath = output_dir / filename

        try:
            filepath.write_text(html_content, encoding="utf-8")
            print(f"    [+] Saved to {filepath.name}")
            successful_downloads += 1
        except Exception as e:
            print(f"    [!] Error writing file {filepath}: {e}")

    print(f"\n[+] Download completed! Successfully downloaded {successful_downloads}/{count_to_download} templates.")
    print(f"[+] You can find the downloaded files in the '{output_dir}' directory.")

if __name__ == "__main__":
    main()
