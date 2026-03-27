"""App-level templates — complete multi-screen app scaffolding.

Each template function populates an AppState with screens, controls,
navigation wiring, and App.OnStart initialization. Templates compose
screen patterns from screen_patterns.py.
"""

from __future__ import annotations

import json
from pathlib import Path

from .controls import create_app_control, create_control, create_screen, behavior, design
from .models import AppState
from .screen_patterns import (
    create_loading_screen,
    create_list_screen,
    create_detail_screen,
    create_form_screen,
    create_settings_screen,
    _add_header_bar,
)
from .styles import generate_app_styles_formula

_DATA_DIR = Path(__file__).parent / "data"
_catalog: dict | None = None


def _load_catalog() -> dict:
    global _catalog
    if _catalog is None:
        path = _DATA_DIR / "app_templates.json"
        with open(path) as f:
            _catalog = json.load(f)
    return _catalog


def list_app_templates() -> dict:
    """Return the template catalog (for the list_templates MCP tool)."""
    catalog = _load_catalog()
    result = {}
    for key, tpl in catalog.items():
        result[key] = {
            "name": tpl["name"],
            "description": tpl["description"],
            "screens": tpl["screens"],
            "config": {
                k: {ck: cv for ck, cv in v.items() if ck != "type"}
                for k, v in tpl.get("config", {}).items()
            },
        }
    return result


# ── Template: List/Detail ─────────────────────────────────────────────


def apply_list_detail_template(state: AppState, config: dict) -> None:
    """Create a List/Detail app: Loading → List → Detail → New Item Form."""
    app_name = state.name
    data_source = config.get("data_source", "[]")
    display_field = config.get("display_field", "Title")
    subtitle_field = config.get("subtitle_field", "")
    fields = config.get("fields", ["Title", "Description", "Status"])

    # Set App.OnStart with gblAppStyles
    styles_formula = generate_app_styles_formula(state.theme.name)
    if state.app_control:
        for r in state.app_control.Rules:
            if r.Property == "OnStart":
                r.InvariantScript = styles_formula
                break

    # Loading screen
    loading = create_loading_screen(
        state, name="LoadingScreen", navigate_to="ListScreen", app_title=app_name,
    )
    state.screens.append(loading)

    # List screen
    list_scr = create_list_screen(
        state, name="ListScreen", title=app_name,
        data_source=data_source, display_field=display_field,
        subtitle_field=subtitle_field, detail_screen="DetailScreen",
    )
    # Add "+" button to header for new item
    add_btn = create_control(
        state, "icon", name="ListScreen_AddIcon",
        properties={
            "Icon": "Icon.Add",
            "X": str(state.width - 50), "Y": "10",
            "Width": "40", "Height": "40",
            "Color": "gblAppStyles.HeaderFontColor",
            "Fill": "RGBA(0, 0, 0, 0)",
            "OnSelect": "Navigate(NewItemScreen, ScreenTransition.CoverRight)",
        },
        parent_name="ListScreen",
    )
    list_scr.Children.append(add_btn)
    state.screens.append(list_scr)

    # Detail screen
    detail = create_detail_screen(
        state, name="DetailScreen", title="Details",
        fields=fields, back_screen="ListScreen",
    )
    state.screens.append(detail)

    # New item form
    form_fields = [{"name": f} for f in fields]
    form = create_form_screen(
        state, name="NewItemScreen", title="New Item",
        fields=form_fields, back_screen="ListScreen",
    )
    state.screens.append(form)


# ── Template: Inspection ──────────────────────────────────────────────


