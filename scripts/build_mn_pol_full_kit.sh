#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$HOME}"
KIT="$ROOT/MN_POL_FULL_KIT"
ZIP="$ROOT/MN_POL_FULL_KIT.zip"

rm -rf "$KIT" "$ZIP"
mkdir -p "$KIT"/{social,visuals,video,assets}

cat > "$KIT/README.md" <<'EOF'
MN_POL_FULL_KIT

Purpose:
Portable, verifiable civic record system for Stearns County / MN House 2026 legislative records.

Core rule:
67-67 = no majority -> no bill passes

Core link:
https://www.house.mn.gov/votes/

Use:
1. Print Page 1 as the Voter Truth Sheet.
2. Print Page 2 as the QR Verification Sheet.
3. Use Page 3 as the field guide.
4. Do not argue. Point to official records.
EOF

cat > "$KIT/01_Voter_Truth_Sheet.md" <<'EOF'
# STEARNS COUNTY VOTER TRUTH SHEET (2026)

## HOW THE HOUSE WORKS

134 members | 68 to pass | 90 to fast-track

67-67 = no majority -> no bill passes

## YOUR REPRESENTATIVES

- Lisa Demuth (13A, GOP)
- Tim O'Driscoll (13B, GOP)
- Bernie Perryman (14A, GOP)
- Dan Wolgamott (14B, DFL)

## RECORDED VOTES

### PROPERTY TAX RELIEF (APRIL 2026)

67 YES | 67 NO -> FAILED

Local votes:
- Demuth -> YES
- O'Driscoll -> YES
- Perryman -> YES
- Wolgamott -> NO

### SF 856 - INSPECTOR GENERAL

66 YES | 67 NO
Needed: 90 -> FAILED

### HF 3493 - SAFE SCHOOLS

Committee: 12-12 -> FAILED
Floor recall: 67-67 -> FAILED

## PUBLIC CONTEXT

- State surplus, Feb 2026 forecast: about $3.7B
- Stearns County levy: about +5% county-level signal
- OLA Audit, Jan 6 2026: DHS Behavioral Health Administration grants report found noncompliance, weak controls, and documentation created/backdated during review.

## WHY THESE RESULTS HAPPENED

Committee -> needs majority
Floor -> needs 68
Fast-track -> needs 90
Tie -> automatic failure

## 68TH VOTE EXPLAINER

67-67 -> FAIL
+1 vote -> 68-66 -> PASS

One vote changes ordinary majority outcomes. It does not solve 90-vote fast-track thresholds.

## VERIFY

- House votes: https://www.house.mn.gov/votes/
- Revisor bills: https://www.revisor.mn.gov/bills/
- SF 856 coverage: https://www.house.mn.gov/SessionDaily/Story/18879
- HF 3493 bill page: https://www.revisor.mn.gov/bills/bill.php?b=House&f=HF3493&ssn=0&y=2026
- OLA audit PDF: https://www.auditor.leg.state.mn.us/fad/pdf/fad2601.pdf

## QUESTIONS TO ASK

- Why did this vote not reach the required threshold?
- What would justify a crossover vote?
- How should the surplus be prioritized?
- What changes follow the audit findings?

## NOTE

Recorded public events only. No claim of intent. Verify yourself.
EOF

cat > "$KIT/02_QR_Sheet.md" <<'EOF'
# VERIFY THE RECORD

Scan -> View -> Decide

## VERIFY ALL VOTES

[QR PLACEHOLDER]

https://www.house.mn.gov/votes/

## SF 856 - INSPECTOR GENERAL

[QR PLACEHOLDER]

https://www.house.mn.gov/SessionDaily/Story/18879

## HF 3493 - SAFE SCHOOLS

[QR PLACEHOLDER]

https://www.revisor.mn.gov/bills/bill.php?b=House&f=HF3493&ssn=0&y=2026

## STATE AUDIT - DHS GRANTS

[QR PLACEHOLDER]

https://www.auditor.leg.state.mn.us/fad/pdf/fad2601.pdf

Official MN House / State records only.
EOF

cat > "$KIT/03_Quick_Use_Guide.md" <<'EOF'
# QUICK USE GUIDE

## Door

"This shows how the votes actually went locally."

## Anchor

"67-67 means nothing passes."

## Verify

"Scan and check it yourself. These are official records."

## Exit

"No worries - just wanted you to have the record."

## Rule

No arguing. No persuading. Only point to records.
EOF

cat > "$KIT/social/10_post_set.txt" <<'EOF'
POST 1
67-67
No majority = no bill passes.
That is how the MN House worked in 2026.
Verify: https://www.house.mn.gov/votes/

POST 2
Property Tax Relief (April 2026)
67 YES | 67 NO
Result: FAILED
Local: Demuth YES, O'Driscoll YES, Perryman YES, Wolgamott NO

POST 3
Not all votes are equal.
Pass bill -> 68
Fast-track -> 90
SF 856: 66-67 failed because 90 were needed.

