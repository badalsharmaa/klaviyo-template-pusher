# Celebrate Festival Inc. — Klaviyo Deliverability & Template Audit Report

## 1. Executive Summary: The Reach Decline
Your Klaviyo account metrics show a **steady and severe decline in open rates** over the last three months:
*   **May 22**: **22.52%** Open Rate
*   **June 16**: **20.82%** Open Rate
*   **June 26**: **19.97%** Open Rate
*   **July 8**: **17.10%** Open Rate
*   **July 22**: **15.83%** Open Rate *(All-Time Low)*

This represents a **30% drop in relative reach**. This drop indicates that a significant percentage of your emails are no longer reaching the primary inbox—they are being routed directly to the **Spam/Junk Folder** or the **Promotions Tab** by mailbox providers (primarily Gmail and Yahoo).

---

## 2. Campaign-by-Campaign Metric Breakdown
Below is the performance data for your recent campaigns sent between May and July 2026, sorted by date:

| Campaign Name | Sent Date | Delivered | Bounces | Open Rate | Click Rate | CTOR | Bounce Rate | Spam Rate |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Campaign Jul 22, 2026** | Jul 22, 2026 | 3,569 | 41 | **15.83%** | 0.28% | 1.77% | 1.14% | 0.00% |
| **Campaign Jul 14, 2026** | Jul 14, 2026 | 3,575 | 35 | **16.90%** | 0.64% | 3.81% | 0.97% | 0.028% |
| **Campaign Jul 8, 2026** | Jul 8, 2026 | 3,591 | 287 | **17.10%** | 0.53% | 3.09% | **7.40%** | 0.0278% |
| **Campaign Jun 26, 2026** | Jun 26, 2026 | 3,460 | 44 | **19.97%** | 1.10% | 5.50% | 1.26% | 0.00% |
| **June 16th** | Jun 16, 2026 | 3,453 | 33 | **20.82%** | 0.49% | 2.36% | 0.95% | 0.00% |
| **Campaign Jun 12, 2026** | Jun 12, 2026 | 3,460 | 46 | **20.87%** | 0.43% | 2.08% | 1.31% | 0.00% |
| **Campaign Jun 5, 2026** | Jun 5, 2026 | 3,462 | 31 | **21.35%** | 6.12% | 28.69% | 0.89% | 0.00% |
| **Campaign Jun 3, 2026** | Jun 3, 2026 | 3,475 | 169 | **21.24%** | 0.49% | 2.30% | **4.64%** | 0.0288% |
| **Campaign May 29, 2026** | May 29, 2026 | 3,368 | 27 | **20.40%** | 0.53% | 2.62% | 0.80% | 0.00% |
| **Campaign May 26, 2026** | May 26, 2026 | 3,379 | 22 | **20.83%** | 0.30% | 1.42% | 0.65% | 0.0296% |
| **Campaign May 22, 2026** | May 22, 2026 | 3,379 | 24 | **22.52%** | 0.41% | 1.84% | 0.71% | 0.00% |
| **Email 1** | May 18, 2026 | 3,408 | 170 | **20.48%** | 0.21% | 1.00% | **4.75%** | 0.00% |
| **Email 1** | May 8, 2026 | 3,343 | 101 | **23.72%** | 0.45% | 1.89% | **2.93%** | 0.00% |

---

## 3. Root Cause Analysis

### Root Cause 1: Deliverability Penalties from High Bounce Rates
Mailbox providers (especially Google and Yahoo under their new Sender Requirements) monitor your **Bounce Rate** to determine if you are a legitimate sender or a spammer. 
*   **The Golden Rule**: Keep your bounce rate **below 2%** (ideally below 1%).
*   **Your Data**: Your campaigns on **May 8 (2.93%)**, **May 18 (4.75%)**, **June 3 (4.64%)**, and **July 8 (7.40%)** massively exceeded the safe limit. 
*   **The Penalty**: Mailing uncleaned lists containing invalid or dead addresses tells providers that your lists are stale or poorly acquired. Once you exceed 2%, your sender reputation drops, and providers start filtering subsequent campaigns into the **Spam folder**. This directly explains your declining open rates.