def apply_inspection_template(state: AppState, config: dict) -> None:
    """Create an Inspection app: Loading → Checklist → Steps → Summary."""
    app_name = state.name
    checklist_source = config.get("checklist_source", "[]")
    step_fields = config.get("step_fields", ["Step", "Status", "Notes"])

    # Set App.OnStart
    styles_formula = generate_app_styles_formula(state.theme.name)
    if state.app_control:
        for r in state.app_control.Rules:
            if r.Property == "OnStart":
                r.InvariantScript = styles_formula
                break

    # Loading
    loading = create_loading_screen(
        state, name="LoadingScreen", navigate_to="ChecklistScreen", app_title=app_name,
    )
    state.screens.append(loading)

    # Checklist screen (list of checklists)
    checklist = create_list_screen(
        state, name="ChecklistScreen", title="Checklists",
        data_source=checklist_source, display_field="Title",
        subtitle_field="Status", detail_screen="StepsScreen",
    )
    state.screens.append(checklist)

    # Steps screen (detail with form fields per step)
    steps = create_form_screen(
        state, name="StepsScreen", title="Inspection Steps",
        fields=[{"name": f} for f in step_fields],
        back_screen="ChecklistScreen",
    )
    # Add a "Complete" button
    complete_btn = create_control(
        state, "button", name="StepsScreen_CompleteBtn",
        properties={
            "Text": '"Mark Complete"',
            "X": "20", "Y": str(80 + len(step_fields) * 86 + 90),
            "Width": str(state.width - 40), "Height": "45",
            "Fill": "gblAppStyles.SuccessColor",
            "Color": "RGBA(255, 255, 255, 1)",
            "RadiusTopLeft": "8", "RadiusTopRight": "8",
            "RadiusBottomLeft": "8", "RadiusBottomRight": "8",
            "OnSelect": "Navigate(SummaryScreen, ScreenTransition.CoverRight)",
        },
        parent_name="StepsScreen",
    )
    steps.Children.append(complete_btn)
    state.screens.append(steps)

    # Summary screen
    summary = create_detail_screen(
        state, name="SummaryScreen", title="Summary",
        fields=step_fields, back_screen="ChecklistScreen",
    )
    # Add checkmark icon
    check_icon = create_control(
        state, "icon", name="SummaryScreen_CheckIcon",
        properties={
            "Icon": "Icon.Check",
            "X": str(int(state.width / 2) - 25),
            "Y": str(80 + len(step_fields) * 80 + 40),
            "Width": "50", "Height": "50",
            "Color": "gblAppStyles.SuccessColor",
            "Fill": "RGBA(0, 0, 0, 0)",
        },
        parent_name="SummaryScreen",
    )
    summary.Children.append(check_icon)
    state.screens.append(summary)


# ── Template: Directory ───────────────────────────────────────────────


def apply_directory_template(state: AppState, config: dict) -> None:
    """Create a Directory app: Loading → People Gallery → Profile Detail."""
    app_name = state.name
    data_source = config.get("data_source", "[]")
    name_field = config.get("name_field", "DisplayName")
    detail_fields = config.get("detail_fields", ["DisplayName", "Email", "Department", "JobTitle"])

    # Set App.OnStart
    styles_formula = generate_app_styles_formula(state.theme.name)
    if state.app_control:
        for r in state.app_control.Rules:
            if r.Property == "OnStart":
                r.InvariantScript = styles_formula
                break

    # Loading
    loading = create_loading_screen(
        state, name="LoadingScreen", navigate_to="DirectoryScreen", app_title=app_name,
    )
    state.screens.append(loading)

    # Directory (people list)
    directory = create_list_screen(
        state, name="DirectoryScreen", title=app_name,
        data_source=data_source, display_field=name_field,
        subtitle_field="Email" if "Email" in detail_fields else "",
        detail_screen="ProfileScreen",
    )
    state.screens.append(directory)

    # Profile detail
    profile = create_detail_screen(
        state, name="ProfileScreen", title="Profile",
        fields=detail_fields, back_screen="DirectoryScreen",
    )
    state.screens.append(profile)


# ── Template: Tracker ─────────────────────────────────────────────────


