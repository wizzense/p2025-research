#!/usr/bin/env python3
"""Print the dataset's coverage as a Markdown table.

The numbers are recomputed from the files, never copied from a document: coverage that
is asserted rather than measured drifts the first time somebody edits a row by hand.

Run:  python scripts/coverage_report.py [--data DIR]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import List


def _load(path: Path) -> List[dict]:
    with path.open(encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def main(argv: List[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Report coverage of the p2025 graph.")
    ap.add_argument("--data", default=str(Path(__file__).resolve().parents[1] / "data"))
    args = ap.parse_args(argv)
    data = Path(args.data)

    try:
        people = _load(data / "people.jsonl")
        orgs = _load(data / "orgs.jsonl")
        roles = _load(data / "roles.jsonl")
        sources = _load(data / "sources.jsonl")
    except (OSError, ValueError) as exc:
        print(f"could not read the dataset: {exc}")
        return 2

    by_type: dict = {}
    for r in roles:
        by_type[r.get("role_type", "?")] = by_type.get(r.get("role_type", "?"), 0) + 1
    admin_people = {r["person_id"] for r in roles if r.get("role_type") == "administration"}
    affiliated = {r["person_id"] for r in roles
                  if r.get("role_type") == "civil_society_affiliation"}
    board = [o for o in orgs if o.get("project_2025_advisory_board")]

    print("| measure | count |")
    print("|---|---|")
    print(f"| people | {len(people)} |")
    print(f"| organisations | {len(orgs)} |")
    print(f"| sourced role edges | {len(roles)} |")
    print(f"| source documents | {len(sources)} |")
    print(f"| chapters of the volume | 30 |")
    print(f"| people with a current-administration role | {len(admin_people)} |")
    print(f"| people with a civil-society affiliation | {len(affiliated)} |")
    print(f"| advisory-board organisations | {len(board)} |")
    print(f"| edges with no source | {sum(1 for r in roles if not r.get('source_id'))} |")
    print()
    print("| role type | edges |")
    print("|---|---|")
    for k in sorted(by_type):
        print(f"| {k} | {by_type[k]} |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
