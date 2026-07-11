# Changelog

## v1.0.1 — 2026-07-11

Tooling and metadata patch. No change to the corpus contents (still 57 instruments across 21 jurisdictions).

- Fixed: the `verify_integrity.py` shipped in v1.0.0 was truncated (missing its `__main__` entry point) and
  silently exited without verifying anything. Restored the complete script — it re-hashes every file against
  `corpus_manifest.json`, re-derives the root hash, and reports GREEN/RED. Anyone who fetched v1.0.0 should
  re-fetch v1.0.1 to independently verify the corpus.
- Added: canonical repository, releases, and citation links in the README; `repository-code` and `url` in `CITATION.cff`.
- Integrity: `corpus_manifest.json` regenerated; `verify_integrity.py` → GREEN (356 files, root hash reproduces).

## v1.0.0 — 2026-07-11

First public release.

- 57 authoritative instruments across 21 jurisdictions, authentic languages: ar, de, en, es, fr, id, it, ja, ko, mt, pt-BR, th, tr, vi, zh-Hans, zh-Hant.
- Every record carries official source, retrieval date, official citation, jurisdiction,
  language, authoritative-status flag, and a SHA-256 content hash; each text verified against
  its official source.
- Derived layer: structural parsing + neutral concept tags (clearly separated from the
  authoritative texts).
- Records whose reuse terms are still to be confirmed are withheld pending confirmation.
- Integrity: `corpus_manifest.json` + `verify_integrity.py` (offline, read-only).
