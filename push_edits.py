#!/usr/bin/env python3
import os
import sys
import argparse
from pathlib import Path
from push_template import load_environment, push_template, get_template

def parse_template_id_from_filename(filename):
    """
    Extracts the template ID from the filename.
    Filename pattern is assumed to be: XX_safename_TEMPLATEID.html
    """
    name_without_ext = Path(filename).stem
    parts = name_without_ext.split("_")
    if len(parts) >= 3:
        # The template ID is the last part
        return parts[-1]
    return None

def main():
    parser = argparse.ArgumentParser(
        description="Push edited HTML templates back to Klaviyo."
    )
    parser.add_argument(
        "file",
        type=str,
        help="Path to the edited HTML template file (e.g. downloaded_templates/01_16_Jun_5_WpuUgk.html)"
    )
    parser.add_argument(
        "--name", "-n",
        type=str,
        default=None,
        help="New name for the template (optional, defaults to current name in Klaviyo)"
    )
    args = parser.parse_args()

    # Load environment configuration
    load_environment()
    api_key = os.getenv("KLAVIYO_API_KEY")
    if not api_key:
        print("[!] Error: KLAVIYO_API_KEY environment variable not found.", file=sys.stderr)
        sys.exit(1)

    file_path = Path(args.file)
    if not file_path.exists():
        print(f"[!] Error: File not found at {file_path.resolve()}", file=sys.stderr)
        sys.exit(1)

    # 1. Parse template ID from the filename
    template_id = parse_template_id_from_filename(file_path.name)
    if not template_id:
        print(f"[!] Error: Could not determine template ID from filename '{file_path.name}'.")
        print("    Expected format: XX_safename_TEMPLATEID.html", file=sys.stderr)
        sys.exit(1)

    print(f"[*] Identified Template ID: {template_id}")

    # 2. Fetch the current name of the template from Klaviyo if not overridden
    template_name = args.name
    if not template_name:
        print(f"[*] Fetching current template details from Klaviyo for ID: {template_id}...")
        get_res = get_template(api_key, template_id)
        if get_res and get_res.status_code == 200:
            try:
                data = get_res.json()
                template_name = data.get("data", {}).get("attributes", {}).get("name")
                print(f"    [+] Current template name: '{template_name}'")
            except Exception:
                pass
        
        if not template_name:
            # Fallback if fetch fails
            template_name = "Updated Email Template"
            print(f"    [!] Warning: Could not fetch template name from Klaviyo. Defaulting to: '{template_name}'")

    # 3. Read the edited HTML content
    try:
        html_content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"[!] Error reading HTML file: {e}", file=sys.stderr)
        sys.exit(1)

    if not html_content.strip():
        print("[!] Error: HTML file is empty.", file=sys.stderr)
        sys.exit(1)

    # 4. Push template update to Klaviyo
    print(f"[*] Pushing updates for template ID: {template_id}...")
    response = push_template(
        api_key=api_key,
        template_name=template_name,
        html_content=html_content,
        template_id=template_id
    )

    if response is None:
        print("[!] Error: Network request failed.", file=sys.stderr)
        sys.exit(2)

    print(f"\nResponse Status Code: {response.status_code}")
    try:
        response_data = response.json()
    except ValueError:
        response_data = None

    if response.status_code == 200:
        print("[+] Template updated successfully on Klaviyo!")
        if response_data and "data" in response_data:
            t_data = response_data["data"]
            print(f"    - ID: {t_data.get('id')}")
            print(f"    - Name: {t_data.get('attributes', {}).get('name')}")
            print(f"    - Access templates here: https://www.klaviyo.com/templates")
    else:
        print("[!] Error: Failed to update template.", file=sys.stderr)
        if response_data:
            errors = response_data.get("errors", [])
            for error in errors:
                print(f"    - Detail: {error.get('detail')}")
        else:
            print(f"    - Response: {response.text}")
        sys.exit(3)

if __name__ == "__main__":
    main()
