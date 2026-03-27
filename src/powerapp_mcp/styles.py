"""gblAppStyles generation — semantic color tokens for light/dark/high-contrast themes.

Based on patterns from Microsoft Teams Power Apps templates. Every MS template
app computes a gblAppStyles record in App.OnStart that controls reference
instead of hardcoded RGBA values. This enables theme switching.
"""

from __future__ import annotations


# Semantic style presets per theme mode
_STYLE_PRESETS: dict[str, dict[str, str]] = {
    "default": {
        "HeaderFill": "RGBA(56, 96, 178, 1)",
        "HeaderFontColor": "RGBA(255, 255, 255, 1)",
        "ScreenFill": "RGBA(245, 245, 245, 1)",
        "CardFill": "RGBA(255, 255, 255, 1)",
        "CardBorderColor": "RGBA(237, 237, 237, 1)",
        "PrimaryButtonFill": "RGBA(56, 96, 178, 1)",
        "PrimaryButtonColor": "RGBA(255, 255, 255, 1)",
        "SecondaryButtonFill": "RGBA(255, 255, 255, 1)",
        "SecondaryButtonColor": "RGBA(56, 96, 178, 1)",
        "SecondaryButtonBorder": "RGBA(56, 96, 178, 1)",
        "TextPrimary": "RGBA(51, 51, 51, 1)",
        "TextSecondary": "RGBA(102, 102, 102, 1)",
        "TextDisabled": "RGBA(166, 166, 166, 1)",
        "InputFill": "RGBA(255, 255, 255, 1)",
        "InputBorderColor": "RGBA(0, 0, 0, 0.4)",
        "InputFocusBorderColor": "RGBA(56, 96, 178, 1)",
        "DividerColor": "RGBA(237, 237, 237, 1)",
        "IconColor": "RGBA(56, 96, 178, 1)",
        "IconSecondary": "RGBA(102, 102, 102, 1)",
        "SuccessColor": "RGBA(16, 124, 16, 1)",
        "ErrorColor": "RGBA(196, 49, 75, 1)",
        "WarningColor": "RGBA(255, 185, 0, 1)",
        "ListItemHoverFill": "RGBA(245, 245, 245, 1)",
        "ListItemSelectedFill": "RGBA(56, 96, 178, 0.1)",
        "GalleryFill": "RGBA(255, 255, 255, 1)",
        "SearchFill": "RGBA(255, 255, 255, 1)",
        "SearchBorder": "RGBA(0, 0, 0, 0.4)",
    },
    "dark": {
        "HeaderFill": "RGBA(30, 30, 30, 1)",
        "HeaderFontColor": "RGBA(255, 255, 255, 1)",
        "ScreenFill": "RGBA(18, 18, 18, 1)",
        "CardFill": "RGBA(40, 40, 40, 1)",
        "CardBorderColor": "RGBA(60, 60, 60, 1)",
        "PrimaryButtonFill": "RGBA(10, 132, 255, 1)",
        "PrimaryButtonColor": "RGBA(255, 255, 255, 1)",
        "SecondaryButtonFill": "RGBA(40, 40, 40, 1)",
        "SecondaryButtonColor": "RGBA(10, 132, 255, 1)",
        "SecondaryButtonBorder": "RGBA(10, 132, 255, 1)",
        "TextPrimary": "RGBA(255, 255, 255, 1)",
        "TextSecondary": "RGBA(180, 180, 180, 1)",
        "TextDisabled": "RGBA(100, 100, 100, 1)",
        "InputFill": "RGBA(45, 45, 45, 1)",
        "InputBorderColor": "RGBA(100, 100, 100, 1)",
        "InputFocusBorderColor": "RGBA(10, 132, 255, 1)",
        "DividerColor": "RGBA(60, 60, 60, 1)",
        "IconColor": "RGBA(10, 132, 255, 1)",
        "IconSecondary": "RGBA(180, 180, 180, 1)",
        "SuccessColor": "RGBA(48, 209, 88, 1)",
        "ErrorColor": "RGBA(255, 69, 58, 1)",
        "WarningColor": "RGBA(255, 159, 10, 1)",
        "ListItemHoverFill": "RGBA(50, 50, 50, 1)",
        "ListItemSelectedFill": "RGBA(10, 132, 255, 0.15)",
        "GalleryFill": "RGBA(40, 40, 40, 1)",
        "SearchFill": "RGBA(45, 45, 45, 1)",
        "SearchBorder": "RGBA(100, 100, 100, 1)",
    },
}


def get_style_preset(theme_name: str) -> dict[str, str]:
    """Get the style preset for a theme name."""
    if theme_name in _STYLE_PRESETS:
        return _STYLE_PRESETS[theme_name]
    # Map common names
    if "dark" in theme_name.lower():
        return _STYLE_PRESETS["dark"]
    return _STYLE_PRESETS["default"]


def generate_app_styles_formula(theme_name: str) -> str:
    """Generate a Set(gblAppStyles, {...}) Power Fx formula for App.OnStart.

    The formula creates a record of semantic color tokens that controls
    reference instead of hardcoded RGBA values.
    """
    preset = get_style_preset(theme_name)
    fields = ",\n        ".join(
        f"{key}: {value}" for key, value in preset.items()
    )
    return f"Set(gblAppStyles, {{\n        {fields}\n    }})"


def get_style_keys() -> list[str]:
    """Return all available style token names."""
    return list(_STYLE_PRESETS["default"].keys())
