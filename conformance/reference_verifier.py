#!/usr/bin/env python3
"""
CBREv1 Reference Verifier — E2-STRICT-CANONICAL

Spec: VERIFIER v1.2+
Opcode table: 0x0001
Dependencies: Python standard library only

Core law:
  The trace executes.
  The stack witnesses.
  The commit binds.
  The verifier compares.
  The SSD has zero execution authority.
"""

from __future__ import annotations

import hashlib
import sys
from typing import Tuple


VERIFIED_TRACE = "VERIFIED_TRACE"

REJECT_INTEGRITY_FAILED = "REJECTED_TRACE | INTEGRITY: FAILED"
REJECT_MULTIPLE_COMMITS = "REJECTED_TRACE | MULTIPLE_COMMITS"
REJECT_NO_COMMIT = "REJECTED_TRACE | NO_COMMIT"
REJECT_NO_END = "REJECTED_TRACE | NO_END"
REJECT_TRAILING_BYTES = "REJECTED_TRACE | TRAILING_BYTES"
REJECT_DIRTY_STACK = "REJECTED_TRACE | DIRTY_STACK"
REJECT_COMMIT_ON_EMPTY_STACK = "REJECTED_TRACE | COMMIT_ON_EMPTY_STACK"
REJECT_MALFORMED_PUSH = "REJECTED_TRACE | MALFORMED_PUSH"
REJECT_INVALID_OPCODE = "REJECTED_TRACE | INVALID_OPCODE"


OP_END = 0x00
OP_PUSH_BYTES = 0x01
OP_HASH_H256 = 0x02
OP_COMMIT_OUTPUT = 0x03


def sha256(data: bytes) -> bytes:
    """Return SHA-256 digest bytes."""
    return hashlib.sha256(data).digest()


def parse_hex(hex_text: str) -> bytes:
    """Parse hex with optional spaces/newlines and optional 0x prefix."""
    cleaned = "".join(hex_text.strip().split())
    if cleaned.startswith("0x") or cleaned.startswith("0X"):
        cleaned = cleaned[2:]
    if len(cleaned) % 2 != 0:
        raise ValueError("hex input has odd length")
    return bytes.fromhex(cleaned)


def verify(trace_bytes: bytes, expected_output_commitment: bytes) -> Tuple[str, str]:
    """
    Verify a CBREv1 trace.

    Initialization contract:
      1. stack: list[bytes] = []
      2. ip: int = 0
      3. committed: bool = False; saw_end: bool = False

    No SSD context. No gas counter. No semantic state. No hidden memory.
    """
    # 1. THE STACK — empty list, bottom-to-top ordering.
    stack: list[bytes] = []

    # 2. THE INSTRUCTION POINTER — integer, starts at 0.
    ip: int = 0

    # 3. THE STATE FLAGS — two booleans, both start False.
    committed: bool = False
    saw_end: bool = False

    while ip < len(trace_bytes):
        op = trace_bytes[ip]

        if op == OP_END:
            saw_end = True
            ip += 1
            if ip != len(trace_bytes):
                return (REJECT_TRAILING_BYTES, "OP_END encountered before final byte")
            break

        if op == OP_PUSH_BYTES:
            if ip + 3 > len(trace_bytes):
                return (REJECT_MALFORMED_PUSH, "OP_PUSH_BYTES missing uint16_be length")

            len_hi = trace_bytes[ip + 1]
            len_lo = trace_bytes[ip + 2]
            length = (len_hi << 8) | len_lo

            if ip + 3 + length > len(trace_bytes):
                return (REJECT_MALFORMED_PUSH, "OP_PUSH_BYTES length exceeds trace boundary")

            data = trace_bytes[ip + 3 : ip + 3 + length]
            stack.append(data)
            ip += 3 + length
            continue

        if op == OP_HASH_H256:
            # Pop all, concat bottom-to-top, push SHA-256.
            concatenated = b"".join(stack)
            stack = [sha256(concatenated)]
            ip += 1
            continue

        if op == OP_COMMIT_OUTPUT:
            if committed:
                return (REJECT_MULTIPLE_COMMITS, "OP_COMMIT_OUTPUT executed more than once")
            if len(stack) == 0:
                return (REJECT_COMMIT_ON_EMPTY_STACK, "OP_COMMIT_OUTPUT with empty stack")

            output = stack.pop()
            if output != expected_output_commitment:
                return (REJECT_INTEGRITY_FAILED, "committed output did not match expected commitment")

            committed = True
            ip += 1
            continue

        return (REJECT_INVALID_OPCODE, f"invalid opcode 0x{op:02x} at offset {ip}")

    if not saw_end:
        return (REJECT_NO_END, "trace ended without OP_END")
    if not committed:
        return (REJECT_NO_COMMIT, "trace ended without OP_COMMIT_OUTPUT")
    if len(stack) != 0:
        return (REJECT_DIRTY_STACK, "stack not empty at OP_END")

    return (VERIFIED_TRACE, "trace verified")


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("Usage: reference_verifier.py <trace_hex> <expected_output_hex>", file=sys.stderr)
        return 2

    try:
        trace_bytes = parse_hex(argv[1])
        expected_output_commitment = parse_hex(argv[2])
    except ValueError as exc:
        print(f"INPUT_ERROR | {exc}", file=sys.stderr)
        return 2

    status, reason = verify(trace_bytes, expected_output_commitment)
    print(status)
    print(reason)
    return 0 if status == VERIFIED_TRACE else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
