"""Built-in themes for Power Apps."""

from __future__ import annotations

import json
from pathlib import Path

from .models import ThemeDefinition, ThemePaletteEntry

_DATA_DIR = Path(__file__).parent / "data"

# Loaded lazily
_default_theme_data: dict | None = None


def _load_default_theme() -> dict:
    global _default_theme_data
    if _default_theme_data is None:
        path = _DATA_DIR / "default_theme.json"
        if path.exists():
            with open(path) as f:
                _default_theme_data = json.load(f)
        else:
            _default_theme_data = {
                "CurrentTheme": "defaultTheme",
                "CustomThemes": [{
                    "name": "defaultTheme",
                    "palette": [],
                }],
            }
    return _default_theme_data


def get_default_theme() -> ThemeDefinition:
    """Get the default theme as a Pydantic model."""
    data = _load_default_theme()
    themes = data.get("CustomThemes", [])
    if themes:
        t = themes[0]
        return ThemeDefinition(
            name=t.get("name", "defaultTheme"),
            palette=[
                ThemePaletteEntry(**p) for p in t.get("palette", [])
            ],
        )
    return ThemeDefinition()


def get_dark_theme() -> ThemeDefinition:
    """Get a dark theme variant."""
    return ThemeDefinition(
        name="darkTheme",
        palette=[
            ThemePaletteEntry(name="ScreenBkgColor", value="RGBA(30, 30, 30, 1)"),
            ThemePaletteEntry(name="PrimaryColor1", value="RGBA(10, 132, 255, 1)"),
            ThemePaletteEntry(name="PrimaryColor2", value="RGBA(100, 210, 255, 1)"),
            ThemePaletteEntry(name="PrimaryColor3", value="RGBA(0, 88, 170, 1)"),
            ThemePaletteEntry(name="TextMainColor", value="RGBA(255, 255, 255, 1)"),
            ThemePaletteEntry(name="TextMainColorInverted", value="RGBA(0, 0, 0, 1)"),
            ThemePaletteEntry(name="InputBkgColor", value="RGBA(45, 45, 45, 1)"),
            ThemePaletteEntry(name="InputBorderColor", value="RGBA(100, 100, 100, 1)"),
            ThemePaletteEntry(name="ReservedSuccessColor", value="RGBA(48, 209, 88, 1)"),
            ThemePaletteEntry(name="ReservedErrorColor", value="RGBA(255, 69, 58, 1)"),
            ThemePaletteEntry(name="ReservedWarningColor", value="RGBA(255, 159, 10, 1)"),
        ],
    )


def get_theme_by_name(name: str) -> ThemeDefinition:
    """Get a theme by name. Falls back to default."""
    if name == "dark":
        return get_dark_theme()
    return get_default_theme()


def generate_themes_json(theme: ThemeDefinition) -> dict:
    """Generate the Themes.json structure for the .msapp."""
    data = _load_default_theme()
    # Override with the provided theme
    data["CurrentTheme"] = theme.name
    data["CustomThemes"] = [{
        "name": theme.name,
        "palette": [p.model_dump() for p in theme.palette],
    }]
    return data
