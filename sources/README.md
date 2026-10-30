# Source registry

Every edge in `data/roles.jsonl` names one row of `data/sources.jsonl` through
`source_id`. This page explains what those documents are, so a reader can check the
dataset without opening every row.

## The volume

| used for | locator |
|---|---|
| the advisory board list (54 organisations) | p. 11 |
| the author bios, and each chapter's authorship | p. 15 |
| the contributors list — "Name, Organization", pp. 25–31 | pp. 25–31 |

Document: *Mandate for Leadership: The Conservative Promise*,
The Heritage Foundation, 2023 —
<https://static.heritage.org/project2025/2025_MandateForLeadership_FULL.pdf>

Each page is its own registry row (`src-mandate-p25-contributors` …), so the `locator`
on a row is exact: not "the volume", but the page the name is printed on.

## Current-administration appointments

Thirteen people in the volume also hold a federal role. Each edge cites a named public
record — an agency leadership page (FCC, State, DHS, HHS), a congress.gov nomination
record, or named reporting where no official page yet lists the appointee. The registry's
`kind` field distinguishes `primary` from `reputable_reporting`, and `confidence` on the
edge reflects it.

## Adding a source

1. Pick the narrowest document that states the role — an agency page beats a news roundup.
2. Give the row `url`, `title`, `publisher`, `kind`, and a `locator` where the document
   has pagination.
3. Set `retrieved_at` to the date you actually read it.
4. Never edit an existing source row's `url` to point somewhere else: add a new row and
   repoint the edges, so the history of what was cited stays readable.
