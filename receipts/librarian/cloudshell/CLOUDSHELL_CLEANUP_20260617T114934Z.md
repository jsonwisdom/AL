# Cloud Shell Cleanup Receipt

timestamp_utc: 20260617T114934Z
incident_class: CLOUDSHELL_DISK_PRESSURE
root_cause: PIP_CACHE_GROWTH
operator_blame: false

## DISK
Filesystem                         Size  Used Avail Use% Mounted on
/dev/disk/by-id/google-home-part1  4.8G  3.8G  749M  84% /home

## CACHE
pip/npm cache minimal or cleared

## PROTECTED CHECK
constitution_dir: PRESENT
feed_files: 0

status: COMPLETE
guardrail: NO_FAKE_GREEN
