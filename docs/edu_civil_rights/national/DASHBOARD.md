# EDU_CIVIL_RIGHTS_OBSERVER – State Receipt Dashboard

This dashboard is generated from:

- `_truth/edu_civil_rights/*/*_EDU_CIVIL_RIGHTS_001.leaf.json`
- `_truth/edu_civil_rights/national/dashboard_state_status.json`

## State Status Codes

- **SCHEMA_LOCKED + no hash + no aggregates** → Scaffold only (no data).
- **numeric_fields_populated = true + hash_present = true** → Eligible for national aggregation.
- **Absent from dashboard_state_status.json** → No leaf exists.

## Commands

```bash
bash scripts/edu_civil_rights/run_dashboard_status.sh
python3 scripts/edu_civil_rights/national_aggregate.py > _truth/edu_civil_rights/national/national_aggregate.json
```

Narrative may gesture. Only receipts prove.
