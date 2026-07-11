# Changelog

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
