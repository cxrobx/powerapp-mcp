"""MCP server for generating Power Apps .msapp files.

Started by Claude Code via stdio transport. Maintains stateful AppState
across tool calls within a single interactive session.
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .app_templates import APP_TEMPLATES, list_app_templates
from .compiler import compile_msapp
from .controls import create_app_control, create_control, create_screen
from .models import AppState
from .preview import generate_preview_html
from .screen_patterns import SCREEN_PATTERNS
from .state import create_state, get_state, has_state
from .styles import generate_app_styles_formula
from .themes import get_theme_by_name

logger = logging.getLogger(__name__)

mcp = FastMCP("powerapp")

_OUTPUT_DIR = Path(__file__).resolve().parent.parent.parent / "output"


# ── Session Management ──────────────────────────────────────────────────


@mcp.tool()
async def create_app(
    name: str,
    app_type: str = "Tablet",
    theme: str = "default",
) -> str:
    """Create a new Power App. Resets any existing app in this session.

    Args:
        name: App display name (e.g., "Inventory Tracker")
        app_type: "Phone" (640x1136), "Tablet" (1366x768), or "Desktop" (1366x768)
        theme: "default" or "dark"
    """
    state = create_state(name, app_type)
    state.app_control = create_app_control(state)
    state.theme = get_theme_by_name(theme)

    return json.dumps({
        "status": "created",
        "name": state.name,
        "app_id": state.app_id,
        "app_type": state.app_type,
        "dimensions": f"{state.width}x{state.height}",
        "orientation": state.orientation,
        "theme": state.theme.name,
    })


@mcp.tool()
async def get_app_state() -> str:
    """Get the current app state — screens, controls, data sources."""
    state = get_state()

    screens_info = []
    for s in state.screens:
        screens_info.append({
            "name": s.Name,
            "children": len(s.Children),
            "control_id": s.ControlUniqueId,
        })

    return json.dumps({
        "name": state.name,
        "app_type": state.app_type,
        "dimensions": f"{state.width}x{state.height}",
        "screens": screens_info,
        "screen_count": len(state.screens),
        "data_sources": [ds.Name for ds in state.data_sources],
        "theme": state.theme.name,
        "total_controls": sum(
            _count_controls(s) for s in state.screens
        ),
    })


@mcp.tool()
async def set_app_property(property: str, value: str) -> str:
    """Set an app-level property.

    Args:
        property: One of "name", "width", "height", "orientation"
        value: New value
    """
    state = get_state()
    if property == "name":
        state.name = value
    elif property == "width":
        state.width = int(value)
    elif property == "height":
        state.height = int(value)
    elif property == "orientation":
        state.orientation = value
    else:
        return json.dumps({"error": f"Unknown property: {property}"})

    return json.dumps({"status": "updated", "property": property, "value": value})


# ── Screen Tools ────────────────────────────────────────────────────────


@mcp.tool()
async def add_screen(
    name: str,
    fill: str = "RGBA(255, 255, 255, 1)",
    on_visible: str = "",
) -> str:
    """Add a new screen to the app.

    Args:
        name: Screen name (e.g., "HomeScreen", "DetailScreen")
        fill: Background color formula (e.g., "RGBA(255, 255, 255, 1)")
        on_visible: Power Fx formula to run when screen becomes visible
    """
    state = get_state()

    if state.find_screen(name):
        return json.dumps({"error": f"Screen '{name}' already exists"})

    screen = create_screen(state, name, fill)
    if on_visible:
        from .controls import _behavior
        screen.Rules.append(_behavior("OnVisible", on_visible))

    state.screens.append(screen)

    return json.dumps({
        "status": "added",
        "screen": name,
        "control_id": screen.ControlUniqueId,
        "total_screens": len(state.screens),
    })


@mcp.tool()
async def remove_screen(name: str) -> str:
    """Remove a screen by name."""
    state = get_state()
    state.screens = [s for s in state.screens if s.Name != name]
    return json.dumps({"status": "removed", "screen": name})


@mcp.tool()
async def list_screens() -> str:
    """List all screens with their child control counts."""
    state = get_state()
    screens = []
    for s in state.screens:
        screens.append({
            "name": s.Name,
            "children": len(s.Children),
            "total_controls": _count_controls(s) - 1,  # exclude screen itself
        })
    return json.dumps({"screens": screens})


# ── Control Tools ───────────────────────────────────────────────────────


@mcp.tool()
async def add_control(
    parent: str,
    control_type: str,
    name: str = "",
    properties: str = "{}",
) -> str:
    """Add a control to a screen or parent control.

    Args:
        parent: Parent name — a screen name or another control's name
        control_type: Type of control. Common types:
            Display: "label", "rectangle", "icon", "image"
            Input: "button", "textInput", "dropdown", "combobox", "checkbox",
                   "toggle", "slider", "rating", "radio", "datePicker"
            Data: "gallery", "form", "dataTable"
            Media: "timer", "camera", "videoPlayback", "audioPlayback"
            Layout: "horizontalAutoLayout", "verticalAutoLayout", "container"
            Charts: "columnChart", "lineChart", "pieChart"
        name: Control name (auto-generated if empty, e.g., "Button1")
        properties: JSON string of property overrides, e.g.:
            {"Text": "\\"Submit\\"", "OnSelect": "Navigate(Screen2)", "Fill": "RGBA(56,96,178,1)"}
    """
    state = get_state()

    # Find parent
    parent_control = state.find_screen(parent) or state.find_control(parent)
    if not parent_control:
        return json.dumps({"error": f"Parent '{parent}' not found"})

    # Parse properties
    try:
        props = json.loads(properties) if properties else {}
    except json.JSONDecodeError as e:
        return json.dumps({"error": f"Invalid properties JSON: {e}"})

    # Auto-name if empty
    ctrl_name = name if name else None

    control = create_control(
        state,
        control_type=control_type,
        name=ctrl_name,
        properties=props,
        parent_name=parent_control.Name,
    )
    parent_control.Children.append(control)

    return json.dumps({
        "status": "added",
        "name": control.Name,
        "type": control_type,
        "parent": parent_control.Name,
        "control_id": control.ControlUniqueId,
    })


@mcp.tool()
async def update_control(name: str, properties: str = "{}") -> str:
    """Update properties on an existing control.

    Args:
        name: Control name to update
        properties: JSON string of property overrides
    """
    state = get_state()
    control = state.find_control(name)
    if not control:
        return json.dumps({"error": f"Control '{name}' not found"})

    try:
        props = json.loads(properties) if properties else {}
    except json.JSONDecodeError as e:
        return json.dumps({"error": f"Invalid properties JSON: {e}"})

    # Update existing rules or add new ones
    existing = {r.Property: r for r in control.Rules}
    for prop, script in props.items():
        if prop in existing:
            existing[prop].InvariantScript = script
        else:
            if prop.startswith("On"):
                category = "Behavior"
            elif prop in ("Items", "Default", "Text", "DataSource", "Item",
                          "DataField", "DisplayName", "Update", "Icon",
                          "Image", "HintText", "Value"):
                category = "Data"
            else:
                category = "Design"
            from .models import Rule
            control.Rules.append(Rule(
                Property=prop,
                Category=category,
                InvariantScript=script,
                RuleProviderType="Unknown",
            ))

    return json.dumps({
        "status": "updated",
        "name": name,
        "properties_updated": list(props.keys()),
    })


@mcp.tool()
async def remove_control(name: str) -> str:
    """Remove a control by name from its parent."""
    state = get_state()

    def _remove_from(parent: "Control") -> bool:
        for i, child in enumerate(parent.Children):
            if child.Name == name:
                parent.Children.pop(i)
                return True
            if _remove_from(child):
                return True
        return False

    for screen in state.screens:
        if _remove_from(screen):
            return json.dumps({"status": "removed", "name": name})

    return json.dumps({"error": f"Control '{name}' not found"})


@mcp.tool()
async def list_controls(screen: str = "", recursive: bool = True) -> str:
    """List controls in the app.

    Args:
        screen: Screen name to list (all screens if empty)
        recursive: Include nested children
    """
    state = get_state()
    screens = state.screens if not screen else [s for s in state.screens if s.Name == screen]

    result = {}
    for s in screens:
        if recursive:
            result[s.Name] = _control_tree(s)
        else:
            result[s.Name] = [
                {"name": c.Name, "type": c.Template.Name, "children": len(c.Children)}
                for c in s.Children
            ]

    return json.dumps(result)


@mcp.tool()
async def get_control(name: str) -> str:
    """Get full details of a control including all properties."""
    state = get_state()
    control = state.find_control(name)
    if not control:
        return json.dumps({"error": f"Control '{name}' not found"})

    rules = {}
    for r in control.Rules:
        rules[r.Property] = {
            "value": r.InvariantScript,
            "category": r.Category,
        }

    return json.dumps({
        "name": control.Name,
        "type": control.Template.Name,
        "parent": control.Parent,
        "control_id": control.ControlUniqueId,
        "children": len(control.Children),
        "properties": rules,
    })


# ── Screen Pattern Tools ────────────────────────────────────────────────


@mcp.tool()
async def add_screen_pattern(
    pattern: str,
    name: str = "",
    config: str = "{}",
) -> str:
    """Add a pre-built screen pattern to the app.

    Args:
        pattern: Pattern type — one of:
            "loading" — splash screen with timer navigation
            "list" — searchable gallery with header and item navigation
            "detail" — record view with field/value pairs and back button
            "form" — data entry with typed inputs and submit/cancel
            "settings" — toggle-based options screen
        name: Screen name (auto-generated from pattern if empty)
        config: JSON string with pattern-specific options:
            loading: {"navigate_to": "HomeScreen", "app_title": "My App"}
            list: {"title": "Items", "data_source": "MyTable", "display_field": "Name",
                   "subtitle_field": "Status", "detail_screen": "DetailScreen", "back_screen": ""}
            detail: {"title": "Details", "fields": ["Name", "Email", "Phone"],
                     "back_screen": "ListScreen"}
            form: {"title": "New Item", "fields": [{"name": "Title"}, {"name": "Status",
                   "type": "dropdown", "options": '["Active", "Closed"]'}], "back_screen": "ListScreen"}
            settings: {"title": "Settings", "options": [{"name": "Dark Mode", "default": "false"}],
                       "back_screen": "HomeScreen"}
    """
    state = get_state()

    if pattern not in SCREEN_PATTERNS:
        available = ", ".join(SCREEN_PATTERNS.keys())
        return json.dumps({"error": f"Unknown pattern '{pattern}'. Available: {available}"})

    try:
        cfg = json.loads(config) if config else {}
    except json.JSONDecodeError as e:
        return json.dumps({"error": f"Invalid config JSON: {e}"})

    pattern_info = SCREEN_PATTERNS[pattern]
    factory = pattern_info["factory"]

    # Auto-generate name if not provided
    if not name:
        base = pattern.capitalize() + "Screen"
        name = base
        i = 1
        while state.find_screen(name):
            i += 1
            name = f"{base}{i}"

    if state.find_screen(name):
        return json.dumps({"error": f"Screen '{name}' already exists"})

    # Call the factory with name + config
    cfg["name"] = name
    screen = factory(state, **cfg)
    state.screens.append(screen)

    return json.dumps({
        "status": "added",
        "pattern": pattern,
        "screen": name,
        "children": len(screen.Children),
        "total_screens": len(state.screens),
    })


# ── App Template Tools ─────────────────────────────────────────────────


@mcp.tool()
async def list_templates() -> str:
    """List available app templates with descriptions and config options.

    Returns template IDs, descriptions, screen lists, and configurable parameters.
    """
    return json.dumps(list_app_templates(), indent=2)


@mcp.tool()
async def create_from_template(
    template: str,
    name: str,
    config: str = "{}",
    app_type: str = "Tablet",
    theme: str = "default",
) -> str:
    """Create a complete multi-screen app from a template.

    This resets any existing app state and creates a full app with multiple
    screens, navigation, and App.OnStart initialization.

    After creation, you can customize with add_control, update_control, etc.

    Args:
        template: Template ID — one of:
            "list_detail" — gallery + detail view + new-item form (4 screens)
            "inspection" — checklist with step tracking and summary (4 screens)
            "directory" — people gallery with profile detail (3 screens)
            "tracker" — dashboard with task list and edit form (4 screens)
        name: App display name
        config: JSON string with template-specific options (see list_templates for schema)
        app_type: "Phone" (640x1136) or "Tablet" (1366x768)
        theme: "default" or "dark"
    """
    if template not in APP_TEMPLATES:
        available = ", ".join(APP_TEMPLATES.keys())
        return json.dumps({"error": f"Unknown template '{template}'. Available: {available}"})

    try:
        cfg = json.loads(config) if config else {}
    except json.JSONDecodeError as e:
        return json.dumps({"error": f"Invalid config JSON: {e}"})

    # Initialize fresh state
    state = create_state(name, app_type)
    state.app_control = create_app_control(state)
    state.theme = get_theme_by_name(theme)

    # Apply the template
    template_fn = APP_TEMPLATES[template]
    template_fn(state, cfg)

    return json.dumps({
        "status": "created",
        "template": template,
        "name": state.name,
        "app_type": state.app_type,
        "dimensions": f"{state.width}x{state.height}",
        "theme": state.theme.name,
        "screens": [s.Name for s in state.screens],
        "screen_count": len(state.screens),
        "total_controls": sum(_count_controls(s) for s in state.screens),
    })


# ── Build Tools ─────────────────────────────────────────────────────────


@mcp.tool()
async def build_msapp(output_path: str = "") -> str:
    """Compile the current app state to a .msapp file.

    Args:
        output_path: File path for output (default: ./output/{app_name}.msapp)
    """
    state = get_state()

    if not state.screens:
        return json.dumps({"error": "App has no screens. Add at least one screen before building."})

    # Compile
    msapp_bytes = compile_msapp(state)

    # Determine output path
    if not output_path:
        _OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        safe_name = state.name.replace(" ", "_").replace("/", "_")
        output_path = str(_OUTPUT_DIR / f"{safe_name}.msapp")

    # Write file
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(msapp_bytes)

    return json.dumps({
        "status": "built",
        "path": str(out.resolve()),
        "size_bytes": len(msapp_bytes),
        "screens": len(state.screens),
        "total_controls": sum(_count_controls(s) for s in state.screens),
    })


@mcp.tool()
async def validate_app() -> str:
    """Validate the current app for structural errors before building."""
    state = get_state()
    errors: list[str] = []
    warnings: list[str] = []

    if not state.screens:
        errors.append("App has no screens")

    # Check for duplicate control names
    all_names: list[str] = []

    def _collect_names(control: "Control") -> None:
        all_names.append(control.Name)
        for child in control.Children:
            _collect_names(child)

    for screen in state.screens:
        _collect_names(screen)

    seen = set()
    for n in all_names:
        if n in seen:
            errors.append(f"Duplicate control name: '{n}'")
        seen.add(n)

    # Check Navigate targets
    screen_names = {s.Name for s in state.screens}

    def _check_navigate(control: "Control") -> None:
        for r in control.Rules:
            if "Navigate(" in r.InvariantScript:
                # Extract target screen name
                import re
                matches = re.findall(r"Navigate\(\s*(\w+)", r.InvariantScript)
                for target in matches:
                    if target not in screen_names:
                        warnings.append(
                            f"Control '{control.Name}' navigates to unknown screen '{target}'"
                        )
        for child in control.Children:
            _check_navigate(child)

    for screen in state.screens:
        _check_navigate(screen)

    return json.dumps({
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "stats": {
            "screens": len(state.screens),
            "total_controls": sum(_count_controls(s) for s in state.screens),
        },
    })


# ── Preview Tools ──────────────────────────────────────────────────────


@mcp.tool()
async def preview_app(output_path: str = "", open_browser: bool = True) -> str:
    """Generate an interactive HTML preview of the current app.

    Creates a standalone HTML file that visually approximates how the app
    will look in Power Apps. Includes screen tabs, interactive controls,
    and navigation. Use this to iterate on the design before exporting.

    Args:
        output_path: File path for the HTML (default: ./output/{app_name}_preview.html)
        open_browser: Whether to open the preview in the default browser
    """
    state = get_state()

    if not state.screens:
        return json.dumps({"error": "App has no screens. Add at least one screen before previewing."})

    # Generate HTML
    html_content = generate_preview_html(state)

    # Determine output path
    if not output_path:
        _OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        safe_name = state.name.replace(" ", "_").replace("/", "_")
        output_path = str(_OUTPUT_DIR / f"{safe_name}_preview.html")

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html_content, encoding="utf-8")

    # Open in browser
    if open_browser:
        import webbrowser
        webbrowser.open(f"file://{out.resolve()}")

    return json.dumps({
        "status": "preview_generated",
        "path": str(out.resolve()),
        "size_bytes": len(html_content.encode("utf-8")),
        "screens": [s.Name for s in state.screens],
        "url": f"file://{out.resolve()}",
    })


# ── Helpers ─────────────────────────────────────────────────────────────


def _count_controls(control: "Control") -> int:
    """Count total controls in a subtree (including the root)."""
    count = 1
    for child in control.Children:
        count += _count_controls(child)
    return count


def _control_tree(control: "Control") -> dict:
    """Build a summary tree of a control and its children."""
    children = [_control_tree(c) for c in control.Children]
    result: dict = {
        "name": control.Name,
        "type": control.Template.Name,
    }
    if children:
        result["children"] = children
    return result


# ── Entry point ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run()
