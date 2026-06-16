# External Membrane Readback Receipt

Timestamp UTC: 20260614T190219Z
Repo: jsonwisdom/AL
Remote Commit: b9fe0173e3034cbfeffe1366d7e0f513ca1399d0

## Case

ALMS-2026-06-14-JW-EXTERNAL-MEMBRANES

## Rule

No external GREEN without live readback.
- HTTP_GREEN 200 sha256:989f128d1207ab4778946e882487906801f3af47d5e0102437891bcccc2bc62d site/unified-mesh.json
- HTTP_GREEN 200 sha256:4f7e7d34691709d54613ddfa51c3329795ff411a0265b426fc82e3724a036bc5 site/nitro-feed.json
- HTTP_GREEN 200 sha256:17496bb0223c680469df863de06cabff4bab9c3ce547e3e77788bbd1e52b58f2 site/systemconfig-mainnet.json
- HTTP_GREEN 200 sha256:5cec23eb8eeef52646a758031044d4339ec3ba0ae2e0c4e862dd83197ecef820 site/systemconfig-sepolia.json
- HTTP_GREEN 200 sha256:5ed8df9a056d9747c8f2ff0f7b98763af24d86a5eb1f74a7355644d8742f382d site/convergence.json
- HTTP_GREEN 200 sha256:b19a70e1f5985996c6753fa6f76862241bff78798a49649c85b333ae6ad34bc6 _truth/cw/receipt.json
- HTTP_GREEN 200 sha256:e7117d9d8b76072150ed35bbd73af504008eeb326910d686b6ef66b1e54ce1d5 _truth/receipts/MN_002.json
- BASE_TX_READBACK=YELLOW_NO_TX_SUBMITTED
