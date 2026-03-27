"""Preview renderer — generates interactive HTML preview from AppState.

Converts the in-memory AppState to a standalone HTML page that visually
approximates how the app will look in Power Apps. Controls are rendered
as HTML elements with CSS styling derived from Power Fx property rules.

Key design: parent dimensions are passed down the render tree so that
Parent.Width, Parent.Height, and arithmetic formulas resolve correctly.
"""

from __future__ import annotations

import html
import json as _json
import re

from .models import AppState, Control, Rule
from .styles import get_style_preset


# ── Named Colors ──────────────────────────────────────────────────────

_NAMED_COLORS = {
    "White": "rgba(255,255,255,1)", "Black": "rgba(0,0,0,1)",
    "Red": "rgba(255,0,0,1)", "Green": "rgba(0,128,0,1)",
    "Blue": "rgba(0,0,255,1)", "Yellow": "rgba(255,255,0,1)",
    "Gray": "rgba(128,128,128,1)", "Silver": "rgba(192,192,192,1)",
    "Orange": "rgba(255,165,0,1)", "Purple": "rgba(128,0,128,1)",
    "Navy": "rgba(0,0,128,1)", "Teal": "rgba(0,128,128,1)",
    "Transparent": "rgba(0,0,0,0)",
    "DarkGray": "rgba(169,169,169,1)", "LightGray": "rgba(211,211,211,1)",
    "GhostWhite": "rgba(248,248,255,1)", "WhiteSmoke": "rgba(245,245,245,1)",
    "AliceBlue": "rgba(240,248,255,1)", "LightBlue": "rgba(173,216,230,1)",
    "Aqua": "rgba(0,255,255,1)", "Lime": "rgba(0,255,0,1)",
    "Maroon": "rgba(128,0,0,1)", "Olive": "rgba(128,128,0,1)",
    "Fuchsia": "rgba(255,0,255,1)", "Cornsilk": "rgba(255,248,220,1)",
    "DarkBlue": "rgba(0,0,139,1)", "DarkRed": "rgba(139,0,0,1)",
    "DarkGreen": "rgba(0,100,0,1)", "OrangeRed": "rgba(255,69,0,1)",
    "Gold": "rgba(255,215,0,1)", "Salmon": "rgba(250,128,114,1)",
    "MidnightBlue": "rgba(25,25,112,1)",
}

# ── Context for rendering ─────────────────────────────────────────────

class RenderContext:
    """Carries parent dimensions, styles, and screen names down the tree."""
    __slots__ = ("parent_w", "parent_h", "styles", "screen_names", "app_w", "app_h")

    def __init__(self, parent_w: float, parent_h: float, styles: dict, screen_names: list, app_w: int, app_h: int):
        self.parent_w = parent_w
        self.parent_h = parent_h
        self.styles = styles
        self.screen_names = screen_names
        self.app_w = app_w
        self.app_h = app_h

    def child(self, w: float, h: float) -> "RenderContext":
        return RenderContext(w, h, self.styles, self.screen_names, self.app_w, self.app_h)


# ── Formula Resolution ─────────────────────────────────────────────────


def _resolve_formula(formula: str, ctx: RenderContext, control_rules: dict[str, str] | None = None) -> str:
    """Resolve a Power Fx formula to a CSS-compatible value."""
    if not formula:
        return ""
    s = formula.strip()

    # RGBA(r, g, b, a)
    m = re.match(r'^RGBA\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*([\d.]+)\s*\)$', s)
    if m:
        return f"rgba({m.group(1)}, {m.group(2)}, {m.group(3)}, {m.group(4)})"

    # gblAppStyles.Property
    m = re.match(r'^gblAppStyles\.(\w+)$', s)
    if m and m.group(1) in ctx.styles:
        return _resolve_formula(ctx.styles[m.group(1)], ctx)

    # Self.Property
    m = re.match(r'^Self\.(\w+)$', s)
    if m and control_rules and m.group(1) in control_rules:
        return _resolve_formula(control_rules[m.group(1)], ctx, None)

    # ColorFade(RGBA(...), pct)
    m = re.match(r'^ColorFade\(\s*RGBA\((\d+),\s*(\d+),\s*(\d+),\s*([\d.]+)\)\s*,\s*(-?[\d.]+)%?\s*\)$', s)
    if m:
        r_, g, b, a = int(m.group(1)), int(m.group(2)), int(m.group(3)), float(m.group(4))
        factor = 1 + float(m.group(5)) / 100
        r_ = max(0, min(255, int(r_ * factor)))
        g = max(0, min(255, int(g * factor)))
        b = max(0, min(255, int(b * factor)))
        return f"rgba({r_}, {g}, {b}, {a})"
    if s.startswith("ColorFade("):
        return ""

    # String literals
    m = re.match(r'^"(.*)"$', s, re.DOTALL)
    if m:
        return m.group(1)

    # Named colors
    m = re.match(r'^Color\.(\w+)$', s)
    if m and m.group(1) in _NAMED_COLORS:
        return _NAMED_COLORS[m.group(1)]

    # Font
    m = re.match(r"^Font\.'(.+)'$", s)
    if m:
        return m.group(1)
    if s.startswith("Font."):
        return s[5:]

    # Enums
    _ENUM_MAPS = {
        "FontWeight": {"Normal": "400", "Semibold": "600", "Bold": "700", "Lighter": "300"},
        "Align": {"Left": "left", "Center": "center", "Right": "right"},
        "VerticalAlign": {"Top": "flex-start", "Middle": "center", "Bottom": "flex-end"},
        "BorderStyle": {"Solid": "solid", "Dashed": "dashed", "Dotted": "dotted", "None": "none"},
        "DisplayMode": {"Edit": "edit", "View": "view", "Disabled": "disabled"},
    }
    for enum_name, enum_map in _ENUM_MAPS.items():
        m = re.match(rf'^{enum_name}\.(\w+)$', s)
        if m and m.group(1) in enum_map:
            return enum_map[m.group(1)]

    # Boolean
    if s in ("true", "false"):
        return s

    # Pure numeric
    if re.match(r'^-?\d+(\.\d+)?$', s):
        return s

    # Icon.Name
    m = re.match(r'^Icon\.(\w+)$', s)
    if m:
        return m.group(1)

    return s


