"""Tests for Kiln's deterministic factory control-plane gates."""
from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from factory.control_plane import (  # noqa: E402
    init_run,
    record,
    validate_run,
)


class ControlPlaneTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)

    def test_stage_order_is_enforced(self) -> None:
        run = init_run("demo requirement", "WO-TEST-001")
        artifact = ROOT / "factory" / "artifacts" / "tablekeeper-plan.md"
        self.assertRaises(SystemExit, record, run, "builder", "passed", str(artifact.relative_to(ROOT)))

    def test_valid_verifier_artifact_can_prove_run(self) -> None:
        run = init_run("demo requirement", "WO-TEST-001")
        plan = str((ROOT / "factory" / "artifacts" / "tablekeeper-plan.md").relative_to(ROOT))
        invariants = str((ROOT / "factory" / "schemas" / "invariants.tablekeeper.json").relative_to(ROOT))
        verification = str((ROOT / "factory" / "runs" / "tablekeeper-local-verification.json").relative_to(ROOT))

        record(run, "architect", "passed", plan)
        record(run, "modeler", "passed", invariants)
        record(run, "builder", "passed", plan)
        record(run, "adversary", "passed", verification)
        record(run, "verifier", "passed", verification)

        self.assertEqual(run["status"], "proved")
        validate_run(run)

    def test_malformed_stage_shape_is_rejected(self) -> None:
        run = init_run("demo requirement", "WO-TEST-001")
        run["stages"][0].pop("attempt")
        self.assertRaises(SystemExit, validate_run, run)


if __name__ == "__main__":
    unittest.main()
