# scripts — the source monitor (tracked, not armed)

`watch_sources.py` is this corpus's source monitor. It fetches every source declared in
`monitoring/sources.json`, reduces the page to **comparable text**, hashes that text, compares the
digest against the baseline in `monitoring/snapshots/`, retains the comparable text of every page
source under `monitoring/snapshots/pages/`, writes a bounded word-level diff note for any source that
moved, and writes `monitoring/last_report.md`. It only watches and queues — nothing is ever ingested
automatically, and a green run must never be read as "every source was checked".

The file is byte-identical to the same monitor in the space-law, bbnj and deep-seabed corpora
(v3.11, md5 `d94b2618d60764fc48fec2c45355fba8`). Its changelog comments record why each behaviour
exists and which failure it prevents; read them before changing anything.

## State: not armed

- **No baselines are committed** — `monitoring/snapshots/` does not exist here, so a first sweep
  would create every baseline at once rather than diff against anything.
- **No workflow runs it.** `.github/workflows/verify-integrity.yml` covers the records only.
- **The watchlist is well-formed but unused:** 57 sources, all whole-page, **56 of 57 declaring an
  `expect_contains` anchor** (the one that does not is recorded in its own `note`), none declared
  manual, none binary. Arming it is a separate decision: a sweep writes state and a change opens a
  triage issue.
- **The crawl layer is not tracked.** `scripts/crawl/` and `scripts/build_sources_from_records.py`
  exist in the working tree but are deliberately not part of this commit. Schema mode needs
  `scripts/crawl/common.py` plus crawl4ai, so a fresh clone runs whole-page mode only — which loses
  nothing today, because no source in this watchlist declares a schema.

## Use

```
python3 scripts/watch_sources.py --selftest    # offline assertions, no network, writes nothing
python3 scripts/watch_sources.py               # LIVE SWEEP — fetches every source and WRITES STATE
python3 scripts/watch_sources.py --tally       # measured whole-page false-alarm rate, read-only
```

## Outside the corpus manifest

`corpus_manifest.json` is the **record** claim: `authoritative/`, `derived/`, `data/`, `schema/` and
the repository's own root files. The monitor is tooling and is deliberately not part of that claim —
`verify_integrity.py` counts files it does not cover and does not fail on them. Keeping tooling
outside the manifest is what allows the records' root hash to keep meaning exactly one thing: that
those record bytes have not changed.

## The integrity gate is currently RED, and it is not this tooling

At the time of this commit, `python3 verify_integrity.py` reports 58 hash mismatches. All 58 are
`metadata.yaml` files, and they are **exactly** the 58 files changed by commit `0474b85` ("add Akoma
Ntoso identifiers to the published records"), which did not regenerate the manifest. The root hash
still reproduces over the manifest's own file list; only those 58 per-file hashes are stale. No
record text has drifted, and no generator for `corpus_manifest.json` exists in the tree. Recorded
here so the next reader does not go looking for a cause in the tooling.
