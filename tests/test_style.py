from pathlib import Path
import pytest
import claroscuro.style as style_mod

def _make_styles(tmp_path, names):
    styles_dir = tmp_path / "styles"
    styles_dir.mkdir()
    for name in names:
        (styles_dir / name).touch()
    return styles_dir


def test_get_styles_returns_paths(monkeypatch, tmp_path):
    styles_dir = _make_styles(
        tmp_path,
        [
            "scale_paper.mplstyle",
            "colors_light.mplstyle",
        ],
    )

    monkeypatch.setattr(style_mod, "STYLE_DIR", styles_dir)

    styles = style_mod._get_styles()

    assert all(isinstance(s, Path) for s in styles)


def test_base_style_is_first(monkeypatch, tmp_path):
    styles_dir = _make_styles(
        tmp_path,
        [
            "scale_paper.mplstyle",
            "colors_light.mplstyle",
        ],
    )

    monkeypatch.setattr(style_mod, "STYLE_DIR", styles_dir)

    styles = style_mod._get_styles()

    assert styles[0] == styles_dir / "base.mplstyle"


def test_filters_by_variant_or_theme(monkeypatch, tmp_path):
    styles_dir = _make_styles(
        tmp_path,
        [
            "scale_paper.mplstyle",     # variant match
            "colors_light.mplstyle",    # theme match
            "bg_dark.mplstyle",         # no match
            "notes.txt",                # wrong extension
        ],
    )

    monkeypatch.setattr(style_mod, "STYLE_DIR", styles_dir)

    styles = style_mod._get_styles(variant="paper", theme="light")

    names = {s.name for s in styles}

    assert "scale_paper.mplstyle" in names
    assert "colors_light.mplstyle" in names
    assert "bg_dark.mplstyle" not in names
    assert "notes.txt" not in names


def test_styles_are_sorted_after_base(monkeypatch, tmp_path):
    styles_dir = _make_styles(
        tmp_path,
        [
            "zeta_light.mplstyle",
            "alpha_paper.mplstyle",
        ],
    )

    monkeypatch.setattr(style_mod, "STYLE_DIR", styles_dir)

    styles = style_mod._get_styles()

    assert styles[1:] == sorted(styles[1:])

@pytest.mark.mpl
def test_use_forwards_styles_to_matplotlib(monkeypatch):
    import matplotlib.pyplot as plt

    called = {}

    def fake_use(*styles):
        called["styles"] = styles

    monkeypatch.setattr(plt.style, "use", fake_use)

    styles = [Path("a.mplstyle"), Path("b.mplstyle")]
    style_mod._use(*styles)

    assert called["styles"] == tuple(styles)

@pytest.mark.mpl
def test_style_calls_get_styles_and_use(monkeypatch):
    fake_styles = [Path("base.mplstyle"), Path("paper_light.mplstyle")]

    called = {}

    def fake_get_styles(*, variant, theme):
        called["variant"] = variant
        called["theme"] = theme
        return fake_styles

    def fake_use(*styles):
        called["used"] = styles

    monkeypatch.setattr(style_mod, "_get_styles", fake_get_styles)
    monkeypatch.setattr(style_mod, "_use", fake_use)

    style_mod._style(variant="paper", bg="light")

    assert called["variant"] == "paper"
    assert called["theme"] == "light"
    assert called["used"] == tuple(fake_styles)

@pytest.mark.mpl
def test_paper_calls_style_with_correct_defaults(monkeypatch):
    called = {}

    def fake_style(*, variant, bg):
        called["variant"] = variant
        called["bg"] = bg

    monkeypatch.setattr(style_mod, "_style", fake_style)

    style_mod.paper()

    assert called == {"variant": "paper", "bg": "light"}

@pytest.mark.mpl
def test_slides_calls_style_with_correct_defaults(monkeypatch):
    called = {}

    def fake_style(*, variant, bg):
        called["variant"] = variant
        called["bg"] = bg

    monkeypatch.setattr(style_mod, "_style", fake_style)

    style_mod.slides()

    assert called == {"variant": "slides", "bg": "dark"}

@pytest.mark.mpl
def test_notebook_calls_style_with_correct_defaults(monkeypatch):
    called = {}

    def fake_style(*, variant, bg):
        called["variant"] = variant
        called["bg"] = bg

    monkeypatch.setattr(style_mod, "_style", fake_style)

    style_mod.notebook()

    assert called == {"variant": "notebook", "bg": "light"}