def _resolve_numeric(formula: str, ctx: RenderContext, default: float,
                     sibling_positions: dict[str, dict[str, float]] | None = None) -> float:
    """Resolve a formula to a numeric value for positioning (X, Y, Width, Height).

    Handles: plain numbers, Parent.Width/Height, basic arithmetic (+, -, *, /),
    App.Width/Height, Max/Min, cross-control references (ControlName.Property),
    and nested combinations.
    """
    if not formula:
        return default

    s = formula.strip()

    # Pure number
    try:
        return float(s)
    except ValueError:
        pass

    # Substitution pass — replace known references with numbers
    expr = s
    expr = re.sub(r'Parent\.Width\b', str(ctx.parent_w), expr)
    expr = re.sub(r'Parent\.Height\b', str(ctx.parent_h), expr)
    expr = re.sub(r'Parent\.X\b', '0', expr)
    expr = re.sub(r'Parent\.Y\b', '0', expr)
    expr = re.sub(r'App\.Width\b', str(ctx.app_w), expr)
    expr = re.sub(r'App\.Height\b', str(ctx.app_h), expr)
    expr = re.sub(r'App\.MinScreenWidth\b', str(ctx.app_w), expr)
    expr = re.sub(r'App\.MinScreenHeight\b', str(ctx.app_h), expr)
    expr = re.sub(r'Self\.Width\b', str(ctx.parent_w), expr)
    expr = re.sub(r'Self\.Height\b', str(ctx.parent_h), expr)

    # Cross-control references: ControlName.Property (e.g., DataCardKey10.Height)
    if sibling_positions:
        def _sub_sibling(m):
            ctrl_name = m.group(1)
            prop = m.group(2)
            if ctrl_name in sibling_positions and prop in sibling_positions[ctrl_name]:
                return str(sibling_positions[ctrl_name][prop])
            return m.group(0)
        expr = re.sub(r'(\w+)\.(X|Y|Width|Height)\b', _sub_sibling, expr)

    # Max(a, b) and Min(a, b) — simple two-arg
    def _eval_maxmin(m):
        fn = m.group(1)
        try:
            a = float(m.group(2))
            b = float(m.group(3))
            return str(max(a, b) if fn == "Max" else min(a, b))
        except (ValueError, TypeError):
            return m.group(0)

    for _ in range(3):  # iterate to handle nesting
        expr = re.sub(r'(Max|Min)\(\s*([\d.]+)\s*,\s*([\d.]+)\s*\)', _eval_maxmin, expr)

    # Try safe arithmetic eval (only digits, +, -, *, /, parens, dots, spaces)
    clean = expr.strip()
    if re.match(r'^[\d\s\+\-\*\/\(\)\.]+$', clean):
        try:
            result = float(eval(clean))  # safe: only numbers and operators
            return result
        except Exception:
            pass

    return default


def _precompute_sibling_positions(children: list[Control], ctx: RenderContext) -> dict[str, dict[str, float]]:
    """Pre-compute positions for all children with simple numeric X/Y/W/H.

    Does multiple passes to resolve cross-references between siblings.
    """
    positions: dict[str, dict[str, float]] = {}

    # Pass 1: collect controls with directly numeric positions
    for child in children:
        rules = _get_rules(child)
        pos = {}
        for prop in ("X", "Y", "Width", "Height"):
            val = rules.get(prop, "")
            try:
                pos[prop] = float(val)
            except (ValueError, TypeError):
                pass
        if pos:
            positions[child.Name] = pos

    # Pass 2-4: resolve cross-references iteratively
    for _ in range(3):
        changed = False
        for child in children:
            rules = _get_rules(child)
            if child.Name not in positions:
                positions[child.Name] = {}
            for prop in ("X", "Y", "Width", "Height"):
                if prop in positions[child.Name]:
                    continue  # already resolved
                val = rules.get(prop, "")
                if not val:
                    continue
                result = _resolve_numeric(val, ctx, -9999, positions)
                if result != -9999:
                    positions[child.Name][prop] = result
                    changed = True
        if not changed:
            break

    return positions


def _get_rules(control: Control) -> dict[str, str]:
    return {r.Property: r.InvariantScript for r in control.Rules}


def _prop(rules: dict[str, str], name: str, ctx: RenderContext, default: str = "") -> str:
    formula = rules.get(name, "")
    if not formula:
        return default
    return _resolve_formula(formula, ctx, rules) or default


def _num(rules: dict[str, str], name: str, ctx: RenderContext, default: float = 0,
         siblings: dict[str, dict[str, float]] | None = None) -> float:
    return _resolve_numeric(rules.get(name, ""), ctx, default, siblings)


# ── Display Text ──────────────────────────────────────────────────────

_RUNTIME_MARKERS = [
    "CountRows(", "Filter(", "LookUp(", "Sum(", "Average(",
    "ThisItem.", "ThisRecord.", "Parent.DisplayName", "Parent.Error",
    "User().", "Now()", "Today()", "Param(",
    "Concat(", "First(", "Last(", "Sort(", "Search(",
    "Text(", "Value(", "If(", "Switch(",
]


