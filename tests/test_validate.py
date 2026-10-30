"""The repository's own gate: an unsourced edge must fail, and private data must fail.

Each test builds a small dataset in a temporary directory, so the real data is never
touched and the arms cannot pass by accident on the shipped files.
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import validate  # noqa: E402


def write_dataset(root: Path, roles, people=None, orgs=None, sources=None) -> None:
    rows = {
        "people": people if people is not None else [
            {"id": "person-a", "name": "A Person", "aliases": [], "notes": ""}],
        "orgs": orgs if orgs is not None else [],
        "roles": roles,
        "sources": sources if sources is not None else [
            {"id": "src-doc", "url": "https://example.gov/doc", "title": "A document",
             "publisher": "Example", "kind": "primary", "retrieved_at": "2026-10-30"}],
    }
    for name, data in rows.items():
        with (root / f"{name}.jsonl").open("w", encoding="utf-8") as fh:
            for row in data:
                fh.write(json.dumps(row) + "\n")


BASE_EDGE = {
    "id": "role-a", "person_id": "person-a", "org_id": "", "role_title": "Director",
    "role_type": "administration", "mandate_chapter": "", "date_from": "2025",
    "date_to": "", "confidence": "high", "source_id": "src-doc", "note": "",
}


class ValidateTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def run_check(self, roles, **kw):
        write_dataset(self.root, roles, **kw)
        return validate.check(self.root)

    def test_a_sourced_edge_is_clean(self) -> None:
        result = self.run_check([dict(BASE_EDGE)])
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["counts"]["roles"], 1)

    def test_an_edge_with_no_source_fails(self) -> None:
        edge = dict(BASE_EDGE, source_id="")
        result = self.run_check([edge])
        self.assertTrue(any("NO source" in e for e in result["errors"]))

    def test_an_edge_citing_an_unknown_source_fails(self) -> None:
        edge = dict(BASE_EDGE, source_id="src-nowhere")
        result = self.run_check([edge])
        self.assertTrue(any("unknown source" in e for e in result["errors"]))

    def test_an_edge_with_no_person_fails(self) -> None:
        result = self.run_check([dict(BASE_EDGE, person_id="person-ghost")])
        self.assertTrue(any("unknown person" in e for e in result["errors"]))

    def test_a_role_type_outside_the_closed_set_fails(self) -> None:
        result = self.run_check([dict(BASE_EDGE, role_type="probably")])
        self.assertTrue(any("role_type" in e for e in result["errors"]))

    def test_a_missing_date_fails(self) -> None:
        result = self.run_check([dict(BASE_EDGE, date_from="")])
        self.assertTrue(any("date_from" in e for e in result["errors"]))

    def test_private_data_in_a_note_fails(self) -> None:
        result = self.run_check([dict(BASE_EDGE, note="reach him at a.person@example.com")])
        self.assertTrue(any("email address" in e for e in result["errors"]))

    def test_a_forbidden_field_fails(self) -> None:
        people = [{"id": "person-a", "name": "A Person", "home_address": "1 Main Street"}]
        result = self.run_check([dict(BASE_EDGE)], people=people)
        self.assertTrue(any("forbidden field" in e for e in result["errors"]))

    def test_a_missing_file_is_could_not_judge(self) -> None:
        with self.assertRaises(FileNotFoundError):
            validate.check(self.root)


if __name__ == "__main__":
    unittest.main()
