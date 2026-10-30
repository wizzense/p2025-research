# The four pillars of Project 2025

Source: *Mandate for Leadership: The Conservative Promise* (The Heritage Foundation,
2023), "A Note on 'Project 2025'", **p. xiv**.
<https://static.heritage.org/project2025/2025_MandateForLeadership_FULL.pdf>

The volume says, in one sentence: *"The project is built on four pillars."* What follows
is the volume's own description of each, paraphrased with the defining words quoted.

## Pillar I — the volume

*Mandate for Leadership* itself. In the volume's words it "puts in one place a consensus
view of how major federal agencies must be governed", and brackets out remaining
disagreement "for the next President to choose a path". It is 30 chapters, one per agency
or agency cluster — the chapter list is in
[`mandate-structure.md`](mandate-structure.md).

**In this dataset:** the chapters and their authors are `mandate_author` edges, and the
people listed on pp. 25–31 are `mandate_contributor` edges.

## Pillar II — the personnel database

A database where "candidates … build their own professional profiles and our coalition
members … review and voice their recommendations", later "collated and shared with the
President-elect's team".

**In this dataset:** nothing. The database itself was never public; the people it held
are not part of this graph, and the graph does not guess at them. What is public is the
personnel the volume and its advisory board name.

## Pillar III — the Presidential Administration Academy

"An online educational system taught by experts from our coalition", with in-person
seminars for experienced staff.

**In this dataset:** nothing directly. Faculty lists were not published as a roster; a
name would need a document that prints it in that role. If one exists, it belongs in a
contribution with that citation.

## Pillar IV — the Playbook

Agency teams drafting transition plans "to move out upon the President's utterance of
'so help me God.'"

**In this dataset:** nothing directly — the playbook is described in the volume but its
team members are not listed there.

## What the volume says about its own lineage

The same note places the project in a line that begins with 1980: "the fledging Heritage
Foundation handed to President-elect Ronald Reagan the inaugural *Mandate for
Leadership*" (p. xiii). The 2023 volume describes itself as going "back to the future —
and then some". The continuity is the *format* — an agency-by-agency policy volume handed
to an incoming administration — not a shared authorship. No 1980 contributor is in this
dataset unless the 2023 volume also names them.

## The honest coverage statement

Of the four pillars, **only Pillar I is publicly documented at the level of named
people**, and this dataset holds all of it that the volume prints: 30 chapter authors
and 276 named contributors. Pillars II–IV are described in the volume but their rosters
are not published, so they contribute no edges. A graph that implied otherwise would be
inventing.
