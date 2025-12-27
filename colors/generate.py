import requests
import json
import numpy as np

def generate_color_palette(n_colors=8, contrast=35, bw_contrast=80, n_results=10, temperature=1.2, mode='transformer'):
    """
    Generate a color palette based on a given base color using an external API.

    Args:
        base_color (str): The base color in hex format (e.g., '#ff5733').

    Returns:
        list: A list of colors in the generated palette.
    """
    adjacency = _adjancency_matrix_bw(n_colors, contrast, bw_contrast)
    print("Adjacency matrix:", adjacency)
    print("Adjacency matrix dtype:", type(adjacency))

    json_data = {
        "mode": mode,
        "num_colors": n_colors,
        "temperature": str(temperature),
        "num_results": n_results,
        "adjacency": adjacency, #["0", "65", "45", "35", "65", "0", "35", "65", "45", "35", "0", "35", "35", "65", "35", "0"],
        "palette": ["-"] * n_colors,
    }
    
    response = requests.post(
        "https://api.huemint.com/color",
        json=json_data,
        headers={"Content-Type": "application/json; charset=utf-8"}
    )
    
    return dict(response.json())


def _adjancency_matrix(n_colors, contrast, bw_contrast):
    """
    Build Huemint adjacency matrix without black & white.

    Indices:
      0.. = line colors
    """
    A = np.zeros((n_colors, n_colors), dtype=float)

    # line colors <-> line colors
    A[:, :] = contrast
    np.fill_diagonal(A, 0)
    A = A.flatten().astype(str).tolist()

    return A

def _adjancency_matrix_bw(n_colors, contrast, bw_contrast):
    """
    Build Huemint adjacency matrix including black & white
    as repulsive anchors.

    Indices:
      0 = white
      1 = black
      2.. = line colors
    """
    A = np.zeros((n_colors, n_colors), dtype=float)

    # white <-> black
    A[0, 1] = A[1, 0] = 0

    # line colors <-> white / black
    A[2:, 0] = bw_contrast
    A[0, 2:] = bw_contrast
    A[2:, 1] = bw_contrast
    A[1, 2:] = bw_contrast

    # line colors <-> line colors
    A[2:, 2:] = contrast
    np.fill_diagonal(A, 0)
    A = A.flatten().astype(str).tolist()

    return A