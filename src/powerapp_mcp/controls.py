"""Control factory — creates controls with correct defaults per type."""

from __future__ import annotations

import json
from typing import Any

from .models import AppState, Control, Rule, Template

# Template URI pattern: http://microsoft.com/appmagic/{name}
_TEMPLATE_BASE = "http://microsoft.com/appmagic"

# Known template versions (from reference app + MS Teams templates repo)
_TEMPLATE_VERSIONS: dict[str, str] = {
    "appinfo": "2.1.0",
    "screen": "2.5.0",
    "button": "2.2.0",
    "label": "2.5.1",
    "text": "2.3.2",
    "rectangle": "2.3.0",
    "circle": "2.3.0",
    "triangle": "2.2.0",
    "icon": "2.5.0",
    "textInput": "2.5.0",
    "dropdown": "2.3.1",
    "combobox": "2.4.0",
    "gallery": "2.13.2",
    "galleryTemplate": "2.13.2",
    "form": "2.4.0",
    "formViewer": "2.1.0",
    "typedDataCard": "2.0.0",
    "dataCard": "2.0.0",
    "fluidGrid": "2.3.0",
    "rating": "2.1.0",
    "timer": "2.1.0",
    "image": "2.2.2",
    "checkbox": "2.1.0",
    "toggle": "2.1.0",
    "toggleSwitch": "2.1.0",
    "slider": "2.1.0",
    "radio": "2.3.0",
    "datePicker": "2.3.0",
    "htmlViewer": "2.1.0",
    "richTextEditor": "2.6.0",
    "penInput": "2.0.0",
    "camera": "2.0.0",
    "videoPlayback": "2.3.2",
    "audioPlayback": "2.0.0",
    "microsoftStreamPlayback": "2.2.0",
    "pdfViewer": "2.0.0",
    "barcodeReader": "2.0.0",
    "columnChart": "2.0.0",
    "lineChart": "2.2.0",
    "pieChart": "2.2.0",
    "legend": "2.1.0",
    "dataTable": "2.0.0",
    "container": "2.0.0",
    "groupContainer": "1.1.0",
    "horizontalAutoLayout": "2.0.0",
    "verticalAutoLayout": "2.0.0",
    "gridContainer": "2.0.0",
    "group": "2.0.0",
    "listbox": "2.2.0",
    "listBox": "2.2.0",
    "addMedia": "2.2.1",
    "addPicture": "2.0.0",
    "attachments": "2.3.0",
    "microphone": "2.0.0",
    "map": "2.0.0",
}


def _make_template(control_type: str) -> Template:
    """Create a Template object for the given control type."""
    version = _TEMPLATE_VERSIONS.get(control_type, "2.0.0")
    # Special case: "text" is the actual template name for label
    template_name = control_type
    return Template(
        Id=f"{_TEMPLATE_BASE}/{template_name}",
        Version=version,
        LastModifiedTimestamp="0",
        Name=template_name,
    )


def _rule(prop: str, category: str, script: str, provider: str = "Unknown") -> Rule:
    """Shorthand for creating a Rule."""
    return Rule(
        Property=prop,
        Category=category,
        InvariantScript=script,
        RuleProviderType=provider,
    )


def _design(prop: str, script: str) -> Rule:
    return _rule(prop, "Design", script)


def _data(prop: str, script: str) -> Rule:
    return _rule(prop, "Data", script)


def _behavior(prop: str, script: str) -> Rule:
    return _rule(prop, "Behavior", script)


# Public aliases for use by screen_patterns and app_templates
design = _design
data = _data
behavior = _behavior


# ── Default rules per control type ──────────────────────────────────────


def _screen_defaults(width: int, height: int) -> list[Rule]:
    return [
        _design("Fill", "RGBA(255, 255, 255, 1)"),
        _design("Height", str(height)),
        _design("Width", str(width)),
        _design("Size", "1 + CountRows(App.SizeBreakpoints) - CountIf(App.SizeBreakpoints, Value >= App.Width)"),
        _design("Orientation", "If(Self.Width < Self.Height, Layout.Vertical, Layout.Horizontal)"),
        _design("LoadingSpinner", "LoadingSpinner.None"),
        _design("LoadingSpinnerColor", "Self.Fill"),
        _design("ImagePosition", "ImagePosition.Fit"),
    ]


