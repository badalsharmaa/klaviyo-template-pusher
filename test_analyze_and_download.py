import unittest
from unittest.mock import patch, MagicMock
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from analyze_and_download import make_safe_filename, extract_products_from_html

class TestAnalyzeAndDownload(unittest.TestCase):
    def test_make_safe_filename(self):
        self.assertEqual(make_safe_filename("Summer Sale - 2026!"), "summer_sale_2026")
        self.assertEqual(make_safe_filename("  Product  Launch / Special  "), "product_launch_special")
        self.assertEqual(make_safe_filename("___"), "template")

    def test_extract_products_from_html(self):
        sample_html = """
        <html>
            <body>
                <h1>Wireless Bluetooth Headphones</h1>
                <img src="banner.jpg" alt="Company Banner logo" />
                <img src="p1.jpg" alt="Leather Travel Backpack" />
                <a href="https://example.com/products/organic-coffee-beans">Buy Coffee</a>
                <p>Hello {{ item.title }} - {{ event.extra.line_items }}</p>
            </body>
        </html>
        """
        result = extract_products_from_html(sample_html)
        
        self.assertIn("Wireless Bluetooth Headphones", result["products"])
        self.assertIn("Leather Travel Backpack", result["products"])
        self.assertIn("Organic Coffee Beans", result["products"])
        self.assertNotIn("Company Banner logo", result["products"])
        
        self.assertIn("item.title", result["dynamic_tags"])
        self.assertIn("event.extra.line_items", result["dynamic_tags"])

if __name__ == "__main__":
    unittest.main()
