# ALMS Trilogy V1 — Public Verification

Anyone can verify the ALMS Trilogy integrity using standard tools such as `curl`, `sha256sum`, and `jq`.

## Step 1: Clone the repository

```bash
git clone https://github.com/jsonwisdom/AL.git
cd AL
git checkout 62bf6450357f8edb2d4494140ca294cf073b0708
git rev-parse HEAD
```

Expected commit:

```text
62bf6450357f8edb2d4494140ca294cf073b0708
```

## Step 2: Run the verifier

```bash
./verify_trilogy.sh
```

Expected output:

```text
Downloading directory from IPFS: bafybeibcc32x2jq3ktmk4epvugprux2ehrsx2ukzqbn5gxffvudztc6ile
Downloading: allison.jpg
✓ allison.jpg matches
Downloading: andy.jpg
✓ andy.jpg matches
Downloading: gary.jpg
✓ gary.jpg matches
PASS: Trilogy verified
```

## Step 3: Manual verification

List the IPFS directory:

```bash
ipfs ls bafybeibcc32x2jq3ktmk4epvugprux2ehrsx2ukzqbn5gxffvudztc6ile
```

Download and hash each file:

```bash
for f in andy.jpg gary.jpg allison.jpg; do
  curl -sL "https://ipfs.io/ipfs/bafybeibcc32x2jq3ktmk4epvugprux2ehrsx2ukzqbn5gxffvudztc6ile/$f" | sha256sum
done
```

Compare with `alms_trilogy/hashes.json`:

```text
andy.jpg    0xfb4521ae28e166ee9442c20e68ea38e2f9dc51d40a68fbfcdf2c0d8e773ea821
gary.jpg    0x603a559a8da229d90c731a8be517f408471e1f72b095fa4361a93ddeba56060c
allison.jpg 0xe7eb95287af70d21676a43c395881e6477968fccfd35fd46b0774c5c0281f4de
```

## Integrity chain

```text
Git commit 62bf6450357f8edb2d4494140ca294cf073b0708 → verifier script → IPFS directory CID → per-file SHA256s → EAS pending
```

No ghost anchors. No "trust me" steps.
