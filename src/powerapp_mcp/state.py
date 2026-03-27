"""Global AppState singleton for the MCP server session."""

from __future__ import annotations

from .models import AppState

# Module-level singleton — persists across tool calls within a session
_state: AppState | None = None


def get_state() -> AppState:
    """Get the current app state. Raises if no app has been created."""
    if _state is None:
        raise RuntimeError("No app created yet. Call create_app first.")
    return _state


def create_state(name: str, app_type: str = "Tablet") -> AppState:
    """Create a new app state, replacing any existing one."""
    global _state

    dimensions = {
        "Phone": (640, 1136, "portrait"),
        "Tablet": (1366, 768, "landscape"),
        "Desktop": (1366, 768, "landscape"),
    }
    w, h, orient = dimensions.get(app_type, (1366, 768, "landscape"))

    _state = AppState(
        name=name,
        app_type=app_type,
        width=w,
        height=h,
        orientation=orient,
    )
    return _state


def reset_state() -> None:
    """Clear the current app state."""
    global _state
    _state = None


def has_state() -> bool:
    """Check if an app state exists."""
    return _state is not None
