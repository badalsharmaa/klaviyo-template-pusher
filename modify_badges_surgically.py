#!/usr/bin/env python3
import sys
from pathlib import Path

# Mapping of filename -> (start_token, end_token, new_block_content)
MODIFICATIONS = {
    # 1. Concept 8 Design (Stacked style card)
    "01_16_Jun_5_WpuUgk.html": (
        "<!-- 4. TRUST BADGES WHITE CARD (CONCEPT 8 DESIGN) -->",
        "<!-- 5. CONVECTION OVENS SECTION -->",
        """<table bgcolor="#FAF8F5" border="0" cellpadding="0" cellspacing="0" class="wrapper" role="presentation" style="width:600px; max-width:600px;" width="600">
<tr>
<td style="padding: 0px 15px 15px 15px;">
<table bgcolor="#FFFFFF" border="0" cellpadding="0" cellspacing="0" role="presentation" style="background-color: #FFFFFF; border: 1px solid #E2DCC8; border-radius: 8px;" width="100%">
<tr>
<td class="badges-container-td" style="padding: 12px 8px;">
<table border="0" cellpadding="0" cellspacing="0" class="badges-table" role="presentation" width="100%">
<tr>
<!-- Price Match -->
<td align="center" class="badge-col" style="padding: 4px 2px; text-align: center;" valign="middle" width="25%">
<img alt="Price Match" class="badge-icon-img" height="50" src="https://cf-images.hiraya.digital/emails/17-mar-cf/images/Price_match.png" style="display:block; border:0; width:50px; height:50px; margin:0 auto;" width="50"/>
</td>
<!-- 100+ Brands -->
<td align="center" class="badge-col" style="padding: 4px 2px; text-align: center; border-left: 1px solid #E2DCC8;" valign="middle" width="25%">
<img alt="Trusted Brands" class="badge-icon-img" height="50" src="https://cf-images.hiraya.digital/emails/17-mar-cf/images/100_Trusted_Brands.png" style="display:block; border:0; width:50px; height:50px; margin:0 auto;" width="50"/>
</td>
<!-- Fast Shipping -->
<td align="center" class="badge-col" style="padding: 4px 2px; text-align: center; border-left: 1px solid #E2DCC8;" valign="middle" width="25%">
<img alt="Fast Shipping" class="badge-icon-img" height="50" src="https://cf-images.hiraya.digital/emails/17-mar-cf/images/Shipping.png" style="display:block; border:0; width:50px; height:50px; margin:0 auto;" width="50"/>
</td>
<!-- Customer Quality -->
<td align="center" class="badge-col" style="padding: 4px 2px; text-align: center; border-left: 1px solid #E2DCC8;" valign="middle" width="25%">
<img alt="Quality Service" class="badge-icon-img" height="50" src="https://cf-images.hiraya.digital/emails/17-mar-cf/images/Customer_Quality.png" style="display:block; border:0; width:50px; height:50px; margin:0 auto;" width="50"/>
</td>
</tr>
</table>
</td>
</tr>
</table>
</td>
</tr>
</table>"""
    ),
    # 2. Horizontal Strip (Dark mode horizontal strip)
    "06_13_Jul_4_XayhtJ.html": (
        "<!-- Horizontal Badges Strip (Directly below Image Block) -->",
        "<!-- 4. SECTION HEADER: WHY RESTAURANTS CHOOSE ANGAAR -->",
        """<tr>
<td bgcolor="#0A1118" class="badges-container-td" style="background-color: #0A1118; padding: 12px 10px; border-bottom: 2px solid #E5DEC9;">
<table border="0" cellpadding="0" cellspacing="0" class="badges-table" role="presentation" width="100%">
<tr>
<!-- Price Match -->
<td align="center" class="badge-col" style="padding: 2px 4px; text-align: center;" valign="middle" width="25%">
<img alt="Price Match" class="badge-icon-img" src="https://cf-images.hiraya.digital/emails/17-mar-cf/images/Price_match.png" style="display:block; border:0; width:40px; height:auto; margin:0 auto;" width="40"/>
</td>
<!-- 100+ Brands -->
<td align="center" class="badge-col" style="padding: 2px 4px; border-left: 1px solid #1E293B; text-align: center;" valign="middle" width="25%">
<img alt="Trusted Brands" class="badge-icon-img" src="https://cf-images.hiraya.digital/emails/17-mar-cf/images/100_Trusted_Brands.png" style="display:block; border:0; width:40px; height:auto; margin:0 auto;" width="40"/>
</td>
<!-- Fast Shipping -->
<td align="center" class="badge-col" style="padding: 2px 4px; border-left: 1px solid #1E293B; text-align: center;" valign="middle" width="25%">
<img alt="Fast Shipping" class="badge-icon-img" src="https://cf-images.hiraya.digital/emails/17-mar-cf/images/Shipping.png" style="display:block; border:0; width:40px; height:auto; margin:0 auto;" width="40"/>
</td>
<!-- Customer Quality -->
<td align="center" class="badge-col" style="padding: 2px 4px; border-left: 1px solid #1E293B; text-align: center;" valign="middle" width="25%">
<img alt="Quality Service" class="badge-icon-img" src="https://cf-images.hiraya.digital/emails/17-mar-cf/images/Customer_Quality.png" style="display:block; border:0; width:40px; height:auto; margin:0 auto;" width="40"/>
</td>
</tr>
</table>
</td>
</tr>"""
    ),
    # 3. Grid style (Side-by-side inside width="50%" table cells)
    "07_not_reviewed_13_Jul_3_XNZ6cw.html": (
        "<!-- 3. MANDATORY TRUST BADGES GRID (With Gold Border Accent) -->",
        "<!-- 4. INTRO EDITIONAL TEXT SECTION -->",
        """<table bgcolor="#FFFFFF" border="0" cellpadding="0" cellspacing="0" class="wrapper" role="presentation" style="width:600px; max-width:600px; border-left:1px solid #EAE6DF; border-right:1px solid #EAE6DF; border-bottom:1px solid #EAE6DF; border-top:1px solid #D97706;" width="600">
<tr>
<td align="center" style="padding:8px 6px;">
<table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
<tr>
<!-- Price Match -->
<td align="center" style="padding: 4px; text-align: center;" valign="middle" width="25%">
<img alt="Price Match" src="https://cf-images.hiraya.digital/emails/17-mar-cf/images/Price_match.png" style="display:block; width:32px; height:auto; margin:0 auto;" width="32"/>
</td>
<!-- 100+ Brands -->
<td align="center" style="padding: 4px; text-align: center;" valign="middle" width="25%">
<img alt="100% Trusted Brands" src="https://cf-images.hiraya.digital/emails/17-mar-cf/images/100_Trusted_Brands.png" style="display:block; width:32px; height:auto; margin:0 auto;" width="32"/>
</td>
<!-- Fast Shipping -->
<td align="center" style="padding: 4px; text-align: center;" valign="middle" width="25%">
<img alt="Fast Shipping" src="https://cf-images.hiraya.digital/emails/17-mar-cf/images/Shipping.png" style="display:block; width:32px; height:auto; margin:0 auto;" width="32"/>
</td>
<!-- Customer Quality -->
<td align="center" style="padding: 4px; text-align: center;" valign="middle" width="25%">
<img alt="Customer Quality" src="https://cf-images.hiraya.digital/emails/17-mar-cf/images/Customer_Quality.png" style="display:block; width:32px; height:auto; margin:0 auto;" width="32"/>
</td>
</tr>
</table>
</td>
</tr>
</table>"""
    ),
    "08_not_reviewed_8_Jul_2_Rm2Bud.html": (
        "<!-- 3. MANDATORY TRUST BADGES GRID -->",
        "<!-- 4. FEATURED TITLE -->",
        """<table bgcolor="#FFFFFF" border="0" cellpadding="0" cellspacing="0" class="wrapper" role="presentation" style="width:600px; max-width:600px; border-left:1px solid #EAE3DB; border-right:1px solid #EAE3DB; border-bottom:1px solid #EFE6DD;" width="600">
<tr>
<td align="center" style="padding:8px 6px;">
<table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
<tr>
<!-- Price Match -->
<td align="center" style="padding: 4px; text-align: center;" valign="middle" width="25%">
<img alt="Price Match" src="https://cf-images.hiraya.digital/emails/17-mar-cf/images/Price_match.png" style="display:block; width:36px; height:auto; margin:0 auto;" width="36"/>
</td>
<!-- 100+ Brands -->
<td align="center" style="padding: 4px; text-align: center;" valign="middle" width="25%">
<img alt="100% Trusted Brands" src="https://cf-images.hiraya.digital/emails/17-mar-cf/images/100_Trusted_Brands.png" style="display:block; width:36px; height:auto; margin:0 auto;" width="36"/>
</td>
<!-- Fast Shipping -->
<td align="center" style="padding: 4px; text-align: center;" valign="middle" width="25%">
<img alt="Fast Shipping" src="https://cf-images.hiraya.digital/emails/17-mar-cf/images/Shipping.png" style="display:block; width:36px; height:auto; margin:0 auto;" width="36"/>
</td>
<!-- Customer Quality -->
<td align="center" style="padding: 4px; text-align: center;" valign="middle" width="25%">
<img alt="Customer Quality" src="https://cf-images.hiraya.digital/emails/17-mar-cf/images/Customer_Quality.png" style="display:block; width:36px; height:auto; margin:0 auto;" width="36"/>
</td>
</tr>
</table>
</td>
</tr>
</table>"""
    ),
    "09_not_reviewed_8_Jul_1_UfDPDj.html": (
        "<!-- 3. MANDATORY TRUST BADGES GRID -->",
        "<!-- 4. EDITORIAL SPOTLIGHT: MINI TANDOOR OVEN -->",
        """<table bgcolor="#FFFFFF" border="0" cellpadding="0" cellspacing="0" class="wrapper" role="presentation" style="width:600px; max-width:600px; border-left:1px solid #EAE6DF; border-right:1px solid #EAE6DF; border-bottom:1px solid #F2EFE9;" width="600">
<tr>
<td align="center" style="padding:8px 6px;">
<table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
<tr>
<!-- Price Match -->
<td align="center" style="padding: 4px; text-align: center;" valign="middle" width="25%">
<img alt="Price Match" src="https://cf-images.hiraya.digital/emails/17-mar-cf/images/Price_match.png" style="display:block; width:36px; height:auto; margin:0 auto;" width="36"/>
</td>
<!-- 100+ Brands -->
<td align="center" style="padding: 4px; text-align: center;" valign="middle" width="25%">
<img alt="100% Trusted Brands" src="https://cf-images.hiraya.digital/emails/17-mar-cf/images/100_Trusted_Brands.png" style="display:block; width:36px; height:auto; margin:0 auto;" width="36"/>
</td>
<!-- Fast Shipping -->
<td align="center" style="padding: 4px; text-align: center;" valign="middle" width="25%">
<img alt="Fast Shipping" src="https://cf-images.hiraya.digital/emails/17-mar-cf/images/Shipping.png" style="display:block; width:36px; height:auto; margin:0 auto;" width="36"/>
</td>
<!-- Customer Quality -->
<td align="center" style="padding: 4px; text-align: center;" valign="middle" width="25%">
<img alt="Customer Quality" src="https://cf-images.hiraya.digital/emails/17-mar-cf/images/Customer_Quality.png" style="display:block; width:36px; height:auto; margin:0 auto;" width="36"/>
</td>
</tr>
</table>
</td>
</tr>
</table>"""
    ),
    "11_not_reviewed_29_Jun_9_UvtLqg.html": (
        "<!-- 4. Mandatory Trust Badges Row -->",
        "<!-- 5. Featured Brand Section: Alto-Shaam -->",
        """<table bgcolor="#FFFFFF" border="0" cellpadding="0" cellspacing="0" class="wrapper" role="presentation" style="width:600px; max-width:600px;" width="600">
<tr>
<td style="padding:6px 8px 3px 8px;">
<table bgcolor="#F4F7F6" border="0" cellpadding="0" cellspacing="0" role="presentation" style="border:1px solid #DDE3E2; padding:4px; border-radius:3px;" width="100%">
<tr>
<td align="center" style="padding:0; font-size:0;">
<table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
<tr>
<!-- Price Match -->
<td align="center" style="padding: 4px; text-align: center;" valign="middle" width="25%">
<img alt="Price Match Guarantee" src="https://cf-images.hiraya.digital/emails/17-mar-cf/images/Price_match.png" style="display:block; width:38px; height:auto; border:0; margin:0 auto;" width="38"/>
</td>
<!-- 100+ Brands -->
<td align="center" style="padding: 4px; text-align: center;" valign="middle" width="25%">
<img alt="100+ Trusted Brands" src="https://cf-images.hiraya.digital/emails/17-mar-cf/images/100_Trusted_Brands.png" style="display:block; width:38px; height:auto; border:0; margin:0 auto;" width="38"/>
</td>
<!-- Fast Shipping -->
<td align="center" style="padding: 4px; text-align: center;" valign="middle" width="25%">
<img alt="Fast Shipping" src="https://cf-images.hiraya.digital/emails/17-mar-cf/images/Shipping.png" style="display:block; width:46px; height:auto; border:0; margin:0 auto;" width="46"/>
</td>
<!-- Customer Quality -->
<td align="center" style="padding: 4px; text-align: center;" valign="middle" width="25%">
<img alt="Customer Quality" src="https://cf-images.hiraya.digital/emails/17-mar-cf/images/Customer_Quality.png" style="display:block; width:38px; height:auto; border:0; margin:0 auto;" width="38"/>
</td>
</tr>
</table>
</td>
</tr>
</table>
</td>
</tr>
</table>"""
    ),
    "13_22_Jun_7_U5hDGi.html": (
        "<!-- 4. Mandatory Trust Badges Row -->",
        "<!-- Rounded buttons -->",
        """<table bgcolor="#0D2236" border="0" cellpadding="0" cellspacing="0" class="wrapper" role="presentation" style="width:100%; max-width:600px;" width="600">
<tr>
<td style="padding:10px 10px 10px 10px;">
<table bgcolor="#1E3042" border="0" cellpadding="0" cellspacing="0" role="presentation" style="border:1px solid #2B3D4F; padding:4px; border-radius:3px;" width="100%">
<tr>
<td align="center" style="padding:0; font-size:0;">
<table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
<tr>
<!-- Price Match -->
<td align="center" style="padding: 4px; text-align: center;" valign="middle" width="25%">
<img alt="Price Match Guarantee" src="https://cf-images.hiraya.digital/emails/17-mar-cf/images/Price_match.png" style="display:block; width:36px; height:auto; border:0; margin:0 auto;" width="36"/>
</td>
<!-- 100+ Brands -->
<td align="center" style="padding: 4px; text-align: center;" valign="middle" width="25%">
<img alt="100+ Trusted Brands" src="https://cf-images.hiraya.digital/emails/17-mar-cf/images/100_Trusted_Brands.png" style="display:block; width:36px; height:auto; border:0; margin:0 auto;" width="36"/>
</td>
<!-- Fast Shipping -->
<td align="center" style="padding: 4px; text-align: center;" valign="middle" width="25%">
<img alt="Fast Shipping" src="https://cf-images.hiraya.digital/emails/17-mar-cf/images/Shipping.png" style="display:block; width:36px; height:auto; border:0; margin:0 auto;" width="36"/>
</td>
<!-- Customer Quality -->
<td align="center" style="padding: 4px; text-align: center;" valign="middle" width="25%">
<img alt="Quality Service" src="https://cf-images.hiraya.digital/emails/17-mar-cf/images/Customer_Quality.png" style="display:block; width:36px; height:auto; border:0; margin:0 auto;" width="36"/>
</td>
</tr>
</table>
</td>
</tr>
</table>
</td>
</tr>
</table>
</td>
</tr>
</table>
<!-- Rounded buttons -->"""
    ),
    "14_not_reviewed_16_Jun_6_Yg5y5j.html": (
        "<!-- 4. MANDATORY TRUST BADGES STRIP -->",
        "<!-- 5. COMMERCIAL TANDOORS SECTION -->",
        """<table bgcolor="#FFFFFF" border="0" cellpadding="0" cellspacing="0" class="wrapper" role="presentation" style="width:100%; max-width:600px;" width="600">
<tr>
<td style="padding: 0px 10px;">
<table bgcolor="#FFFFFF" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;" width="100%">
<tr>
<td class="badges-container-td" style="padding: 10px 10px; border-bottom: 2px solid #C59B27; border-top: 1px solid #C59B27;">
<table border="0" cellpadding="0" cellspacing="0" class="badges-table" role="presentation" width="100%">
<tr>
<!-- Price Match -->
<td align="center" class="badge-col" style="padding: 2px 4px; text-align: center;" valign="middle" width="25%">
<img alt="Price Match" class="badge-icon-img" src="https://cf-images.hiraya.digital/emails/17-mar-cf/images/Price_match.png" style="display:block; border:0; width:40px; height:auto; margin:0 auto;" width="40"/>
</td>
<!-- 100+ Brands -->
<td align="center" class="badge-col" style="padding: 2px 4px; border-left: 1px solid #5C4B43; text-align: center;" valign="middle" width="25%">
<img alt="Trusted Brands" class="badge-icon-img" src="https://cf-images.hiraya.digital/emails/17-mar-cf/images/100_Trusted_Brands.png" style="display:block; border:0; width:40px; height:auto; margin:0 auto;" width="40"/>
</td>
<!-- Fast Shipping -->
<td align="center" class="badge-col" style="padding: 2px 4px; border-left: 1px solid #5C4B43; text-align: center;" valign="middle" width="25%">
<img alt="Fast Shipping" class="badge-icon-img" src="https://cf-images.hiraya.digital/emails/17-mar-cf/images/Shipping.png" style="display:block; border:0; width:40px; height:auto; margin:0 auto;" width="40"/>
</td>
<!-- Customer Quality -->
<td align="center" class="badge-col" style="padding: 2px 4px; border-left: 1px solid #5C4B43; text-align: center;" valign="middle" width="25%">
<img alt="Quality Service" class="badge-icon-img" src="https://cf-images.hiraya.digital/emails/17-mar-cf/images/Customer_Quality.png" style="display:block; border:0; width:40px; height:auto; margin:0 auto;" width="40"/>
</td>
</tr>
</table>
</td>
</tr>
</table>
</td>
</tr>
</table>"""
    ),
    "16_not_reviewed_12_Junu_3_Y3uBiz.html": (
        "<!-- Horizontal Badges Strip (Directly below Image Block) -->",
        "<!-- 4. FOOD PREPARATION EQUIPMENT -->",
        """<tr>
<td bgcolor="#0A1118" class="badges-container-td" style="background-color: #0A1118; padding: 12px 10px; border-bottom: 2px solid #E5DEC9;">
<table border="0" cellpadding="0" cellspacing="0" class="badges-table" role="presentation" width="100%">
<tr>
<!-- Price Match -->
<td align="center" class="badge-col" style="padding: 2px 4px; text-align: center;" valign="middle" width="25%">
<img alt="Price Match" class="badge-icon-img" src="https://cf-images.hiraya.digital/emails/17-mar-cf/images/Price_match.png" style="display:block; border:0; width:40px; height:auto; margin:0 auto;" width="40"/>
</td>
<!-- 100+ Brands -->
<td align="center" class="badge-col" style="padding: 2px 4px; border-left: 1px solid #1E293B; text-align: center;" valign="middle" width="25%">
<img alt="Trusted Brands" class="badge-icon-img" src="https://cf-images.hiraya.digital/emails/17-mar-cf/images/100_Trusted_Brands.png" style="display:block; border:0; width:40px; height:auto; margin:0 auto;" width="40"/>
</td>
<!-- Fast Shipping -->
<td align="center" class="badge-col" style="padding: 2px 4px; border-left: 1px solid #1E293B; text-align: center;" valign="middle" width="25%">
<img alt="Fast Shipping" class="badge-icon-img" src="https://cf-images.hiraya.digital/emails/17-mar-cf/images/Shipping.png" style="display:block; border:0; width:40px; height:auto; margin:0 auto;" width="40"/>
</td>
<!-- Customer Quality -->
<td align="center" class="badge-col" style="padding: 2px 4px; border-left: 1px solid #1E293B; text-align: center;" valign="middle" width="25%">
<img alt="Quality Service" class="badge-icon-img" src="https://cf-images.hiraya.digital/emails/17-mar-cf/images/Customer_Quality.png" style="display:block; border:0; width:40px; height:auto; margin:0 auto;" width="40"/>
</td>
</tr>
</table>
</td>
</tr>"""
    ),
    # 4. Vertical card stacked
    "15_not_reviewed_12_Junu_4_UUYCfN.html": (
        'class="trust-card-wrapper"',
        "second-table-end",
        """<table bgcolor="#FFFFFF" border="0" cellpadding="0" cellspacing="0" class="trust-card-wrapper" role="presentation" style="background-color: #FFFFFF; border-radius: 16px; max-width: 240px; margin: 0 auto; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" width="100%">
<tr>
<td class="trust-card-container-td" style="padding: 10px 8px;">
<table border="0" cellpadding="0" cellspacing="0" class="trust-card-table" role="presentation" width="100%">
<!-- Price Match -->
<tr class="badge-row">
<td style="padding: 5px 0; text-align: center;" valign="middle">
<img alt="Price Match" src="https://cf-images.hiraya.digital/emails/17-mar-cf/images/Price_match.png" style="display:block; border:0; width:40px; height:auto; margin: 0 auto;" width="40"/>
</td>
</tr>
<!-- Divider -->
<tr class="badge-divider">
<td style="border-bottom: 1px solid #F1F5F9; height: 1px; font-size: 1px; line-height: 1px;">
&nbsp;
</td>
</tr>
<!-- 100+ Brands -->
<tr class="badge-row">
<td style="padding: 5px 0; text-align: center;" valign="middle">
<img alt="Trusted Brands" src="https://cf-images.hiraya.digital/emails/17-mar-cf/images/100_Trusted_Brands.png" style="display:block; border:0; width:40px; height:auto; margin: 0 auto;" width="40"/>
</td>
</tr>
<!-- Divider -->
<tr class="badge-divider">
<td style="border-bottom: 1px solid #F1F5F9; height: 1px; font-size: 1px; line-height: 1px;">
&nbsp;
</td>
</tr>
<!-- Fast Shipping -->
<tr class="badge-row">
<td style="padding: 5px 0; text-align: center;" valign="middle">
<img alt="Fast Shipping" src="https://cf-images.hiraya.digital/emails/17-mar-cf/images/Shipping.png" style="display:block; border:0; width:40px; height:auto; margin: 0 auto;" width="40"/>
</td>
</tr>
<!-- Divider -->
<tr class="badge-divider">
<td style="border-bottom: 1px solid #F1F5F9; height: 1px; font-size: 1px; line-height: 1px;">
&nbsp;
</td>
</tr>
<!-- Quality Customer Service -->
<tr class="badge-row">
<td style="padding: 5px 0; text-align: center;" valign="middle">
<img alt="Customer Service" src="https://cf-images.hiraya.digital/emails/17-mar-cf/images/Customer_Quality.png" style="display:block; border:0; width:40px; height:auto; margin: 0 auto;" width="40"/>
</td>
</tr>
</table>
</td>
</tr>
</table>"""
    )
}