def _display_text(rules: dict[str, str], ctx: RenderContext, default: str = "") -> str:
    """Resolve Text for display, converting runtime formulas to placeholders."""
    formula = rules.get("Text", "")
    if not formula:
        return default

    # String literal
    m = re.match(r'^"(.*)"$', formula.strip(), re.DOTALL)
    if m:
        return m.group(1)

    resolved = _resolve_formula(formula, ctx, rules)

    # Parent.DisplayName → "[Field]"
    if "Parent.DisplayName" in formula:
        return ""
    if "Parent.Error" in formula:
        return ""

    # Runtime formula → placeholder
    if any(marker in resolved for marker in _RUNTIME_MARKERS):
        if "CountRows(" in formula or "Count(" in formula:
            return "0"
        if "ThisItem." in formula:
            field = re.search(r'ThisItem\.(\w+)', formula)
            return f"[{field.group(1)}]" if field else "[data]"
        if "User()." in formula:
            return "User Name"
        if "Now()" in formula or "Today()" in formula:
            return "3/27/2026"
        return ""

    return resolved


# ── Icon SVGs ─────────────────────────────────────────────────────────

_ICON_SVG = {
    "Add": '<path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/>',
    "BackArrow": '<path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/>',
    "ChevronRight": '<path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/>',
    "Check": '<path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>',
    "Cancel": '<path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>',
    "Edit": '<path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04a1 1 0 000-1.41l-2.34-2.34a1 1 0 00-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/>',
    "Search": '<path d="M15.5 14h-.79l-.28-.27A6.47 6.47 0 0016 9.5 6.5 6.5 0 109.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>',
    "Settings": '<path d="M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58a.49.49 0 00.12-.61l-1.92-3.32a.49.49 0 00-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94L14.4 2.81a.47.47 0 00-.47-.41h-3.84c-.24 0-.43.17-.47.41L9.25 5.35c-.59.24-1.13.57-1.62.94l-2.39-.96a.49.49 0 00-.59.22L2.74 8.87a.49.49 0 00.12.61l2.03 1.58c-.05.3-.07.62-.07.94s.02.64.07.94l-2.03 1.58a.49.49 0 00-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6A3.6 3.6 0 1115.6 12 3.61 3.61 0 0112 15.6z"/>',
    "Home": '<path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/>',
    "Trash": '<path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"/>',
    "Information": '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/>',
    "Warning": '<path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"/>',
}


# ── Navigate helper ───────────────────────────────────────────────────

def _navigate_js(formula: str, screen_names: list[str]) -> str:
    if not formula:
        return ""
    m = re.search(r'Navigate\(\s*(\w+)', formula)
    if m and m.group(1) in screen_names:
        return f'onclick="switchScreen(\'{m.group(1)}\')"'
    return ""


# ── Styling helpers ───────────────────────────────────────────────────

def _font_css(rules: dict[str, str], ctx: RenderContext) -> str:
    parts = []
    font = _prop(rules, "Font", ctx)
    if font:
        parts.append(f"font-family:'{font}',sans-serif")
    size = _prop(rules, "Size", ctx)
    if size and re.match(r'^\d+$', size):
        parts.append(f"font-size:{size}px")
    weight = _prop(rules, "FontWeight", ctx)
    if weight:
        parts.append(f"font-weight:{weight}")
    align = _prop(rules, "Align", ctx)
    if align:
        parts.append(f"text-align:{align}")
    return ";".join(parts)


def _border_css(rules: dict[str, str], ctx: RenderContext) -> str:
    thickness = _prop(rules, "BorderThickness", ctx, "0")
    if not re.match(r'^\d+', thickness):
        thickness = "0"
    color = _prop(rules, "BorderColor", ctx, "transparent")
    style = _prop(rules, "BorderStyle", ctx, "solid")
    if style not in ("solid", "dashed", "dotted", "none"):
        style = "solid"
    radius_parts = []
    for corner in ["RadiusTopLeft", "RadiusTopRight", "RadiusBottomRight", "RadiusBottomLeft"]:
        r = _prop(rules, corner, ctx, "0")
        if not re.match(r'^\d+', r):
            r = "0"
        radius_parts.append(f"{r}px")
    return f"border:{thickness}px {style} {color};border-radius:{' '.join(radius_parts)}"


def _pos_css(rules: dict[str, str], ctx: RenderContext,
             siblings: dict[str, dict[str, float]] | None = None) -> tuple[str, float, float]:
    """Return (CSS string, resolved_width, resolved_height)."""
    x = _num(rules, "X", ctx, 0, siblings)
    y = _num(rules, "Y", ctx, 0, siblings)
    w = _num(rules, "Width", ctx, ctx.parent_w, siblings)
    h = _num(rules, "Height", ctx, 50, siblings)
    z = _num(rules, "ZIndex", ctx, 1, siblings)
    visible = _prop(rules, "Visible", ctx, "true")
    display = "none" if visible == "false" else "block"

    css = (
        f"position:absolute;left:{x:.0f}px;top:{y:.0f}px;"
        f"width:{w:.0f}px;height:{h:.0f}px;"
        f"z-index:{z:.0f};display:{display};box-sizing:border-box;"
    )
    return css, w, h


# ── Control renderers ─────────────────────────────────────────────────
# Every renderer signature: (control, rules, ctx) -> str


def _get_z(control: Control) -> float:
    for r in control.Rules:
        if r.Property == "ZIndex":
            try:
                return float(r.InvariantScript)
            except (ValueError, TypeError):
                pass
    return control.Index


