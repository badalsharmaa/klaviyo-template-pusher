#!/usr/bin/env python3
import os
import re
from pathlib import Path

# The 10 templates to modify
TEMPLATES = [
    "01_16_Jun_5_WpuUgk.html",
    "06_13_Jul_4_XayhtJ.html",
    "07_not_reviewed_13_Jul_3_XNZ6cw.html",
    "08_not_reviewed_8_Jul_2_Rm2Bud.html",
    "09_not_reviewed_8_Jul_1_UfDPDj.html",
    "11_not_reviewed_29_Jun_9_UvtLqg.html",
    "13_22_Jun_7_U5hDGi.html",
    "14_not_reviewed_16_Jun_6_Yg5y5j.html",
    "15_not_reviewed_12_Junu_4_UUYCfN.html",
    "16_not_reviewed_12_Junu_3_Y3uBiz.html"
]

def modify_structure_a(content):
    """
    Concept 8 Design (stacked icon/text inside badge-inner-table)
    Found in: 01_16_Jun_5_WpuUgk.html
    """
    # Regex to find each badge-inner-table and its content
    # We want to keep only the img tag, wrapped in a single centered td.
    pattern = re.compile(
        r'(<table[^>]*class="badge-inner-table"[^>]*>)(.*?)(</table>)',
        re.DOTALL
    )
    
    def replacer(match):
        table_start = match.group(1)
        inner_content = match.group(2)
        table_end = match.group(3)
        
        # Search for img tag inside
        img_match = re.search(r'(<img[^>]+>)', inner_content)
        if img_match:
            img_tag = img_match.group(1)
            # Ensure img style has margin: 0 auto;
            if 'style="' in img_tag:
                # Add margin: 0 auto; if not already present
                if 'margin:0 auto' not in img_tag and 'margin: 0 auto' not in img_tag:
                    img_tag = img_tag.replace('style="', 'style="margin:0 auto; ')
            
            new_inner = (
                "\n                      <tr>\n"
                "                        <td align=\"center\" class=\"badge-icon-td\" style=\"display: block; width: 100%; font-size: 0; line-height: 0;\" valign=\"middle\">\n"
                f"                          {img_tag}\n"
                "                        </td>\n"
                "                      </tr>\n"
            )
            return f"{table_start}{new_inner}{table_end}"
        return match.group(0)

    return pattern.sub(replacer, content)

def modify_structure_b(content):
    """
    Horizontal Strip (side-by-side icon/text in badge-inner-table)
    Found in: 06, 14, 16
    """
    # Pattern to match the table and keep only the img tag in a centered cell
    pattern = re.compile(
        r'(<table[^>]*class="badge-inner-table"[^>]*>)(.*?)(</table>)',
        re.DOTALL
    )
    
    def replacer(match):
        table_start = match.group(1)
        inner_content = match.group(2)
        table_end = match.group(3)
        
        img_match = re.search(r'(<img[^>]+>)', inner_content)
        if img_match:
            img_tag = img_match.group(1)
            # Ensure it is centered
            if 'style="' in img_tag:
                if 'margin:0 auto' not in img_tag and 'margin: 0 auto' not in img_tag:
                    img_tag = img_tag.replace('style="', 'style="margin: 0 auto; ')
            
            new_inner = (
                "\n                      <tr>\n"
                "                        <td align=\"center\" class=\"badge-icon-td\" style=\"text-align: center;\" valign=\"middle\">\n"
                f"                          {img_tag}\n"
                "                        </td>\n"
                "                      </tr>\n"
            )
            return f"{table_start}{new_inner}{table_end}"
        return match.group(0)

    return pattern.sub(replacer, content)