def main():
    templates_dir = Path("downloaded_templates")
    modified_count = 0

    for filename, (start_token, end_token, new_block) in MODIFICATIONS.items():
        filepath = templates_dir / filename
        if not filepath.exists():
            print(f"[!] Warning: File {filename} not found.")
            continue

        print(f"[*] Processing {filename}...")
        try:
            content = filepath.read_text(encoding="utf-8")
            
            # Handle special tag-based parsing for File 15
            if filename == "15_not_reviewed_12_Junu_4_UUYCfN.html":
                start_idx = content.find(start_token)
                if start_idx == -1:
                    print(f"    [!] Error: Could not find '{start_token}' in {filename}")
                    continue
                start_table_idx = content.rfind("<table", 0, start_idx)
                
                # Count the second closing </table> tag
                first_close = content.find("</table>", start_idx)
                second_close = content.find("</table>", first_close + 8)
                end_table_idx = second_close + 8
                
                modified_content = content[:start_table_idx] + new_block + content[end_table_idx:]
            else:
                start_idx = content.find(start_token)
                if start_idx == -1:
                    print(f"    [!] Error: Could not find start token in {filename}")
                    continue
                end_idx = content.find(end_token, start_idx)
                if end_idx == -1:
                    print(f"    [!] Error: Could not find end token in {filename}")
                    continue
                
                modified_content = content[:start_idx] + start_token + "\n" + new_block + "\n" + content[end_idx:]

            filepath.write_text(modified_content, encoding="utf-8")
            print(f"    [+] Saved modifications to {filename}")
            modified_count += 1
        except Exception as e:
            print(f"    [!] Error processing {filename}: {e}")

    print(f"\n[+] Surgical modifications complete! Modified {modified_count}/10 files.")

if __name__ == "__main__":
    main()