def _render_children(control: Control, ctx: RenderContext) -> str:
    return "\n".join(
        _render_control(c, ctx) for c in sorted(control.Children, key=_get_z)
    )


def _render_control(control: Control, ctx: RenderContext) -> str:
    ctype = control.Template.Name
    rules = _get_rules(control)
    renderer = _RENDERERS.get(ctype, _render_container)
    return renderer(control, rules, ctx)


def _render_screen(control: Control, rules: dict[str, str], ctx: RenderContext) -> str:
    fill = _prop(rules, "Fill", ctx, "rgba(255,255,255,1)")
    w = _num(rules, "Width", ctx, ctx.app_w)
    h = _num(rules, "Height", ctx, ctx.app_h)

    child_ctx = ctx.child(w, h)
    children = _render_children(control, child_ctx)

    return (
        f'<div class="pa-screen" data-screen="{html.escape(control.Name)}" '
        f'style="position:relative;width:{w:.0f}px;height:{h:.0f}px;background:{fill};overflow:hidden">'
        f'{children}</div>'
    )


def _render_button(control: Control, rules: dict[str, str], ctx: RenderContext) -> str:
    pos, w, h = _pos_css(rules, ctx)
    fill = _prop(rules, "Fill", ctx, "rgba(56,96,178,1)")
    color = _prop(rules, "Color", ctx, "rgba(255,255,255,1)")
    text = _display_text(rules, ctx, "Button")
    font = _font_css(rules, ctx)
    border = _border_css(rules, ctx)
    onclick = _navigate_js(rules.get("OnSelect", ""), ctx.screen_names)

    return (
        f'<button class="pa-ctrl" data-name="{html.escape(control.Name)}" '
        f'style="{pos}background:{fill};color:{color};{font};{border};cursor:pointer;outline:none;'
        f'display:flex;align-items:center;justify-content:center" {onclick}>'
        f'{html.escape(text)}</button>'
    )


def _render_label(control: Control, rules: dict[str, str], ctx: RenderContext) -> str:
    pos, w, h = _pos_css(rules, ctx)
    fill = _prop(rules, "Fill", ctx, "transparent")
    color = _prop(rules, "Color", ctx, "rgba(0,0,0,1)")
    text = _display_text(rules, ctx, "")
    if not text:
        # Don't render empty labels
        return ""
    font = _font_css(rules, ctx)
    valign = _prop(rules, "VerticalAlign", ctx, "flex-start")
    overflow = _prop(rules, "Overflow", ctx, "hidden")
    padding = ""
    for side in ["Top", "Right", "Bottom", "Left"]:
        p = _prop(rules, f"Padding{side}", ctx, "0")
        if not re.match(r'^\d+', p):
            p = "0"
        padding += f"padding-{side.lower()}:{p}px;"

    is_placeholder = text.startswith("[") and text.endswith("]")
    opacity = "opacity:0.45;font-style:italic;" if is_placeholder else ""

    return (
        f'<div class="pa-ctrl" data-name="{html.escape(control.Name)}" '
        f'style="{pos}background:{fill};color:{color};{font};{padding}{opacity}'
        f'display:flex;align-items:{valign};overflow:{overflow};word-wrap:break-word">'
        f'<span style="width:100%">{html.escape(text)}</span></div>'
    )


def _render_text_input(control: Control, rules: dict[str, str], ctx: RenderContext) -> str:
    pos, w, h = _pos_css(rules, ctx)
    fill = _prop(rules, "Fill", ctx, "rgba(255,255,255,1)")
    color = _prop(rules, "Color", ctx, "rgba(0,0,0,1)")
    hint = _prop(rules, "HintText", ctx, "")
    font = _font_css(rules, ctx)
    border = _border_css(rules, ctx)

    return (
        f'<input class="pa-ctrl" data-name="{html.escape(control.Name)}" '
        f'type="text" placeholder="{html.escape(hint)}" '
        f'style="{pos}background:{fill};color:{color};{font};{border};padding:0 12px;outline:none" />'
    )


def _render_rectangle(control: Control, rules: dict[str, str], ctx: RenderContext) -> str:
    pos, w, h = _pos_css(rules, ctx)
    fill = _prop(rules, "Fill", ctx, "rgba(56,96,178,1)")
    border = _border_css(rules, ctx)
    return f'<div class="pa-ctrl" data-name="{html.escape(control.Name)}" style="{pos}background:{fill};{border}"></div>'


def _render_circle(control: Control, rules: dict[str, str], ctx: RenderContext) -> str:
    pos, w, h = _pos_css(rules, ctx)
    fill = _prop(rules, "Fill", ctx, "rgba(56,96,178,1)")
    border = _border_css(rules, ctx)
    return f'<div class="pa-ctrl" data-name="{html.escape(control.Name)}" style="{pos}background:{fill};{border};border-radius:50%"></div>'


def _render_icon(control: Control, rules: dict[str, str], ctx: RenderContext) -> str:
    pos, w, h = _pos_css(rules, ctx)
    color = _prop(rules, "Color", ctx, "rgba(0,0,0,1)")
    fill = _prop(rules, "Fill", ctx, "transparent")
    icon_name = _prop(rules, "Icon", ctx, "Add")
    onclick = _navigate_js(rules.get("OnSelect", ""), ctx.screen_names)

    svg_path = _ICON_SVG.get(icon_name, _ICON_SVG.get("Add", ""))
    svg = f'<svg viewBox="0 0 24 24" fill="currentColor" style="width:60%;height:60%">{svg_path}</svg>'

    return (
        f'<div class="pa-ctrl pa-icon" data-name="{html.escape(control.Name)}" '
        f'style="{pos}background:{fill};color:{color};cursor:pointer;'
        f'display:flex;align-items:center;justify-content:center" {onclick}>{svg}</div>'
    )


