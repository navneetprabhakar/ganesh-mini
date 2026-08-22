#!/usr/bin/env python3
"""Compile/execute every tranche-1 reference and reject every known-bad locally."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from scripts.eval.authoring.build_decision_tranche1 import MANIFEST, ROOT
from scripts.eval.contracts import load_json, sha256_object, validate_task


def commands(language: str) -> list[list[str]]:
    configured = {
        "go": [["go", "test", "./..."]],
        "java": [["javac", "Solution.java", "SolutionTest.java"], ["java", "-ea", "SolutionTest"]],
        "javascript": [["node", "solution.test.js"]],
        "typescript": [["tsc", "--strict", "--skipLibCheck", "--module", "commonjs", "--target", "es2022", "solution.ts", "solution.test.ts"], ["node", "solution.test.js"]],
        "python": [[sys.executable, "test_solution.py"]],
        "rust": [["rustc", "--edition=2021", "--test", "solution_test.rs", "-o", "ganesh-tests"], ["./ganesh-tests"]],
    }[language]
    for command in configured:
        if command[0].startswith("./"):
            continue
        resolved = shutil.which(command[0])
        if not resolved:
            raise RuntimeError(f"missing native tool: {command[0]}")
        command[0] = resolved
    return configured


def check() -> dict[str, object]:
    manifest = load_json(MANIFEST)
    rows = []
    for entry in manifest["tasks"]:
        task = validate_task(load_json(ROOT / entry["path"]))
        if sha256_object(task) != entry["sha256"]:
            raise RuntimeError(f"sealed task hash mismatch: {task['task_id']}")
        artifacts = [("reference", task["validation"]["reference"]), ("known_bad", task["validation"]["known_bad"][0])]
        for artifact_name, artifact in artifacts:
            with tempfile.TemporaryDirectory(prefix="ganesh-mini-decision-t1-") as raw:
                work = Path(raw)
                (work / task["candidate_path"]).write_text(artifact["code"], encoding="utf-8")
                for file in task["files"]:
                    (work / file["path"]).write_text(file["content"], encoding="utf-8")
                transcripts = []
                observed_pass = True
                for command in commands(task["language"]):
                    result = subprocess.run(command, cwd=work, capture_output=True, text=True, timeout=task["limits"]["timeout_seconds"], check=False)
                    transcripts.append({"command": command, "returncode": result.returncode, "stdout": result.stdout, "stderr": result.stderr})
                    if result.returncode != 0:
                        observed_pass = False
                        break
                expected_pass = artifact_name == "reference"
                if observed_pass != expected_pass:
                    raise RuntimeError(json.dumps({"task_id": task["task_id"], "artifact": artifact_name, "expected_pass": expected_pass, "observed_pass": observed_pass, "transcript": transcripts}, sort_keys=True))
                rows.append({"task_id": task["task_id"], "language": task["language"], "artifact": artifact_name, "status": "passed"})
    languages = sorted({row["language"] for row in rows})
    return {
        "status": "passed",
        "task_count": manifest["task_count"],
        "execution_count": len(rows),
        "reference_passes": sum(row["artifact"] == "reference" for row in rows),
        "known_bad_rejections": sum(row["artifact"] == "known_bad" for row in rows),
        "counts_by_lane": {language: sum(row["language"] == language for row in rows) for language in languages},
    }


if __name__ == "__main__":
    print(json.dumps(check(), sort_keys=True))
