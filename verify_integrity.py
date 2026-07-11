#!/usr/bin/env python3
"""
verify_integrity.py -- offline, READ-ONLY integrity check for the Digital-Asset Law Corpus.

Recomputes the SHA-256 of every file against corpus_manifest.json and re-derives the single
root hash. GREEN = every file matches and the root reproduces; RED = something changed.
No dependencies, no network, no writes. Run from the corpus root:

    python3 verify_integrity.py
"""
import json, hashlib, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))

def sha(path):
    return "sha256:" + hashlib.sha256(open(path, "rb").read()).hexdigest()

def main():
    mpath = os.path.join(ROOT, "corpus_manifest.json")
    if not os.path.exists(mpath):
        print("RED — corpus_manifest.json not found"); return 2
    man = json.load(open(mpath, encoding="utf-8"))
    files = man["files"]
    bad, missing = [], []
    for rel, want in sorted(files.items()):
        p = os.path.join(ROOT, rel)                       # forward-slash keys work on all OSes
        if not os.path.exists(p):
            missing.append(rel); continue
        if sha(p) != want:
            bad.append(rel)
    # untracked extra files (manifest can't hash itself; skip the VCS dir)
    tracked = set(files) | {"corpus_manifest.json"}
    extra = []
    for dirpath, dirs, fnames in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        for fn in fnames:
            rel = os.path.relpath(os.path.join(dirpath, fn), ROOT).replace(os.sep, "/")
            if rel not in tracked:
                extra.append(rel)
    # re-derive the root hash from the manifest's own file list
    root = "sha256:" + hashlib.sha256(
        "".join(f"{k}:{v}" for k, v in sorted(files.items())).encode()).hexdigest()
    root_ok = (root == man.get("root_hash"))

    ok = not bad and not missing and root_ok
    print(f"Digital-Asset Law Corpus — integrity: {'GREEN' if ok else 'RED'}")
    print(f"  files checked : {len(files)}")
    print(f"  hash mismatch : {len(bad)}")
    print(f"  missing       : {len(missing)}")
    print(f"  root hash     : {'reproduces' if root_ok else 'MISMATCH'}")
    if extra:
        print(f"  untracked     : {len(extra)} file(s) present but not in the manifest")
    for r in bad[:20]:     print("   CHANGED", r)
    for r in missing[:20]: print("   MISSING", r)
    for r in extra[:20]:   print("   UNTRACKED", r)
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