def apply_tracker_template(state: AppState, config: dict) -> None:
    """Create a Tracker app: Loading → Dashboard → Task List → Task Edit."""
    app_name = state.name
    data_source = config.get("data_source", "[]")
    status_options = config.get("status_options", '["Not Started", "In Progress", "Complete"]')

    # Set App.OnStart
    styles_formula = generate_app_styles_formula(state.theme.name)
    if state.app_control:
        for r in state.app_control.Rules:
            if r.Property == "OnStart":
                r.InvariantScript = styles_formula
                break

    # Loading
    loading = create_loading_screen(
        state, name="LoadingScreen", navigate_to="DashboardScreen", app_title=app_name,
    )
    state.screens.append(loading)

    # Dashboard screen (custom — not a standard pattern)
    w, h = state.width, state.height
    dashboard = create_screen(state, "DashboardScreen", "gblAppStyles.ScreenFill")
    _add_header_bar(state, dashboard, app_name)

    # Status summary cards
    statuses = json.loads(status_options) if isinstance(status_options, str) else status_options
    card_w = int((w - 40 - (len(statuses) - 1) * 10) / len(statuses))
    for i, status in enumerate(statuses):
        safe = status.replace(" ", "")
        x = 20 + i * (card_w + 10)

        card = create_control(
            state, "rectangle", name=f"Dashboard_{safe}Card",
            properties={
                "X": str(x), "Y": "80",
                "Width": str(card_w), "Height": "90",
                "Fill": "gblAppStyles.CardFill",
                "BorderColor": "gblAppStyles.CardBorderColor",
                "BorderStyle": "BorderStyle.Solid",
                "BorderThickness": "1",
                "RadiusTopLeft": "8", "RadiusTopRight": "8",
                "RadiusBottomLeft": "8", "RadiusBottomRight": "8",
            },
            parent_name="DashboardScreen",
        )
        dashboard.Children.append(card)

        count_lbl = create_control(
            state, "label", name=f"Dashboard_{safe}Count",
            properties={
                "Text": f'CountRows(Filter({data_source}, Status = "{status}"))',
                "X": str(x), "Y": "85",
                "Width": str(card_w), "Height": "40",
                "Color": "gblAppStyles.TextPrimary",
                "Fill": "RGBA(0, 0, 0, 0)",
                "Size": "24",
                "FontWeight": "FontWeight.Bold",
                "Align": "Align.Center",
            },
            parent_name="DashboardScreen",
        )
        dashboard.Children.append(count_lbl)

        status_lbl = create_control(
            state, "label", name=f"Dashboard_{safe}Label",
            properties={
                "Text": f'"{status}"',
                "X": str(x), "Y": "125",
                "Width": str(card_w), "Height": "30",
                "Color": "gblAppStyles.TextSecondary",
                "Fill": "RGBA(0, 0, 0, 0)",
                "Size": "11",
                "Align": "Align.Center",
            },
            parent_name="DashboardScreen",
        )
        dashboard.Children.append(status_lbl)

    # "View All Tasks" button
    view_all = create_control(
        state, "button", name="Dashboard_ViewAllBtn",
        properties={
            "Text": '"View All Tasks"',
            "X": "20", "Y": "190",
            "Width": str(w - 40), "Height": "45",
            "Fill": "gblAppStyles.PrimaryButtonFill",
            "Color": "gblAppStyles.PrimaryButtonColor",
            "RadiusTopLeft": "8", "RadiusTopRight": "8",
            "RadiusBottomLeft": "8", "RadiusBottomRight": "8",
            "OnSelect": "Navigate(TaskListScreen, ScreenTransition.CoverRight)",
        },
        parent_name="DashboardScreen",
    )
    dashboard.Children.append(view_all)
    state.screens.append(dashboard)

    # Task list
    task_list = create_list_screen(
        state, name="TaskListScreen", title="Tasks",
        data_source=data_source, display_field="Title",
        subtitle_field="Status", detail_screen="TaskEditScreen",
        back_screen="DashboardScreen",
    )
    state.screens.append(task_list)

    # Task edit form
    task_edit = create_form_screen(
        state, name="TaskEditScreen", title="Edit Task",
        fields=[
            {"name": "Title"},
            {"name": "Description"},
            {"name": "Status", "type": "dropdown", "options": status_options},
            {"name": "DueDate", "type": "date"},
        ],
        back_screen="TaskListScreen",
    )
    state.screens.append(task_edit)


# ── Template Registry ─────────────────────────────────────────────────

APP_TEMPLATES = {
    "list_detail": apply_list_detail_template,
    "inspection": apply_inspection_template,
    "directory": apply_directory_template,
    "tracker": apply_tracker_template,
}
