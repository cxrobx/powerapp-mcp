"""Properties.json generation — app config, feature flags, connection refs."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from .models import AppState

_DATA_DIR = Path(__file__).parent / "data"

# Loaded lazily
_default_flags: dict | None = None


def _load_default_flags() -> dict:
    global _default_flags
    if _default_flags is None:
        path = _DATA_DIR / "default_flags.json"
        if path.exists():
            with open(path) as f:
                _default_flags = json.load(f)
        else:
            _default_flags = {}
    return _default_flags


def generate_properties(state: AppState) -> dict:
    """Generate the full Properties.json dict from app state."""
    control_counts = state.count_controls_by_type()

    # Build connection references JSON string
    conn_refs_str = json.dumps(
        {k: v.model_dump() for k, v in state.connection_references.items()}
    ) if state.connection_references else "{}"

    return {
        "Author": "",
        "Name": state.name,
        "Id": state.app_id,
        "FileID": state.app_id,
        "AppDescription": "",
        "AppCreationSource": "FromBlank",
        "DocumentLayoutWidth": state.width,
        "DocumentLayoutHeight": state.height,
        "DocumentLayoutOrientation": state.orientation,
        "DocumentLayoutScaleToFit": True,
        "DocumentLayoutMaintainAspectRatio": True,
        "DocumentLayoutLockOrientation": False,
        "DocumentAppType": state.app_type,
        "OriginatingVersion": state.doc_version,
        "DocumentType": "App",
        "DefaultConnectedDataSourceMaxGetRowsCount": 500,
        "ManualOfflineProfileId": "",
        "LocalConnectionReferences": conn_refs_str,
        "LocalDatabaseReferences": "{}",
        "LibraryDependencies": "[]",
        "ControlCount": control_counts,
        "DeserializationLoadTime": 0.0,
        "AnalysisLoadTime": 0.0,
        "ParserErrorCount": 0,
        "BindingErrorCount": 0,
        "ContainsThirdPartyPcfControls": False,
        "InstrumentationKey": "",
        "EnableInstrumentation": False,
        "AppPreviewFlagsMap": _load_default_flags(),
    }
