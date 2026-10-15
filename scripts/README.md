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
  `expect_contains` anchor**. The 57th, `us/statute/genius-act-2025`, declares none, and its `note`
  records a held version rather than an anchor: *held version 2025-07-18; retrieved 2026-07-08*. So
  that source's comparability rests on the retrieval record, not on an anchor. None declared manual,
  none binary. Arming it is a separate decision: a sweep writes state and a change opens a triage
  issue.
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

## The integrity gate: how the manifest is regenerated

`verify_integrity.py` fails whenever any covered file's bytes differ from `corpus_manifest.json`.
`gen_corpus_manifest.py` closes that loop:

```
python3 scripts/gen_corpus_manifest.py --check    # report the drift; writes nothing; exit 1 if drifted
python3 scripts/gen_corpus_manifest.py            # update the stale hashes, the root hash and the date
```

It re-hashes **only the paths the manifest already lists** — never adding or dropping one — and refuses
outright if a listed file is missing, because a claim about a file nobody can check is worse than no
claim at all. Files on disk that the claim does not cover are reported and never added automatically.
The root hash is derived exactly as `verify_integrity.py` re-derives it, so the two cannot disagree.

Run it **after** any deliberate change to a covered file: that is the moment the corpus's root hash is
restated. Then run `verify_integrity.py`, or let CI run it, and expect GREEN.

**Fixed 2026-10-15.** The gate had been RED since 5 August: commit `0474b85` ("add Akoma Ntoso
identifiers to the published records") edited **57 `metadata.yaml` files and one JSON Schema**
(`schema/authoritative-metadata.schema.json`, extended by 65 lines to declare the new `akn_*` fields)
and did not regenerate the manifest — so all 58 hashes were stale, and CI failed on every push for ten
weeks. The root hash still reproduced over the manifest's own list, no record text had drifted, and no
generator existed in the tree; hence this one. Regenerated: 58 hashes, root hash
`sha256:70929aa801c732f1480ec34982cadd13eaead2f4b3f94fb3d62861e88733dd31`, file list unchanged,
`verify_integrity.py` → GREEN (356 files, root hash reproduces). An earlier note in this file said all 58
were `metadata.yaml`; one of them was the schema, and the same slip stands in the message of commit
`148b31d`, which cannot be rewritten without rewriting pushed history.