def _button_defaults() -> list[Rule]:
    return [
        _data("Text", '"Button"'),
        _design("X", "0"),
        _design("Y", "0"),
        _design("Width", "200"),
        _design("Height", "50"),
        _design("ZIndex", "1"),
        _design("Fill", "RGBA(56, 96, 178, 1)"),
        _design("Color", "RGBA(255, 255, 255, 1)"),
        _design("BorderColor", "ColorFade(Self.Fill, -15%)"),
        _design("BorderStyle", "BorderStyle.Solid"),
        _design("BorderThickness", "2"),
        _design("DisabledFill", "RGBA(244, 244, 244, 1)"),
        _design("DisabledColor", "RGBA(166, 166, 166, 1)"),
        _design("DisabledBorderColor", "RGBA(166, 166, 166, 1)"),
        _design("HoverFill", "ColorFade(RGBA(56, 96, 178, 1), -20%)"),
        _design("HoverColor", "Self.Color"),
        _design("HoverBorderColor", "ColorFade(Self.BorderColor, 20%)"),
        _design("PressedFill", "ColorFade(RGBA(56, 96, 178, 1), -50%)"),
        _design("PressedColor", "Self.Color"),
        _design("PressedBorderColor", "Self.Fill"),
        _design("FocusedBorderColor", "Self.BorderColor"),
        _design("FocusedBorderThickness", "4"),
        _design("Font", "Font.'Open Sans'"),
        _design("FontWeight", "FontWeight.Semibold"),
        _design("Size", "15"),
        _design("Align", "Align.Center"),
        _design("RadiusTopLeft", "5"),
        _design("RadiusTopRight", "5"),
        _design("RadiusBottomLeft", "5"),
        _design("RadiusBottomRight", "5"),
        _design("DisplayMode", "DisplayMode.Edit"),
        _design("Visible", "true"),
        _behavior("OnSelect", "false"),
    ]


def _label_defaults() -> list[Rule]:
    return [
        _data("Text", '"Text"'),
        _design("X", "0"),
        _design("Y", "0"),
        _design("Width", "200"),
        _design("Height", "40"),
        _design("ZIndex", "1"),
        _design("Fill", "RGBA(0, 0, 0, 0)"),
        _design("Color", "RGBA(0, 0, 0, 1)"),
        _design("BorderColor", "RGBA(0, 0, 0, 0)"),
        _design("BorderStyle", "BorderStyle.Solid"),
        _design("BorderThickness", "0"),
        _design("DisabledFill", "RGBA(0, 0, 0, 0)"),
        _design("DisabledColor", "RGBA(166, 166, 166, 1)"),
        _design("DisabledBorderColor", "RGBA(0, 0, 0, 0)"),
        _design("HoverFill", "RGBA(0, 0, 0, 0)"),
        _design("HoverColor", "Self.Color"),
        _design("HoverBorderColor", "Self.BorderColor"),
        _design("PressedFill", "RGBA(0, 0, 0, 0)"),
        _design("PressedColor", "Self.Color"),
        _design("PressedBorderColor", "Self.BorderColor"),
        _design("FocusedBorderColor", "Self.BorderColor"),
        _design("FocusedBorderThickness", "4"),
        _design("Font", "Font.'Open Sans'"),
        _design("FontWeight", "FontWeight.Normal"),
        _design("Size", "13"),
        _design("Align", "Align.Left"),
        _design("VerticalAlign", "VerticalAlign.Middle"),
        _design("Overflow", "Overflow.Hidden"),
        _design("PaddingLeft", "5"),
        _design("PaddingRight", "5"),
        _design("PaddingTop", "5"),
        _design("PaddingBottom", "5"),
        _design("DisplayMode", "DisplayMode.Edit"),
        _design("Visible", "true"),
        _design("Live", "Live.Off"),
        _design("Role", "TextRole.Default"),
    ]


def _rectangle_defaults() -> list[Rule]:
    return [
        _design("X", "0"),
        _design("Y", "0"),
        _design("Width", "200"),
        _design("Height", "50"),
        _design("ZIndex", "1"),
        _design("Fill", "RGBA(56, 96, 178, 1)"),
        _design("BorderColor", "RGBA(0, 0, 0, 1)"),
        _design("BorderStyle", "BorderStyle.Solid"),
        _design("BorderThickness", "0"),
        _design("DisabledFill", "Self.Fill"),
        _design("HoverFill", "Self.Fill"),
        _design("PressedFill", "Self.Fill"),
        _design("FocusedBorderColor", "Self.BorderColor"),
        _design("FocusedBorderThickness", "4"),
        _design("DisplayMode", "DisplayMode.Edit"),
        _design("Visible", "true"),
    ]


