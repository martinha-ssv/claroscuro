import requests
import numpy as np
from .metrics import saturation

HUEMINT_URL = "https://api.huemint.com/color"


def generate_color_palettes(n_colors=8, contrast=0, n_results=10, temperature=1.2, mode='random'):
    """
    Generate candidate color palettes using the Huemint API.

    Args:
        n_colors (int): Number of colors per palette.
        contrast (float): Pairwise contrast constraint sent to the API.
        n_results (int): Number of palettes to request.
        temperature (float): Randomness of the generation.
        mode (str): Huemint generation mode.

    Returns:
        list[list[str]]: Palettes (hex colors), each sorted by decreasing saturation.
    """
    adjacency = _adjacency_matrix(n_colors, contrast)

    json_data = {
        "mode": mode,
        "num_colors": n_colors,
        "temperature": str(temperature),
        "num_results": n_results,
        "adjacency": adjacency,
        "palette": ["-"] * n_colors,
    }

    response = requests.post(
        HUEMINT_URL,
        json=json_data,
        headers={"Content-Type": "application/json; charset=utf-8"}
    )

    palettes = [sorted(result['palette'], key=saturation, reverse=True) for result in response.json().get('results', [])]

    return palettes


def _adjacency_matrix(n_colors, contrast):
    """Build the Huemint adjacency matrix: every pair of colors gets the same contrast."""
    A = np.zeros((n_colors, n_colors), dtype=float)
    A[:, :] = contrast
    np.fill_diagonal(A, 0)
    return A.flatten().astype(str).tolist()
