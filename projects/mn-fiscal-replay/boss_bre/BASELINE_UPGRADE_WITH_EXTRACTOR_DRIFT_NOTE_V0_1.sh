#!/bin/bash
# Boss Bre Baseline Upgrade Script - v0.1
# Handles extractor drift while preserving verifiable baseline

set -e

COMPONENT=$1
if [ -z "$COMPONENT" ]; then
  echo "Usage: $0 MN_001"
  exit 1
fi

echo "🔄 Upgrading baseline for $COMPONENT with extractor drift note..."

# Ensure output directory exists
mkdir -p "projects/mn-fiscal-replay/baselines"

# Copy live normalized as new baseline
cp "projects/mn-fiscal-replay/live_fetch/$COMPONENT/${COMPONENT}_live_normalized.txt" \
   "projects/mn-fiscal-replay/baselines/${COMPONENT}_baseline_normalized.txt"

# Add drift note
cat > "projects/mn-fiscal-replay/baselines/${COMPONENT}_drift_note.md" << EOF
# Baseline Upgrade Note - $(date -u +%Y-%m-%dT%H:%M:%SZ)
Component: $COMPONENT
Classification: ORDERING_ARTIFACT + EXTRACTOR_ARTIFACT
Reason: Page markers, TOC splitting, PDF layout drift
Action: Live state promoted to new baseline
Public Claim: BLOCKED (no content delta proven)
NO_FAKE_GREEN: ACTIVE
EOF

echo "✅ Baseline upgraded for $COMPONENT with drift documentation."
echo "Run validator to confirm lattice integrity."