def _icon_defaults() -> list[Rule]:
    return [
        _data("Icon", "Icon.Add"),
        _design("X", "0"),
        _design("Y", "0"),
        _design("Width", "50"),
        _design("Height", "50"),
        _design("ZIndex", "1"),
        _design("Fill", "RGBA(0, 0, 0, 0)"),
        _design("Color", "RGBA(0, 0, 0, 1)"),
        _design("BorderColor", "RGBA(0, 0, 0, 0)"),
        _design("BorderStyle", "BorderStyle.Solid"),
        _design("BorderThickness", "0"),
        _design("DisabledFill", "RGBA(244, 244, 244, 1)"),
        _design("DisabledColor", "RGBA(166, 166, 166, 1)"),
        _design("DisabledBorderColor", "RGBA(166, 166, 166, 1)"),
        _design("HoverFill", "RGBA(0, 0, 0, 0)"),
        _design("HoverColor", "Self.Color"),
        _design("HoverBorderColor", "Self.BorderColor"),
        _design("PressedFill", "RGBA(0, 0, 0, 0)"),
        _design("PressedColor", "Self.Color"),
        _design("PressedBorderColor", "Self.BorderColor"),
        _design("FocusedBorderColor", "Self.BorderColor"),
        _design("FocusedBorderThickness", "4"),
        _design("PaddingTop", "5"),
        _design("PaddingRight", "5"),
        _design("PaddingBottom", "5"),
        _design("PaddingLeft", "5"),
        _design("DisplayMode", "DisplayMode.Edit"),
        _design("Visible", "true"),
        _behavior("OnSelect", "false"),
    ]


def _text_input_defaults() -> list[Rule]:
    return [
        _data("Default", '""'),
        _data("HintText", '"Text input"'),
        _design("X", "0"),
        _design("Y", "0"),
        _design("Width", "270"),
        _design("Height", "50"),
        _design("ZIndex", "1"),
        _design("Fill", "RGBA(255, 255, 255, 1)"),
        _design("Color", "RGBA(0, 0, 0, 1)"),
        _design("BorderColor", "RGBA(0, 0, 0, 0.4)"),
        _design("BorderStyle", "BorderStyle.Solid"),
        _design("BorderThickness", "2"),
        _design("DisabledFill", "RGBA(244, 244, 244, 1)"),
        _design("DisabledColor", "RGBA(166, 166, 166, 1)"),
        _design("DisabledBorderColor", "RGBA(166, 166, 166, 1)"),
        _design("HoverFill", "Self.Fill"),
        _design("HoverColor", "Self.Color"),
        _design("HoverBorderColor", "Self.BorderColor"),
        _design("PressedFill", "Self.Fill"),
        _design("PressedColor", "Self.Color"),
        _design("PressedBorderColor", "Self.BorderColor"),
        _design("FocusedBorderColor", "Self.BorderColor"),
        _design("FocusedBorderThickness", "4"),
        _design("Font", "Font.'Open Sans'"),
        _design("FontWeight", "FontWeight.Normal"),
        _design("Size", "13"),
        _design("Align", "Align.Left"),
        _design("RadiusTopLeft", "5"),
        _design("RadiusTopRight", "5"),
        _design("RadiusBottomLeft", "5"),
        _design("RadiusBottomRight", "5"),
        _design("PaddingLeft", "12"),
        _design("PaddingRight", "5"),
        _design("PaddingTop", "5"),
        _design("PaddingBottom", "5"),
        _design("Mode", "TextMode.SingleLine"),
        _design("DisplayMode", "DisplayMode.Edit"),
        _design("Visible", "true"),
        _behavior("OnChange", "false"),
    ]


def _dropdown_defaults() -> list[Rule]:
    return [
        _data("Items", '["Option 1", "Option 2", "Option 3"]'),
        _design("X", "0"),
        _design("Y", "0"),
        _design("Width", "200"),
        _design("Height", "50"),
        _design("ZIndex", "1"),
        _design("Fill", "RGBA(255, 255, 255, 1)"),
        _design("Color", "RGBA(0, 0, 0, 1)"),
        _design("BorderColor", "RGBA(0, 0, 0, 0.4)"),
        _design("BorderStyle", "BorderStyle.Solid"),
        _design("BorderThickness", "2"),
        _design("ChevronFill", "RGBA(0, 0, 0, 1)"),
        _design("ChevronBackground", "RGBA(255, 255, 255, 1)"),
        _design("SelectionColor", "RGBA(0, 0, 0, 1)"),
        _design("SelectionFill", "RGBA(56, 96, 178, 0.2)"),
        _design("Font", "Font.'Open Sans'"),
        _design("Size", "13"),
        _design("DisplayMode", "DisplayMode.Edit"),
        _design("Visible", "true"),
        _behavior("OnChange", "false"),
    ]


