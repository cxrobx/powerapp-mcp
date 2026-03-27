"""Screen pattern library — pre-built screen layouts based on MS Teams Power Apps templates.

Each pattern function creates a complete screen with child controls, using the
existing create_control/create_screen factories. Layout positions are calculated
from the app's width/height for Phone/Tablet compatibility.
"""

from __future__ import annotations

from .controls import create_control, create_screen, design, data, behavior
from .models import AppState, Control


# ── Helper: Header Bar ────────────────────────────────────────────────


def _add_header_bar(
    state: AppState,
    screen: Control,
    title: str,
    show_back: bool = False,
    back_screen: str = "",
) -> None:
    """Add a header bar (rectangle + title label + optional back icon) to a screen."""
    w = state.width

    # Header background
    header_bg = create_control(
        state, "rectangle", name=f"{screen.Name}_HeaderBg",
        properties={
            "X": "0", "Y": "0",
            "Width": str(w), "Height": "60",
            "Fill": "gblAppStyles.HeaderFill",
            "BorderThickness": "0",
        },
        parent_name=screen.Name,
    )
    screen.Children.append(header_bg)

    title_x = "60" if show_back else "20"
    title_w = str(w - (80 if show_back else 40))

    # Title label
    title_lbl = create_control(
        state, "label", name=f"{screen.Name}_Title",
        properties={
            "Text": f'"{title}"',
            "X": title_x, "Y": "0",
            "Width": title_w, "Height": "60",
            "Color": "gblAppStyles.HeaderFontColor",
            "Fill": "RGBA(0, 0, 0, 0)",
            "Size": "20",
            "FontWeight": "FontWeight.Bold",
            "VerticalAlign": "VerticalAlign.Middle",
            "Align": "Align.Left",
        },
        parent_name=screen.Name,
    )
    screen.Children.append(title_lbl)

    # Back button
    if show_back and back_screen:
        back_icon = create_control(
            state, "icon", name=f"{screen.Name}_BackIcon",
            properties={
                "Icon": "Icon.BackArrow",
                "X": "10", "Y": "10",
                "Width": "40", "Height": "40",
                "Color": "gblAppStyles.HeaderFontColor",
                "Fill": "RGBA(0, 0, 0, 0)",
                "OnSelect": f"Navigate({back_screen}, ScreenTransition.UnCoverRight)",
            },
            parent_name=screen.Name,
        )
        screen.Children.append(back_icon)


# ── Pattern: Loading Screen ───────────────────────────────────────────


def create_loading_screen(
    state: AppState,
    name: str = "LoadingScreen",
    navigate_to: str = "HomeScreen",
    app_title: str = "My App",
    fill: str = "gblAppStyles.ScreenFill",
) -> Control:
    """Create a loading/splash screen with timer-based navigation.

    Pattern from MS templates: timer triggers OnTimerEnd to navigate to main screen.
    """
    screen = create_screen(state, name, fill)
    w, h = state.width, state.height

    # App title label (centered)
    title = create_control(
        state, "label", name=f"{name}_AppTitle",
        properties={
            "Text": f'"{app_title}"',
            "X": str(int(w * 0.1)),
            "Y": str(int(h * 0.3)),
            "Width": str(int(w * 0.8)),
            "Height": "80",
            "Color": "gblAppStyles.TextPrimary",
            "Fill": "RGBA(0, 0, 0, 0)",
            "Size": "32",
            "FontWeight": "FontWeight.Bold",
            "Align": "Align.Center",
            "VerticalAlign": "VerticalAlign.Middle",
        },
        parent_name=name,
    )
    screen.Children.append(title)

    # Subtitle
    subtitle = create_control(
        state, "label", name=f"{name}_Subtitle",
        properties={
            "Text": '"Loading..."',
            "X": str(int(w * 0.2)),
            "Y": str(int(h * 0.3) + 80),
            "Width": str(int(w * 0.6)),
            "Height": "40",
            "Color": "gblAppStyles.TextSecondary",
            "Fill": "RGBA(0, 0, 0, 0)",
            "Size": "14",
            "Align": "Align.Center",
            "VerticalAlign": "VerticalAlign.Middle",
        },
        parent_name=name,
    )
    screen.Children.append(subtitle)

    # Navigation timer (auto-navigates after 1.5s)
    timer_ctrl = create_control(
        state, "timer", name=f"{name}_Timer",
        properties={
            "Duration": "1500",
            "Start": "true",
            "Repeat": "false",
            "OnTimerEnd": f"Navigate({navigate_to}, ScreenTransition.Fade)",
            "Visible": "false",
            "X": "0", "Y": "0",
            "Width": "0", "Height": "0",
        },
        parent_name=name,
    )
    screen.Children.append(timer_ctrl)

    return screen