def _render_gallery(control: Control, rules: dict[str, str], ctx: RenderContext) -> str:
    pos, w, h = _pos_css(rules, ctx)
    fill = _prop(rules, "Fill", ctx, "transparent")
    template_size = _num(rules, "TemplateSize", ctx, 60)
    border = _border_css(rules, ctx)

    # Gallery children are the template controls — repeat them N times
    sample_count = max(1, min(6, int(h / max(template_size, 1))))
    child_ctx = ctx.child(w, template_size)

    items_html = ""
    for i in range(sample_count):
        item_children = "\n".join(
            _render_control(c, child_ctx) for c in sorted(control.Children, key=_get_z)
        )
        items_html += (
            f'<div style="position:relative;width:{w:.0f}px;height:{template_size:.0f}px;'
            f'overflow:hidden;border-bottom:1px solid rgba(0,0,0,0.06)">'
            f'{item_children}</div>'
        )

    return (
        f'<div class="pa-ctrl" data-name="{html.escape(control.Name)}" '
        f'style="{pos}background:{fill};{border};overflow-y:auto">'
        f'{items_html}</div>'
    )


def _render_dropdown(control: Control, rules: dict[str, str], ctx: RenderContext) -> str:
    pos, w, h = _pos_css(rules, ctx)
    fill = _prop(rules, "Fill", ctx, "rgba(255,255,255,1)")
    color = _prop(rules, "Color", ctx, "rgba(0,0,0,1)")
    border = _border_css(rules, ctx)
    font = _font_css(rules, ctx)

    items_raw = _prop(rules, "Items", ctx, "")
    options = ""
    try:
        items = _json.loads(items_raw.replace("'", '"'))
        for item in items:
            options += f'<option>{html.escape(str(item))}</option>'
    except Exception:
        display = items_raw[:40] if items_raw else "Select..."
        options = f'<option>{html.escape(display)}</option>'

    return (
        f'<select class="pa-ctrl" data-name="{html.escape(control.Name)}" '
        f'style="{pos}background:{fill};color:{color};{font};{border};outline:none;padding:0 8px">'
        f'{options}</select>'
    )


def _render_checkbox(control: Control, rules: dict[str, str], ctx: RenderContext) -> str:
    pos, w, h = _pos_css(rules, ctx)
    color = _prop(rules, "Color", ctx, "rgba(0,0,0,1)")
    text = _display_text(rules, ctx, "Option")
    font = _font_css(rules, ctx)
    checked = _prop(rules, "Default", ctx, "false") == "true"

    return (
        f'<label class="pa-ctrl" data-name="{html.escape(control.Name)}" '
        f'style="{pos}color:{color};{font};display:flex;align-items:center;gap:8px;cursor:pointer">'
        f'<input type="checkbox" {"checked" if checked else ""} />{html.escape(text)}</label>'
    )


def _render_toggle(control: Control, rules: dict[str, str], ctx: RenderContext) -> str:
    pos, w, h = _pos_css(rules, ctx)
    true_fill = _prop(rules, "TrueFill", ctx, "rgba(56,96,178,1)")
    false_fill = _prop(rules, "FalseFill", ctx, "rgba(186,186,186,1)")
    checked = _prop(rules, "Default", ctx, "false") == "true"
    bg = true_fill if checked else false_fill

    return (
        f'<div class="pa-ctrl" data-name="{html.escape(control.Name)}" style="{pos}display:flex;align-items:center">'
        f'<label class="toggle-switch"><input type="checkbox" {"checked" if checked else ""} '
        f'data-true-fill="{true_fill}" data-false-fill="{false_fill}" />'
        f'<span class="toggle-slider" style="background:{bg}"></span></label></div>'
    )


def _render_slider(control: Control, rules: dict[str, str], ctx: RenderContext) -> str:
    pos, w, h = _pos_css(rules, ctx)
    min_v = _prop(rules, "Min", ctx, "0")
    max_v = _prop(rules, "Max", ctx, "100")
    default = _prop(rules, "Default", ctx, "50")
    accent = _prop(rules, "HandleFill", ctx, "rgba(56,96,178,1)")

    return (
        f'<div class="pa-ctrl" data-name="{html.escape(control.Name)}" style="{pos}display:flex;align-items:center">'
        f'<input type="range" min="{min_v}" max="{max_v}" value="{default}" '
        f'style="width:100%;accent-color:{accent}" /></div>'
    )


def _render_date_picker(control: Control, rules: dict[str, str], ctx: RenderContext) -> str:
    pos, w, h = _pos_css(rules, ctx)
    fill = _prop(rules, "Fill", ctx, "rgba(255,255,255,1)")
    color = _prop(rules, "Color", ctx, "rgba(0,0,0,1)")
    border = _border_css(rules, ctx)
    return (
        f'<input class="pa-ctrl" data-name="{html.escape(control.Name)}" type="date" '
        f'style="{pos}background:{fill};color:{color};{border};outline:none;padding:0 10px" />'
    )


def _render_rating(control: Control, rules: dict[str, str], ctx: RenderContext) -> str:
    pos, w, h = _pos_css(rules, ctx)
    max_v = int(_num(rules, "Max", ctx, 5))
    default = int(_num(rules, "Default", ctx, 0))
    fill_color = _prop(rules, "RatingFill", ctx, "rgba(255,193,7,1)")

    stars = ""
    for i in range(1, max_v + 1):
        c = fill_color if i <= default else "rgba(200,200,200,1)"
        stars += f'<span style="color:{c};font-size:16px">&#9733;</span>'

    return (
        f'<div class="pa-ctrl" data-name="{html.escape(control.Name)}" '
        f'style="{pos}display:flex;align-items:center;gap:1px;overflow:hidden">{stars}</div>'
    )


