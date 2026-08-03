# Emailer Best Practices: Celebrate Festival Inc

This instruction sheet is stored in the system knowledge base to guide future coding sessions for the email templates in `/Users/badalsharma/Work/Caleberate Festival/emailer` and `/Users/badalsharma/Work/klaviyo-template-pusher`.

---

## 1. Core Technical Rules for Spam Prevention (HTML Coding)

To prevent emails from landing in the **Spam folder** due to rendering or formatting issues, always follow these rules:

1.  **Mandatory Solid Background Fallbacks (`bgcolor` attribute)**:
    Every single table cell (`<td>`) or table (`<table>`) that uses a background image (`background="..."`) or a CSS background image style (`background-image: ...`) **must** have an explicit, solid background color attribute (`bgcolor="..."`) and matching CSS style.
    *   **Why**: Email clients like Gmail completely strip CSS linear gradients and block external images by default. Without a fallback color, text color will mismatch with the default white canvas, causing **invisible text** which spam filters flag as "hidden text" (a major spam trigger).
    
2.  **Color Alignment Standard**:
    *   **For sections with light/white text** (e.g., `#ffffff`, `#cbd5e1`): Use a dark fallback color like `bgcolor="#0F172A"` or `bgcolor="#1B2A32"`.
    *   **For sections with dark text** (e.g., `#1B2A32`, `#4A5568`): Use a light fallback color like `bgcolor="#FAF8F5"` or `bgcolor="#FFFFFF"`.
    
3.  **Correct Coding Examples**:
    *   *Bad*: `<td style="background-image: linear-gradient(to right, #0F172A, transparent), url('bg.png'); color: #ffffff;">`
    *   *Good*: `<td bgcolor="#0F172A" style="background-color: #0F172A; background-image: linear-gradient(to right, #0F172A, transparent), url('bg.png'); color: #ffffff;">`
    
4.  **Avoid HTML-Only Gradients**:
    Do not rely on complex CSS gradients for visual structure. Where possible, bake/flatten gradients directly onto the image assets before hosting them.

5.  **Clean Footer & Unsubscribe Links**:
    Ensure the email footer contains a physical mailing address and a valid unsubscribe link utilizing Klaviyo's syntax:
    *   `<a href="{% unsubscribe_link %}" style="...">Unsubscribe</a>`

---

## 2. Core Operational Rules for Deliverability (List Sending)

No matter how clean the code is, poor sending practices will trigger spam placement. Always recommend the following standards:

1.  **Strict Bounce Rate Threshold**:
    *   Keep bounce rates **below 2%** (Google and Yahoo's hard threshold).
    *   If bounce rates exceed this, proactively advise the user to perform list hygiene.

2.  **Use Engagement-Based Segments**:
    *   Do not send campaigns to the uncleaned master list.
    *   Always segment lists based on engagement. The standard target group is **"Engaged 60 Days"** (profiles that opened/clicked an email in the last 60 days, or subscribed in the last 30 days, and are not suppressed).

3.  **Dedicated Subdomain Alignment**:
    *   Always verify that the `From` header email uses the dedicated sending domain (e.g., `sales@celebratefestivalinc.com` using the `send.celebratefestivalinc.com` server). Any mismatch with the root domain's DMARC `p=reject` policy will cause immediate rejection or spam placement.
