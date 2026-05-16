from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class EphemeralCIRuntimeReceipt(BaseModel):
    """Minimal receipt proving ephemeral runtime convergence in CI."""

    receipt_version: Literal["witness_ci_runtime_receipt_v0.1"] = "witness_ci_runtime_receipt_v0.1"
    receipt_type: Literal["EPHEMERAL_CI_RUNTIME_RECEIPT"] = "EPHEMERAL_CI_RUNTIME_RECEIPT"
    status: Literal["CONVERGED_BY_CI"] = "CONVERGED_BY_CI"
    render_status: Literal["OPTIONAL_HOSTING_LAYER"] = "OPTIONAL_HOSTING_LAYER"

    timestamp: datetime
    repo: Literal["jsonwisdom/AL"]
    branch: Literal["project/witness-v0.4-runtime"]
    commit_sha: str = Field(..., min_length=7, max_length=40)
    workflow_name: Literal["Witness v0.4 Project Runtime Check"]
    workflow_run: str | int
    workflow_attempt: str | int

    runtime: Literal["uvicorn"] = "uvicorn"
    runtime_mode: Literal["EPHEMERAL_CI_RUNTIME"] = "EPHEMERAL_CI_RUNTIME"
    project_root: Literal["projects/witness-v0.4-runtime"] = "projects/witness-v0.4-runtime"
    checks: list[str]
    claim_boundary: str

    model_config = ConfigDict(extra="forbid", frozen=True)

    def proves_runtime_convergence(self) -> bool:
        required = {
            "pip_install",
            "py_compile",
            "uvicorn_boot",
            "health_endpoint",
            "summarize_endpoint",
            "convergence_receipt_endpoint",
        }
        return required.issubset(set(self.checks))


PrimaryRuntimeReceipt = EphemeralCIRuntimeReceipt
