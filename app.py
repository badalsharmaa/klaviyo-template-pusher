#!/usr/bin/env python3
import os
import sys
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

# Import pushing logic from our existing push_template.py
from push_template import push_template, load_environment, get_templates, get_template

app = Flask(__name__)
# Set maximum upload size to 2MB (emails are usually small)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

@app.route('/')
def index():
    # Load environment settings to check status
    load_environment()
    api_key = os.getenv("KLAVIYO_API_KEY")
    
    # Hide the API key values but return status and a masked version
    key_exists = bool(api_key)
    masked_key = ""
    if key_exists:
        # Keep only first 4 and last 4 characters visible, mask the rest
        clean_key = api_key.strip()
        if len(clean_key) > 8:
            masked_key = f"{clean_key[:4]}...{clean_key[-4:]}"
        else:
            masked_key = "****"

    return render_template('index.html', key_exists=key_exists, masked_key=masked_key)

@app.route('/templates', methods=['GET'])
def list_templates():
    # Ensure environment is up-to-date
    load_environment()
    api_key = os.getenv("KLAVIYO_API_KEY")
    if not api_key:
        return jsonify({
            "success": False,
            "message": "Klaviyo API Key not configured on the server. Please add it to your .env file."
        }), 400

    response = get_templates(api_key)
    if response is None:
        return jsonify({
            "success": False,
            "message": "Failed to connect to Klaviyo. Please check your internet connection."
        }), 500

    try:
        response_data = response.json()
    except ValueError:
        response_data = None

    if response.status_code == 200:
        templates_list = []
        if response_data and "data" in response_data:
            for item in response_data["data"]:
                attrs = item.get("attributes", {})
                templates_list.append({
                    "id": item.get("id"),
                    "name": attrs.get("name", "Untitled Template"),
                    "editor_type": attrs.get("editor_type", "UNKNOWN"),
                    "updated": attrs.get("updated", "")
                })
        return jsonify({
            "success": True,
            "templates": templates_list
        })
    else:
        # Request failed - parse details
        errors_list = []
        if response_data and "errors" in response_data:
            for err in response_data["errors"]:
                errors_list.append(err.get("detail", "Unknown Klaviyo API error."))
        else:
            errors_list.append(response.text or f"HTTP Error Status {response.status_code}")

        return jsonify({
            "success": False,
            "message": "Klaviyo API rejected the template list request.",
            "status_code": response.status_code,
            "errors": errors_list
        }), response.status_code

@app.route('/templates/<template_id>/download', methods=['GET'])
def download_template(template_id):
    load_environment()
    api_key = os.getenv("KLAVIYO_API_KEY")
    if not api_key:
        return jsonify({
            "success": False,
            "message": "Klaviyo API Key not configured on the server. Please add it to your .env file."
        }), 400

    response = get_template(api_key, template_id)
    if response is None:
        return jsonify({
            "success": False,
            "message": "Failed to connect to Klaviyo. Please check your network connection."
        }), 500

    try:
        response_data = response.json()
    except ValueError:
        response_data = None

    if response.status_code == 200:
        if response_data and "data" in response_data:
            attrs = response_data["data"].get("attributes", {})
            html_content = attrs.get("html", "")
            template_name = attrs.get("name", "template")
            
            # Secure filename for the download attachment
            safe_name = "".join([c for c in template_name if c.isalnum() or c==' ']).rstrip()
            safe_name = safe_name.replace(" ", "_") or "template"
            
            # Create a response with attachment headers
            from flask import Response
            return Response(
                html_content,
                mimetype="text/html",
                headers={"Content-disposition": f"attachment; filename={safe_name}.html"}
            )
        return jsonify({
            "success": False,
            "message": "Template data not found in response."
        }), 404
    else:
        return jsonify({
            "success": False,
            "message": f"Klaviyo API error (Status {response.status_code})"
        }), response.status_code

@app.route('/push', methods=['POST'])
def handle_push():
    # Ensure environment is up-to-date
    load_environment()
    api_key = os.getenv("KLAVIYO_API_KEY")
    if not api_key:
        return jsonify({
            "success": False,
            "message": "Klaviyo API Key not configured on the server. Please add it to your .env file."
        }), 400

    # Retrieve form data
    template_name = request.form.get('name', 'HTML Email Template').strip()
    template_id = request.form.get('template_id', '').strip()
    if not template_id:
        template_id = None

    # Retrieve file upload
    if 'html_file' not in request.files:
        return jsonify({
            "success": False,
            "message": "No file was uploaded. Please select an HTML file."
        }), 400

    file = request.files['html_file']
    if file.filename == '':
        return jsonify({
            "success": False,
            "message": "Selected file has an empty filename."
        }), 400

    # Check extension
    if not file.filename.lower().endswith(('.html', '.htm')):
        return jsonify({
            "success": False,
            "message": "Invalid file type. Please upload a .html or .htm file."
        }), 400

    try:
        html_content = file.read().decode('utf-8')
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Could not read the uploaded HTML file: {str(e)}"
        }), 400

    if not html_content.strip():
        return jsonify({
            "success": False,
            "message": "The uploaded HTML file is empty."
        }), 400

    # Call push function
    response = push_template(
        api_key=api_key,
        template_name=template_name,
        html_content=html_content,
        template_id=template_id
    )

    if response is None:
        return jsonify({
            "success": False,
            "message": "Failed to connect to Klaviyo. Please check your internet connection."
        }), 500

    try:
        response_data = response.json()
    except ValueError:
        response_data = None

    if response.status_code in (200, 201):
        action_word = "created" if response.status_code == 201 else "updated"
        
        # Build clean response data
        result = {
            "success": True,
            "message": f"Template successfully {action_word}!",
            "status_code": response.status_code
        }
        
        if response_data and "data" in response_data:
            t_data = response_data["data"]
            result.update({
                "template_id": t_data.get("id"),
                "template_name": t_data.get("attributes", {}).get("name"),
                "klaviyo_url": "https://www.klaviyo.com/templates"
            })
        return jsonify(result), response.status_code
    else:
        # Request failed - parse details
        errors_list = []
        if response_data and "errors" in response_data:
            for err in response_data["errors"]:
                errors_list.append(err.get("detail", "Unknown Klaviyo API error."))
        else:
            errors_list.append(response.text or f"HTTP Error Status {response.status_code}")

        return jsonify({
            "success": False,
            "message": "Klaviyo API rejected the template request.",
            "status_code": response.status_code,
            "errors": errors_list
        }), response.status_code

if __name__ == '__main__':
    print("[*] Starting Klaviyo Template Pusher interface...")
    print("[*] Open http://127.0.0.1:8080 in your browser.")
    app.run(host='127.0.0.1', port=8080, debug=True)

