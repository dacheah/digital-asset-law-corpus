# Digital-Asset Law Corpus

A neutral, **provenance-first**, machine-readable record of **digital-asset market-structure and
prudential law** across many jurisdictions. Every authoritative text carries its official source,
retrieval date, official citation, issuing body, instrument type, jurisdiction, language, an
authoritative-status flag, and a SHA-256 content hash; every change is a new dated version; and
nothing generated is ever presented as authoritative.

> **Not legal or compliance advice.** The corpus records what each instrument provides; it takes no
> policy position and no position on any live matter, institution, or enforcement action. The
> authoritative text of each instrument is the official original in its authentic language;
> translations and concept tags are unofficial and derived. Always confirm against the cited official
> source for anything legally operative.

## What's here

**57 authoritative instruments across 21 jurisdictions**, in their authentic enacting languages
(Arabic, Chinese (Simplified & Traditional), English, French, German, Indonesian, Italian, Japanese,
Korean, Maltese, Portuguese, Spanish, Thai, Turkish, Vietnamese). Parallel authentic-language texts
(e.g. Switzerland de/fr/it, Hong Kong en/zh-Hant) are recorded as separate records under one instrument.

This public release contains only records whose reuse terms are confirmed clean (statutory
non-copyright, government public-domain, or an explicit open/attribution licence). A further 13 records
whose terms are still to be confirmed are held back pending confirmation — see LICENSE and NOTICE.

## Layout

```
authoritative/<corpus_id>/<version>/
    metadata.yaml     provenance: source, citation, jurisdiction, language, dates,
                      authoritative-status, licence, SHA-256 hashes, verification block
    text.txt          the authoritative text, in its authentic language
    original.*        the byte-exact official source file (PDF/XML/JSON) — the integrity anchor
derived/<corpus_id>/<version>/
    structure.json    structural parse (parts / articles / sections)
    concepts.json     neutral concept tags (an unreviewed model/keyword pass — clearly labelled)
    derived-metadata.yaml
derived/concept-index.json   concept → provision index across the corpus
schema/               JSON Schema for the authoritative metadata
data/                 flat exports: documents.jsonl (one row per record) + provisions.jsonl
corpus_manifest.json  SHA-256 of every file + a single root hash
verify_integrity.py   offline, read-only integrity check against the manifest
```

The **wall** is deliberate: `authoritative/` holds only official texts and their provenance;
everything generated (structure, concept tags) lives in `derived/`, separately and clearly labelled.

## Verify integrity

```bash
python3 verify_integrity.py          # recomputes every hash against corpus_manifest.json
```

GREEN means every file matches its recorded SHA-256 and the root hash reproduces; changing a single
byte turns it RED. No dependencies, fully offline.

## Two-layer licensing (read LICENSE + NOTICE)

- **Derived / compilation layer** (structure, concept tags, arrangement, schema) — **CC BY 4.0**.
- **Source texts** (`text.txt`, `original.*`) — **not relicensed**; each official instrument keeps its
  own terms, recorded per record in `metadata.yaml` and summarised in NOTICE.

## Provenance guarantees (and their limits)

- **Fidelity** — every text is verified against its official source (completeness deltas; cross-source
  or independent-OCR corroboration where a second official rendering exists).
- **Integrity** — every text re-hashes to its recorded SHA-256; the manifest carries a root hash.
- **Datedness** — each record is a dated version; supersessions are explicit.

What this corpus does **not** claim: it is not a consolidation service, not exhaustive, and the concept
tags are an unreviewed pass (expect occasional over/under-tagging). Treat it as citation-grounded input,
not as the last word.
