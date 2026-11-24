#!/usr/bin/env python3
"""CI-FIRST synthetic Merkle/MMR reproducibility gate; stdlib, no cloud I/O."""
import hashlib
import json

H = lambda data: hashlib.sha256(data).digest()
J = lambda data: json.dumps(data, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()
LEAF = lambda data: H(b'\x00' + data)
NODE = lambda left, right: H(b'\x01' + left + right)

def commitment(count, peaks):
    header = b'\x02' + count.to_bytes(8, 'big') + len(peaks).to_bytes(4, 'big')
    return H(header + b''.join(start.to_bytes(8, 'big') + height.to_bytes(2, 'big') + digest
                               for start, height, digest in peaks))

def recursive_root(nodes):
    if len(nodes) == 1:
        return nodes[0]
    midpoint = len(nodes) // 2
    return NODE(recursive_root(nodes[:midpoint]), recursive_root(nodes[midpoint:]))

def append(peaks, index, digest):
    peaks = list(peaks)
    start, height = index, 0
    while peaks and peaks[-1][1] == height:
        left_start, _, left = peaks.pop()
        digest = NODE(left, digest)
        start, height = left_start, height + 1
    peaks.append((start, height, digest))
    return peaks

def path(nodes, index):
    if len(nodes) == 1:
        return []
    midpoint = len(nodes) // 2
    if index < midpoint:
        return path(nodes[:midpoint], index) + [('right', recursive_root(nodes[midpoint:]))]
    return path(nodes[midpoint:], index - midpoint) + [('left', recursive_root(nodes[:midpoint]))]

def proof_valid(blob, index, peaks, count, expected):
    if not (0 <= index < count) or commitment(count, peaks) != expected:
        return False
    peak = next((p for p in peaks if p[0] <= index < p[0] + (1 << p[1])), None)
    if peak is None:
        return False
    start, height, top = peak
    siblings = path(LEAVES[start:start + (1 << height)], index - start)
    digest = LEAF(blob)
    for side, sibling in siblings:
        digest = NODE(digest, sibling) if side == 'right' else NODE(sibling, digest)
    return digest == top

raw = []
previous = None
for i in range(8):
    receipt = {'schema': 'cw-synthetic-receipt-v1', 'sequence': i,
               'receipt_id': f'CW-TEST-{i:04d}',
               'evidence_sha256': H(f'synthetic-evidence-{i}\n'.encode()).hex(),
               'previous_receipt_hash': previous,
               'gate': 'PASS' if i % 3 == 0 else 'HOLD',
               'authority_created': False, 'synthetic': True}
    blob = J(receipt)
    raw.append(blob)
    previous = H(blob).hex()
LEAVES = [LEAF(blob) for blob in raw]
snapshots = []
peaks = []
for index, digest in enumerate(LEAVES):
    peaks = append(peaks, index, digest)
    snapshots.append(peaks)

checks = {}
def check(name, predicate):
    checks[name] = bool(predicate)

for n, current in enumerate(snapshots, 1):
    heights = [height for _, height, _ in current]
    expected_heights = [i for i in range(n.bit_length() - 1, -1, -1) if n & (1 << i)]
    check(f'popcount_peaks_{n}', heights == expected_heights)
for i, blob in enumerate(raw):
    check(f'inclusion_{i}', proof_valid(blob, i, peaks, 8, commitment(8, peaks)))
    check(f'tamper_rejected_{i}', not proof_valid(blob + b'X', i, peaks, 8, commitment(8, peaks)))
check('reject_wrong_index', not proof_valid(raw[0], 9, peaks, 8, commitment(8, peaks)))
check('merkle_root4', recursive_root(LEAVES[:4]).hex() ==
      'ea66945b63387fa29ae2b3aecb7c26e9b3022c96b7c6166abfc8296fa9fbc6f1')
check('merkle_root8', recursive_root(LEAVES).hex() ==
      '76a99074098e1855bc0c3fa729f532446c0780bc4df219b59f6624de7fb13011')
check('mmr_commit4', commitment(4, snapshots[3]).hex() ==
      '08a42bee190c48af332c6ffc9cfd267965f94bde2cfb6f3cb01e8bbf2204c846')
check('mmr_commit8', commitment(8, snapshots[7]).hex() ==
      '980c91865b229080230031ed86b61c28bffa4540bc1bdb6a2b8d391e12acf7ae')
extended = snapshots[3]
for index in range(4, 8):
    extended = append(extended, index, LEAVES[index])
check('full_suffix_extension', commitment(8, extended) == commitment(8, snapshots[7]))
altered = append(snapshots[3], 4, LEAF(raw[4] + b'altered'))
for index in range(5, 8):
    altered = append(altered, index, LEAVES[index])
check('reject_altered_suffix', commitment(8, altered) != commitment(8, snapshots[7]))
check('ordered_receipt_chain', all(json.loads(raw[i])['previous_receipt_hash'] == H(raw[i-1]).hex()
                                   for i in range(1, 8)))
out = {'schema': 'cw-ci-first-github-offline-v1', 'synthetic_receipts': 8,
       'tests': len(checks), 'passed': sum(checks.values()),
       'failures': [name for name, passed in checks.items() if not passed],
       'root4': recursive_root(LEAVES[:4]).hex(), 'root8': recursive_root(LEAVES).hex(),
       'mmr4': commitment(4, snapshots[3]).hex(), 'mmr8': commitment(8, snapshots[7]).hex(),
       'general_compact_consistency_proof': 'NOT_RUN',
       'cloudflare_r2_local': 'NOT_RUN', 'production_ledger': 'HOLD',
       'deployment': False, 'production_write': False, 'external_anchor': False}
print(json.dumps(out, sort_keys=True, indent=2))
if out['failures']:
    raise SystemExit(1)
