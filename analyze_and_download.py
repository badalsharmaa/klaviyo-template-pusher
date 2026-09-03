#!/usr/bin/env python3
import os
import sys
import re
import csv
from pathlib import Path
from collections import defaultdict
from html.parser import HTMLParser
from push_template import load_environment, get_templates, get_template

def make_safe_filename(name):
    """Generate a clean, standardized filename from a template name."""
    safe = re.sub(r'[^\w\s-]', '', name).strip()
    safe = re.sub(r'[\s-]+', '_', safe)
    while "__" in safe:
        safe = safe.replace("__", "_")
    safe = safe.strip("_").lower()
    return safe or "template"

class EmailerHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.products = set()
        self.dynamic_tags = set()
        self.product_urls = set()
        self.current_tag = None
        self.current_text = []

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        attr_dict = dict(attrs)
        
        # 1. Extract image alt attributes
        if tag == 'img':
            alt = attr_dict.get('alt', '').strip()
            if alt and len(alt) > 2 and not any(ignored in alt.lower() for ignored in ['logo', 'icon', 'banner', 'footer', 'header', 'social', 'facebook', 'instagram', 'twitter']):
                self.products.add(alt)

        # 2. Extract links
        if tag == 'a':
            href = attr_dict.get('href', '')
            if '/products/' in href or 'product' in href.lower():
                match = re.search(r'/products/([a-zA-Z0-9_-]+)', href)
                if match:
                    product_slug = match.group(1).replace('-', ' ').title()
                    self.products.add(product_slug)
                else:
                    self.product_urls.add(href)

    def handle_data(self, data):
        if self.current_tag in ['h1', 'h2', 'h3', 'h4']:
            text = data.strip()
            if text and len(text) < 60 and not any(w in text.lower() for w in ['shop now', 'unsubscribe', 'welcome', 'view in browser', 'follow us']):
                self.products.add(text)

def extract_products_from_html(html_content):
    """
    Extract product details from HTML emailer content using standard library HTMLParser & regex.
    """
    parser = EmailerHTMLParser()
    try:
        parser.feed(html_content)
    except Exception:
        pass

    # Extract dynamic Klaviyo tags
    dynamic_tags = set()
    klaviyo_tags = re.findall(r'\{\{\s*([^{}]+)\s*\}\}', html_content)
    for tag in klaviyo_tags:
        tag_str = tag.strip()
        if any(term in tag_str for term in ['item', 'product', 'line_items', 'title', 'sku', 'name']):
            dynamic_tags.add(tag_str)

    return {
        "products": sorted(list(parser.products)),
        "dynamic_tags": sorted(list(dynamic_tags)),
        "product_urls": sorted(list(parser.product_urls))
    }