### Root Cause 2: HTML Emailer Design and Render Issues
We analyzed the HTML template used in your recent campaigns (ID: `UH5f4L`). We found two major coding issues:

1.  **The "Invisible Text" Rendering Trap**:
    The hero section sets a white background (`bgcolor="#FFFFFF"`) on the table, but places white text (`color:#FFFFFF`) and light gray text (`color:#CBD5E1`) over a background image. To make the text readable, it uses a CSS `linear-gradient` overlay to darken the image.
    *   **Gmail Limitation**: Gmail mobile and web clients do not support CSS `linear-gradient` in background images and strip them. Additionally, many users have images blocked by default.
    *   **The Result**: If the background image fails to load or the gradient is stripped, the cell falls back to white. Your white text becomes **completely invisible (white text on a white background)**.
2.  **Hidden Text Spam Trigger**:
    Spam filters evaluate the contrast ratio between your text and the underlying HTML cell background. White text inside a cell with a white background is flagged as "hidden text" (a black-hat SEO spam technique). This triggers immediate spam folder routing.

---

## 4. Sender Domain Authentication Status
We performed DNS checks on your sending domain `celebratefestivalinc.com` to see if your domain setup is causing issues:
*   **DMARC Record**: `"v=DMARC1; p=reject; rua=mailto:dmarc-reports@celebratefestivalinc.com"` (Active and highly secure).
*   **Sending Subdomain**: `send.celebratefestivalinc.com` is registered in Klaviyo with active NS records pointing to Klaviyo name servers (`ns1.klaviyo.com` - `ns4.klaviyo.com`).
*   **Authentication Status**: **Pass**. Because your dedicated sending subdomain is active, your emails pass SPF, DKIM, and DMARC alignment. Your domain setup is not the problem; the issue is entirely **list hygiene (bounces)** and **HTML coding fallbacks**.

---

## 5. Action Plan: How to Increase Your Reach

To restore your sender reputation and get your open rates back to 22%+, follow these steps:

### Step A: Fix Your HTML Template Fallbacks
1.  **Set Dark Table Backgrounds**:
    When using white text, always set a dark solid background color on the table cell (`bgcolor="#0F172A"` or `bgcolor="#1E293B"`). If the image doesn't load, the text remains readable.
    ```html
    <!-- Fix for template.html -->
    <td class="hero" bgcolor="#0F172A" style="background-color: #0F172A;">
    ```
2.  **Flatten Background Images**:
    Instead of using HTML/CSS code gradients to darken background images, apply the dark overlay directly to your image files in Photoshop or Canva before uploading them to Klaviyo.

### Step B: Segment and Clean Your Klaviyo Lists
You must stop sending emails to unengaged and dead email addresses:
1.  **Create an "Engaged 90 Days" Segment**:
    *   Set the definition to:
        *   `Someone can receive email marketing`
        *   **AND** (`Someone has opened an email in the last 90 days` **OR** `Someone has clicked an email in the last 90 days` **OR** `Someone has subscribed in the last 30 days`).
2.  **Send ONLY to this Segment**:
    *   For the next 4 weeks, send campaigns **only** to this segment. Do not mail your master list.
    *   This will reduce your bounce rate to nearly 0% and increase open rates, proving to Gmail and Yahoo that your subscribers want your emails.
3.  **Perform a Suppression Audit**:
    *   Go to **Audience > Profiles > Suppressed Profiles** and check that all historical hard-bounced addresses are fully suppressed.

### Step C: Domain Reputation Warm-up
*   Start by sending your fixed campaigns to your most active 1,000 subscribers (your 30-day openers) to establish a very high open rate (40%+).
*   Gradually expand the audience size over 2–3 weeks.
*   Monitor your bounce rate closely—if it ever exceeds **1.5%**, immediately pause and tighten your list segmentation.
