#!/usr/bin/env bash
set -euo pipefail

REPO="https://github.com/jsonwisdom/AL.git"
WORKDIR="${1:-$HOME/alms-mirror}"

mkdir -p "$WORKDIR"
cd "$WORKDIR"

if [ ! -d AL ]; then
  git clone "$REPO"
fi

cd AL
git pull origin master

chmod +x scripts/*.sh || true

./scripts/validate_jsonl.sh
./scripts/build_alms_root.sh

LOCAL_ROOT="$(jq -r '.root_sha256' _truth/root/alms_root.json)"
PUBLIC_ROOT="$(curl -s https://jsonwisdom.github.io/AL/status.json | jq -r '.root_sha256')"
MERKLE_ROOT="$(curl -s https://jsonwisdom.github.io/AL/status.json | jq -r '.merkle_root')"
COMMIT="$(git rev-parse HEAD)"
NOW="$(date -u +%FT%TZ)"
HOST="$(hostname)"

RESULT="MISMATCH"
if [ "$LOCAL_ROOT" = "$PUBLIC_ROOT" ]; then
  RESULT="CONVERGED"
fi

OUT="mirror_proof_${NOW}.json"

jq -cS -n \
  --arg id "$HOST" \
  --arg repo "$REPO" \
  --arg commit "$COMMIT" \
  --arg ts "$NOW" \
  --arg local "$LOCAL_ROOT" \
  --arg pub "$PUBLIC_ROOT" \
  --arg merkle "$MERKLE_ROOT" \
  --arg res "$RESULT" \
'{
  mirror_id: $id,
  source_repo: $repo,
  source_commit: $commit,
  observed_at: $ts,
  local_root_sha256: $local,
  public_root_sha256: $pub,
  merkle_root: $merkle,
  result: $res
}' > "$OUT"

echo "MIRROR_PROOF_WRITTEN $OUT"
cat "$OUT"