def main():
    load_environment()
    api_key = os.getenv("KLAVIYO_API_KEY")
    if not api_key:
        print("[!] Error: KLAVIYO_API_KEY environment variable not found.", file=sys.stderr)
        sys.exit(1)

    print("[*] Fetching 40 latest email templates from Klaviyo...")
    response = get_templates(api_key, limit=10, max_count=40)
    if response is None or response.status_code != 200:
        status = response.status_code if response else "Unknown"
        print(f"[!] Error fetching template list: {status}", file=sys.stderr)
        sys.exit(1)

    templates_list = response.json().get("data", [])[:40]
    total_found = len(templates_list)
    print(f"[+] Found {total_found} template(s) on the server to download.")

    output_dir = Path("downloaded_templates")
    output_dir.mkdir(exist_ok=True)

    template_records = []
    product_to_templates = defaultdict(list)

    for idx, item in enumerate(templates_list):
        template_id = item.get("id")
        attrs = item.get("attributes", {})
        template_name = attrs.get("name", "Untitled Template")
        updated_at = attrs.get("updated", "N/A")

        print(f"\n[{idx+1}/{total_found}] Processing '{template_name}' (ID: {template_id})...")

        detail_response = get_template(api_key, template_id)
        if detail_response is None or detail_response.status_code != 200:
            print(f"    [!] Failed to fetch template details for {template_id}.")
            continue

        try:
            detail_data = detail_response.json()
        except ValueError:
            print(f"    [!] Invalid JSON for template {template_id}.")
            continue

        detail_attrs = detail_data.get("data", {}).get("attributes", {})
        html_content = detail_attrs.get("html", "")
        if not html_content:
            print(f"    [!] No HTML content found in '{template_name}'.")
            continue

        # Standardized naming format
        safe_name = make_safe_filename(template_name)
        filename = f"{idx+1:02d}_{safe_name}_{template_id}.html"
        filepath = output_dir / filename

        filepath.write_text(html_content, encoding="utf-8")
        print(f"    [+] Saved HTML to {filepath.name}")

        # Product extraction
        extraction = extract_products_from_html(html_content)
        detected_products = extraction["products"]

        for prod in detected_products:
            product_to_templates[prod].append(template_name)

        template_records.append({
            "index": idx + 1,
            "id": template_id,
            "name": template_name,
            "filename": filename,
            "updated_at": updated_at,
            "products": detected_products,
            "dynamic_tags": extraction["dynamic_tags"],
            "product_urls": extraction["product_urls"]
        })

    # Generate Product Repetition & Production List Summary
    print("\n[*] Generating Product Usage & Repetition Analysis...")

    csv_path = Path("template_product_summary.csv")
    with open(csv_path, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Template Index", "Template ID", "Template Name", "Saved Filename", "Updated At", "Detected Products Count", "Detected Products List", "Dynamic Klaviyo Tags"])

        for rec in template_records:
            writer.writerow([
                rec["index"],
                rec["id"],
                rec["name"],
                rec["filename"],
                rec["updated_at"],
                len(rec["products"]),
                ", ".join(rec["products"]),
                ", ".join(rec["dynamic_tags"])
            ])

    # Markdown Report
    md_path = Path("template_product_summary.md")
    with open(md_path, mode="w", encoding="utf-8") as md_file:
        md_file.write("# Klaviyo Emailer Templates & Product Repetition Report\n\n")
        md_file.write(f"**Total Templates Downloaded & Analyzed**: {len(template_records)}\n\n")
        
        md_file.write("## 1. Product Usage & Repetition across Emailers\n\n")
        if product_to_templates:
            md_file.write("| Product / Item Name | Times Used | Templates Used In |\n")
            md_file.write("|---|---|---|\n")
            for prod, t_list in sorted(product_to_templates.items(), key=lambda x: len(x[1]), reverse=True):
                repetition_badge = f" ⚠️ **(Repeated in {len(t_list)} emailers)**" if len(t_list) > 1 else ""
                md_file.write(f"| **{prod}** | {len(t_list)} | {', '.join(t_list)}{repetition_badge} |\n")
        else:
            md_file.write("_No specific static product names detected in alt texts/links._\n")

        md_file.write("\n\n## 2. Downloaded Emailer List & Naming\n\n")
        md_file.write("| # | Template Name | ID | Saved Filename | Products Found | Klaviyo Dynamic Tags |\n")
        md_file.write("|---|---|---|---|---|---|\n")
        for rec in template_records:
            prods_str = ", ".join(rec["products"]) if rec["products"] else "_None_"
            tags_str = f"`{', '.join(rec['dynamic_tags'][:3])}`" if rec["dynamic_tags"] else "_None_"
            md_file.write(f"| {rec['index']} | **{rec['name']}** | `{rec['id']}` | `{rec['filename']}` | {prods_str} | {tags_str} |\n")

    print(f"[+] CSV Summary report saved to: {csv_path.resolve()}")
    print(f"[+] Markdown Report saved to: {md_path.resolve()}")

if __name__ == "__main__":
    main()
