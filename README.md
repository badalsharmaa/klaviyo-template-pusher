# 🚀 Klaviyo Template Pusher & Management Suite

> A modern developer toolkit and interactive web dashboard for downloading, analyzing, modifying, testing, and pushing HTML email templates directly to Klaviyo via the Klaviyo REST API.

---

## 📌 Overview

**Klaviyo Template Pusher** eliminates the tedious web-GUI workflow for managing Klaviyo email templates. It provides both an intuitive **Flask Web UI** and **CLI automation scripts** to synchronize local HTML templates with remote Klaviyo accounts, perform deliverability audits, and automate batch template edits.

---

## ✨ Key Features

- **🖥️ Interactive Web Dashboard:** Built with Flask (`app.py`), featuring live template previews, one-click deploy/sync buttons, and error reporting.
- **🔒 Secure API Key Management:** Zero hardcoded API keys. All credentials are read securely from environment variables (`.env`) with masked status indicators in the UI.
- **⚡ Batch Download & Sync:** Fetch all remote templates locally in one command (`download_templates.py`, `analyze_and_download.py`).
- **🛠️ Automated HTML AST Manipulation:** Programmatically modify badges, layout elements, and footer links across dozens of templates (`modify_badges_surgically.py`).
- **📊 Deliverability & Product Audits:** Generates markdown and CSV breakdown reports (`template_product_summary.csv`, `klaviyo_deliverability_report.md`).
- **🧪 Comprehensive Test Suite:** Unit and integration tests covering API endpoints, mock handlers, and parser logic.
- **🍏 macOS Quick Launcher:** Includes `start.command` for zero-friction launch with port clearance and auto-browser opening.

---

## 🛠️ Tech Stack

- **Backend:** Python 3.10+, Flask
- **HTTP Client:** `requests`
- **Environment Management:** `python-dotenv`
- **HTML Parsing & AST:** `BeautifulSoup4` / Regex
- **Testing:** `unittest`, `unittest.mock`

---

## 📂 Project Structure

```bash
├── app.py                         # Flask web dashboard application
├── start.command                  # macOS double-click launcher
├── requirements.txt               # Python package dependencies
├── .env.example                   # Environment configuration template
│
├── push_template.py               # CLI tool to upload/update templates
├── push_edits.py                  # CLI tool for selective template edits
├── download_templates.py          # Script to fetch remote templates
├── analyze_and_download.py        # Analytics & batch template downloader
├── modify_badges.py               # Template badge modifier
├── modify_badges_surgically.py    # Surgical regex/AST HTML modifier
│
├── templates/                     # Flask Jinja2 frontend templates
│   └── index.html                 # Main dashboard UI
│
├── downloaded_templates/          # Local cache of downloaded email templates
│
├── test_app.py                    # Unit tests for Flask web endpoints
├── test_push_template.py          # Unit tests for Klaviyo API sync logic
└── test_analyze_and_download.py   # Unit tests for template parsing
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- A Klaviyo account with a **Private API Key** (with `Templates: Read/Write` permissions)

### 2. Installation & Setup
Clone the repository and set up a virtual environment:
```bash
git clone https://github.com/badalsharmaa/klaviyo-template-pusher.git
cd klaviyo-template-pusher

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure API Credentials (Secret Key)
Copy the template `.env.example` to `.env`:
```bash
cp .env.example .env
```

Open `.env` and add your Klaviyo private key:
```env
KLAVIYO_API_KEY=pk_your_actual_klaviyo_private_api_key
KLAVIYO_API_REVISION=2026-04-15
```

> [!IMPORTANT]
> Never commit your `.env` file or share your private API keys. The `.gitignore` is pre-configured to keep your credentials safe.

---

## 💻 Usage

### 🌐 Option A: Run the Web Dashboard
```bash
python app.py
```
Open [http://localhost:8080](http://localhost:8080) in your browser.

*(On macOS, you can also simply double-click `start.command`)*

---

### ⌨️ Option B: Command Line Interface (CLI)

#### Fetch & Download All Templates:
```bash
python download_templates.py
```

#### Push a New or Existing Template:
```bash
# Push raw HTML file to Klaviyo
python push_template.py template.html --name "Summer Launch 2026"

# Update an existing template by ID
python push_template.py template.html --id "TEMPLATE_ID_HERE"
```

#### Run Deliverability & Product Summary Analysis:
```bash
python analyze_and_download.py
```

---

## 🧪 Running Tests

Execute the automated test suite with Python's built-in test runner:
```bash
python -m unittest discover -p "test_*.py"
```

---

## 📄 License

MIT License. Free to use for internal and commercial Klaviyo template automation.