POST 4
HF 3493
Committee: 12-12 -> FAILED
Floor recall: 67-67 -> FAILED
Record: https://www.revisor.mn.gov/bills/bill.php?b=House&f=HF3493&ssn=0&y=2026

POST 5
Tie = automatic failure.
12-12 -> no advance
67-67 -> no passage
No majority -> no outcome

POST 6
67-67 -> FAIL
+1 vote -> 68-66 -> PASS
One vote changes ordinary majority outcomes.

POST 7
Property relief: 67-67 -> +1 vote could pass.
SF 856: 66-67 still failed because fast-track needed 90.
Rules decide outcomes.

POST 8
State Audit (Jan 6, 2026)
Findings: noncompliance, weak controls, documentation issues.
Source: https://www.auditor.leg.state.mn.us/fad/pdf/fad2601.pdf

POST 9
Do not argue.
Verify.
Records are public:
https://www.house.mn.gov/votes/
https://www.revisor.mn.gov/bills/

POST 10
The record is public.
The rules are clear.
Check it yourself.
EOF

cat > "$KIT/social/captions.txt" <<'EOF'
All from official MN House records. Scan or verify: https://www.house.mn.gov/votes/

Reply discipline:
"Can you show the vote record?"
EOF

cat > "$KIT/visuals/card_specs.md" <<'EOF'
# MN_POL Visual Cards

Size: 1080x1080
Style: black / white / red
Font: Inter or Arial
Numbers: extra large and bold
QR: bottom-right, 12-15% canvas
Label: Scan to verify
Primary QR URL: https://www.house.mn.gov/votes/

Cards:
1. 67-67 / No majority / No bill passes
2. Property Tax Relief / 67 YES 67 NO / Failed
3. Your Area / Demuth YES / O'Driscoll YES / Perryman YES / Wolgamott NO
4. SF 856 / 66 YES 67 NO / Needed 90 / Failed
5. HF 3493 / 12-12 failed / 67-67 failed / Blocked twice
6. How it works / 12-12 no advance / 67-67 no passage
7. One Vote / 67-67 fail / 68-66 pass
8. Thresholds / Pass 68 / Fast-track 90
9. State Audit / Noncompliance / Weak controls / Documentation issues
10. Do not argue / Verify / The record is public
EOF

cat > "$KIT/visuals/qr_overlay_rules.md" <<'EOF'
QR Size: 12-15%
Position: bottom-right
Label: Scan to verify
Primary URL: https://www.house.mn.gov/votes/
Optional OLA QR on audit card: https://www.auditor.leg.state.mn.us/fad/pdf/fad2601.pdf
EOF

cat > "$KIT/video/10_video_scripts.md" <<'EOF'
# MN_POL Video Scripts

Format: 9:16 vertical
Background: black
Text: white with red highlights
Font: Inter or Arial
Length: 5-7 seconds
End every clip with QR + Scan to verify

1. 67-67 -> No majority -> No bill passes
2. Property Tax Relief -> 67 YES / 67 NO -> Failed
3. Your Area -> Demuth YES / O'Driscoll YES / Perryman YES / Wolgamott NO -> Verify
4. SF 856 -> 66 YES / 67 NO -> Needed 90 -> Failed
5. HF 3493 -> 12-12 failed -> 67-67 failed -> Blocked twice
6. Mechanic -> 12-12 no advance -> 67-67 no pass -> No majority
7. 68th Vote -> 67-67 fail -> +1 vote -> 68-66 pass
8. Thresholds -> Pass 68 -> Fast-track 90 -> 66 is not enough
9. Audit -> State audit -> Noncompliance -> Documentation issues
10. Close -> Do not argue -> Verify -> The record is public
EOF

cat > "$KIT/video/capcut_template_guide.md" <<'EOF'
# CapCut Template Guide

1. New project
2. Ratio: 9:16
3. Background: solid black
4. Add three text layers:
   - top label
   - big center text
   - bottom explanation
5. Add QR bottom-right, 12-15% canvas
6. Add "Scan to verify" under QR
7. Timing:
   - 0-2s: hook
   - 2-4s: data
   - 4-6s: result + QR
8. Duplicate project 10 times
9. Swap text only
10. Export 1080x1920, 30 FPS

Caption:
All from official MN House records. Scan to verify.
EOF

cat > "$KIT/MANIFEST.json" <<'EOF'
{
  "name": "MN_POL_FULL_KIT",
  "version": "1.0",
  "scope": "Stearns County / MN House 2026 legislative record",
  "core_rule": "67-67 = no majority -> no bill passes",
  "primary_verification_url": "https://www.house.mn.gov/votes/",
  "status": "deployment_ready"
}
EOF

(
  cd "$ROOT"
  zip -r "MN_POL_FULL_KIT.zip" "MN_POL_FULL_KIT" >/dev/null
)

sha256sum "$ZIP" > "$ZIP.sha256"

echo "BUILT $ZIP"
echo "HASH  $(cat "$ZIP.sha256")"
echo "DOWNLOAD in Google Cloud Shell: cloudshell download $ZIP"
