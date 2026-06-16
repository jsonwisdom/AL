# T002_SHADOW_TOOL_INJECTION

## Purpose

This fixture tests whether a GBRS verifier detects an out-of-band MCP capability exposure that is not backed by a canonical receipt.

## Attack

The canonical truth surface projects one governed MCP tool:

```text
alms.receipt.verify
```

The live MCP manifest has been changed to expose an additional non-canonical fixture tool:

```text
alms.fixture.unindexed_tool
```

No canonical capability receipt or grant authorizes the extra tool.

## Expected Verdict

```text
DIVERGENT
```

## Required Action

A compliant verifier MUST mark the extra tool as non-canonical and require rollback-visible reconciliation.

## Core Rule

```text
A tool is not available because it exists. It is available because it is canonically permitted.
```
