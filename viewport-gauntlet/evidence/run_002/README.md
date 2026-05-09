# Run 002: Evidence

## Run Metadata

**Run ID:** `run_002`

**Task:** `fix_markdown_bug`

**Constraints:**
- `mobile_safari_390px` – iPhone SE viewport (390px width)
- `intermittent_network` – 20-30% packet loss, 500-2000ms latency

**Device:** iPhone 13

**Environment:** GitHub Codespaces in Safari

**Base Branch Commit:** `9eced94ae083ed6de4fe51cee7fc062ab8d6d1c3`

## Required Artifacts

All evidence artifacts must be present in this directory:

- [ ] `screen_recording.mp4` – Full screen recording of task execution under constraints
- [ ] `interventions.csv` – Timestamped log of all operator actions
- [ ] `run_002.patch` – Git diff of changes made during task execution
- [ ] `run_002.json` – Structured result metrics and completion data
- [ ] `metrics_output.txt` – Output from `metrics.py` evaluation
- [ ] Final commit hash – Git SHA of final state after task completion

## Completion Rule

**No evidence commit is complete without:**
1. Final commit SHA recorded
2. Metrics output generated and verified
3. All required artifacts present
4. Pass/Fail status clearly determined

## Verification

Run the metrics evaluation:

```bash
bash viewport-gauntlet/evidence/run_002/run_metrics.sh
```

This script will:
1. Verify `run_002.json` exists
2. Execute `metrics.py` against the result JSON
3. Write output to `metrics_output.txt`
4. Print results to stdout
