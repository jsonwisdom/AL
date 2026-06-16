#!/usr/bin/env bash
set -euo pipefail

printf '\n⚙️  ALMS BigQuery / Python Bootstrap\n'
printf 'Policy: TERMINAL_FIRST / NO_GHOST_PROMOTION\n\n'

command -v gcloud >/dev/null || {
  echo "❌ gcloud not found. Install/use Google Cloud SDK first."
  exit 1
}

command -v bq >/dev/null || {
  echo "❌ bq not found. BigQuery CLI should come with Google Cloud SDK."
  exit 1
}

echo "🔐 Active gcloud accounts:"
gcloud auth list

CURRENT_PROJECT="$(gcloud config get-value project 2>/dev/null || true)"
if [[ -n "${CURRENT_PROJECT}" && "${CURRENT_PROJECT}" != "(unset)" ]]; then
  read -rp "Use current project '${CURRENT_PROJECT}'? [Y/n]: " USE_CURRENT
  if [[ "${USE_CURRENT:-Y}" =~ ^[Yy]$ ]]; then
    PROJECT_ID="${CURRENT_PROJECT}"
  else
    read -rp "Enter GCP PROJECT_ID: " PROJECT_ID
  fi
else
  read -rp "Enter GCP PROJECT_ID: " PROJECT_ID
fi

if [[ -z "${PROJECT_ID}" ]]; then
  echo "❌ PROJECT_ID is empty. Stop."
  exit 1
fi

echo "📌 Setting project: ${PROJECT_ID}"
gcloud config set project "${PROJECT_ID}"

echo "🔌 Enabling required APIs..."
gcloud services enable \
  bigquery.googleapis.com \
  notebooks.googleapis.com \
  aiplatform.googleapis.com \
  compute.googleapis.com

echo "🧪 Checking BigQuery access..."
bq ls || true

echo "🐍 Creating Python virtual environment..."
python3 -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install \
  google-cloud-bigquery \
  google-cloud-aiplatform \
  pandas \
  pyarrow \
  db-dtypes \
  jupyter \
  notebook

echo "📁 Creating ALMS folders..."
mkdir -p \
  _truth/bigquery \
  _truth/notebooks \
  _truth/receipts \
  scripts

cat > .alms_env <<ENV
PROJECT_ID=${PROJECT_ID}
ALMS_MODE=TERMINAL_FIRST
RECEIPT_POLICY=NO_GHOST_PROMOTION
ENV

echo "🧾 Writing bootstrap receipt..."
BOOTSTRAP_RECEIPT="_truth/receipts/alms_bigquery_bootstrap_$(date -u +%Y%m%dT%H%M%SZ).txt"
{
  echo "ALMS_BIGQUERY_BOOTSTRAP_RECEIPT"
  echo "timestamp_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "project_id=${PROJECT_ID}"
  echo "mode=TERMINAL_FIRST"
  echo "policy=NO_GHOST_PROMOTION"
  echo "anchor=false"
} > "${BOOTSTRAP_RECEIPT}"

python - <<'PY'
from google.cloud import bigquery
client = bigquery.Client()
print("BIGQUERY_CLIENT_OK")
PY

sha256sum "${BOOTSTRAP_RECEIPT}" > "${BOOTSTRAP_RECEIPT}.sha256"

echo "✅ Bootstrap complete"
echo "Receipt: ${BOOTSTRAP_RECEIPT}"
echo "Receipt SHA256: ${BOOTSTRAP_RECEIPT}.sha256"
echo "Run next: source .venv/bin/activate && source .alms_env"
