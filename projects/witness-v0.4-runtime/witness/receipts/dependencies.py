from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from .loader import load_ci_runtime_receipt
from .models import PrimaryRuntimeReceipt


@lru_cache(maxsize=1)
def get_primary_runtime_receipt() -> PrimaryRuntimeReceipt | None:
    """Return the highest-priority valid runtime receipt available locally.

    Current priority:
    1. EPHEMERAL_CI_RUNTIME_RECEIPT from ci-runtime-receipt.json
    2. Future Render/live-hosting receipt path
    3. None
    """
    return load_ci_runtime_receipt()


def get_runtime_evidence_state() -> dict:
    """Expose runtime evidence without over-claiming persistence or hosting."""
    receipt = get_primary_runtime_receipt()

    if receipt is None:
        return {
            "runtime_converged": False,
            "evidence_path": None,
            "render_blocking": False,
            "claim_boundary": "No valid runtime receipt found. No runtime legitimacy claim.",
        }

    return {
        "runtime_converged": True,
        "evidence_path": receipt.receipt_type,
        "render_blocking": False,
        "repo": receipt.repo,
        "branch": receipt.branch,
        "commit_sha": receipt.commit_sha,
        "workflow_run": str(receipt.workflow_run),
        "runtime_mode": receipt.runtime_mode,
        "claim_boundary": receipt.claim_boundary,
    }


RuntimeEvidence = Annotated[dict, Depends(get_runtime_evidence_state)]
