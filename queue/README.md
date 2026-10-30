# Review queue

Proposals filed through the `p2025_contribute` tool land here — as **proposed edges**,
never as data.

- A proposal is written to `proposals.jsonl` with `status: "proposed"`.
- Nothing in `data/` reads this directory. A proposal cannot alter an answer.
- A human reviews a proposal, checks its citation, and — if it holds up — adds the row to
  `data/` by hand and clears it from the queue.
- The live AitherOS deployment keeps its own queue at `$P2025_DATA_DIR/queue/`; this
  file documents the shape, not a shared inbox.

Reasons a proposal is refused before it queues: no `source_url`, a `role_type` outside
the closed set, or anything that looks like private data (an email, a phone number, a
street address).
