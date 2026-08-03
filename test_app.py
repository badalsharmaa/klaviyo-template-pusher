import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Ensure current directory is on path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch("app.get_templates")
    @patch("app.os.getenv")
    def test_list_templates_success(self, mock_getenv, mock_get_templates):
        # Mock environment API key
        mock_getenv.return_value = "mock_api_key"

        # Mock Klaviyo response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {
                    "type": "template",
                    "id": "T_123",
                    "attributes": {
                        "name": "My Custom Template",
                        "editor_type": "CODE",
                        "updated": "2026-07-22T10:00:00Z"
                    }
                }
            ]
        }
        mock_get_templates.return_value = mock_response

        # Execute GET request
        response = self.app.get('/templates')
        self.assertEqual(response.status_code, 200)
        
        json_data = response.get_json()
        self.assertTrue(json_data["success"])
        self.assertEqual(len(json_data["templates"]), 1)
        self.assertEqual(json_data["templates"][0]["id"], "T_123")
        self.assertEqual(json_data["templates"][0]["name"], "My Custom Template")

    @patch("app.os.getenv")
    def test_list_templates_missing_key(self, mock_getenv):
        # Mock environment missing API key
        mock_getenv.return_value = None

        response = self.app.get('/templates')
        self.assertEqual(response.status_code, 400)
        json_data = response.get_json()
        self.assertFalse(json_data["success"])
        self.assertIn("API Key not configured", json_data["message"])

    @patch("app.get_template")
    @patch("app.os.getenv")
    def test_download_template_success(self, mock_getenv, mock_get_template):
        mock_getenv.return_value = "mock_api_key"

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "attributes": {
                    "html": "<html>Content</html>",
                    "name": "Special Newsletter"
                }
            }
        }
        mock_get_template.return_value = mock_response

        response = self.app.get('/templates/T123/download')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"<html>Content</html>")
        self.assertIn("attachment; filename=Special_Newsletter.html", response.headers["Content-disposition"])

if __name__ == "__main__":
    unittest.main()
