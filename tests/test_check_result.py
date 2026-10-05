"""Contract tests for the bundled CLI-result checker; no OpenScreen needed."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "skills/openscreen-cli/scripts/check-result.py"


class ResultContractTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.stdout = self.root / "stdout.jsonl"

    def check(self, command, lines, artifact=None, code=0):
        self.stdout.write_text("\n".join(json.dumps(x) for x in lines) + "\n")
        args = [sys.executable, str(SCRIPT), "--command", command, "--exit-code", str(code), "--input", str(self.stdout)]
        if artifact:
            args += ["--artifact", str(artifact)]
        return subprocess.run(args, text=True, capture_output=True, check=False)

    def test_export_checks_existing_artifact_and_path(self):
        artifact = self.root / "output.mp4"
        artifact.write_bytes(b"sample")
        done = {"event": "done", "success": True, "outputPath": str(artifact)}
        self.assertEqual(self.check("export", [done], artifact).returncode, 0)
        self.assertNotEqual(self.check("export", [done], self.root / "missing.mp4").returncode, 0)

    def test_nonzero_cli_exit_is_failure_even_with_done(self):
        result = self.check("sources", [{"event": "done", "success": True, "sources": []}], code=1)
        self.assertNotEqual(result.returncode, 0)

    def test_error_event_rejected_even_if_final_done(self):
        result = self.check("sources", [{"event": "error"}, {"event": "done", "success": True, "sources": []}])
        self.assertNotEqual(result.returncode, 0)

    def test_info_requires_video_existence(self):
        summary = {"projectPath": str(self.root / "p.openscreen"), "screenVideoExists": True}
        self.assertEqual(self.check("info", [summary]).returncode, 0)
        self.assertNotEqual(self.check("info", [{**summary, "screenVideoExists": False}]).returncode, 0)

    def test_pack_requires_all_listed_files_within_bundle(self):
        bundle = self.root / "bundle"
        bundle.mkdir()
        project = bundle / "p.openscreen"
        project.write_text("{}")
        video = bundle / "v.mp4"
        video.write_bytes(b"sample")
        done = {"event": "done", "success": True, "projectPath": str(project), "files": [str(project), str(video)]}
        self.assertEqual(self.check("pack", [done], bundle).returncode, 0)
        video.unlink()
        self.assertNotEqual(self.check("pack", [done], bundle).returncode, 0)


if __name__ == "__main__":
    unittest.main()