def _render_image(control: Control, rules: dict[str, str], ctx: RenderContext) -> str:
    pos, w, h = _pos_css(rules, ctx)
    border = _border_css(rules, ctx)
    return (
        f'<div class="pa-ctrl" data-name="{html.escape(control.Name)}" '
        f'style="{pos}{border};background:rgba(200,200,200,0.2);'
        f'display:flex;align-items:center;justify-content:center;color:rgba(150,150,150,0.5)">'
        f'<svg viewBox="0 0 24 24" fill="currentColor" width="24" height="24">'
        f'<path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2z'
        f'M8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/></svg></div>'
    )


def _render_timer(control: Control, rules: dict[str, str], ctx: RenderContext) -> str:
    visible = _prop(rules, "Visible", ctx, "true")
    if visible == "false":
        return ""
    pos, w, h = _pos_css(rules, ctx)
    fill = _prop(rules, "Fill", ctx, "rgba(56,96,178,1)")
    color = _prop(rules, "Color", ctx, "rgba(255,255,255,1)")
    return (
        f'<div class="pa-ctrl" data-name="{html.escape(control.Name)}" '
        f'style="{pos}background:{fill};color:{color};display:flex;align-items:center;justify-content:center;'
        f'font-size:11px">Timer</div>'
    )


def _render_html_viewer(control: Control, rules: dict[str, str], ctx: RenderContext) -> str:
    pos, w, h = _pos_css(rules, ctx)
    fill = _prop(rules, "Fill", ctx, "rgba(255,255,255,1)")
    border = _border_css(rules, ctx)
    return (
        f'<div class="pa-ctrl" data-name="{html.escape(control.Name)}" '
        f'style="{pos}background:{fill};{border};overflow:auto;padding:5px"></div>'
    )


def _render_data_table(control: Control, rules: dict[str, str], ctx: RenderContext) -> str:
    pos, w, h = _pos_css(rules, ctx)
    fill = _prop(rules, "Fill", ctx, "rgba(255,255,255,1)")
    border = _border_css(rules, ctx)
    hfill = _prop(rules, "HeadingFill", ctx, "rgba(234,234,236,1)")
    hcolor = _prop(rules, "HeadingColor", ctx, "rgba(0,0,0,1)")

    return (
        f'<div class="pa-ctrl" data-name="{html.escape(control.Name)}" '
        f'style="{pos}background:{fill};{border};overflow:auto">'
        f'<div style="background:{hfill};color:{hcolor};padding:8px 12px;font-weight:600;font-size:13px;'
        f'border-bottom:1px solid rgba(0,0,0,0.1)">Column 1 | Column 2 | Column 3</div>'
        f'<div style="padding:8px 12px;color:rgba(150,150,150,1);font-size:12px">No data</div></div>'
    )


def _is_form_grid(control: Control) -> bool:
    """Detect if a form/container uses grid coordinates (small integers for X/Y)."""
    if not control.Children:
        return False
    card_types = {"typedDataCard", "dataCard"}
    grid_children = 0
    for child in control.Children:
        if child.Template.Name not in card_types:
            continue
        rules = _get_rules(child)
        try:
            x = float(rules.get("X", "999"))
            y = float(rules.get("Y", "999"))
            if x < 20 and y < 50 and x == int(x) and y == int(y):
                grid_children += 1
        except (ValueError, TypeError):
            pass
    return grid_children >= 3  # at least 3 cards using grid coords


def _render_form_grid(control: Control, rules: dict[str, str], ctx: RenderContext) -> str:
    """Render a form that uses grid coordinates for its data card children."""
    pos, w, h = _pos_css(rules, ctx)
    fill = _prop(rules, "Fill", ctx, "transparent")

    # Determine grid dimensions from children
    max_col = 0
    max_row = 0
    card_w = 370  # default
    card_h = 108  # default
    card_types = {"typedDataCard", "dataCard"}

    for child in control.Children:
        if child.Template.Name not in card_types:
            continue
        crules = _get_rules(child)
        try:
            col = int(float(crules.get("X", "0")))
            row = int(float(crules.get("Y", "0")))
            max_col = max(max_col, col)
            max_row = max(max_row, row)
            cw = crules.get("Width", "")
            ch = crules.get("Height", "")
            if cw and cw.isdigit():
                card_w = int(cw)
            if ch and ch.isdigit():
                card_h = int(ch)
        except (ValueError, TypeError):
            pass

    num_cols = max_col + 1
    # Compute actual grid size to fit parent
    col_w = min(card_w, int(w / max(num_cols, 1)))
    total_h = (max_row + 1) * card_h

    # Render each card at its grid position
    cards_html = ""
    for child in sorted(control.Children, key=_get_z):
        crules = _get_rules(child)
        if child.Template.Name in card_types:
            try:
                col = int(float(crules.get("X", "0")))
                row = int(float(crules.get("Y", "0")))
            except (ValueError, TypeError):
                col, row = 0, 0
            px_x = col * col_w
            px_y = row * card_h

            # Render the card's children with sibling-aware positioning
            child_ctx = ctx.child(col_w, card_h)
            siblings = _precompute_sibling_positions(child.Children, child_ctx)
            inner_html = ""
            for grandchild in sorted(child.Children, key=_get_z):
                inner_html += _render_control_with_siblings(grandchild, child_ctx, siblings)

            cards_html += (
                f'<div class="pa-ctrl" data-name="{html.escape(child.Name)}" '
                f'style="position:absolute;left:{px_x}px;top:{px_y}px;'
                f'width:{col_w}px;height:{card_h}px;box-sizing:border-box;'
                f'overflow:hidden;border-bottom:1px solid rgba(0,0,0,0.06);'
                f'padding:4px 0">{inner_html}</div>'
            )
        else:
            # Non-card children render normally
            child_ctx = ctx.child(w, total_h)
            cards_html += _render_control(child, child_ctx)

    actual_h = max(total_h, h)
    return (
        f'<div class="pa-ctrl" data-name="{html.escape(control.Name)}" '
        f'style="{pos}background:{fill};overflow-y:auto;height:{actual_h:.0f}px">'
        f'{cards_html}</div>'
    )


