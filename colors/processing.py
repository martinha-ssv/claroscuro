from colorspacious import cspace_convert
import numpy as np

def hex_to_cielab(hex_color):
    """Convert hex color to CIELAB color space."""
    hex_color = hex_color.lstrip('#')
    rgb = np.array([int(hex_color[i:i+2], 16) for i in (0, 2, 4)]) / 255.0
    lab = cspace_convert(rgb, "sRGB1", "CIELab")
    return lab

def cielab_to_hex(lab_color):
    """Convert CIELAB color space to hex color."""
    rgb = cspace_convert(lab_color, "CIELab", "sRGB1")
    rgb = np.clip(rgb * 255, 0, 255).astype(int)
    hex_color = '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])
    return hex_color

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

