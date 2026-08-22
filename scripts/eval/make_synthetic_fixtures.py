from __future__ import annotations

from pathlib import Path

from scripts.eval.contracts import LANGUAGE_FAMILY, sha256_text, validate_task, write_json


SPECS = {
    "go": {
        "runtime_id": "go-1.22.12", "candidate_path": "solution.go",
        "reference": "package solution\n\nfunc Add(a, b int) int { return a + b }\n",
        "known_bad": "package solution\n\nfunc Add(a, b int) int { return a - b }\n",
        "files": {
            "go.mod": ("support", "module synthetic.invalid/add\n\ngo 1.22\n"),
            "solution_test.go": ("test", "package solution\n\nimport \"testing\"\n\nfunc TestAdd(t *testing.T) { if Add(2, 3) != 5 { t.Fatal(\"bad sum\") } }\n"),
        },
    },
    "java": {
        "runtime_id": "java-21.0.11", "candidate_path": "Solution.java",
        "reference": "public final class Solution { public static int add(int a, int b) { return a + b; } }\n",
        "known_bad": "public final class Solution { public static int add(int a, int b) { return a - b; } }\n",
        "files": {"SolutionTest.java": ("test", "public final class SolutionTest { public static void main(String[] args) { assert Solution.add(2, 3) == 5; } }\n")},
    },
    "javascript": {
        "runtime_id": "javascript-node-22.23.2", "candidate_path": "solution.js",
        "reference": "exports.add = (a, b) => a + b;\n",
        "known_bad": "exports.add = (a, b) => a - b;\n",
        "files": {"solution.test.js": ("test", "const { add } = require('./solution');\nif (add(2, 3) !== 5) throw new Error('bad sum');\n")},
    },
    "typescript": {
        "runtime_id": "typescript-5.5.4-node-22", "candidate_path": "solution.ts",
        "reference": "export const add = (a: number, b: number): number => a + b;\n",
        "known_bad": "export const add = (a: number, b: number): number => a - b;\n",
        "files": {"solution.test.ts": ("test", "import { add } from './solution';\nif (add(2, 3) !== 5) throw new Error('bad sum');\n")},
    },
    "python": {
        "runtime_id": "python-3.11.15", "candidate_path": "solution.py",
        "reference": "def add(a: int, b: int) -> int:\n    return a + b\n",
        "known_bad": "def add(a: int, b: int) -> int:\n    return a - b\n",
        "files": {"test_solution.py": ("test", "from solution import add\nassert add(2, 3) == 5, 'bad sum'\n")},
    },
    "rust": {
        "runtime_id": "rust-1.85.0", "candidate_path": "solution.rs",
        "reference": "pub fn add(a: i32, b: i32) -> i32 { a + b }\n",
        "known_bad": "pub fn add(a: i32, b: i32) -> i32 { a - b }\n",
        "files": {"solution_test.rs": ("test", "#[path = \"solution.rs\"] mod solution;\n#[test] fn adds() { assert_eq!(solution::add(2, 3), 5); }\n")},
    },
}


def make_task(language: str, spec: dict) -> dict:
    prompt = f"SYNTHETIC HARNESS TEST ONLY ({language}): implement add(a, b)."
    files = [
        {"path": path, "role": role, "content": content, "sha256": sha256_text(content)}
        for path, (role, content) in sorted(spec["files"].items())
    ]
    task = {
        "schema_version": "1.0",
        "task_id": f"synthetic-{language}-add",
        "surface": "synthetic_harness",
        "language": language,
        "family": LANGUAGE_FAMILY[language],
        "task_type": "generation",
        "prompt": {"text": prompt, "sha256": sha256_text(prompt)},
        "rendered_prompt": {"text": prompt, "sha256": sha256_text(prompt)},
        "candidate_path": spec["candidate_path"],
        "files": files,
        "runtime_id": spec["runtime_id"],
        "limits": {"timeout_seconds": 30, "memory_mb": 512, "cpus": 1, "pids": 64, "output_bytes": 65536},
        "validation": {
            "reference": {"label": "synthetic-reference", "code": spec["reference"], "sha256": sha256_text(spec["reference"])},
            "known_bad": [{"label": "synthetic-subtraction-bug", "code": spec["known_bad"], "sha256": sha256_text(spec["known_bad"])}],
        },
    }
    return validate_task(task)


def main() -> int:
    root = Path("eval/fixtures/synthetic_harness")
    for language, spec in SPECS.items():
        write_json(root / f"{language}.task.json", make_task(language, spec))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
