#!/usr/bin/env python3
import sys
import hashlib

if len(sys.argv) < 2:
    print("Usage: hash_text_bytes.py <text_file>")
    sys.exit(1)

path = sys.argv[1]
sha = hashlib.sha256()

with open(path, "rb") as f:
    for chunk in iter(lambda: f.read(4096), b""):
        sha.update(chunk)

print(sha.hexdigest())