def _gallery_defaults() -> list[Rule]:
    return [
        _data("Items", "[]"),
        _design("X", "0"),
        _design("Y", "0"),
        _design("Width", "500"),
        _design("Height", "400"),
        _design("ZIndex", "1"),
        _design("Fill", "RGBA(0, 0, 0, 0)"),
        _design("BorderColor", "RGBA(0, 0, 0, 1)"),
        _design("BorderStyle", "BorderStyle.None"),
        _design("BorderThickness", "0"),
        _design("TemplatePadding", "0"),
        _design("TemplateSize", "60"),
        _design("Layout", "Layout.Vertical"),
        _design("LoadingSpinner", "LoadingSpinner.None"),
        _design("Transition", "Transition.None"),
        _design("DisplayMode", "DisplayMode.Edit"),
        _design("Visible", "true"),
    ]


def _image_defaults() -> list[Rule]:
    return [
        _data("Image", '""'),
        _design("X", "0"),
        _design("Y", "0"),
        _design("Width", "200"),
        _design("Height", "200"),
        _design("ZIndex", "1"),
        _design("ImagePosition", "ImagePosition.Fit"),
        _design("BorderColor", "RGBA(0, 0, 0, 0)"),
        _design("BorderStyle", "BorderStyle.None"),
        _design("BorderThickness", "0"),
        _design("DisplayMode", "DisplayMode.Edit"),
        _design("Visible", "true"),
    ]


def _checkbox_defaults() -> list[Rule]:
    return [
        _data("Default", "false"),
        _data("Text", '"Option"'),
        _design("X", "0"),
        _design("Y", "0"),
        _design("Width", "200"),
        _design("Height", "40"),
        _design("ZIndex", "1"),
        _design("Fill", "RGBA(0, 0, 0, 0)"),
        _design("Color", "RGBA(0, 0, 0, 1)"),
        _design("BorderColor", "RGBA(0, 0, 0, 0)"),
        _design("CheckboxBackgroundFill", "RGBA(255, 255, 255, 1)"),
        _design("CheckboxBorderColor", "RGBA(0, 0, 0, 0.6)"),
        _design("CheckmarkFill", "RGBA(255, 255, 255, 1)"),
        _design("CheckboxSize", "26"),
        _design("Font", "Font.'Open Sans'"),
        _design("Size", "15"),
        _design("DisplayMode", "DisplayMode.Edit"),
        _design("Visible", "true"),
        _behavior("OnCheck", "false"),
        _behavior("OnUncheck", "false"),
    ]


def _toggle_defaults() -> list[Rule]:
    return [
        _data("Default", "false"),
        _design("X", "0"),
        _design("Y", "0"),
        _design("Width", "160"),
        _design("Height", "44"),
        _design("ZIndex", "1"),
        _design("TrueFill", "RGBA(56, 96, 178, 1)"),
        _design("FalseFill", "RGBA(186, 186, 186, 1)"),
        _design("HandleFill", "RGBA(255, 255, 255, 1)"),
        _design("Color", "RGBA(0, 0, 0, 1)"),
        _design("Font", "Font.'Open Sans'"),
        _design("Size", "13"),
        _design("DisplayMode", "DisplayMode.Edit"),
        _design("Visible", "true"),
        _behavior("OnChange", "false"),
    ]


def _slider_defaults() -> list[Rule]:
    return [
        _data("Default", "50"),
        _design("X", "0"),
        _design("Y", "0"),
        _design("Width", "300"),
        _design("Height", "48"),
        _design("ZIndex", "1"),
        _design("Min", "0"),
        _design("Max", "100"),
        _design("HandleFill", "RGBA(56, 96, 178, 1)"),
        _design("HandleActiveFill", "RGBA(56, 96, 178, 1)"),
        _design("HandleHoverFill", "ColorFade(RGBA(56, 96, 178, 1), -20%)"),
        _design("ValueFill", "RGBA(56, 96, 178, 1)"),
        _design("RailFill", "RGBA(204, 204, 204, 1)"),
        _design("Layout", "Layout.Horizontal"),
        _design("DisplayMode", "DisplayMode.Edit"),
        _design("Visible", "true"),
        _behavior("OnChange", "false"),
    ]


def _rating_defaults() -> list[Rule]:
    return [
        _data("Default", "0"),
        _design("X", "0"),
        _design("Y", "0"),
        _design("Width", "200"),
        _design("Height", "50"),
        _design("ZIndex", "1"),
        _design("Fill", "RGBA(0, 0, 0, 0)"),
        _design("RatingFill", "RGBA(255, 193, 7, 1)"),
        _design("BorderColor", "RGBA(0, 0, 0, 0)"),
        _design("BorderStyle", "BorderStyle.None"),
        _design("Max", "5"),
        _design("DisplayMode", "DisplayMode.Edit"),
        _design("Visible", "true"),
        _behavior("OnChange", "false"),
    ]


