# Contributing

Thank you for helping keep this record accurate. The rule that matters most:

> **No edge without a source.** A person→role edge that cannot name a primary document is
> not added, however well known it is.

## The sourcing standard

An accepted edge cites one of:

1. **The volume itself** — *Mandate for Leadership: The Conservative Promise* (2023), with
   the page (`locator`, e.g. `p. 27`).
2. **The Project 2025 advisory board list** — printed in the volume, p. 11.
3. **An official record** — an agency leadership page, a White House announcement, a
   Senate nomination record (congress.gov), a Federal Register notice.
4. **The organisation's own staff or leadership page**, for a civil-society post.
5. **Named reporting** from an outlet of record, only where 1–4 cannot be reached; mark
   it `kind: reputable_reporting` and say which outlet.

Fan wikis, social posts, aggregator listicles and AI summaries are **not** sources.

## The shape of a contribution

Add rows to the JSONL files, one JSON object per line, matching
[`schema/`](schema/). Every edge needs:

- `role_type` from the closed set in [`schema/roles.schema.json`](schema/roles.schema.json);
- `date_from` and `date_to` — the years the role is documented as held. Use an empty
  `date_to` for a currently held role, and the publication year for a volume role;
- `confidence` — `high` (the primary document states it directly), `medium` (a primary
  document supports it indirectly, e.g. a roster without a title), `low` (named reporting
  only);
- `source_id` pointing at a row in `sources.jsonl`, which itself carries `url`,
  `publisher`, `title` and `locator`.

Run it before opening the pull request:

```bash
python scripts/validate.py
```

CI runs the same script. A pull request that fails it is not reviewed.

## What is refused

- **Anything not about a public role.** No home addresses, family members, personal
  phone numbers or emails, dates of birth, or material from a non-public record. The
  validator refuses rows that look like any of these; a human reviewer refuses the rest.
- **Inference.** "Worked at X, and X is on the board" is not an edge. The volume printing
  the organisation beside the name is.
- **Guilt by association.** Being named in someone else's biography is not a role.
- **Unattributed synthesis.** If a claim is your own analysis, it belongs in `articles/`,
  clearly marked as opinion, not in `data/`.

## Corrections and takedowns

This is a public-accountability record, and it should be easy to correct.

- **A factual correction** — open an issue titled `correction: <person or org>`, cite the
  document that shows the correct value, and it is fixed with the citation retained in
  the commit.
- **A removal request** — open an issue titled `takedown: <person>`. If the row concerns a
  private individual, or any non-public data, it is removed first and discussed after.
  Rows about public roles are corrected rather than deleted, because the deletion of a
  correctly sourced public fact is itself a distortion of the record; the reasoning is
  recorded in the issue either way.

No contributor is asked to justify their identity to file a correction.

## Review

A human maintains this repository. Contributions arrive as pull requests; the review
question is only ever *"does the cited document say this?"*, never whether the claim is
convenient.
