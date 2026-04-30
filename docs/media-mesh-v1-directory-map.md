# MEDIA_MESH_V1 Directory Map

## Terminal Rule

Run commands from the repository root:

```bash
cd AL
```

Do not run Media Mesh scripts from inside `watchers/media/` unless a command explicitly says to.

## Repository Layout

```txt
AL/
  docs/
    media-mesh-v1-public-verification-guide.md
    media-mesh-ml-boundary-v1.md
    media-mesh-anchor-spec-v1.md
    media-mesh-v1-directory-map.md

  schemas/
    media_source_intake_v1.json

  watchers/
    media/
      watch_media_mesh.sh
      extractor_v1.sh
      drift_engine_v1.sh
      domain_cluster_v1.sh
      break_detector_v1.sh
      merged_receipt_v1.sh
      batch_aggregator_v1.sh
      anchor_publisher_v1.sh
      anchor_verifier_v1.sh
      anchor_verifier_v1_net.sh
      batch_proof_v1.sh
      proof_verifier_v1.sh
      portable_proof_bundle_v1.sh
      bundle_verifier_v1.sh

  examples/
    README.md
    valid_bundle.json
    invalid_bundle_tampered.json
    invalid_bundle_bad_proof.json

  _truth/
    media_mesh/
      intake/
      extractor/
      drift/
      merged/
      batches/
      proofs/
      bundles/
      anchors/
      verify/
```

## Recommended Working Directories

Use `_truth/media_mesh/` for generated runtime artifacts.

```bash
mkdir -p \
  _truth/media_mesh/intake \
  _truth/media_mesh/extractor \
  _truth/media_mesh/drift \
  _truth/media_mesh/merged \
  _truth/media_mesh/batches \
  _truth/media_mesh/proofs \
  _truth/media_mesh/bundles \
  _truth/media_mesh/anchors \
  _truth/media_mesh/verify
```

## First Contact Example Layout

```txt
examples/
  README.md
  valid_bundle.json
  invalid_bundle_tampered.json
  invalid_bundle_bad_proof.json
```

These files are public fixtures. Do not use `_truth/` paths for first-contact examples.

## Canonical Command Forms

### Verify a bundle

```bash
bash watchers/media/bundle_verifier_v1.sh examples/valid_bundle.json
```

### Generate a proof

```bash
bash watchers/media/batch_proof_v1.sh \
  _truth/media_mesh/merged/merged.jsonl \
  0 \
  _truth/media_mesh/batches/batch.json \
  > _truth/media_mesh/proofs/proof_000.json
```

### Verify a proof

```bash
bash watchers/media/proof_verifier_v1.sh _truth/media_mesh/proofs/proof_000.json
```

### Build a portable bundle

```bash
bash watchers/media/portable_proof_bundle_v1.sh \
  _truth/media_mesh/merged/leaf_000.json \
  _truth/media_mesh/proofs/proof_000.json \
  _truth/media_mesh/batches/batch.json \
  _truth/media_mesh/anchors/anchor.json \
  > _truth/media_mesh/bundles/bundle_000.json
```

### Verify a portable bundle

```bash
bash watchers/media/bundle_verifier_v1.sh _truth/media_mesh/bundles/bundle_000.json
```

## Boundary

- `watchers/media/` contains executable verifier machinery.
- `docs/` contains doctrine and public verification instructions.
- `schemas/` contains stable intake schemas.
- `examples/` contains public fixtures only.
- `_truth/media_mesh/` contains generated local run artifacts.

Do not mix generated local artifacts into `watchers/` or `docs/`.
