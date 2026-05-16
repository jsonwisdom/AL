import json
from pathlib import Path

from .models import PrimaryRuntimeReceipt


def load_ci_runtime_receipt(
    path: str | Path = "ci-runtime-receipt.json",
    github_artifact_dir: str | Path | None = None,
) -> PrimaryRuntimeReceipt | None:
    """Load and validate CI runtime receipt using priority ordering."""

    paths_to_try: list[Path] = [Path(path)]

    if github_artifact_dir:
        paths_to_try.append(Path(github_artifact_dir) / "ci-runtime-receipt.json")

    for receipt_path in paths_to_try:
        try:
            if not receipt_path.exists():
                continue

            data = json.loads(receipt_path.read_text(encoding="utf-8"))
            receipt = PrimaryRuntimeReceipt.model_validate(data)

            if not receipt.proves_runtime_convergence():
                print(
                    f"⚠️ Receipt failed convergence proof checks: {receipt.commit_sha[:12]}"
                )
                continue

            print(
                f"✅ CI Runtime Receipt loaded: "
                f"{receipt.commit_sha[:12]} on "
                f"{receipt.branch} ({receipt.status})"
            )

            return receipt

        except Exception as exc:
            print(f"⚠️ Failed to load receipt from {receipt_path}: {exc}")

    print("⚠️ No valid CI Runtime Receipt found.")
    return None
