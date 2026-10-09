from cycler import cycler
from pathlib import Path

def build_style(dark_palette, light_palette, STYLES_DIR):
    """Build a Matplotlib style sheet from given color palettes.

    Args:
        dark_palette (list): List of colors for dark theme.
        light_palette (list): List of colors for light theme.
        STYLES_DIR (str | Path): Directory to save the generated style sheet.
    """

    build_colors(dark_palette, light_palette, STYLES_DIR)

def build_colors(dark_palette: list[str], light_palette: list[str], STYLES_DIR: str | Path):
    '''Generate color style sheets for dark and light themes. '''

    light_cycler = cycler(color=light_palette)
    dark_cycler = cycler(color=dark_palette)

    for theme, cycler_colors in [('light', light_cycler), ('dark', dark_cycler)]:
        style_lines = [
            f"# Claroscuro generated style sheet - {theme} theme",
            "",
            f"axes.prop_cycle: {str(cycler_colors)}",
            "",
        ]

        output_path = Path(STYLES_DIR) / f"colors_{theme}.mplstyle"
        with open(output_path, 'w') as f:
            f.write('\n'.join(style_lines))