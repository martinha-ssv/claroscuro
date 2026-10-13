from pathlib import Path
import pytest
import claroscuro.authoring.build as build_mod

pytestmark = pytest.mark.integration

def test_build_colors_creates_light_and_dark_files(tmp_path):
    dark_palette = ["#000000", "#111111"]
    light_palette = ["#ffffff", "#eeeeee"]

    build_mod.build_colors(
        dark_palette=dark_palette,
        light_palette=light_palette,
        STYLES_DIR=tmp_path,
    )

    assert (tmp_path / "colors_light.mplstyle").exists()
    assert (tmp_path / "colors_dark.mplstyle").exists()


def test_build_colors_writes_correct_prop_cycle(tmp_path):
    dark_palette = ["#000000", "#111111"]
    light_palette = ["#ffffff", "#eeeeee"]

    build_mod.build_colors(
        dark_palette=dark_palette,
        light_palette=light_palette,
        STYLES_DIR=tmp_path,
    )

    light_text = (tmp_path / "colors_light.mplstyle").read_text()
    dark_text = (tmp_path / "colors_dark.mplstyle").read_text()

    assert "axes.prop_cycle" in light_text
    assert "axes.prop_cycle" in dark_text

    for color in light_palette:
        assert color in light_text

    for color in dark_palette:
        assert color in dark_text


def test_build_colors_accepts_string_path(tmp_path):
    styles_dir = str(tmp_path)

    build_mod.build_colors(
        dark_palette=["#000"],
        light_palette=["#fff"],
        STYLES_DIR=styles_dir,
    )

    assert (tmp_path / "colors_light.mplstyle").exists()


def test_build_style_calls_build_colors(monkeypatch, tmp_path):
    called = {}

    def fake_build_colors(dark_palette, light_palette, STYLES_DIR):
        called["dark"] = dark_palette
        called["light"] = light_palette
        called["dir"] = STYLES_DIR

    monkeypatch.setattr(build_mod, "build_colors", fake_build_colors)

    dark = ["#000"]
    light = ["#fff"]

    build_mod.build_style(
        dark_palette=dark,
        light_palette=light,
        STYLES_DIR=tmp_path,
    )

    assert called == {
        "dark": dark,
        "light": light,
        "dir": tmp_path,
    }
