#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "Minnesota/automation/migrate_minnesota_v1.py"
POLICY = REPO_ROOT / "Minnesota/MIGRATION_POLICY_V1.json"


def run(cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=True)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class MinnesotaMigrationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        run(self.root, "git", "init", "-b", "test-migration")
        run(self.root, "git", "config", "user.name", "Migration Test")
        run(self.root, "git", "config", "user.email", "migration-test@example.invalid")

        (self.root / "Minnesota/automation").mkdir(parents=True)
        shutil.copy2(SCRIPT, self.root / "Minnesota/automation/migrate_minnesota_v1.py")
        shutil.copy2(POLICY, self.root / "Minnesota/MIGRATION_POLICY_V1.json")

        (self.root / "projects/mn-fiscal-replay").mkdir(parents=True)
        (self.root / "projects/mn-fiscal-replay/worker.py").write_text(
            'SOURCE = "_truth/mn/evidence.txt"\n', encoding="utf-8"
        )
        (self.root / "_truth/mn").mkdir(parents=True)
        self.evidence = self.root / "_truth/mn/evidence.txt"
        self.evidence.write_bytes(b"Minnesota evidence bytes\x00must remain exact\n")
        self.before_hash = digest(self.evidence)

        (self.root / "README.md").write_text(
            "Run projects/mn-fiscal-replay/worker.py\n", encoding="utf-8"
        )
        (self.root / "possible-record.txt").write_text(
            "A Minnesota reference requiring human classification.\n", encoding="utf-8"
        )

        run(self.root, "git", "add", "-A")
        run(self.root, "git", "commit", "-m", "fixture")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_dry_run_then_verified_apply(self) -> None:
        plan_path = self.root / "dry-run.json"
        run(
            self.root,
            "python3",
            "Minnesota/automation/migrate_minnesota_v1.py",
            "--mode",
            "dry-run",
            "--run-id",
            "test-dry-run",
            "--output",
            str(plan_path),
        )
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        self.assertEqual(plan["status"], "DRY_RUN_COMPLETE")
        self.assertGreaterEqual(plan["move_count"], 2)
        self.assertIn(
            "possible-record.txt",
            {item["path"] for item in plan["review_queue"]},
        )
        self.assertTrue(self.evidence.exists(), "dry-run must not move evidence")
        self.assertFalse((self.root / "Minnesota/_truth/mn/evidence.txt").exists())

        run(
            self.root,
            "python3",
            "Minnesota/automation/migrate_minnesota_v1.py",
            "--mode",
            "apply",
            "--confirm",
            "MOVE_MINNESOTA_WITH_RECEIPTS",
            "--run-id",
            "test-apply",
        )

        moved_evidence = self.root / "Minnesota/_truth/mn/evidence.txt"
        moved_worker = self.root / "Minnesota/projects/mn-fiscal-replay/worker.py"
        self.assertTrue(moved_evidence.exists())
        self.assertTrue(moved_worker.exists())
        self.assertFalse(self.evidence.exists())
        self.assertEqual(digest(moved_evidence), self.before_hash)
        self.assertTrue((self.root / "possible-record.txt").exists())
        self.assertIn(
            "Minnesota/projects/mn-fiscal-replay/worker.py",
            (self.root / "README.md").read_text(encoding="utf-8"),
        )

        receipt = json.loads(
            (self.root / "Minnesota/receipts/migration/latest.json").read_text(encoding="utf-8")
        )
        self.assertEqual(receipt["status"], "APPLY_VERIFIED")
        self.assertEqual(receipt["conflict_count"], 0)
        self.assertTrue(
            (self.root / "Minnesota/manifests/MN_CORPUS_MANIFEST_V1.json").exists()
        )

    def test_apply_requires_exact_phrase(self) -> None:
        result = subprocess.run(
            [
                "python3",
                "Minnesota/automation/migrate_minnesota_v1.py",
                "--mode",
                "apply",
                "--confirm",
                "yes",
            ],
            cwd=self.root,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("exact confirmation phrase", result.stderr + result.stdout)
        self.assertTrue(self.evidence.exists())


if __name__ == "__main__":
    unittest.main()
