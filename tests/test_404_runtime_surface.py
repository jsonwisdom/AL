import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agents.four04_crawler.proof_blob_surface import AllowedSurface
from agents.four04_crawler.runtime_surface import RUNTIME_ALLOWED_404


def test_404_runtime_surface_is_subset_of_membrane():
    assert RUNTIME_ALLOWED_404.issubset(set(AllowedSurface))


def test_404_runtime_surface_is_strict_subset():
    deferred = {
        AllowedSurface.TOMBSTONED,
        AllowedSurface.MANIFEST_MISMATCH,
        AllowedSurface.REPLAY_FAIL,
    }
    assert RUNTIME_ALLOWED_404.isdisjoint(deferred)
