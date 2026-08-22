#!/usr/bin/env python3
"""Compile and execute all decision-tranche1 JavaScript/TypeScript references locally."""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from scripts.eval.authoring.build_decision_tranche1 import MANIFEST, ROOT
from scripts.eval.contracts import load_json, sha256_object, validate_task


def check() -> dict[str, object]:
    manifest = load_json(MANIFEST)
    rows: list[dict[str, object]] = []
    tsc = shutil.which("tsc")
    node = shutil.which("node")
    if not node or not tsc:
        raise RuntimeError("native node and tsc are required")
    for entry in manifest["tasks"]:
        if entry["language"] not in {"javascript", "typescript"}:
            continue
        task = validate_task(load_json(ROOT / entry["path"]))
        if sha256_object(task) != entry["sha256"]:
            raise RuntimeError(f"sealed task hash mismatch: {task['task_id']}")
        with tempfile.TemporaryDirectory(prefix="ganesh-mini-decision-t1-") as raw:
            work = Path(raw)
            (work / task["candidate_path"]).write_text(task["validation"]["reference"]["code"], encoding="utf-8")
            for file in task["files"]:
                (work / file["path"]).write_text(file["content"], encoding="utf-8")
            commands = [[node, "solution.test.js"]]
            if task["language"] == "typescript":
                commands = [
                    [tsc, "--strict", "--skipLibCheck", "--module", "commonjs", "--target", "es2022", "solution.ts", "solution.test.ts"],
                    [node, "solution.test.js"],
                ]
            transcripts = []
            for command in commands:
                result = subprocess.run(command, cwd=work, capture_output=True, text=True, timeout=30, check=False)
                transcripts.append({"command": command, "returncode": result.returncode, "stdout": result.stdout, "stderr": result.stderr})
                if result.returncode != 0:
                    raise RuntimeError(json.dumps({"task_id": task["task_id"], "transcript": transcripts}, sort_keys=True))
            rows.append({"task_id": task["task_id"], "language": task["language"], "commands": len(commands), "status": "passed"})
    return {"status": "passed", "task_count": len(rows), "javascript": sum(row["language"] == "javascript" for row in rows), "typescript": sum(row["language"] == "typescript" for row in rows), "results": rows}


if __name__ == "__main__":
    print(json.dumps(check(), sort_keys=True))
