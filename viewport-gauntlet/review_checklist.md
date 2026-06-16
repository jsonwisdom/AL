# Viewport Gauntlet Review Checklist

## Pre-Run Validation

### Environment Setup
- [ ] Constraint definitions loaded from `constraints/`
- [ ] Baseline hash recorded in `replays/baseline_run_hash.txt`
- [ ] Logging directories exist: `logs/raw`, `logs/recordings`
- [ ] Results directory ready: `results/`

### Task Review
- [ ] All assigned tasks understood
- [ ] Success criteria clearly defined
- [ ] Expected output format documented
- [ ] No ambiguity in task specifications

### Constraint Verification
- [ ] Active constraints identified
- [ ] Tier level confirmed (1, 2, or 3)
- [ ] Constraint implications reviewed
- [ ] Enforcement method validated

## During Execution

### Operator Actions
- [ ] All interventions logged to `logs/interventions.csv`
- [ ] Timestamps recorded for each action
- [ ] Recovery attempts documented
- [ ] State transitions tracked

### Task Progress
- [ ] Task started and logged
- [ ] Incremental progress recorded
- [ ] Constraint violations noted
- [ ] Error handling verified

## Post-Run Validation

### Result Completeness
- [ ] All tasks completed or failed status recorded
- [ ] Metrics JSON populated: `results/run_NNN_operator_hybrid.json`
- [ ] Summary metrics generated: `results/summary_metrics.md`
- [ ] Diff clean and reviewable

### Pass/Fail Determination
- [ ] `metrics.py` executed successfully
- [ ] Status: PASS or FAIL clearly indicated
- [ ] Completion rate calculated
- [ ] Unintended edits: 0
- [ ] State loss incidents: 0

### Logs & Artifacts
- [ ] `logs/interventions.csv` complete with all actions
- [ ] `logs/raw/` contains execution traces
- [ ] `logs/recordings/` has viewport/network recordings
- [ ] All logs compressed if needed

### Commit & PR
- [ ] Git diff reviewed for correctness
- [ ] Only intended files modified
- [ ] Commit message clear and atomic
- [ ] PR opened with:
  - [ ] Run ID in title
  - [ ] Constraint tier documented
  - [ ] Metrics summary in description
  - [ ] Links to result JSON
  - [ ] Pass/fail status visible

## Review Surfaces

### For Code Review
1. **Diff check**: `git diff main viewport-gauntlet-v1`
2. **File changes**: Count and categorize modifications
3. **Unintended edits**: Verify zero drift outside task scope

### For Metrics Review
1. **metrics.py output**: PASS/FAIL determination
2. **Completion rate**: 100% or documented failures
3. **Intervention log**: Assess operator effectiveness
4. **State integrity**: Verify no loss incidents

### For Reproducibility
1. **Baseline hash**: Git commit for replay
2. **Constraint definition**: JSON specs match execution
3. **Task inputs**: Specifications match actual work
4. **Logs attachment**: Full trace available for audit

### For Operational Insights
1. **Tier difficulty**: Expected vs actual time
2. **Recovery patterns**: What worked, what failed
3. **Constraint impact**: Which constraint caused issues
4. **Human-AI coordination**: Intervention effectiveness
