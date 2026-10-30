#!/usr/bin/env python3
"""Validate the Project 2025 personnel graph.

The one rule this enforces is the repository's reason to exist: **no edge without a
source**. A role row that names no document, or names one that is not in the registry,
fails. So does a role that points at a person who is not in the file, a confidence value
outside the closed set, a date that cannot be read, or a string that looks like private
data (an address, a phone number, an email, a date of birth, a social-security number).

Exit codes follow the fleet contract: 0 clean, 1 a violation, 2 could-not-judge. It never
reports 0 because it could not read the files.

Run:  python scripts/validate.py [--data DIR] [--quiet]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

ROLE_TYPES = {"mandate_author", "mandate_contributor", "civil_society_affiliation",
              "administration"}
CONFIDENCE = {"high", "medium", "low"}
SOURCE_KINDS = {"primary", "reputable_reporting"}

#: Keys that must never appear in any row, under any spelling we can imagine.
FORBIDDEN_KEYS = {
    "address", "home_address", "street", "residence", "phone", "phone_number",
    "mobile", "email", "e_mail", "dob", "date_of_birth", "birthdate", "ssn",
    "social_security", "family", "spouse", "children", "relatives", "contacts",
}

#: Private-data shapes, checked on values we expect to be public prose only.
PRIVATE_PATTERNS: List[Tuple[str, re.Pattern]] = [
    ("an email address", re.compile(r"[\w.+-]+@[\w-]+\.[A-Za-z]{2,}")),
    ("a phone number", re.compile(r"(?<!\d)(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}(?!\d)")),
    ("a social-security number", re.compile(r"(?<!\d)\d{3}-\d{2}-\d{4}(?!\d)")),
    ("a street address", re.compile(
        r"\b\d{1,6}\s+[A-Za-z0-9.'-]+(?:\s+[A-Za-z0-9.'-]+){0,4}\s+"
        r"(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr|Way|Court|Ct|Place|Pl)\b",
        re.IGNORECASE)),
]
#: Fields that are identifiers or URLs and are exempt from the prose scan.
SCAN_SKIP = {"id", "person_id", "org_id", "source_id", "source_ids", "url", "title",
             "publisher", "retrieved_at", "locator", "section", "mandate_chapter"}


def _rows(path: Path) -> List[Dict[str, Any]]:
    """Parse a JSONL file. Raises ValueError naming the line on a bad row."""
    out: List[Dict[str, Any]] = []
    with path.open(encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path.name}:{n}: not JSON ({exc})") from exc
            if not isinstance(row, dict):
                raise ValueError(f"{path.name}:{n}: a row must be a JSON object")
            out.append(row)
    return out


def _strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from _strings(item)


def check(data_dir: Path) -> Dict[str, Any]:
    """Return {'errors': [...], 'counts': {...}}. Never raises on a row; only on I/O."""
    errors: List[str] = []
    files = {name: data_dir / f"{name}.jsonl" for name in ("people", "orgs", "roles", "sources")}
    for name, path in files.items():
        if not path.exists():
            raise FileNotFoundError(f"{path} is missing - cannot judge the dataset")

    people = _rows(files["people"])
    orgs = _rows(files["orgs"])
    roles = _rows(files["roles"])
    sources = _rows(files["sources"])

    pids: Dict[str, Dict[str, Any]] = {}
    for p in people:
        pid = p.get("id")
        if not isinstance(pid, str) or not pid.startswith("person-"):
            errors.append(f"people: bad id {pid!r}")
            continue
        if pid in pids:
            errors.append(f"people: duplicate id {pid}")
        if not str(p.get("name") or "").strip():
            errors.append(f"people: {pid} has no name")
        pids[pid] = p

    oids: Dict[str, Dict[str, Any]] = {}
    for o in orgs:
        oid = o.get("id")
        if not isinstance(oid, str) or not oid.startswith("org-"):
            errors.append(f"orgs: bad id {oid!r}")
            continue
        if oid in oids:
            errors.append(f"orgs: duplicate id {oid}")
        if not str(o.get("name") or "").strip():
            errors.append(f"orgs: {oid} has no name")
        oids[oid] = o

    sids: Dict[str, Dict[str, Any]] = {}
    for s in sources:
        sid = s.get("id")
        if not isinstance(sid, str) or not sid.startswith("src-"):
            errors.append(f"sources: bad id {sid!r}")
            continue
        if sid in sids:
            errors.append(f"sources: duplicate id {sid}")
        url = str(s.get("url") or "")
        if not re.match(r"^https?://", url):
            errors.append(f"sources: {sid} has no http(s) url ({url!r})")
        if s.get("kind") not in SOURCE_KINDS:
            errors.append(f"sources: {sid} has kind {s.get('kind')!r}")
        if not str(s.get("title") or "").strip():
            errors.append(f"sources: {sid} has no title")
        if not str(s.get("publisher") or "").strip():
            errors.append(f"sources: {sid} has no publisher")
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(s.get("retrieved_at") or "")):
            errors.append(f"sources: {sid} has no retrieved_at (YYYY-MM-DD)")
        sids[sid] = s

    for o in orgs:
        for sid in o.get("source_ids") or []:
            if sid not in sids:
                errors.append(f"orgs: {o.get('id')} cites unknown source {sid!r}")

    edge_counts: Dict[str, int] = {}
    by_person: Dict[str, int] = {}
    for r in roles:
        rid = r.get("id") or "?"
        sid = r.get("source_id")
        if not sid:
            errors.append(f"roles: {rid} has NO source - the one rule of this dataset")
        elif sid not in sids:
            errors.append(f"roles: {rid} cites unknown source {sid!r}")
        pid = r.get("person_id")
        if pid not in pids:
            errors.append(f"roles: {rid} names unknown person {pid!r}")
        oid = r.get("org_id")
        if oid and oid not in oids:
            errors.append(f"roles: {rid} names unknown org {oid!r}")
        rtype = r.get("role_type")
        if rtype not in ROLE_TYPES:
            errors.append(f"roles: {rid} has role_type {rtype!r}")
        edge_counts[str(rtype)] = edge_counts.get(str(rtype), 0) + 1
        by_person[str(pid)] = by_person.get(str(pid), 0) + 1
        if r.get("confidence") not in CONFIDENCE:
            errors.append(f"roles: {rid} has confidence {r.get('confidence')!r}")
        if not re.match(r"^\d{4}(-\d{2}-\d{2})?$", str(r.get("date_from") or "")):
            errors.append(f"roles: {rid} has no readable date_from ({r.get('date_from')!r})")
        dto = str(r.get("date_to") or "")
        if dto and not re.match(r"^\d{4}(-\d{2}-\d{2})?$", dto):
            errors.append(f"roles: {rid} has an unreadable date_to ({dto!r})")
        if dto and str(r.get("date_from")) > dto:
            errors.append(f"roles: {rid} ends ({dto}) before it begins ({r.get('date_from')})")
        if not str(r.get("role_title") or "").strip():
            errors.append(f"roles: {rid} has no role_title")

    # Privacy: a forbidden key anywhere, or a private-data shape in public prose.
    for label, rows in (("people", people), ("orgs", orgs), ("roles", roles),
                        ("sources", sources)):
        for n, row in enumerate(rows, 1):
            for key in row:
                if key.lower() in FORBIDDEN_KEYS:
                    errors.append(f"{label}: row {n} carries a forbidden field {key!r}")
            for key, value in row.items():
                if key in SCAN_SKIP:
                    continue
                for text in _strings(value):
                    for what, pat in PRIVATE_PATTERNS:
                        if pat.search(text):
                            errors.append(f"{label}: row {n} field {key!r} looks like {what}")

    return {
        "errors": errors,
        "counts": {
            "people": len(people),
            "orgs": len(orgs),
            "roles": len(roles),
            "sources": len(sources),
            "edges_by_type": dict(sorted(edge_counts.items())),
            "people_with_administration_role": sum(
                1 for pid, _n in by_person.items()
                if any(r.get("person_id") == pid and r.get("role_type") == "administration"
                       for r in roles)),
            "advisory_board_orgs": sum(1 for o in orgs if o.get("project_2025_advisory_board")),
            "unsourced_edges": sum(1 for r in roles if not r.get("source_id")),
        },
    }


def main(argv: List[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Validate the Project 2025 personnel graph.")
    ap.add_argument("--data", default=str(Path(__file__).resolve().parents[1] / "data"),
                    help="Directory holding people/orgs/roles/sources .jsonl")
    ap.add_argument("--quiet", action="store_true", help="Print only the verdict.")
    args = ap.parse_args(argv)

    try:
        result = check(Path(args.data))
    except (OSError, ValueError) as exc:
        print(f"could not judge: {exc}")
        return 2

    counts = result["counts"]
    if not args.quiet:
        print(f"people={counts['people']} orgs={counts['orgs']} roles={counts['roles']} "
              f"sources={counts['sources']} unsourced={counts['unsourced_edges']}")
        print(f"edges by type: {json.dumps(counts['edges_by_type'], sort_keys=True)}")
        print(f"administration={counts['people_with_administration_role']} "
              f"advisory_board_orgs={counts['advisory_board_orgs']}")

    if result["errors"]:
        for err in result["errors"]:
            print(f"VIOLATION: {err}")
        print(f"{len(result['errors'])} violation(s)")
        return 1
    print("clean: every edge resolves to a document")
    return 0


if __name__ == "__main__":
    sys.exit(main())
