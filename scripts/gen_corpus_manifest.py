#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_corpus_manifest.py — recompute corpus_manifest.json's per-file SHA-256 values and its root hash.

The manifest's own file LIST is the authority here: this tool re-hashes the paths already listed, and
refuses to invent, add or drop one. Regenerating after a deliberate change therefore cannot quietly
widen or narrow the corpus's integrity claim. A file that has appeared since is reported for a human to
decide about, never added on the tool's own initiative; a listed file that has gone missing is a hard
error, because a claim about a file nobody can check is worse than no claim at all.

Run from anywhere; paths are resolved from this file's location:

    python3 scripts/gen_corpus_manifest.py --check    # report the drift, write nothing; exit 1 if drifted
    python3 scripts/gen_corpus_manifest.py            # update those hashes, the root hash and the date

Stdlib only, no network. The root hash is derived exactly as verify_integrity.py re-derives it, so the
two tools cannot come to disagree about what the corpus's root hash is.
"""
import datetime
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "corpus_manifest.json")
SKIP_DIRS = {".git", "__pycache__"}


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def root_of(files):
    """The corpus's single root hash: sha256 over "path:hash" pairs, sorted. Mirrors verify_integrity.py."""
    return "sha256:" + hashlib.sha256(
        "".join(f"{k}:{v}" for k, v in sorted(files.items())).encode()).hexdigest()


def main(argv):
    check = "--check" in argv
    man = json.load(open(MANIFEST, encoding="utf-8"))
    listed = man["files"]

    missing, changed, now_hashes = [], {}, {}
    for rel in sorted(listed):
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            missing.append(rel)
            continue
        now = sha(p)
        now_hashes[rel] = now
        if now != listed[rel]:
            changed[rel] = (listed[rel], now)
    if missing:
        print(f"REFUSED — {len(missing)} listed file(s) are not on disk:", file=sys.stderr)
        for m in missing[:20]:
            print("   MISSING", m, file=sys.stderr)
        print("A manifest entry with no file behind it cannot be regenerated into truth; decide what "
              "happened to those files first.", file=sys.stderr)
        return 3

    covered = set(listed) | {"corpus_manifest.json"}
    extra = []
    for dirpath, dirs, fnames in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in fnames:
            rel = os.path.relpath(os.path.join(dirpath, fn), ROOT).replace(os.sep, "/")
            if rel not in covered:
                extra.append(rel)

    new_root = root_of(now_hashes)
    root_moved = new_root != man.get("root_hash")

    print(f"files covered     : {len(listed)}")
    print(f"hash mismatches   : {len(changed)}")
    print(f"root hash         : {new_root if root_moved else 'unchanged (' + str(man.get('root_hash')) + ')'}")
    print(f"not in the claim  : {len(extra)} file(s) — reported, never added automatically")
    for rel, (old, new) in sorted(changed.items())[:20]:
        print(f"   STALE  {rel}\n          was {old}\n          now {new}")
    if len(changed) > 20:
        print(f"   ... and {len(changed) - 20} more")

    if check:
        if changed or root_moved:
            print("DRIFTED — the manifest is not a true statement about these bytes. "
                  "Run without --check to regenerate.")
            return 1
        print("CLEAN — the manifest already matches the bytes on disk.")
        return 0

    if not changed and not root_moved:
        print("Nothing to do: every hash and the root hash already match.")
        return 0

    listed.update(now_hashes)
    man["files"] = listed
    man["root_hash"] = new_root
    man["generated"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    tmp = MANIFEST + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(man, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    os.replace(tmp, MANIFEST)
    print(f"WROTE corpus_manifest.json — {len(changed)} hash(es) updated, root hash {new_root}, "
          f"generated {man['generated']} (UTC).")
    print("The file list is unchanged: no path was added or dropped by this run.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