def _render_control_with_siblings(control: Control, ctx: RenderContext,
                                   siblings: dict[str, dict[str, float]]) -> str:
    """Render a control using pre-computed sibling positions for cross-references."""
    rules = _get_rules(control)
    ctype = control.Template.Name

    # Use sibling-aware positioning
    pos, w, h = _pos_css(rules, ctx, siblings)
    fill = _prop(rules, "Fill", ctx, "transparent")
    color = _prop(rules, "Color", ctx, "rgba(0,0,0,1)")

    if ctype in ("label", "text"):
        text = _display_text(rules, ctx, "")
        if not text:
            return ""
        font = _font_css(rules, ctx)
        valign = _prop(rules, "VerticalAlign", ctx, "flex-start")
        is_placeholder = text.startswith("[") and text.endswith("]")
        opacity = "opacity:0.45;font-style:italic;" if is_placeholder else ""
        return (
            f'<div class="pa-ctrl" data-name="{html.escape(control.Name)}" '
            f'style="{pos}background:{fill};color:{color};{font};{opacity}'
            f'display:flex;align-items:{valign};overflow:hidden;word-wrap:break-word">'
            f'<span style="width:100%">{html.escape(text)}</span></div>'
        )
    elif ctype in ("combobox", "dropdown"):
        border = _border_css(rules, ctx)
        font = _font_css(rules, ctx)
        items_raw = _prop(rules, "Items", ctx, "")
        display = items_raw[:40] if items_raw else "Select..."
        return (
            f'<select class="pa-ctrl" data-name="{html.escape(control.Name)}" '
            f'style="{pos}background:{fill};color:{color};{font};{border};outline:none;padding:0 8px">'
            f'<option>{html.escape(display)}</option></select>'
        )
    else:
        # Fallback — render as-is with the renderer registry
        renderer = _RENDERERS.get(ctype, _render_container)
        return renderer(control, rules, ctx)


def _render_container(control: Control, rules: dict[str, str], ctx: RenderContext) -> str:
    """Transparent container — used for typedDataCard, dataCard, galleryTemplate, group, form, fluidGrid, etc."""
    # Check if this is a form using grid coordinates
    ctype = control.Template.Name
    if ctype in ("form", "formViewer") and _is_form_grid(control):
        return _render_form_grid(control, rules, ctx)

    pos, w, h = _pos_css(rules, ctx)
    fill = _prop(rules, "Fill", ctx, "transparent")

    child_ctx = ctx.child(w, h)
    # Pre-compute sibling positions for cross-references
    siblings = _precompute_sibling_positions(control.Children, child_ctx)

    children_html = ""
    for child in sorted(control.Children, key=_get_z):
        children_html += _render_control_with_siblings(child, child_ctx, siblings)

    if not children_html.strip():
        return ""

    return (
        f'<div class="pa-ctrl" data-name="{html.escape(control.Name)}" '
        f'style="{pos}background:{fill};overflow:hidden">{children_html}</div>'
    )


# ── Renderer Registry ─────────────────────────────────────────────────

_RENDERERS: dict[str, object] = {
    "screen": _render_screen,
    "button": _render_button,
    "label": _render_label,
    "text": _render_label,
    "textInput": _render_text_input,
    "rectangle": _render_rectangle,
    "circle": _render_circle,
    "triangle": _render_rectangle,
    "icon": _render_icon,
    "gallery": _render_gallery,
    "dropdown": _render_dropdown,
    "combobox": _render_dropdown,
    "checkbox": _render_checkbox,
    "toggle": _render_toggle,
    "toggleSwitch": _render_toggle,
    "slider": _render_slider,
    "datePicker": _render_date_picker,
    "radio": _render_dropdown,
    "rating": _render_rating,
    "timer": _render_timer,
    "image": _render_image,
    "htmlViewer": _render_html_viewer,
    "richTextEditor": _render_html_viewer,
    "dataTable": _render_data_table,
    "videoPlayback": _render_image,
    "addMedia": _render_image,
    "addPicture": _render_image,
    # Container types — render as transparent positioned divs with children
    "form": _render_container,
    "formViewer": _render_container,
    "typedDataCard": _render_container,
    "dataCard": _render_container,
    "galleryTemplate": _render_container,
    "fluidGrid": _render_container,
    "container": _render_container,
    "groupContainer": _render_container,
    "horizontalAutoLayout": _render_container,
    "verticalAutoLayout": _render_container,
    "group": _render_container,
    "hostControl": _render_container,
}


# ── HTML Page Generator ───────────────────────────────────────────────