def modify_structure_c(content):
    """
    Grid Layout (side-by-side inside width="50%" table cells)
    Found in: 07, 08, 09, 11, 13
    """
    # We find table structures inside width="50%" td elements under the trust badges section.
    # To be safe, we can match tables containing the trust badge images
    # (Price_match.png, 100_Trusted_Brands.png, Shipping.png, Customer_Quality.png)
    # and having a two-column tr structure.
    
    # We target tables nested in td width="50%" containing Price_match, 100_Trusted_Brands, Shipping, Customer_Quality
    pattern = re.compile(
        r'(<td[^>]*width="50%"[^>]*>\s*<table[^>]*role="presentation"[^>]*>)(.*?)(</table>\s*</td>)',
        re.DOTALL
    )
    
    def replacer(match):
        table_start = match.group(1)
        inner_content = match.group(2)
        table_end = match.group(3)
        
        # Check if it has any of our badge images
        if any(img in inner_content for img in ["Price_match.png", "100_Trusted_Brands.png", "Shipping.png", "Customer_Quality.png"]):
            img_match = re.search(r'(<img[^>]+>)', inner_content)
            if img_match:
                img_tag = img_match.group(1)
                
                # Make sure the image has display:block and margin:0 auto in style
                if 'style="' in img_tag:
                    # Update style to include margin:0 auto; display:block;
                    style_pat = re.compile(r'style="([^"]*)"')
                    style_match = style_pat.search(img_tag)
                    if style_match:
                        style_str = style_match.group(1)
                        if 'margin:0 auto' not in style_str and 'margin: 0 auto' not in style_str:
                            style_str += '; margin: 0 auto'
                        if 'display:block' not in style_str and 'display: block' not in style_str:
                            style_str += '; display: block'
                        # Clean up formatting
                        style_str = style_str.replace(';;', ';').strip()
                        img_tag = style_pat.sub(f'style="{style_str}"', img_tag)
                else:
                    img_tag = img_tag.replace('src=', 'style="display:block; margin:0 auto;" src=')
                
                new_inner = (
                    "\n                              <tr>\n"
                    "                                <td align=\"center\" valign=\"middle\" style=\"text-align: center;\">\n"
                    f"                                  {img_tag}\n"
                    "                                </td>\n"
                    "                              </tr>\n"
                )
                return f"{table_start}{new_inner}{table_end}"
        return match.group(0)

    return pattern.sub(replacer, content)

def modify_structure_d(content):
    """
    Vertical Card Layout (inside trust-card-table with tr.badge-row and tr.badge-divider)
    Found in: 15_not_reviewed_12_Junu_4_UUYCfN.html
    """
    # 1. Update tr class="badge-row" to remove the text td
    row_pattern = re.compile(
        r'(<tr[^>]*class="badge-row"[^>]*>)(.*?)(</tr>)',
        re.DOTALL
    )
    
    def row_replacer(match):
        tr_start = match.group(1)
        inner_content = match.group(2)
        tr_end = match.group(3)
        
        # Find first td (icon td)
        td_match = re.search(r'(<td[^>]*>.*?</td>)', inner_content, re.DOTALL)
        if td_match:
            icon_td = td_match.group(1)
            # Remove any width="45" or width constraints from the td style to let it occupy full width
            icon_td = re.sub(r'width="\d+"', '', icon_td)
            icon_td = re.sub(r'width:\s*\d+px;?', '', icon_td)
            return f"{tr_start}\n                                  {icon_td}\n                                {tr_end}"
        return match.group(0)
    
    content = row_pattern.sub(row_replacer, content)
    
    # 2. Update tr class="badge-divider" to remove colspan="2"
    content = content.replace('colspan="2"', '')
    content = content.replace('colspan=2', '')
    
    return content

def main():
    templates_dir = Path("downloaded_templates")
    
    print("[*] Modifying trust badges for the 10 specified templates...")
    
    modified_count = 0
    
    for filename in TEMPLATES:
        filepath = templates_dir / filename
        if not filepath.exists():
            print(f"[!] Warning: File not found {filepath}")
            continue
            
        print(f"[*] Processing {filename}...")
        try:
            content = filepath.read_text(encoding="utf-8")
            
            # Determine modification function based on filename
            if filename == "01_16_Jun_5_WpuUgk.html":
                modified_content = modify_structure_a(content)
            elif filename in ["06_13_Jul_4_XayhtJ.html", "14_not_reviewed_16_Jun_6_Yg5y5j.html", "16_not_reviewed_12_Junu_3_Y3uBiz.html"]:
                modified_content = modify_structure_b(content)
            elif filename in ["07_not_reviewed_13_Jul_3_XNZ6cw.html", "08_not_reviewed_8_Jul_2_Rm2Bud.html", "09_not_reviewed_8_Jul_1_UfDPDj.html", "11_not_reviewed_29_Jun_9_UvtLqg.html", "13_22_Jun_7_U5hDGi.html"]:
                modified_content = modify_structure_c(content)
            elif filename == "15_not_reviewed_12_Junu_4_UUYCfN.html":
                modified_content = modify_structure_d(content)
            else:
                print(f"    [!] Error: No modifier for {filename}")
                continue
                
            filepath.write_text(modified_content, encoding="utf-8")
            print(f"    [+] Saved modifications to {filename}")
            modified_count += 1
            
        except Exception as e:
            print(f"    [!] Error processing {filename}: {e}")

    print(f"\n[+] Completed! Modified {modified_count}/10 templates.")

if __name__ == "__main__":
    main()
