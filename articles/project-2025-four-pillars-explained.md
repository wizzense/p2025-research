# Project 2025: what the four pillars actually are

*A reference explainer. Every claim below is cited to a page of the volume; nothing here
is inferred. Data: [`data/`](../data/).*

The phrase "Project 2025" is used to mean at least four different things, which is why
arguments about it so often talk past each other. The volume itself is explicit: *"The
project is built on four pillars."* (p. xiv)
<https://static.heritage.org/project2025/2025_MandateForLeadership_FULL.pdf>

## 1. A 920-page agency-by-agency policy volume

*Mandate for Leadership: The Conservative Promise* is 30 chapters, one per department,
agency or agency cluster — from the White House Office (ch. 1) to the Federal Trade
Commission (ch. 30). Each chapter sets out how the volume's authors would run that part
of the government, and where its own contributors disagreed the text brackets out the
alternative for the President to choose (p. xiv).

The authors are named on the contents pages and in the author bios (pp. 15–23). The full
list is in [`knowledge/mandate-structure.md`](../knowledge/mandate-structure.md), and
every one of them is a `mandate_author` edge in this repository.

## 2. A personnel database (not public)

The volume describes a database where candidates build profiles and coalition members
make recommendations, collated for the President-elect's team (p. xiv). No public roster
of it exists. **This repository makes no claim about it.** Anything a reader has heard
about "the Project 2025 list of names" that is not the volume's own contributors pages or
advisory board is, so far as this dataset can tell, not documented.

## 3. A training body — the Presidential Administration Academy

An online academy "taught by experts from our coalition", plus in-person seminars for
senior staff (p. xiv). No faculty roster was published with the volume, so no `role_type`
covers it here. Adding one would need a document that prints a name in that role.

## 4. A transition playbook

Agency teams drafting plans to be executed from inauguration day (p. xiv). Described, not
roster-published; likewise no edges.

## What this means for a reader

Three of the four pillars are described in the volume but **not documented at the level
of named individuals**. Only Pillar I is, and it is fully captured here: 30 chapters,
38 author edges, 276 contributors, and 54 organisations on the advisory board printed at
p. 11.

That asymmetry is the honest finding, and it cuts in both directions:

- A claim that a *specific person* was "part of Project 2025" needs a page number. If the
  volume does not print it, this dataset does not assert it.
- A claim that Project 2025 was only a document, with no machinery behind it, is equally
  unsupported: the volume describes all four pillars in its own words.

The lineage point is often muddled too. Heritage gave Ronald Reagan a *Mandate for
Leadership* in 1980 (p. xiii); the 2023 volume says it went "back to the future — and then
some". What is shared is the form — an agency-by-agency volume for an incoming
administration — not an authorship or an organisation. No 1980 figure appears in this
dataset unless the 2023 volume also names them.
