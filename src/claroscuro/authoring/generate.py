import requests
import json
import numpy as np
from .processing import saturation

class ThemeGenerator:
    """
    Generate a color palette using an external API.

    Args:
        base_color (str): The base color in hex format (e.g., '#ff5733').

    Returns:
        list: A list of colors in the generated palette.
    """

    def __init__(self, n_colors: int = 8, contrast: int = 0, n_results: int = 20, temperature: float = 1.2, mode: str = 'random'):
        self.n_colors = n_colors
        self.contrast = contrast
        self.n_results = n_results
        self.temperature = temperature
        self.mode = mode

        self.palettes = self.generate_palettes_from_api()


    def generate(self):
        """
        Generate a color palette using an external API.

        Args:
            base_color (str): The base color in hex format (e.g., '#ff5733').

        Returns:
            list: A list of colors in the generated palette.
        """
        adjacency = self._adjancency_matrix(self.n_colors, self.contrast, 0)

        json_data = {
            "mode": self.mode,
            "num_colors": self.n_colors,
            "temperature": str(self.temperature),
            "num_results": self.n_results,
            "adjacency": adjacency, 
            "palette": ["-"] * self.n_colors,
        }
        
        response = requests.post(
            "https://api.huemint.com/color",
            json=json_data,
            headers={"Content-Type": "application/json; charset=utf-8"}
        )

        palettes = [sorted(result['palette'], key=saturation, reverse=True) for result in response.json().get('results', [])]
        
        return palettes


    def _adjancency_matrix(self):
        """
        Build Huemint adjacency matrix without black & white.

        Indices:
        0.. = line colors
        """
        A = np.zeros((self.n_colors, self.n_colors), dtype=float)

        # line colors <-> line colors
        A[:, :] = self.contrast
        np.fill_diagonal(A, 0)
        A = A.flatten().astype(str).tolist()

        return A

class Palette:
    def __init__(self, colors):
        self.colors = colors

        