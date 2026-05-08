# ALMS Core Quickstart

```bash
git clone https://github.com/jsonwisdom/AL.git
cd AL
git checkout alms-core-v0.1.1-fork-resolution
cd alms-core
chmod +x reproduce.sh
./reproduce.sh
sha256sum examples/claim.pass.json examples/bundle.pass.json examples/runtime.pass.json
```

## Expected output from `./reproduce.sh`

`./reproduce.sh` verifies the embedded ALMS canonical object hashes using the stdlib verifier.

Expected embedded object hashes:

```text
claim_hash   sha256:e40ec1f8fbe50938b739a4c8e3ac74ed264e719a5d87b9be7e54d6364db18832
bundle_hash  sha256:2347b91688f2f2e52dfd85080737eea25707273032c283b27d536f46726c3480
runtime_hash sha256:7ab21151c6096225b549a88381e2a5f0257046359fd50c4cc268183137e5b23e
```

## Expected raw file-byte `sha256sum` output

The file-byte hashes are different from the embedded ALMS canonical object hashes.

Expected file-byte hashes:

```text
bd37ce61369650af2d03a66644c6ea9a34ed057fdfb32d2c9b6609d4239861c7  examples/claim.pass.json
e4869bdf8d4f6474f952e07cfd50109d9f092750a84adfcf0789fead6a4af9db  examples/bundle.pass.json
520913a00483715062f0f2dc9b77cf3ec45efb819118344588c699e2ad40b5d2  examples/runtime.pass.json
```

If either class of hash differs, open a challenge PR with plaintext logs.
