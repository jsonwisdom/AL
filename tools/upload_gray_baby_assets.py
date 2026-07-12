#!/usr/bin/env python3
"""Upload the GB-007 and GB-008 PNGs to the review branch atomically.

Required environment:
  GITHUB_TOKEN  Fine-grained token with Contents: Read and write on jsonwisdom/AL

Usage:
  python3 tools/upload_gray_baby_assets.py \
    --gb007 /path/to/GB-007-Witness-Feedback-Loop.png \
    --gb008 /path/to/GB-008-Dissent-Protocol.png

The script:
  1. verifies both local SHA-256 fingerprints;
  2. creates two Git blobs using Base64;
  3. creates one tree based on the current branch tree;
  4. creates one commit with both assets;
  5. advances the branch using a non-forced ref update;
  6. prints the new commit SHA and canonical blob URLs.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

OWNER = "jsonwisdom"
REPO = "AL"
BRANCH = "feature/gray-baby-007-009-review"
API = "https://api.github.com"

ASSETS = {
    "gb007": {
        "path": "assets/GB-007-Witness-Feedback-Loop.png",
        "sha256": "1aa726e2741c94a6d76be93ab4fbe8e0575018b9d8124e6f3f00043a8b69fbc7",
    },
    "gb008": {
        "path": "assets/GB-008-Dissent-Protocol.png",
        "sha256": "87053babf6bc1176a8218cf201b6f000fb889e7a6a687c10eb0969e80dffb5d1",
    },
}


def die(message: str) -> "NoReturn":
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def request(token: str, method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    url = f"{API}{path}"
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
            "User-Agent": "gray-baby-asset-uploader/1.0",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        die(f"GitHub API {exc.code} for {method} {path}: {body}")
    except urllib.error.URLError as exc:
        die(f"Network failure for {method} {path}: {exc}")


def read_verified(path: Path, expected_sha256: str) -> bytes:
    if not path.is_file():
        die(f"file not found: {path}")
    data = path.read_bytes()
    actual = hashlib.sha256(data).hexdigest()
    if actual != expected_sha256:
        die(f"SHA-256 mismatch for {path}: expected {expected_sha256}, got {actual}")
    print(f"VERIFIED {path}  bytes={len(data)}  sha256={actual}")
    return data


def create_blob(token: str, data: bytes) -> str:
    result = request(
        token,
        "POST",
        f"/repos/{OWNER}/{REPO}/git/blobs",
        {"content": base64.b64encode(data).decode("ascii"), "encoding": "base64"},
    )
    sha = result.get("sha")
    if not isinstance(sha, str):
        die(f"blob creation returned no SHA: {result}")
    return sha


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gb007", type=Path, required=True)
    parser.add_argument("--gb008", type=Path, required=True)
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        die("GITHUB_TOKEN is not set")

    local = {
        "gb007": read_verified(args.gb007, ASSETS["gb007"]["sha256"]),
        "gb008": read_verified(args.gb008, ASSETS["gb008"]["sha256"]),
    }

    encoded_branch = urllib.parse.quote(BRANCH, safe="")
    ref = request(token, "GET", f"/repos/{OWNER}/{REPO}/git/ref/heads/{encoded_branch}")
    head_sha = ref.get("object", {}).get("sha")
    if not isinstance(head_sha, str):
        die(f"could not resolve branch head: {ref}")

    commit = request(token, "GET", f"/repos/{OWNER}/{REPO}/git/commits/{head_sha}")
    base_tree_sha = commit.get("tree", {}).get("sha")
    if not isinstance(base_tree_sha, str):
        die(f"could not resolve base tree: {commit}")

    blob007 = create_blob(token, local["gb007"])
    blob008 = create_blob(token, local["gb008"])

    tree = request(
        token,
        "POST",
        f"/repos/{OWNER}/{REPO}/git/trees",
        {
            "base_tree": base_tree_sha,
            "tree": [
                {
                    "path": ASSETS["gb007"]["path"],
                    "mode": "100644",
                    "type": "blob",
                    "sha": blob007,
                },
                {
                    "path": ASSETS["gb008"]["path"],
                    "mode": "100644",
                    "type": "blob",
                    "sha": blob008,
                },
            ],
        },
    )
    tree_sha = tree.get("sha")
    if not isinstance(tree_sha, str):
        die(f"tree creation returned no SHA: {tree}")

    new_commit = request(
        token,
        "POST",
        f"/repos/{OWNER}/{REPO}/git/commits",
        {
            "message": "feat(assets): bind GB-007 and GB-008 verified PNGs",
            "tree": tree_sha,
            "parents": [head_sha],
        },
    )
    new_commit_sha = new_commit.get("sha")
    if not isinstance(new_commit_sha, str):
        die(f"commit creation returned no SHA: {new_commit}")

    request(
        token,
        "PATCH",
        f"/repos/{OWNER}/{REPO}/git/refs/heads/{encoded_branch}",
        {"sha": new_commit_sha, "force": False},
    )

    print("UPLOAD_COMPLETE")
    print(f"OLD_HEAD_SHA={head_sha}")
    print(f"NEW_COMMIT_SHA={new_commit_sha}")
    print(f"GB007_BLOB_SHA={blob007}")
    print(f"GB008_BLOB_SHA={blob008}")
    print(
        "GB007_BLOB_URL="
        f"https://github.com/{OWNER}/{REPO}/blob/{new_commit_sha}/{ASSETS['gb007']['path']}"
    )
    print(
        "GB008_BLOB_URL="
        f"https://github.com/{OWNER}/{REPO}/blob/{new_commit_sha}/{ASSETS['gb008']['path']}"
    )


if __name__ == "__main__":
    main()
