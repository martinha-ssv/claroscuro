import unittest
from unittest.mock import patch, Mock
import json

from colors.generate import generate_color_palette

class TestGenerateColorPalette(unittest.TestCase):

    @patch('colors.generate.requests.post')
    def test_generate_color_palette(self, mock_post):
        # Configure the mock to return a successful response
        expected_palette = {"results": [["#b2e8f5", "#79b5c9", "#4b8da1", "#236a7f"]]}
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_palette
        mock_post.return_value = mock_response

        # Call the function with some base colors (even though they are not used)
        base_colors = ['#ff5733', '#33ff57', '#3357ff']
        palette = generate_color_palette(*base_colors)

        # Assert the function returned the expected palette
        self.assertEqual(palette, expected_palette)

        # Assert that requests.post was called correctly
        expected_url = "https://api.huemint.com/color"
        expected_json_data = {
            "mode": "transformer",
            "num_colors": 4,
            "temperature": "1.2",
            "num_results": 50,
            "adjacency": ["0", "65", "45", "35", "65", "0", "35", "65", "45", "35", "0", "35", "35", "65", "35", "0"],
            "palette": ["#ffffff", "-", "-", "-"]
        }
        mock_post.assert_called_once_with(
            expected_url,
            json=expected_json_data,
            headers={"Content-Type": "application/json; charset=utf-8"}
        )

if __name__ == '__main__':
    unittest.main()
