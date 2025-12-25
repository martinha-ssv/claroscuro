import requests
import json

def generate_color_palette(*base_colors):
    """
    Generate a color palette based on a given base color using an external API.

    Args:
        base_color (str): The base color in hex format (e.g., '#ff5733').

    Returns:
        list: A list of colors in the generated palette.
    """
    json_data = {
        "mode": "transformer",
        "num_colors": 4,
        "temperature": "1.2",
        "num_results": 50,
        "adjacency": ["0", "65", "45", "35", "65", "0", "35", "65", "45", "35", "0", "35", "35", "65", "35", "0"],
        "palette": ["#ffffff", "-", "-", "-"]
    }
    
    response = requests.post(
        "https://api.huemint.com/color",
        json=json_data,
        headers={"Content-Type": "application/json; charset=utf-8"}
    )
    
    return response.json()

if __name__ == "__main__":
    base_colors = ['#ff5733', '#33ff57', '#3357ff']
    palette = generate_color_palette(*base_colors)
    print(json.dumps(palette, indent=4))

    