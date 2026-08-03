import unittest
from unittest.mock import patch, MagicMock
import requests
import os
import sys

# Add directory to path to import push_template
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from push_template import push_template, API_URL, DEFAULT_REVISION

class TestPushTemplate(unittest.TestCase):

    @patch("push_template.requests.post")
    def test_push_template_create_success(self, mock_post):
        """Test successful POST request to create a template."""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "data": {
                "type": "template",
                "id": "T12345",
                "attributes": {
                    "name": "Test Template"
                }
            }
        }
        mock_post.return_value = mock_response

        # Execute target function
        response = push_template(
            api_key="mock_api_key",
            template_name="Test Template",
            html_content="<h1>Hello</h1>"
        )

        # Assertions
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        
        # Verify endpoint URL
        self.assertEqual(args[0], API_URL)
        
        # Verify Headers
        headers = kwargs["headers"]
        self.assertEqual(headers["Authorization"], "Klaviyo-API-Key mock_api_key")
        self.assertEqual(headers["revision"], DEFAULT_REVISION)
        self.assertEqual(headers["Content-Type"], "application/vnd.api+json")
        self.assertEqual(headers["Accept"], "application/vnd.api+json")
        
        # Verify Payload
        payload = kwargs["json"]
        self.assertEqual(payload["data"]["type"], "template")
        self.assertEqual(payload["data"]["attributes"]["name"], "Test Template")
        self.assertEqual(payload["data"]["attributes"]["editor_type"], "CODE")
        self.assertEqual(payload["data"]["attributes"]["html"], "<h1>Hello</h1>")
        
        self.assertEqual(response.status_code, 201)

    @patch("push_template.requests.patch")
    def test_push_template_update_success(self, mock_patch):
        """Test successful PATCH request to update an existing template."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "type": "template",
                "id": "T12345",
                "attributes": {
                    "name": "Updated Template"
                }
            }
        }
        mock_patch.return_value = mock_response

        # Execute target function
        response = push_template(
            api_key="mock_api_key",
            template_name="Updated Template",
            html_content="<h1>Updated</h1>",
            template_id="T12345"
        )

        # Assertions
        mock_patch.assert_called_once()
        args, kwargs = mock_patch.call_args
        
        # Verify endpoint URL includes template id
        self.assertEqual(args[0], f"{API_URL}T12345/")
        
        # Verify Payload structure for PATCH (including id key)
        payload = kwargs["json"]
        self.assertEqual(payload["data"]["id"], "T12345")
        self.assertEqual(payload["data"]["attributes"]["name"], "Updated Template")
        self.assertEqual(payload["data"]["attributes"]["html"], "<h1>Updated</h1>")
        self.assertNotIn("editor_type", payload["data"]["attributes"])
        
        self.assertEqual(response.status_code, 200)

    @patch("push_template.requests.post")
    def test_push_template_network_error(self, mock_post):
        """Test how network failures/exceptions are handled."""
        mock_post.side_effect = requests.exceptions.RequestException("Connection refused")
        
        # Execute target function
        response = push_template(
            api_key="mock_api_key",
            template_name="Test Template",
            html_content="<h1>Hello</h1>"
        )
        
        # Assertions
        mock_post.assert_called_once()
        self.assertIsNone(response)

    @patch("push_template.requests.get")
    def test_get_templates_success(self, mock_get):
        """Test successful GET request to fetch templates."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "template",
                    "id": "T123",
                    "attributes": {
                        "name": "Promo Template",
                        "editor_type": "CODE",
                        "updated": "2026-07-22T00:00:00Z"
                    }
                }
            ]
        }
        mock_get.return_value = mock_response

        from push_template import get_templates
        response = get_templates("mock_api_key")

        mock_get.assert_called_once()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"][0]["id"], "T123")

    @patch("push_template.requests.get")
    def test_get_templates_network_error(self, mock_get):
        """Test how network failures are handled in get_templates."""
        mock_get.side_effect = requests.exceptions.RequestException("Connection timed out")
        
        from push_template import get_templates
        response = get_templates("mock_api_key")
        
        mock_get.assert_called_once()
        self.assertIsNone(response)

    @patch("push_template.requests.get")
    def test_get_templates_pagination(self, mock_get):
        """Test that get_templates fetches multiple pages if next links exist."""
        # Mock response sequence
        res1 = MagicMock()
        res1.status_code = 200
        res1.json.return_value = {
            "data": [{"id": "T1", "attributes": {"name": "T1"}}],
            "links": {"next": "https://a.klaviyo.com/api/templates/?page[cursor]=abc"}
        }

        res2 = MagicMock()
        res2.status_code = 200
        res2.json.return_value = {
            "data": [{"id": "T2", "attributes": {"name": "T2"}}],
            "links": {}
        }

        mock_get.side_effect = [res1, res2]

        from push_template import get_templates
        response = get_templates("mock_api_key")

        self.assertEqual(response.status_code, 200)
        data = response.json().get("data", [])
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["id"], "T1")
        self.assertEqual(data[1]["id"], "T2")

    @patch("push_template.requests.get")
    def test_get_template_single_success(self, mock_get):
        """Test successful single GET template request."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "id": "T123",
                "attributes": {
                    "name": "Template Title",
                    "html": "<h1>Test</h1>"
                }
            }
        }
        mock_get.return_value = mock_response

        from push_template import get_template
        response = get_template("mock_api_key", "T123")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["data"]["attributes"]["name"], "Template Title")

if __name__ == "__main__":
    unittest.main()
