#!/usr/bin/env bash
set -euo pipefail

python3 - "$1" <<'PY'
import sys, urllib.parse, posixpath, unicodedata

raw = sys.argv[1]
u = urllib.parse.urlsplit(raw)

scheme = (u.scheme or "https").lower()
host = (u.hostname or "").lower()
port = u.port

path = unicodedata.normalize("NFC", urllib.parse.unquote(u.path or "/"))
path = posixpath.normpath(path)
if path == ".":
    path = ""
if path != "/" and path.endswith("/"):
    path = path[:-1]

drop = {"utm", "ref", "fbclid", "gclid", "mc_cid", "mc_eid"}
pairs = urllib.parse.parse_qsl(u.query, keep_blank_values=True)
kept = []
for k, v in pairs:
    lk = k.lower()
    if lk in drop or lk.startswith("utm_"):
        continue
    kept.append((lk, v))

query = urllib.parse.urlencode(sorted(kept), doseq=True)

netloc = host
if port and not ((scheme == "https" and port == 443) or (scheme == "http" and port == 80)):
    netloc = f"{host}:{port}"

print(urllib.parse.urlunsplit((scheme, netloc, path, query, "")))
PY
