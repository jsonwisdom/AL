# Sovereign Replay Court — Public Law

## Constitutional Invariant

```text
Host_Witness == Chamber_Witness == Registry
```

Execution ≡ Registry.

No witness may bless a root independently.
Consensus exists only when all replay surfaces converge.

## Public Stranger Test

### Host Witness

```bash
git clone https://github.com/jsonwisdom/AL.git
cd AL
chmod +x verify.sh
./verify.sh
```

### Chamber Witness

```bash
docker build -t al-court -f Dockerfile.replay .
docker run --rm al-court
```

## Expected Verdict

```text
REPLAY_CONFIRMED
MATRIX: GREEN
Execution ≡ Registry holds.
```

## Witness Roles

### Host Clerk

The host witness executes against the ambient machine environment.
It introduces real-world entropy and validates environmental reproducibility.

### Chamber Judge

The chamber witness executes inside the replay container.
It validates hermetic replay under pinned execution conditions.

## Registry Roots

### AFP_MINIMAL_001

```text
27e37c8d23fb3e1f841de98731d54241da2825f6bfdc78bc3f7c9b8100eeb812
```

### AFP_NESTED_002

```text
75fe512e17fd630336da1554228b68c1f821066b9b5d0d7b3c078101dabc0c3a
```

## Constitutional Rule

No phantom scripts.
No assumed infrastructure.
No ceremonial green.

Only executable artifacts present on `master` may participate in the public oath.