def generate_preview_html(state: AppState) -> str:
    """Generate a standalone HTML page previewing the full app."""
    if "dark" in state.theme.name.lower():
        styles = get_style_preset("dark")
    else:
        styles = get_style_preset("default")

    screen_names = [s.Name for s in state.screens]
    app_w = state.width
    app_h = state.height

    base_ctx = RenderContext(
        parent_w=app_w, parent_h=app_h,
        styles=styles, screen_names=screen_names,
        app_w=app_w, app_h=app_h,
    )

    screens_html = ""
    for screen in state.screens:
        rules = _get_rules(screen)
        screens_html += _render_screen(screen, rules, base_ctx)

    tabs_html = ""
    for i, name in enumerate(screen_names):
        active = "active" if i == 0 else ""
        tabs_html += f'<button class="tab-btn {active}" onclick="switchScreen(\'{name}\')">{html.escape(name)}</button>'

    is_phone = state.app_type == "Phone" or app_h > app_w

    return _HTML_TEMPLATE.format(
        app_name=html.escape(state.name),
        app_type=state.app_type,
        app_w=app_w,
        app_h=app_h,
        screen_count=len(state.screens),
        first_screen=screen_names[0] if screen_names else "",
        tabs_html=tabs_html,
        screens_html=screens_html,
        is_phone_class="phone" if is_phone else "tablet",
    )


_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{app_name} — Power App Preview</title>
<style>
  * {{ margin: 0; padding: 0; }}
  body {{
    font-family: 'Segoe UI', 'Open Sans', -apple-system, sans-serif;
    background: #1a1a2e;
    color: #fff;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
  }}
  .preview-header {{
    padding: 16px 24px;
    text-align: center;
    width: 100%;
    max-width: 1400px;
  }}
  .preview-header h1 {{ font-size: 18px; font-weight: 600; margin-bottom: 4px; }}
  .preview-header .meta {{ font-size: 12px; color: rgba(255,255,255,0.5); }}
  .tab-bar {{
    display: flex; gap: 4px; padding: 8px 24px;
    flex-wrap: wrap; justify-content: center; max-width: 1400px;
  }}
  .tab-btn {{
    padding: 6px 16px; border: 1px solid rgba(255,255,255,0.15);
    background: rgba(255,255,255,0.05); color: rgba(255,255,255,0.7);
    border-radius: 6px; cursor: pointer; font-size: 12px;
    font-family: inherit; transition: all 0.15s;
  }}
  .tab-btn:hover {{ background: rgba(255,255,255,0.1); color: #fff; }}
  .tab-btn.active {{
    background: rgba(99,140,255,0.25);
    border-color: rgba(99,140,255,0.5); color: #fff;
  }}
  .canvas-wrapper {{
    padding: 20px; display: flex; justify-content: center;
    width: 100%; overflow-x: auto;
  }}
  .canvas-frame {{
    border-radius: 12px; overflow: hidden;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4), 0 0 0 1px rgba(255,255,255,0.08);
    transform-origin: top center; flex-shrink: 0;
  }}
  .canvas-frame.phone {{ border-radius: 24px; border: 3px solid #333; }}
  @media (max-width: 1400px) {{
    .canvas-frame.tablet {{
      transform: scale(calc(min(1, (100vw - 60px) / {app_w})));
    }}
  }}
  .pa-screen {{ display: none; }}
  .pa-screen.active {{ display: block; }}
  .toggle-switch {{ position: relative; display: inline-block; width: 48px; height: 24px; }}
  .toggle-switch input {{ opacity: 0; width: 0; height: 0; }}
  .toggle-slider {{
    position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0;
    border-radius: 24px; transition: 0.2s;
  }}
  .toggle-slider::before {{
    content: ""; position: absolute; height: 18px; width: 18px;
    left: 3px; bottom: 3px; background: white; border-radius: 50%; transition: 0.2s;
  }}
  .toggle-switch input:checked + .toggle-slider::before {{ transform: translateX(24px); }}
  .pa-icon:hover {{ opacity: 0.8; }}
  button.pa-ctrl:hover {{ filter: brightness(0.92); }}
  button.pa-ctrl:active {{ filter: brightness(0.85); }}
  input.pa-ctrl:focus {{ outline: 2px solid rgba(56,96,178,0.5); }}
  .preview-footer {{
    padding: 12px; text-align: center;
    font-size: 11px; color: rgba(255,255,255,0.3);
  }}
</style>
</head>
<body>

<div class="preview-header">
  <h1>{app_name}</h1>
  <div class="meta">{app_type} &middot; {app_w}&times;{app_h} &middot; {screen_count} screens &middot; Power App Preview</div>
</div>

<div class="tab-bar">{tabs_html}</div>

<div class="canvas-wrapper">
  <div class="canvas-frame {is_phone_class}">
    {screens_html}
  </div>
</div>

<div class="preview-footer">
  Generated by powerapp-mcp &middot; Approximation — actual rendering may differ in Power Apps Studio
</div>

<script>
  let currentScreen = '{first_screen}';
  function switchScreen(name) {{
    document.querySelectorAll('.pa-screen').forEach(s => s.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(t => t.classList.remove('active'));
    const el = document.querySelector('[data-screen="' + name + '"]');
    if (el) {{ el.classList.add('active'); currentScreen = name; }}
    document.querySelectorAll('.tab-btn').forEach(t => {{
      if (t.textContent === name) t.classList.add('active');
    }});
  }}
  document.querySelectorAll('.toggle-switch input').forEach(input => {{
    input.addEventListener('change', function() {{
      const sl = this.nextElementSibling;
      sl.style.background = this.checked ? (this.dataset.trueFill||'rgba(56,96,178,1)') : (this.dataset.falseFill||'rgba(186,186,186,1)');
    }});
  }});
  switchScreen(currentScreen);
</script>
</body>
</html>"""