# ── Pattern: List Screen ──────────────────────────────────────────────


def create_list_screen(
    state: AppState,
    name: str = "ListScreen",
    title: str = "Items",
    data_source: str = "[]",
    display_field: str = "Title",
    subtitle_field: str = "",
    detail_screen: str = "",
    back_screen: str = "",
    fill: str = "gblAppStyles.ScreenFill",
) -> Control:
    """Create a list screen with search, gallery, and navigation.

    Pattern: Header + search input + gallery with clickable items.
    """
    screen = create_screen(state, name, fill)
    w, h = state.width, state.height

    # Header bar
    _add_header_bar(state, screen, title, show_back=bool(back_screen), back_screen=back_screen)

    # Search input
    search = create_control(
        state, "textInput", name=f"{name}_Search",
        properties={
            "HintText": '"Search..."',
            "X": "20", "Y": "70",
            "Width": str(w - 40), "Height": "45",
            "Fill": "gblAppStyles.SearchFill",
            "BorderColor": "gblAppStyles.SearchBorder",
            "Color": "gblAppStyles.TextPrimary",
            "RadiusTopLeft": "8", "RadiusTopRight": "8",
            "RadiusBottomLeft": "8", "RadiusBottomRight": "8",
        },
        parent_name=name,
    )
    screen.Children.append(search)

    # Gallery
    items_formula = data_source
    if data_source != "[]":
        items_formula = (
            f'Filter({data_source}, '
            f'StartsWith({display_field}, {name}_Search.Text) '
            f'|| {name}_Search.Text = "")'
        )

    gallery = create_control(
        state, "gallery", name=f"{name}_Gallery",
        properties={
            "Items": items_formula,
            "X": "0", "Y": "125",
            "Width": str(w), "Height": str(h - 125),
            "Fill": "RGBA(0, 0, 0, 0)",
            "TemplatePadding": "0",
            "TemplateSize": str(70 if subtitle_field else 55),
        },
        parent_name=name,
    )

    # Gallery item template children
    # Item separator line
    separator = create_control(
        state, "rectangle", name=f"{name}_Separator",
        properties={
            "X": "20", "Y": "0",
            "Width": str(w - 40), "Height": "1",
            "Fill": "gblAppStyles.DividerColor",
            "BorderThickness": "0",
        },
        parent_name=f"{name}_Gallery",
    )
    gallery.Children.append(separator)

    # Item title
    item_title = create_control(
        state, "label", name=f"{name}_ItemTitle",
        properties={
            "Text": f"ThisItem.{display_field}",
            "X": "20", "Y": "5",
            "Width": str(w - 80), "Height": "30",
            "Color": "gblAppStyles.TextPrimary",
            "Fill": "RGBA(0, 0, 0, 0)",
            "Size": "15",
            "FontWeight": "FontWeight.Semibold",
            "VerticalAlign": "VerticalAlign.Middle",
        },
        parent_name=f"{name}_Gallery",
    )
    gallery.Children.append(item_title)

    # Optional subtitle
    if subtitle_field:
        item_sub = create_control(
            state, "label", name=f"{name}_ItemSubtitle",
            properties={
                "Text": f"ThisItem.{subtitle_field}",
                "X": "20", "Y": "33",
                "Width": str(w - 80), "Height": "25",
                "Color": "gblAppStyles.TextSecondary",
                "Fill": "RGBA(0, 0, 0, 0)",
                "Size": "12",
                "VerticalAlign": "VerticalAlign.Middle",
            },
            parent_name=f"{name}_Gallery",
        )
        gallery.Children.append(item_sub)

    # Chevron icon (navigate to detail)
    if detail_screen:
        chevron = create_control(
            state, "icon", name=f"{name}_Chevron",
            properties={
                "Icon": "Icon.ChevronRight",
                "X": str(w - 50), "Y": "10",
                "Width": "35", "Height": "35",
                "Color": "gblAppStyles.IconSecondary",
                "Fill": "RGBA(0, 0, 0, 0)",
                "OnSelect": f"Navigate({detail_screen}, ScreenTransition.CoverRight)",
            },
            parent_name=f"{name}_Gallery",
        )
        gallery.Children.append(chevron)

    screen.Children.append(gallery)
    return screen


