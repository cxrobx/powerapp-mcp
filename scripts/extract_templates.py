#!/usr/bin/env python3
"""Extract OAX XML widget templates from MS Teams Power Apps templates repo.

Usage:
    python scripts/extract_templates.py --repo-path /path/to/teams-powerapps-app-templates

Walks all pkgs/ directories, reads XML widget files, deduplicates by control type
(keeping highest version), and updates data/template_registry.json.
"""

from __future__ import annotations

import argparse
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from packaging.version import Version


def parse_widget_xml(xml_path: Path) -> dict | None:
    """Parse a widget XML file and extract name, version, and full XML string."""
    try:
        xml_text = xml_path.read_text(encoding="utf-8")
        # Parse to extract attributes from <widget> root
        root = ET.fromstring(xml_text)
        name = root.get("name", "")
        version = root.get("version", "")
        widget_id = root.get("id", "")

        if not name or not version:
            return None

        return {
            "Name": name,
            "Version": version,
            "Id": widget_id,
            "Template": xml_text,
        }
    except (ET.ParseError, UnicodeDecodeError) as e:
        print(f"  Warning: Could not parse {xml_path}: {e}")
        return None


def find_all_templates(repo_path: Path) -> dict[str, dict]:
    """Walk all pkgs/ dirs and collect templates, keeping highest version per type."""
    templates: dict[str, dict] = {}

    # Find all XML files in pkgs/ directories (excluding Wadl/ and TableDefinitions/)
    for xml_path in repo_path.rglob("pkgs/*.xml"):
        # Skip connector/WADL/table definition files
        if "/Wadl/" in str(xml_path) or "/TableDefinitions/" in str(xml_path):
            continue

        widget = parse_widget_xml(xml_path)
        if not widget:
            continue

        name = widget["Name"]
        version = widget["Version"]

        if name in templates:
            try:
                existing_ver = Version(templates[name]["Version"])
                new_ver = Version(version)
                if new_ver <= existing_ver:
                    continue
            except Exception:
                pass

        templates[name] = widget
        print(f"  Found: {name} v{version}")

    return templates


def merge_with_existing(existing: dict, extracted: dict) -> dict:
    """Merge extracted templates into existing registry, keeping higher versions."""
    merged = dict(existing)

    for name, data in extracted.items():
        if name in merged:
            try:
                existing_ver = Version(merged[name]["Version"])
                new_ver = Version(data["Version"])
                if new_ver > existing_ver:
                    print(f"  Upgrading {name}: {merged[name]['Version']} -> {data['Version']}")
                    merged[name] = data
                else:
                    print(f"  Keeping existing {name} v{merged[name]['Version']} (extracted: v{data['Version']})")
            except Exception:
                merged[name] = data
        else:
            print(f"  Adding new: {name} v{data['Version']}")
            merged[name] = data

    return merged


def main():
    parser = argparse.ArgumentParser(description="Extract XML templates from MS Power Apps repo")
    parser.add_argument("--repo-path", required=True, help="Path to cloned teams-powerapps-app-templates repo")
    parser.add_argument("--output", default=None, help="Output path (default: src/powerapp_mcp/data/template_registry.json)")
    parser.add_argument("--dry-run", action="store_true", help="Print results without writing")
    args = parser.parse_args()

    repo_path = Path(args.repo_path)
    if not repo_path.exists():
        print(f"Error: Repo path does not exist: {repo_path}")
        return 1

    project_root = Path(__file__).resolve().parent.parent
    registry_path = Path(args.output) if args.output else project_root / "src" / "powerapp_mcp" / "data" / "template_registry.json"

    # Load existing registry
    existing = {}
    if registry_path.exists():
        with open(registry_path) as f:
            existing = json.load(f)
        print(f"Loaded existing registry: {len(existing)} templates")

    # Extract from repo
    print(f"\nScanning {repo_path} for XML widget templates...")
    extracted = find_all_templates(repo_path)
    print(f"\nExtracted {len(extracted)} unique control types")

    # Merge
    print("\nMerging with existing registry...")
    merged = merge_with_existing(existing, extracted)
    print(f"\nFinal registry: {len(merged)} templates")

    # Report version mismatches for controls.py _TEMPLATE_VERSIONS
    print("\n--- Version Summary (for controls.py sync) ---")
    for name in sorted(merged.keys()):
        print(f"  {name}: {merged[name]['Version']}")

    if args.dry_run:
        print("\n[Dry run — not writing]")
        return 0

    # Write
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    with open(registry_path, "w") as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
    print(f"\nWrote {registry_path}")
    return 0


if __name__ == "__main__":
    exit(main())
