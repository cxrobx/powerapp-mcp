"""Template registry — XML template blobs for each control type."""

from __future__ import annotations

import json
from pathlib import Path

_DATA_DIR = Path(__file__).parent / "data"

# Loaded lazily on first access
_registry: dict[str, dict] | None = None


def _load_registry() -> dict[str, dict]:
    global _registry
    if _registry is None:
        registry_path = _DATA_DIR / "template_registry.json"
        if registry_path.exists():
            with open(registry_path) as f:
                _registry = json.load(f)
        else:
            _registry = {}
    return _registry


def get_template_xml(control_type: str) -> str | None:
    """Get the XML template blob for a control type. Returns None if not found."""
    reg = _load_registry()
    entry = reg.get(control_type)
    if entry:
        return entry.get("Template")
    return None


def get_template_version(control_type: str) -> str | None:
    """Get the known template version for a control type."""
    reg = _load_registry()
    entry = reg.get(control_type)
    if entry:
        return entry.get("Version")
    return None


def get_used_templates(control_types: set[str]) -> list[dict]:
    """Get the UsedTemplates array for Templates.json.

    Only includes templates for control types actually used in the app.
    """
    reg = _load_registry()
    used = []
    for ct in sorted(control_types):
        entry = reg.get(ct)
        if entry and entry.get("Template"):
            used.append({
                "Name": entry["Name"],
                "Version": entry["Version"],
                "Template": entry["Template"],
            })
    return used


def list_available_templates() -> list[str]:
    """List all control types that have XML templates registered."""
    reg = _load_registry()
    return sorted(reg.keys())