def _date_picker_defaults() -> list[Rule]:
    return [
        _design("X", "0"),
        _design("Y", "0"),
        _design("Width", "270"),
        _design("Height", "50"),
        _design("ZIndex", "1"),
        _design("Fill", "RGBA(255, 255, 255, 1)"),
        _design("Color", "RGBA(0, 0, 0, 1)"),
        _design("BorderColor", "RGBA(0, 0, 0, 0.4)"),
        _design("BorderStyle", "BorderStyle.Solid"),
        _design("BorderThickness", "2"),
        _design("IconFill", "RGBA(0, 0, 0, 1)"),
        _design("IconBackground", "RGBA(255, 255, 255, 1)"),
        _design("Font", "Font.'Open Sans'"),
        _design("Size", "13"),
        _design("DisplayMode", "DisplayMode.Edit"),
        _design("Visible", "true"),
        _behavior("OnChange", "false"),
    ]


def _radio_defaults() -> list[Rule]:
    return [
        _data("Items", '["Option 1", "Option 2", "Option 3"]'),
        _design("X", "0"),
        _design("Y", "0"),
        _design("Width", "200"),
        _design("Height", "150"),
        _design("ZIndex", "1"),
        _design("Fill", "RGBA(0, 0, 0, 0)"),
        _design("Color", "RGBA(0, 0, 0, 1)"),
        _design("RadioBackgroundFill", "RGBA(255, 255, 255, 1)"),
        _design("RadioBorderColor", "RGBA(0, 0, 0, 0.6)"),
        _design("RadioSelectionFill", "RGBA(56, 96, 178, 1)"),
        _design("Font", "Font.'Open Sans'"),
        _design("Size", "13"),
        _design("Layout", "Layout.Vertical"),
        _design("DisplayMode", "DisplayMode.Edit"),
        _design("Visible", "true"),
        _behavior("OnChange", "false"),
    ]


def _timer_defaults() -> list[Rule]:
    return [
        _data("Duration", "60000"),
        _data("Start", "true"),
        _data("Repeat", "false"),
        _data("Text", '"Timer"'),
        _design("X", "0"),
        _design("Y", "0"),
        _design("Width", "200"),
        _design("Height", "50"),
        _design("ZIndex", "1"),
        _design("Fill", "RGBA(56, 96, 178, 1)"),
        _design("Color", "RGBA(255, 255, 255, 1)"),
        _design("Font", "Font.'Open Sans'"),
        _design("Size", "15"),
        _design("Align", "Align.Center"),
        _design("DisplayMode", "DisplayMode.Edit"),
        _design("Visible", "true"),
        _behavior("OnTimerEnd", "false"),
    ]


def _circle_defaults() -> list[Rule]:
    return [
        _design("X", "0"),
        _design("Y", "0"),
        _design("Width", "100"),
        _design("Height", "100"),
        _design("ZIndex", "1"),
        _design("Fill", "RGBA(56, 96, 178, 1)"),
        _design("BorderColor", "RGBA(0, 0, 0, 1)"),
        _design("BorderStyle", "BorderStyle.Solid"),
        _design("BorderThickness", "0"),
        _design("DisabledFill", "Self.Fill"),
        _design("HoverFill", "Self.Fill"),
        _design("PressedFill", "Self.Fill"),
        _design("FocusedBorderColor", "Self.BorderColor"),
        _design("FocusedBorderThickness", "4"),
        _design("DisplayMode", "DisplayMode.Edit"),
        _design("Visible", "true"),
    ]


def _triangle_defaults() -> list[Rule]:
    return [
        _design("X", "0"),
        _design("Y", "0"),
        _design("Width", "100"),
        _design("Height", "100"),
        _design("ZIndex", "1"),
        _design("Fill", "RGBA(56, 96, 178, 1)"),
        _design("BorderColor", "RGBA(0, 0, 0, 1)"),
        _design("BorderStyle", "BorderStyle.Solid"),
        _design("BorderThickness", "0"),
        _design("DisplayMode", "DisplayMode.Edit"),
        _design("Visible", "true"),
    ]


