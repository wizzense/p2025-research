# How a role is classified

The four `role_type` values are a closed set. Each answers one question, and none of them
is a judgement about a person.

| `role_type` | the claim | the document that carries it |
|---|---|---|
| `mandate_author` | wrote a chapter of the 2023 volume | the contents page / author lists (pp. 15–23) |
| `mandate_contributor` | named on the volume's contributors list | pp. 25–31 |
| `civil_society_affiliation` | the organisation printed beside that contributor's name | the same line as the contributor entry |
| `administration` | holds a current federal appointment, and is also in the volume | an agency leadership page, congress.gov nomination record, or named reporting |

## What each one is not

- **`mandate_contributor` is not "helped write it".** The volume lists contributors
  without saying what each contributed. The claim is exactly "named on this list".
- **`civil_society_affiliation` is not membership or sympathy.** It records that the
  volume prints an organisation beside a person's name. Someone who worked at an
  organisation that sat on the advisory board is *not* thereby a participant — which is
  why the affiliation edge exists only where the volume itself prints the pairing.
- **`administration` is not "got the job because of Project 2025".** It records that a
  person in the volume now holds a federal role, with the appointment's own source. The
  causal claim is not in this dataset and is not made by it.
- **`confidence` is about the document, not the person.** `high` means the cited document
  states the role directly; `low` means the only citation is named reporting.

## Dates

- Volume roles carry the publication year (2023) in both `date_from` and `date_to`.
- Administration roles carry the year the appointment was documented in `date_from`, and
  an empty `date_to` when it is still held.
- An empty `date_to` means "still held or not stated", never "ended".

## The privacy line

The schema has no field for an address, a family member, a contact detail, a date of
birth or a private record, and [`scripts/validate.py`](../scripts/validate.py) refuses a
row that carries one. This is a record of public professional roles; anything else is out
of scope by construction, not by reviewer discretion.