# ── Pattern: Detail Screen ────────────────────────────────────────────


def create_detail_screen(
    state: AppState,
    name: str = "DetailScreen",
    title: str = "Details",
    fields: list[str] | None = None,
    back_screen: str = "ListScreen",
    fill: str = "gblAppStyles.ScreenFill",
) -> Control:
    """Create a detail view screen showing field/value pairs.

    Pattern: Header with back button + vertically stacked field labels.
    """
    if fields is None:
        fields = ["Title", "Description", "Status"]

    screen = create_screen(state, name, fill)
    w = state.width

    # Header with back
    _add_header_bar(state, screen, title, show_back=True, back_screen=back_screen)

    # Content card background
    card_bg = create_control(
        state, "rectangle", name=f"{name}_CardBg",
        properties={
            "X": "20", "Y": "80",
            "Width": str(w - 40), "Height": str(len(fields) * 80 + 20),
            "Fill": "gblAppStyles.CardFill",
            "BorderColor": "gblAppStyles.CardBorderColor",
            "BorderStyle": "BorderStyle.Solid",
            "BorderThickness": "1",
            "RadiusTopLeft": "8", "RadiusTopRight": "8",
            "RadiusBottomLeft": "8", "RadiusBottomRight": "8",
        },
        parent_name=name,
    )
    screen.Children.append(card_bg)

    # Field label/value pairs
    for i, field in enumerate(fields):
        y_offset = 90 + (i * 80)

        # Field label
        field_label = create_control(
            state, "label", name=f"{name}_{field}Label",
            properties={
                "Text": f'"{field}"',
                "X": "40", "Y": str(y_offset),
                "Width": str(w - 80), "Height": "25",
                "Color": "gblAppStyles.TextSecondary",
                "Fill": "RGBA(0, 0, 0, 0)",
                "Size": "11",
                "FontWeight": "FontWeight.Semibold",
            },
            parent_name=name,
        )
        screen.Children.append(field_label)

        # Field value
        field_value = create_control(
            state, "label", name=f"{name}_{field}Value",
            properties={
                "Text": f"ThisItem.{field}",
                "X": "40", "Y": str(y_offset + 25),
                "Width": str(w - 80), "Height": "35",
                "Color": "gblAppStyles.TextPrimary",
                "Fill": "RGBA(0, 0, 0, 0)",
                "Size": "15",
                "VerticalAlign": "VerticalAlign.Top",
            },
            parent_name=name,
        )
        screen.Children.append(field_value)

    return screen


# ── Pattern: Form Screen ─────────────────────────────────────────────


