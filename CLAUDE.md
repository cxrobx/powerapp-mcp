# Power Apps MCP Server

MCP server that generates Power Apps `.msapp` files from natural language via Claude Code.

## Architecture

- **Python + FastMCP** — `@mcp.tool()` decorators, stateful in-memory AppState
- **Compiler pipeline** — AppState (Pydantic models) → JSON files → ZIP → .msapp
- **Knowledge base** — `knowledge/` contains .msapp format reference docs

## Key Modules

| Module | Purpose |
|--------|---------|
| `server.py` | FastMCP("powerapp") + all tool definitions (17 tools) |
| `models.py` | Pydantic models: AppState, Control, Rule, Template |
| `state.py` | Global AppState singleton + ID counter |
| `compiler.py` | Compiles AppState → .msapp ZIP |
| `controls.py` | Control factory with defaults for 40+ control types |
| `templates.py` | XML template registry per control type (30 types) |
| `screen_patterns.py` | Pre-built screen patterns (loading, list, detail, form, settings) |
| `app_templates.py` | Full app templates (list_detail, inspection, directory, tracker) |
| `styles.py` | gblAppStyles semantic color tokens (light/dark themes) |
| `preview.py` | HTML preview renderer — generates interactive visual preview from AppState |
| `properties.py` | Properties.json generation + feature flags |
| `checksum.py` | C8_ + base64(SHA-256) |
| `themes.py` | Built-in theme palettes |
| `datasources.py` | Data source connector configs |
| `validation.py` | Pre-build validation checks |

## Commands

```bash
# Install deps
pip install -e ".[dev]"

# Run MCP server directly (for testing)
python -m powerapp_mcp.server

# Run tests
pytest
```

## Data Files

`src/powerapp_mcp/data/` contains:
- `template_registry.json` — OAX XML templates for 30 control types (extracted from MS Teams templates repo)
- `app_templates.json` — App template catalog with config schemas (4 templates)
- `default_flags.json` — 90 AppPreviewFlagsMap feature flags (aligned with MS production apps)
- `default_theme.json` — Default theme with 62 palette colors

## Knowledge Base

`knowledge/` contains comprehensive Power Apps reference documentation (~150KB total):

| File | Content |
|------|---------|
| [`MSAPP_SCHEMA_REFERENCE.md`](knowledge/MSAPP_SCHEMA_REFERENCE.md) | .msapp ZIP format — Header, Properties, Controls, References, checksums |
| [`POWERAPPS_COMPLETE_REFERENCE.md`](knowledge/POWERAPPS_COMPLETE_REFERENCE.md) | All 60+ controls, 200+ Power Fx functions, operators, connectors, delegation |
| [`CONTROL_PROPERTIES_REFERENCE.md`](knowledge/CONTROL_PROPERTIES_REFERENCE.md) | Every property for every control type with categories and examples |
| [`CONTROL_TYPES_JSON_SCHEMA.json`](knowledge/CONTROL_TYPES_JSON_SCHEMA.json) | JSON Schema v7 for ControlInfo, Template, Rule structures |
| [`AI_FEATURES_REFERENCE.md`](knowledge/AI_FEATURES_REFERENCE.md) | AI Power Fx functions, Copilot, AI Builder, Azure OpenAI, data source compatibility |
| [`CAPABILITIES_OVERVIEW.md`](knowledge/CAPABILITIES_OVERVIEW.md) | App types, data sources, patterns, deployment, integration ecosystem, limitations |
| [`README_SCHEMA_DOCS.md`](knowledge/README_SCHEMA_DOCS.md) | Quick start guide and implementation roadmap |

## .msapp Format

The .msapp is a ZIP containing JSON files. See [`knowledge/MSAPP_SCHEMA_REFERENCE.md`](knowledge/MSAPP_SCHEMA_REFERENCE.md) for the complete format specification.

Key files in the ZIP:
- `Header.json` — version info
- `Properties.json` — app config, feature flags, connection refs
- `Controls/*.json` — one per screen, each a tree of ControlInfo nodes
- `References/` — DataSources, Templates, Themes
- `checksum.json` — file integrity

## Stateful Server

Unlike plex-agent (stateless), this server maintains an in-memory `AppState` across tool calls within a Claude Code session. The state tracks screens, controls, data sources, and theme. Call `build_msapp` to compile the current state to a file.
