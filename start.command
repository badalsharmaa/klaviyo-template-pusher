#!/bin/bash

# Move to the directory where this script is located
cd "$(dirname "$0")"

echo "============================================="
echo "  Klaviyo Template Pusher Startup Utility"
echo "============================================="
echo ""

# 1. Clean up any existing Flask server running on port 8080
echo "[*] Checking for existing servers running on port 8080..."
PID=$(lsof -t -i:8080)
if [ ! -z "$PID" ]; then
    echo "[+] Found running server (PID: $PID). Stopping it now..."
    kill -9 $PID
    sleep 1
else
    echo "[+] Port 8080 is clear."
fi

# 2. Check virtual environment
if [ ! -d ".venv" ]; then
    echo "[*] Virtual environment not found. Setting up..."
    python3 -m venv .venv
    .venv/bin/pip install -r requirements.txt
fi

# 3. Automatically open web dashboard in default browser
echo "[*] Opening web dashboard in your browser..."
open "http://127.0.0.1:8080"

# 4. Start the server
echo "[*] Starting Flask server... (Press Ctrl+C in this terminal window to stop)"
echo ""
.venv/bin/python app.py