def _html_viewer_defaults() -> list[Rule]:
    return [
        _data("HtmlText", '""'),
        _design("X", "0"),
        _design("Y", "0"),
        _design("Width", "400"),
        _design("Height", "300"),
        _design("ZIndex", "1"),
        _design("Fill", "RGBA(255, 255, 255, 1)"),
        _design("BorderColor", "RGBA(0, 0, 0, 0)"),
        _design("BorderStyle", "BorderStyle.None"),
        _design("BorderThickness", "0"),
        _design("PaddingTop", "5"),
        _design("PaddingRight", "5"),
        _design("PaddingBottom", "5"),
        _design("PaddingLeft", "5"),
        _design("DisplayMode", "DisplayMode.Edit"),
        _design("Visible", "true"),
    ]


def _rich_text_editor_defaults() -> list[Rule]:
    return [
        _data("Default", '""'),
        _data("HintText", '"Enter rich text"'),
        _design("X", "0"),
        _design("Y", "0"),
        _design("Width", "400"),
        _design("Height", "250"),
        _design("ZIndex", "1"),
        _design("Fill", "RGBA(255, 255, 255, 1)"),
        _design("Color", "RGBA(0, 0, 0, 1)"),
        _design("BorderColor", "RGBA(0, 0, 0, 0.4)"),
        _design("BorderStyle", "BorderStyle.Solid"),
        _design("BorderThickness", "2"),
        _design("Font", "Font.'Open Sans'"),
        _design("Size", "13"),
        _design("DisplayMode", "DisplayMode.Edit"),
        _design("Visible", "true"),
        _behavior("OnChange", "false"),
    ]


def _data_table_defaults() -> list[Rule]:
    return [
        _data("Items", "[]"),
        _design("X", "0"),
        _design("Y", "0"),
        _design("Width", "500"),
        _design("Height", "400"),
        _design("ZIndex", "1"),
        _design("Fill", "RGBA(255, 255, 255, 1)"),
        _design("BorderColor", "RGBA(0, 0, 0, 0.4)"),
        _design("BorderStyle", "BorderStyle.Solid"),
        _design("BorderThickness", "1"),
        _design("HeadingFill", "RGBA(234, 234, 236, 1)"),
        _design("HeadingColor", "RGBA(0, 0, 0, 1)"),
        _design("HeadingSize", "13"),
        _design("HeadingFont", "Font.'Open Sans'"),
        _design("HeadingFontWeight", "FontWeight.Semibold"),
        _design("Font", "Font.'Open Sans'"),
        _design("Color", "RGBA(0, 0, 0, 1)"),
        _design("Size", "13"),
        _design("DisplayMode", "DisplayMode.Edit"),
        _design("Visible", "true"),
    ]


def _container_defaults() -> list[Rule]:
    return [
        _design("X", "0"),
        _design("Y", "0"),
        _design("Width", "300"),
        _design("Height", "300"),
        _design("ZIndex", "1"),
        _design("Fill", "RGBA(0, 0, 0, 0)"),
        _design("BorderColor", "RGBA(0, 0, 0, 0)"),
        _design("BorderStyle", "BorderStyle.None"),
        _design("BorderThickness", "0"),
        _design("DisplayMode", "DisplayMode.Edit"),
        _design("Visible", "true"),
    ]


def _auto_layout_defaults() -> list[Rule]:
    return [
        _design("X", "0"),
        _design("Y", "0"),
        _design("Width", "300"),
        _design("Height", "300"),
        _design("ZIndex", "1"),
        _design("Fill", "RGBA(0, 0, 0, 0)"),
        _design("BorderColor", "RGBA(0, 0, 0, 0)"),
        _design("BorderStyle", "BorderStyle.None"),
        _design("BorderThickness", "0"),
        _design("LayoutGap", "0"),
        _design("LayoutAlignItems", "LayoutAlignItems.Start"),
        _design("LayoutDirection", "LayoutDirection.Vertical"),
        _design("LayoutOverflow", "LayoutOverflow.Hide"),
        _design("PaddingTop", "0"),
        _design("PaddingRight", "0"),
        _design("PaddingBottom", "0"),
        _design("PaddingLeft", "0"),
        _design("DisplayMode", "DisplayMode.Edit"),
        _design("Visible", "true"),
    ]


def _form_defaults() -> list[Rule]:
    return [
        _data("DataSource", ""),
        _data("Item", ""),
        _design("X", "0"),
        _design("Y", "0"),
        _design("Width", "500"),
        _design("Height", "600"),
        _design("ZIndex", "1"),
        _design("Fill", "RGBA(0, 0, 0, 0)"),
        _design("BorderColor", "RGBA(0, 0, 0, 0)"),
        _design("BorderStyle", "BorderStyle.None"),
        _design("BorderThickness", "0"),
        _design("DisplayMode", "DisplayMode.Edit"),
        _design("Visible", "true"),
    ]


