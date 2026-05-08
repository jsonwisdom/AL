# ALMS Core v0.1.1 — Reproducibility Contract

## Branch

`alms-core-v0.1.1-fork-resolution`

## Commit

`33277e41ecf469ddc867a72b73693406debcf65c`

## Expected Golden Hashes

```text
bd37ce61369650af2d03a66644c6ea9a34ed057fdfb32d2c9b6609d4239861c7  examples/claim.pass.json
e4869bdf8d4f6474f952e07cfd50109d9f092750a84adfcf0789fead6a4af9db  examples/bundle.pass.json
520913a00483715062f0f2dc9b77cf3ec45efb819118344588c699e2ad40b5d2  examples/runtime.pass.json
```

## Receipt Hash to Sign

```text
sha256:cfa5f97b51625dde24184843fe155af868fb419b5d5f868cd1f79c27ea185e01
```

Hex digest, without prefix:

```text
cfa5f97b51625dde24184843fe155af868fb419b5d5f868cd1f79c27ea185e01
```

## Reproduce

```bash
git clone https://github.com/jsonwisdom/AL.git
cd AL
git checkout alms-core-v0.1.1-fork-resolution
cd alms-core
chmod +x reproduce.sh
./reproduce.sh
sha256sum examples/claim.pass.json examples/bundle.pass.json examples/runtime.pass.json
```

## Sign

```bash
openssl genrsa -out observer_private_key.pem 2048

openssl rsa -in observer_private_key.pem -pubout \
  -out observer_public_key.pem

sha256sum observer_public_key.pem

echo -n "cfa5f97b51625dde24184843fe155af868fb419b5d5f868cd1f79c27ea185e01" | \
  openssl dgst -sha256 -sign observer_private_key.pem | \
  base64 -w 0
```

## Observer Submission Packet

Create a file in `signatures/observer_N.json` with:

```json
{
  "observer_id": "observer_N",
  "receipt_hash": "sha256:cfa5f97b51625dde24184843fe155af868fb419b5d5f868cd1f79c27ea185e01",
  "public_key_fingerprint": "sha256:<fingerprint>",
  "signature_base64": "<base64 signature>",
  "environment": {
    "os": "...",
    "python_version": "..."
  },
  "reproduction_log": "..."
}
```

## Rule — No Anchor Before Three

- 2/3 is not finality. It is partial evidence.
- 3/3 is quorum.
- Receipt status remains `TRANSPARENCY_LOG_PENDING` until Observer 3 signs.

## Safety

- Do not commit private keys.
- Only publish observer ID, public key fingerprint, signature, reproduction log, and environment fingerprint.
