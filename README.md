# Project 2025 personnel graph — an open, sourced record

A machine-readable graph of **who is documented in Project 2025 and in what role**, where
every person→role edge points at a specific page of a specific public document. It is
data, not commentary: the field names are neutral, and no edge exists without a citation.

Built to be read by a person, by a spreadsheet, or by somebody's own AI agent. The same
graph is served inside AitherOS through the `p2025_*` tools (agent pack, MCP gateway, and
the browser WebMCP surface), and it feeds the Civic Atlas retrieval corpus.

- **Data licence:** [CC BY-SA 4.0](LICENSE-DATA). Share and adapt with attribution.
- **Code licence:** [MIT](LICENSE).
- **Primary document:** *Mandate for Leadership: The Conservative Promise* (The Heritage
  Foundation, 2023) — <https://static.heritage.org/project2025/2025_MandateForLeadership_FULL.pdf>

## What "involved in Project 2025" means here

Only a **documented role** counts:

| role_type | means | cited from |
|---|---|---|
| `mandate_author` | authored a chapter of the volume | the contents page and the author bios |
| `mandate_contributor` | named on the volume's contributors list, with the organisation printed beside the name | the contributors pages (pp. 25–31) |
| `civil_society_affiliation` | the organisation the volume prints beside that contributor's name | same lines |
| `administration` | a current federal appointment, where the person is also in the volume | the agency's own page, a Senate nomination record, or named reporting |

It is **never** inferred from an employer, a donation, an acquaintance or a photograph. A
person absent from the volume is absent from this record, and absence is not a claim that
they took no part.

## Data

| file | one row per | key fields |
|---|---|---|
| `data/people.jsonl` | person | `id`, `name`, `aliases` |
| `data/orgs.jsonl` | organisation | `id`, `name`, `kind`, `project_2025_advisory_board`, `source_ids` |
| `data/roles.jsonl` | person→role edge | `person_id`, `org_id`, `role_title`, `role_type`, `date_from`, `date_to`, `confidence`, `source_id` |
| `data/sources.jsonl` | document | `id`, `url`, `title`, `publisher`, `kind`, `locator`, `retrieved_at` |
| `data/coverage.json` | build | counts, and what the record does not claim |

`coverage.json` is honest about limits: it states how many people were found, how many
carry an administration role, and how many edges were dropped for lack of a source.

## Reproduce it

```bash
python scripts/validate.py          # every edge resolves to a document; no private data
python scripts/coverage_report.py   # the same numbers the tools report
```

`scripts/validate.py` is the CI gate: a pull request that adds an edge with no source, an
unresolvable `source_id`, a missing date, or anything resembling private data **fails**.

## Use it from an agent

Inside AitherOS the graph is reachable as `p2025_person`, `p2025_org`, `p2025_search`,
`p2025_roles_by_agency` and `p2025_coverage` — from the civic tool pack, the MCP gateway,
and the WebMCP browser surface on aitherium.com. Elsewhere, read the JSONL directly; the
schema is in [`schema/`](schema/).

## Contributing

Read [`CONTRIBUTING.md`](CONTRIBUTING.md). The short version: add no edge without a
primary citation, and corrections and takedowns are honoured on request.

## Articles and knowledge pages

- [`articles/`](articles/) — the four-pillar explainer and the status of the companion
  essay.
- [`knowledge/`](knowledge/) — short, cited pages: the four pillars, the volume's
  structure, and how a role is classified.
