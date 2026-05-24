#!/usr/bin/env bash
set -euo pipefail

REPO="${REPO:-jsonwisdom/AL}"
COMMIT="${COMMIT:-da123f7dcd0f26f838cff856f7e17676c2153305}"
ENV_NAME="${ENV_NAME:-three-green-seal}"

echo "== PRE-FLIGHT: 3-GREEN SEAL =="
echo ""

# 1) Verify workflow approval gate
echo "1) Verify workflow contains approval gate..."
if git show "$COMMIT":.github/workflows/heartbeat-transition.yml \
  | grep -A4 "advance_state:" \
  | grep -q "environment: $ENV_NAME"; then
  echo "✅ Workflow contains environment: $ENV_NAME"
else
  echo "❌ Workflow missing environment: $ENV_NAME"
  exit 1
fi

# 2) Verify GitHub environment protection rules
echo "2) Verify GitHub environment protection rules..."
RULES="$(gh api "repos/$REPO/environments/$ENV_NAME" --jq '.protection_rules[].type' 2>/dev/null || true)"
if echo "$RULES" | grep -q "required_reviewers"; then
  echo "✅ Environment has required reviewers"
else
  echo "❌ Missing required_reviewers protection rule on environment: $ENV_NAME"
  echo "   → Configure at: https://github.com/$REPO/settings/environments/$ENV_NAME"
  exit 1
fi

# 3) Verify governance root has no ceremony pollution
echo "3) Verify governance root ceremony-clean..."
if git ls-tree "$COMMIT" _truth/governance/ | grep -qi "CEREMONY_COURT_RULES"; then
  echo "❌ Post-milestone ceremony artifact still present in governance root"
  exit 1
fi
echo "✅ Governance root ceremony-clean"

# 4) Verify state machine is pre-milestone safe
echo "4) Verify state machine is pre-milestone safe..."
if git show "$COMMIT":_truth/governance/TRACK_001_STATE_MACHINE.json \
  | grep -q '"depends_on_post_milestone_state": false' && \
   git show "$COMMIT":_truth/governance/TRACK_001_STATE_MACHINE.json \
  | grep -q '"ceremony_phase_support": false'; then
  echo "✅ State machine retained as valid root leaf"
else
  echo "❌ State machine has post-milestone dependencies"
  exit 1
fi

# 5) Verify receipt code disables ceremony court
echo "5) Verify receipt code disables ceremony court..."
if git show "$COMMIT":verifier/src/ceremony/receipt.rs \
  | grep -q '"CEREMONY_COURT" => false'; then
  echo "✅ Receipt verifier disables ceremony court"
else
  echo "❌ Receipt verifier still has active ceremony court logic"
  exit 1
fi

echo ""
echo "🟢 PRE-FLIGHT PASSED — All checks successful"
echo ""
echo "📋 Summary:"
echo "   • Workflow approval gate:     ✅"
echo "   • Environment protection:     ✅"
echo "   • Governance root clean:      ✅"
echo "   • State machine safe:         ✅"
echo "   • Receipt verifier safe:      ✅"
echo ""
echo "=== TRIGGER INSTRUCTIONS ==="
echo "This workflow is triggered by workflow_run (not workflow_dispatch)."
echo ""
echo "To trigger the Heartbeat Transition workflow:"
echo "  1. Run the upstream 'Verifier Heartbeat' workflow on branch: master"
echo "  2. The Heartbeat Transition workflow will automatically start"
echo "  3. It will PAUSE at environment: $ENV_NAME"
echo "  4. Required reviewers must approve in GitHub Actions UI"
echo "  5. After approval, the seal will commit and push"
echo ""
echo "Do NOT use: gh workflow run heartbeat-transition.yml"
echo "Do trigger: Upstream Verifier Heartbeat on master"