def create_form_screen(
    state: AppState,
    name: str = "FormScreen",
    title: str = "New Item",
    fields: list[dict] | None = None,
    back_screen: str = "ListScreen",
    fill: str = "gblAppStyles.ScreenFill",
) -> Control:
    """Create a form entry screen with inputs and submit/cancel buttons.

    Args:
        fields: List of field dicts, each with "name" and optional "type"
                (text, dropdown, date, toggle). Default type is "text".
                Example: [{"name": "Title"}, {"name": "Status", "type": "dropdown",
                          "options": '["Active", "Closed"]'}]
    """
    if fields is None:
        fields = [{"name": "Title"}, {"name": "Description"}]

    screen = create_screen(state, name, fill)
    w, h = state.width, state.height

    # Header with back
    _add_header_bar(state, screen, title, show_back=True, back_screen=back_screen)

    # Form fields
    y_pos = 80
    for field_def in fields:
        fname = field_def["name"]
        ftype = field_def.get("type", "text")

        # Field label
        flbl = create_control(
            state, "label", name=f"{name}_{fname}Label",
            properties={
                "Text": f'"{fname}"',
                "X": "20", "Y": str(y_pos),
                "Width": str(w - 40), "Height": "25",
                "Color": "gblAppStyles.TextSecondary",
                "Fill": "RGBA(0, 0, 0, 0)",
                "Size": "12",
                "FontWeight": "FontWeight.Semibold",
            },
            parent_name=name,
        )
        screen.Children.append(flbl)

        y_pos += 28

        # Field input
        if ftype == "dropdown":
            options = field_def.get("options", '["Option 1", "Option 2"]')
            finput = create_control(
                state, "dropdown", name=f"{name}_{fname}Input",
                properties={
                    "Items": options,
                    "X": "20", "Y": str(y_pos),
                    "Width": str(w - 40), "Height": "45",
                    "Fill": "gblAppStyles.InputFill",
                    "BorderColor": "gblAppStyles.InputBorderColor",
                    "Color": "gblAppStyles.TextPrimary",
                },
                parent_name=name,
            )
        elif ftype == "date":
            finput = create_control(
                state, "datePicker", name=f"{name}_{fname}Input",
                properties={
                    "X": "20", "Y": str(y_pos),
                    "Width": str(w - 40), "Height": "45",
                    "Fill": "gblAppStyles.InputFill",
                    "BorderColor": "gblAppStyles.InputBorderColor",
                    "Color": "gblAppStyles.TextPrimary",
                },
                parent_name=name,
            )
        elif ftype == "toggle":
            finput = create_control(
                state, "toggle", name=f"{name}_{fname}Input",
                properties={
                    "X": "20", "Y": str(y_pos),
                    "Width": str(w - 40), "Height": "44",
                    "TrueFill": "gblAppStyles.PrimaryButtonFill",
                },
                parent_name=name,
            )
        else:
            # Default: text input
            finput = create_control(
                state, "textInput", name=f"{name}_{fname}Input",
                properties={
                    "HintText": f'"Enter {fname.lower()}"',
                    "X": "20", "Y": str(y_pos),
                    "Width": str(w - 40), "Height": "45",
                    "Fill": "gblAppStyles.InputFill",
                    "BorderColor": "gblAppStyles.InputBorderColor",
                    "Color": "gblAppStyles.TextPrimary",
                    "RadiusTopLeft": "5", "RadiusTopRight": "5",
                    "RadiusBottomLeft": "5", "RadiusBottomRight": "5",
                },
                parent_name=name,
            )
        screen.Children.append(finput)
        y_pos += 58

    # Button row
    btn_y = y_pos + 20
    btn_w = int((w - 60) / 2)

    # Cancel button
    cancel_btn = create_control(
        state, "button", name=f"{name}_CancelBtn",
        properties={
            "Text": '"Cancel"',
            "X": "20", "Y": str(btn_y),
            "Width": str(btn_w), "Height": "45",
            "Fill": "gblAppStyles.SecondaryButtonFill",
            "Color": "gblAppStyles.SecondaryButtonColor",
            "BorderColor": "gblAppStyles.SecondaryButtonBorder",
            "BorderThickness": "1",
            "RadiusTopLeft": "8", "RadiusTopRight": "8",
            "RadiusBottomLeft": "8", "RadiusBottomRight": "8",
            "OnSelect": f"Navigate({back_screen}, ScreenTransition.UnCoverRight)",
        },
        parent_name=name,
    )
    screen.Children.append(cancel_btn)

    # Submit button
    submit_btn = create_control(
        state, "button", name=f"{name}_SubmitBtn",
        properties={
            "Text": '"Submit"',
            "X": str(40 + btn_w), "Y": str(btn_y),
            "Width": str(btn_w), "Height": "45",
            "Fill": "gblAppStyles.PrimaryButtonFill",
            "Color": "gblAppStyles.PrimaryButtonColor",
            "RadiusTopLeft": "8", "RadiusTopRight": "8",
            "RadiusBottomLeft": "8", "RadiusBottomRight": "8",
            "OnSelect": f"Navigate({back_screen}, ScreenTransition.UnCoverRight)",
        },
        parent_name=name,
    )
    screen.Children.append(submit_btn)

    return screen


