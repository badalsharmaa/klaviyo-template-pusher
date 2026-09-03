#!/usr/bin/env python3
import os
import sys
import argparse
import requests
from pathlib import Path
from dotenv import load_dotenv

# API Config
API_URL = "https://a.klaviyo.com/api/templates/"
DEFAULT_REVISION = "2026-04-15"

def load_environment():
    """Load configuration from local project .env or home directory .env."""
    # 1. Load from current working directory
    load_dotenv()
    
    # 2. Fallback to user home directory
    home_env = Path.home() / '.env'
    if home_env.exists():
        load_dotenv(dotenv_path=home_env)

def get_templates(api_key, revision=DEFAULT_REVISION, sort="-updated", limit=10, max_count=50):
    """
    Fetch existing email templates from Klaviyo.
    Supports sequential pagination following next links up to max_count templates.
    """
    headers = {
        "Authorization": f"Klaviyo-API-Key {api_key}",
        "revision": revision,
        "Accept": "application/vnd.api+json"
    }
    url = f"{API_URL}?sort={sort}&page[size]={limit}"
    all_data = []

    try:
        current_url = url
        while current_url and len(all_data) < max_count:
            response = requests.get(current_url, headers=headers)
            if response.status_code != 200:
                if not all_data:
                    return response
                break

            response_data = response.json()
            items = response_data.get("data", [])
            all_data.extend(items)

            if len(all_data) >= max_count:
                all_data = all_data[:max_count]
                break

            current_url = response_data.get("links", {}).get("next")

        class UnifiedResponse:
            def __init__(self, status_code, data_dict):
                self.status_code = status_code
                self._data = data_dict
            def json(self):
                return self._data

        return UnifiedResponse(200, {"data": all_data})

    except requests.exceptions.RequestException as e:
        print(f"[!] Network error fetching templates: {e}", file=sys.stderr)
        return None

def get_template(api_key, template_id, revision=DEFAULT_REVISION):
    """
    Fetch a single template's details from Klaviyo.
    """
    headers = {
        "Authorization": f"Klaviyo-API-Key {api_key}",
        "revision": revision,
        "Accept": "application/vnd.api+json"
    }
    url = f"{API_URL}{template_id}/"
    try:
        response = requests.get(url, headers=headers)
        return response
    except requests.exceptions.RequestException as e:
        print(f"[!] Network error fetching template {template_id}: {e}", file=sys.stderr)
        return None

def push_template(api_key, template_name, html_content, template_id=None, revision=DEFAULT_REVISION):
    """
    Push HTML content to Klaviyo's Template section.
    Creates a new template if template_id is None, otherwise updates the existing one.
    """
    headers = {
        "Authorization": f"Klaviyo-API-Key {api_key}",
        "revision": revision,
        "Content-Type": "application/vnd.api+json",
        "Accept": "application/vnd.api+json"
    }

    # Base payload structure (without editor_type)
    payload = {
        "data": {
            "type": "template",
            "attributes": {
                "name": template_name,
                "html": html_content
            }
        }
    }

    try:
        if template_id:
            # For PATCH requests, Klaviyo requires the template ID in the body data object as well.
            # Do NOT include editor_type in attributes since it is immutable.
            payload["data"]["id"] = template_id
            url = f"{API_URL}{template_id}/"
            print(f"[*] Sending PATCH request to update template ID: {template_id}...")
            response = requests.patch(url, json=payload, headers=headers)
        else:
            # Include editor_type only for POST requests (new creations)
            payload["data"]["attributes"]["editor_type"] = "CODE"
            print(f"[*] Sending POST request to create new template: '{template_name}'...")
            response = requests.post(API_URL, json=payload, headers=headers)
        
        return response
    except requests.exceptions.RequestException as e:
        print(f"[!] Network error occurred: {e}", file=sys.stderr)
        return None

def main():
    parser = argparse.ArgumentParser(
        description="Push an HTML email template to Klaviyo."
    )
    parser.add_argument(
        "--html", "-f",
        type=str,
        default="template.html",
        help="Path to the HTML email template file (default: template.html)"
    )
    parser.add_argument(
        "--name", "-n",
        type=str,
        default="HTML Email Template",
        help="Name of the template in Klaviyo (default: HTML Email Template)"
    )
    parser.add_argument(
        "--template-id", "-t",
        type=str,
        default=None,
        help="Template ID to update (performs a PATCH request instead of creating a new one)"
    )
    parser.add_argument(
        "--revision", "-r",
        type=str,
        default=DEFAULT_REVISION,
        help=f"Klaviyo API revision date (default: {DEFAULT_REVISION})"
    )
    args = parser.parse_args()

    # Load environment variables
    load_environment()
    
    api_key = os.getenv("KLAVIYO_API_KEY")
    if not api_key:
        print("[!] Error: KLAVIYO_API_KEY environment variable not found.", file=sys.stderr)
        print("Please check your .env file or run the setup command to add your key.", file=sys.stderr)
        sys.exit(1)

    # Read HTML content
    html_path = Path(args.html)
    if not html_path.exists():
        print(f"[!] Error: HTML file not found at {html_path.resolve()}", file=sys.stderr)
        sys.exit(1)
        
    try:
        html_content = html_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"[!] Error reading HTML file: {e}", file=sys.stderr)
        sys.exit(1)

    # Perform API Request
    response = push_template(
        api_key=api_key,
        template_name=args.name,
        html_content=html_content,
        template_id=args.template_id,
        revision=args.revision
    )

    if response is None:
        sys.exit(2)

    # Print results
    print(f"\nResponse Status Code: {response.status_code}")
    
    try:
        response_data = response.json()
    except ValueError:
        response_data = None

    if response.status_code in (201, 200):
        if response.status_code == 201:
            print("[+] Template created successfully!")
        else:
            print("[+] Template updated successfully!")
            
        if response_data and "data" in response_data:
            template_info = response_data["data"]
            tid = template_info.get("id")
            attributes = template_info.get("attributes", {})
            tname = attributes.get("name")
            print(f"    - ID: {tid}")
            print(f"    - Name: {tname}")
            print(f"    - Access templates here: https://www.klaviyo.com/templates")
        else:
            print(f"[?] Request succeeded, but response format was unexpected: {response.text}")
    else:
        print("[!] Error: Request failed.")
        print(f"    Status: {response.status_code}")
        if response_data:
            # Attempt to extract error messages from JSON api response
            errors = response_data.get("errors", [])
            for error in errors:
                print(f"    - Error Detail: {error.get('detail')}")
        else:
            print(f"    - Response: {response.text}")
        sys.exit(3)

if __name__ == "__main__":
    main()
