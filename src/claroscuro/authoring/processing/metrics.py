import numpy as np
from .spaces import hex_to_cielab

def calculate_contrast(color1, color2):
    """Calculate contrast between two colors in CIELAB space."""
    lab1 = hex_to_cielab(color1)
    lab2 = hex_to_cielab(color2)
    delta_e = np.linalg.norm(lab1 - lab2)
    return delta_e

def saturation(hex_color):
    """Calculate saturation of a color in CIELAB space."""
    lab = hex_to_cielab(hex_color)
    a, b = lab[1], lab[2]
    sat = np.sqrt(a**2 + b**2)
    return sat
