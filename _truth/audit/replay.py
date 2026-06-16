#!/usr/bin/env python3
import argparse
import hashlib
import subprocess
import sys

EXCLUDES = {
    "_truth/audit/replay.py",
}

def git_ls(commit):
    out = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", commit, "_truth"],
        text=True
    )
    return [
        p for p in out.splitlines()
        if p
        and p not in EXCLUDES
        and not p.startswith("_truth/tmp/")
    ]

def git_blob(commit, path):
    return subprocess.check_output(["git", "show", f"{commit}:{path}"])

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def compute(commit):
    leaves = []
    for path in sorted(git_ls(commit)):
        data = git_blob(commit, path)
        leaf = sha256(path.encode("utf-8") + b"\0" + data)
        leaves.append(leaf.encode("ascii"))

    if not leaves:
        return sha256(b"")

    level = leaves
    while len(level) > 1:
        nxt = []
        for i in range(0, len(level), 2):
            left = level[i]
            right = level[i + 1] if i + 1 < len(level) else left
            nxt.append(sha256(left + right).encode("ascii"))
        level = nxt

    return level[0].decode("ascii")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--commit", default="HEAD")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()
    print(compute(args.commit))

if __name__ == "__main__":
    main()