def _form_viewer_defaults() -> list[Rule]:
    return [
        _data("DataSource", ""),
        _data("Item", ""),
        _design("X", "0"),
        _design("Y", "0"),
        _design("Width", "500"),
        _design("Height", "600"),
        _design("ZIndex", "1"),
        _design("Fill", "RGBA(0, 0, 0, 0)"),
        _design("BorderColor", "RGBA(0, 0, 0, 0)"),
        _design("BorderStyle", "BorderStyle.None"),
        _design("BorderThickness", "0"),
        _design("DisplayMode", "DisplayMode.View"),
        _design("Visible", "true"),
    ]


def _video_playback_defaults() -> list[Rule]:
    return [
        _data("Media", '""'),
        _design("X", "0"),
        _design("Y", "0"),
        _design("Width", "400"),
        _design("Height", "300"),
        _design("ZIndex", "1"),
        _design("Fill", "RGBA(0, 0, 0, 1)"),
        _design("BorderColor", "RGBA(0, 0, 0, 0)"),
        _design("BorderStyle", "BorderStyle.None"),
        _design("BorderThickness", "0"),
        _design("AutoStart", "false"),
        _design("ShowControls", "true"),
        _design("Loop", "false"),
        _design("DisplayMode", "DisplayMode.Edit"),
        _design("Visible", "true"),
    ]


def _chart_defaults() -> list[Rule]:
    return [
        _data("Items", "[]"),
        _design("X", "0"),
        _design("Y", "0"),
        _design("Width", "400"),
        _design("Height", "300"),
        _design("ZIndex", "1"),
        _design("Fill", "RGBA(255, 255, 255, 1)"),
        _design("BorderColor", "RGBA(0, 0, 0, 0)"),
        _design("BorderStyle", "BorderStyle.None"),
        _design("BorderThickness", "0"),
        _design("DisplayMode", "DisplayMode.Edit"),
        _design("Visible", "true"),
    ]


def _attachments_defaults() -> list[Rule]:
    return [
        _data("Items", "[]"),
        _design("X", "0"),
        _design("Y", "0"),
        _design("Width", "200"),
        _design("Height", "200"),
        _design("ZIndex", "1"),
        _design("Fill", "RGBA(255, 255, 255, 1)"),
        _design("BorderColor", "RGBA(0, 0, 0, 0.4)"),
        _design("BorderStyle", "BorderStyle.Solid"),
        _design("BorderThickness", "1"),
        _design("DisplayMode", "DisplayMode.Edit"),
        _design("Visible", "true"),
    ]


def _listbox_defaults() -> list[Rule]:
    return [
        _data("Items", '["Option 1", "Option 2", "Option 3"]'),
        _design("X", "0"),
        _design("Y", "0"),
        _design("Width", "200"),
        _design("Height", "200"),
        _design("ZIndex", "1"),
        _design("Fill", "RGBA(255, 255, 255, 1)"),
        _design("Color", "RGBA(0, 0, 0, 1)"),
        _design("BorderColor", "RGBA(0, 0, 0, 0.4)"),
        _design("BorderStyle", "BorderStyle.Solid"),
        _design("BorderThickness", "2"),
        _design("SelectionColor", "RGBA(0, 0, 0, 1)"),
        _design("SelectionFill", "RGBA(56, 96, 178, 0.2)"),
        _design("Font", "Font.'Open Sans'"),
        _design("Size", "13"),
        _design("DisplayMode", "DisplayMode.Edit"),
        _design("Visible", "true"),
        _behavior("OnChange", "false"),
    ]


# ── Default rules lookup ────────────────────────────────────────────────

_DEFAULT_RULES: dict[str, Any] = {
    "button": _button_defaults,
    "label": _label_defaults,
    "text": _label_defaults,  # alias
    "rectangle": _rectangle_defaults,
    "circle": _circle_defaults,
    "triangle": _triangle_defaults,
    "icon": _icon_defaults,
    "textInput": _text_input_defaults,
    "dropdown": _dropdown_defaults,
    "combobox": _dropdown_defaults,
    "gallery": _gallery_defaults,
    "image": _image_defaults,
    "checkbox": _checkbox_defaults,
    "toggle": _toggle_defaults,
    "toggleSwitch": _toggle_defaults,
    "slider": _slider_defaults,
    "rating": _rating_defaults,
    "datePicker": _date_picker_defaults,
    "radio": _radio_defaults,
    "timer": _timer_defaults,
    "htmlViewer": _html_viewer_defaults,
    "richTextEditor": _rich_text_editor_defaults,
    "dataTable": _data_table_defaults,
    "container": _container_defaults,
    "groupContainer": _container_defaults,
    "horizontalAutoLayout": _auto_layout_defaults,
    "verticalAutoLayout": _auto_layout_defaults,
    "gridContainer": _container_defaults,
    "form": _form_defaults,
    "formViewer": _form_viewer_defaults,
    "fluidGrid": _container_defaults,
    "videoPlayback": _video_playback_defaults,
    "microsoftStreamPlayback": _video_playback_defaults,
    "audioPlayback": _video_playback_defaults,
    "columnChart": _chart_defaults,
    "lineChart": _chart_defaults,
    "pieChart": _chart_defaults,
    "legend": _chart_defaults,
    "attachments": _attachments_defaults,
    "listbox": _listbox_defaults,
    "listBox": _listbox_defaults,
    "addMedia": _image_defaults,
    "addPicture": _image_defaults,
}


