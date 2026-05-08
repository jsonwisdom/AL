# ALMS Core Quickstart
```bash
git clone https://github.com/jsonwisdom/AL.git
cd AL
git checkout alms-core-v0.1.1-fork-resolution
cd alms-core
chmod +x reproduce.sh
./reproduce.sh
sha256sum examples/claim.pass.json examples/bundle.pass.json examples/runtime.pass.json

Expected:

e40ec1f8fbe50938b739a4c8e3ac74ed264e719a5d87b9be7e54d6364db18832  examples/claim.pass.json
2347b91688f2f2e52dfd85080737eea25707273032c283b27d536f46726c3480  examples/bundle.pass.json
7ab21151c6096225b549a88381e2a5f0257046359fd50c4cc268183137e5b23e  examples/runtime.pass.json

If hashes differ, open a challenge PR.