# ── Pattern: Settings Screen ─────────────────────────────────────────


def create_settings_screen(
    state: AppState,
    name: str = "SettingsScreen",
    title: str = "Settings",
    options: list[dict] | None = None,
    back_screen: str = "",
    fill: str = "gblAppStyles.ScreenFill",
) -> Control:
    """Create a settings screen with toggle options.

    Args:
        options: List of dicts with "name" and optional "default" (bool).
                 Example: [{"name": "Dark Mode", "default": "false"},
                          {"name": "Notifications", "default": "true"}]
    """
    if options is None:
        options = [
            {"name": "Dark Mode", "default": "false"},
            {"name": "Notifications", "default": "true"},
        ]

    screen = create_screen(state, name, fill)
    w = state.width

    _add_header_bar(state, screen, title, show_back=bool(back_screen), back_screen=back_screen)

    y_pos = 80
    for opt in options:
        opt_name = opt["name"]
        safe_name = opt_name.replace(" ", "")
        default = opt.get("default", "false")

        # Option label
        opt_lbl = create_control(
            state, "label", name=f"{name}_{safe_name}Label",
            properties={
                "Text": f'"{opt_name}"',
                "X": "20", "Y": str(y_pos),
                "Width": str(w - 200), "Height": "44",
                "Color": "gblAppStyles.TextPrimary",
                "Fill": "RGBA(0, 0, 0, 0)",
                "Size": "14",
                "VerticalAlign": "VerticalAlign.Middle",
            },
            parent_name=name,
        )
        screen.Children.append(opt_lbl)

        # Toggle
        opt_toggle = create_control(
            state, "toggle", name=f"{name}_{safe_name}Toggle",
            properties={
                "Default": default,
                "X": str(w - 180), "Y": str(y_pos),
                "Width": "160", "Height": "44",
                "TrueFill": "gblAppStyles.PrimaryButtonFill",
            },
            parent_name=name,
        )
        screen.Children.append(opt_toggle)

        # Divider
        divider = create_control(
            state, "rectangle", name=f"{name}_{safe_name}Divider",
            properties={
                "X": "20", "Y": str(y_pos + 50),
                "Width": str(w - 40), "Height": "1",
                "Fill": "gblAppStyles.DividerColor",
                "BorderThickness": "0",
            },
            parent_name=name,
        )
        screen.Children.append(divider)
        y_pos += 60

    return screen


# ── Registry ─────────────────────────────────────────────────────────

SCREEN_PATTERNS = {
    "loading": {
        "name": "Loading Screen",
        "description": "Splash screen with timer-based navigation to the main screen",
        "factory": create_loading_screen,
        "config_keys": ["navigate_to", "app_title"],
    },
    "list": {
        "name": "List Screen",
        "description": "Gallery with search, header bar, and clickable items for navigation",
        "factory": create_list_screen,
        "config_keys": ["title", "data_source", "display_field", "subtitle_field", "detail_screen", "back_screen"],
    },
    "detail": {
        "name": "Detail Screen",
        "description": "Record detail view with field/value pairs and back navigation",
        "factory": create_detail_screen,
        "config_keys": ["title", "fields", "back_screen"],
    },
    "form": {
        "name": "Form Screen",
        "description": "Data entry form with typed inputs and submit/cancel buttons",
        "factory": create_form_screen,
        "config_keys": ["title", "fields", "back_screen"],
    },
    "settings": {
        "name": "Settings Screen",
        "description": "Toggle-based settings with labeled options",
        "factory": create_settings_screen,
        "config_keys": ["title", "options", "back_screen"],
    },
}