# ── Public API ──────────────────────────────────────────────────────────


def create_app_control(state: AppState) -> Control:
    """Create the App host control (Controls/1.json)."""
    uid = state.allocate_id()
    return Control(
        Name="App",
        Template=Template(
            Id=f"{_TEMPLATE_BASE}/appinfo",
            Version=_TEMPLATE_VERSIONS["appinfo"],
            Name="appinfo",
        ),
        Index=0.0,
        ControlUniqueId=uid,
        IsDataControl=True,
        AllowAccessToGlobals=True,
        Rules=[
            _behavior("OnStart", "false"),
            _behavior("OnError", "false"),
            _design("Theme", 'PowerAppsTheme.DataField("defaultTheme")'),
            _design("BackEnabled", "false"),
        ],
        Children=[],
    )


def create_screen(state: AppState, name: str, fill: str = "RGBA(255, 255, 255, 1)") -> Control:
    """Create a screen control."""
    uid = state.allocate_id()
    idx = state.allocate_index()

    rules = _screen_defaults(state.width, state.height)
    # Override fill if specified
    for r in rules:
        if r.Property == "Fill":
            r.InvariantScript = fill

    return Control(
        Name=name,
        Template=_make_template("screen"),
        Index=idx,
        ControlUniqueId=uid,
        IsDataControl=True,
        AllowAccessToGlobals=True,
        Rules=rules,
        ControlPropertyState=["Fill", "Height", "Width", "Size", "Orientation",
                              "LoadingSpinner", "LoadingSpinnerColor", "ImagePosition"],
    )


def create_control(
    state: AppState,
    control_type: str,
    name: str | None = None,
    properties: dict[str, str] | None = None,
    parent_name: str = "",
) -> Control:
    """Create a control of any type with optional property overrides.

    Args:
        state: Current app state (for ID allocation and auto-naming)
        control_type: Type name (e.g., "button", "label", "textInput")
        name: Control name (auto-generated if None)
        properties: Dict of {property_name: formula_string} overrides
        parent_name: Name of the parent control
    """
    if name is None:
        name = state.auto_name(control_type)

    uid = state.allocate_id()
    idx = state.allocate_index()

    # Get default rules for this type
    defaults_fn = _DEFAULT_RULES.get(control_type)
    if defaults_fn:
        rules = defaults_fn()
    else:
        # Generic fallback for unknown types
        rules = [
            _design("X", "0"),
            _design("Y", "0"),
            _design("Width", "200"),
            _design("Height", "50"),
            _design("ZIndex", "1"),
            _design("DisplayMode", "DisplayMode.Edit"),
            _design("Visible", "true"),
        ]

    # Apply property overrides
    if properties:
        existing_props = {r.Property: r for r in rules}
        for prop, script in properties.items():
            if prop in existing_props:
                existing_props[prop].InvariantScript = script
            else:
                # Determine category from property name
                if prop.startswith("On"):
                    category = "Behavior"
                elif prop in ("Items", "Default", "Text", "DataSource", "Item",
                              "DataField", "DisplayName", "Update", "Icon",
                              "Image", "HintText", "Value", "Duration",
                              "Start", "Repeat", "DefaultDate", "SearchItems"):
                    category = "Data"
                else:
                    category = "Design"
                rules.append(_rule(prop, category, script))

    # Update ZIndex to match the control's index
    for r in rules:
        if r.Property == "ZIndex":
            r.InvariantScript = str(int(idx))

    prop_state = [r.Property for r in rules]

    return Control(
        Name=name,
        Template=_make_template(control_type),
        Index=idx,
        ControlUniqueId=uid,
        Parent=parent_name,
        Rules=rules,
        ControlPropertyState=prop_state,
    )
