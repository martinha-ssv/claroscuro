import importlib
import pkgutil

import numpy as np
import pytest

import claroscuro
from claroscuro.authoring.processing import generate as generate_mod
from claroscuro.authoring.processing.metrics import calculate_contrast, saturation
from claroscuro.authoring.processing.spaces import cielab_to_hex, hex_to_cielab


def _all_modules():
    return [
        m.name
        for m in pkgutil.walk_packages(claroscuro.__path__, prefix="claroscuro.")
        if not m.name.endswith(".__main__")
    ]


@pytest.mark.unit
@pytest.mark.parametrize("name", _all_modules())
def test_every_module_imports(name):
    importlib.import_module(name)


@pytest.mark.unit
def test_hex_lab_round_trip():
    assert cielab_to_hex(hex_to_cielab("#336699")) == "#336699"


@pytest.mark.unit
def test_contrast_is_zero_for_same_color_and_large_for_black_white():
    assert calculate_contrast("#808080", "#808080") == pytest.approx(0)
    assert calculate_contrast("#000000", "#ffffff") == pytest.approx(100, abs=0.5)


@pytest.mark.unit
def test_gray_has_no_saturation_and_red_has_a_lot():
    assert saturation("#777777") < 1
    assert saturation("#ff0000") > 50


@pytest.mark.unit
def test_adjacency_matrix_is_flat_string_list_with_zero_diagonal():
    adjacency = generate_mod._adjacency_matrix(3, 30)

    assert adjacency == ["0.0", "30.0", "30.0", "30.0", "0.0", "30.0", "30.0", "30.0", "0.0"]


@pytest.mark.unit
def test_generate_color_palettes_sorts_by_saturation_and_posts_expected_payload(monkeypatch):
    captured = {}

    class FakeResponse:
        def json(self):
            return {"results": [{"palette": ["#777777", "#ff0000", "#aa5555"]}]}

    def fake_post(url, json, headers):
        captured["url"] = url
        captured["json"] = json
        return FakeResponse()

    monkeypatch.setattr(generate_mod.requests, "post", fake_post)

    palettes = generate_mod.generate_color_palettes(n_colors=3, n_results=1)

    assert palettes == [["#ff0000", "#aa5555", "#777777"]]
    assert captured["url"] == "https://api.huemint.com/color"
    assert captured["json"]["num_colors"] == 3
    assert captured["json"]["mode"] == "random"
    assert captured["json"]["palette"] == ["-", "-", "-"]
    assert len(captured["json"]["adjacency"]) == 9
