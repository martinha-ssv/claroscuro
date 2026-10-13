from pathlib import Path
import matplotlib.pyplot as plt
import os

STYLE_DIR = Path(__file__).parent / "styles"

def _get_styles(
    variant: str = "paper",
    theme: str = "light",
) -> list[Path]:
    styles = []
    for path in STYLE_DIR.glob("*.mplstyle"):
        name = path.name
        if variant in name or theme in name:
            styles.append(path)

    return [STYLE_DIR / "base.mplstyle", *sorted(styles)]

def _use(*styles) -> None:
    """Apply the given style sheets.

    Args:
        *styles: Style sheet names to apply.
    """
    plt.style.use(*styles)

def _style(variant: str, bg: str) -> None:
    """Apply the 'paper' variant style sheet.

    Args:
        bg: Background theme, either 'light' or 'dark'.
    """
    styles = _get_styles(variant=variant, theme=bg)
    _use(*styles)


def paper(bg: str = "light") -> None:
    """Apply the 'paper' variant style sheet.

    Args:
        bg: Background theme, either 'light' or 'dark'.
    """
    _style(variant="paper", bg=bg)

def slides(bg: str = "dark") -> None:
    """Apply the 'slides' variant style sheet.

    Args:
        bg: Background theme, either 'light' or 'dark'.
    """
    _style(variant="slides", bg=bg)

def notebook(bg: str = "light") -> None:
    """Apply the 'notebook' variant style sheet.

    Args:
        bg: Background theme, either 'light' or 'dark'.
    """
    _style(variant="notebook", bg=bg)