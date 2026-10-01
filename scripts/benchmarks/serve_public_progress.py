#!/usr/bin/env python3
"""Local, read-only progress page for the full public MultiPL-E run."""

from __future__ import annotations

import argparse
import gzip
import json
import subprocess
from datetime import datetime, timezone
from functools import partial
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from scripts.benchmarks.execute_public_suite import FULL_COUNTS


RUN_ORDER = ("js", "ts", "rs", "py", "java", "go")
LABELS = {
    "js": "JavaScript", "ts": "TypeScript", "rs": "Rust",
    "py": "Python", "java": "Java", "go": "Go",
}
SIDES = ("candidate", "upstream")


def controller_alive(pid: int, run_prefix: str) -> bool:
    result = subprocess.run(
        ["ps", "-p", str(pid), "-o", "command="],
        capture_output=True, text=True, check=False,
    )
    return (
        result.returncode == 0
        and "scripts.benchmarks.execute_public_suite" in result.stdout
        and run_prefix in result.stdout
    )


def summarize(root: Path, run_prefix: str, alive: bool) -> dict:
    lanes = []
    generated_total = verified_total = passed_total = 0
    expected_total = 2 * sum(FULL_COUNTS[lang] for lang in RUN_ORDER)
    current_stage = None
    latest_activity = None
    warnings = []
    for language in RUN_ORDER:
        expected = FULL_COUNTS[language]
        sides = {}
        for side in SIDES:
            path = root / f"{run_prefix}-{side}-{language}"
            raw_count = len(list((path / "raw").glob("*.json")))
            completion_count = len(list((path / "completions").glob("*.json.gz")))
            verified_files = list((path / "verified").glob("*.results.json.gz"))
            verified_count = passed_count = 0
            for result_file in verified_files:
                try:
                    with gzip.open(result_file, "rt") as stream:
                        result = json.load(stream)
                    entries = result.get("results")
                    if (
                        result.get("name") != result_file.name.removesuffix(".results.json.gz")
                        or not isinstance(entries, list) or len(entries) != 1
                        or not isinstance(entries[0].get("status"), str)
                    ):
                        raise ValueError("malformed verifier result")
                except (OSError, EOFError, ValueError, TypeError, KeyError):
                    continue  # A verifier file may still be in the middle of a write.
                verified_count += 1
                passed_count += entries[0]["status"] == "OK"
            generated = min(raw_count, completion_count)
            if raw_count != completion_count:
                warnings.append(f"{LABELS[language]} {side}: generation files disagree")
            if max(raw_count, completion_count, len(verified_files)) > expected:
                warnings.append(f"{LABELS[language]} {side}: unexpected extra files")
            if len(verified_files) == expected and verified_count != expected:
                warnings.append(f"{LABELS[language]} {side}: unreadable verifier output")
            manifest_path = path / "manifest.json"
            sealed = False
            if manifest_path.is_file():
                try:
                    manifest = json.loads(manifest_path.read_text())
                    sealed = (
                        manifest.get("status") == "completed"
                        and manifest.get("task_count") == expected
                        and bool(manifest.get("manifest_sha256"))
                    )
                except (OSError, ValueError, TypeError):
                    warnings.append(f"{LABELS[language]} {side}: unreadable manifest")
            if generated == expected and not sealed:
                warnings.append(f"{LABELS[language]} {side}: generation seal pending")
            for activity_file in (
                path / "generation-controller.log",
                path / "verification-controller.log",
            ):
                if activity_file.is_file():
                    timestamp = activity_file.stat().st_mtime
                    latest_activity = max(latest_activity or timestamp, timestamp)
            sides[side] = {
                "generated": min(generated, expected),
                "verified": min(verified_count, expected),
                "passed": passed_count if verified_count else None,
                "pass_count_final": sealed and verified_count == expected,
                "expected": expected,
                "generation_sealed": sealed,
            }
            generated_total += min(generated, expected)
            verified_total += min(verified_count, expected)
            passed_total += passed_count
            if current_stage is None and verified_count < expected:
                verb = "Generating" if generated < expected else "Verifying"
                current_stage = f"{verb} {LABELS[language]} · {side}"
        lanes.append({"language": language, "label": LABELS[language], "sides": sides})
    if verified_total == expected_total and not warnings:
        status = "complete"
        current_stage = "All verifier outputs present; final scoring pending"
    elif alive:
        status = "running"
    else:
        status = "stopped"
        if current_stage:
            current_stage = f"Controller stopped · {current_stage}"
    return {
        "status": status,
        "current_stage": current_stage,
        "generated": generated_total,
        "verified": verified_total,
        "passed": passed_total,
        "expected": expected_total,
        "lanes": lanes,
        "warnings": warnings,
        "last_activity_utc": (
            datetime.fromtimestamp(latest_activity, timezone.utc).isoformat()
            if latest_activity is not None else None
        ),
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
    }


HTML = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ganesh Mini · benchmark tracker</title>
<style>
:root{color-scheme:dark;font-family:ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
*{box-sizing:border-box}body{margin:0;background:#0b1020;color:#e9edf8}main{max-width:1120px;margin:auto;padding:32px 22px 64px}
.eyebrow{color:#91a3c7;text-transform:uppercase;letter-spacing:.13em;font-size:.76rem;font-weight:700}
h1{font-size:clamp(2rem,4vw,3.1rem);margin:10px 0 5px;letter-spacing:-.04em}p{color:#a9b6d0;line-height:1.55}
.top{display:flex;justify-content:space-between;gap:16px;align-items:flex-start}.badge{padding:8px 13px;border-radius:999px;background:#21385e;color:#b8d8ff;font-weight:700;white-space:nowrap}
.badge.complete{background:#174738;color:#b8f4d5}.badge.stopped{background:#533126;color:#ffd0b8}
.metrics{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:28px 0}.metric,.lane{background:#141d33;border:1px solid #273451;border-radius:16px;padding:20px}
.metric .number{font-size:2rem;font-weight:750;letter-spacing:-.04em}.sub{color:#9aaac8;font-size:.86rem}
.bar{height:9px;background:#29354d;border-radius:20px;overflow:hidden;margin:12px 0 4px}.fill{height:100%;background:linear-gradient(90deg,#53a8ff,#83ddff);transition:width .3s}.fill.verified{background:linear-gradient(90deg,#35ba8a,#85e7b3)}
.toolbar{display:flex;align-items:center;justify-content:space-between;gap:12px;margin:28px 0 14px}button{background:#3c78ef;color:white;border:0;border-radius:10px;padding:10px 16px;font:inherit;font-weight:700;cursor:pointer}button:hover{background:#5690ff}
.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}.lane h3{margin:0 0 16px}.side{margin-top:13px}.side-head{display:flex;justify-content:space-between;gap:12px;font-size:.91rem}.side-head span:last-child{color:#bdc9df}
.meta{margin-top:23px;font-size:.85rem;color:#8799ba}.warn{color:#ffc58f}.foot{margin-top:28px;border-top:1px solid #273451;padding-top:14px}
@media(max-width:680px){.top{display:block}.badge{display:inline-block;margin-top:10px}.metrics,.grid{grid-template-columns:1fr}}
</style></head><body><main>
<div class="top"><div><div class="eyebrow">Local public assessment · MultiPL-E HumanEval</div><h1>Ganesh Mini benchmark</h1><p id="stage">Connecting to the local tracker…</p></div><span id="status" class="badge">Checking</span></div>
<div class="metrics"><div class="metric"><div class="sub">Generated outputs</div><div class="number" id="generated">—</div><div class="bar"><div id="generated-bar" class="fill"></div></div><div class="sub" id="generated-percent">—</div></div><div class="metric"><div class="sub">Correctness tests executed</div><div class="number" id="verified">—</div><div class="bar"><div id="verified-bar" class="fill verified"></div></div><div class="sub" id="verified-percent">—</div></div><div class="metric"><div class="sub">Passed tests so far</div><div class="number" id="passed">—</div><div class="sub">Verifier status <code>OK</code> · provisional until final scoring</div></div></div>
<div class="toolbar"><div><strong>Language progress</strong><div class="sub">Candidate and pinned upstream · full public task set</div></div><button id="refresh">Refresh now</button></div>
<div id="lanes" class="grid"></div><p class="meta" id="meta"></p><p class="warn" id="warnings"></p>
<p class="foot">“Tests executed” does not mean correct. “Passed” counts only verifier results with status <code>OK</code>. Live counts are provisional; final paired scores require sealed evidence. This page is available only on this computer.</p>
</main><script>
const $=id=>document.getElementById(id);
const pct=(n,d)=>d?Math.min(100,Math.round(n*100/d)):0;
function side(label,value){const generated=pct(value.generated,value.expected),verified=pct(value.verified,value.expected),passes=value.passed===null?'—':value.passed+'/'+value.verified;return `<div class="side"><div class="side-head"><strong>${label}</strong><span>${value.generated}/${value.expected} generated · ${value.verified}/${value.expected} tested</span></div><div class="sub">Passed: ${passes}${value.pass_count_final?' · batch complete':value.passed===null?'':' · provisional'}</div><div class="bar"><div class="fill" style="width:${generated}%"></div></div><div class="bar"><div class="fill verified" style="width:${verified}%"></div></div></div>`}
async function refresh(){try{const response=await fetch('/api/status',{cache:'no-store'});if(!response.ok)throw new Error('HTTP '+response.status);const data=await response.json();$('stage').textContent=data.current_stage||'Waiting for run output';$('status').textContent=data.status.toUpperCase();$('status').className='badge '+data.status;$('generated').textContent=`${data.generated.toLocaleString()} / ${data.expected.toLocaleString()}`;$('verified').textContent=`${data.verified.toLocaleString()} / ${data.expected.toLocaleString()}`;$('passed').textContent=`${data.passed.toLocaleString()} / ${data.verified.toLocaleString()}`;$('generated-bar').style.width=pct(data.generated,data.expected)+'%';$('verified-bar').style.width=pct(data.verified,data.expected)+'%';$('generated-percent').textContent=pct(data.generated,data.expected)+'% of model-task outputs';$('verified-percent').textContent=pct(data.verified,data.expected)+'% of model-task executions';$('lanes').innerHTML=data.lanes.map(lane=>`<section class="lane"><h3>${lane.label}</h3>${side('Ganesh Mini',lane.sides.candidate)}${side('Qwen upstream',lane.sides.upstream)}</section>`).join('');$('meta').textContent='Checked '+new Date(data.checked_at_utc).toLocaleString()+(data.last_activity_utc?' · Last run activity '+new Date(data.last_activity_utc).toLocaleString():'');$('warnings').textContent=data.warnings.join(' · ');}catch(error){$('stage').textContent='Tracker unavailable: '+error.message;$('status').textContent='OFFLINE';$('status').className='badge stopped'}}
$('refresh').addEventListener('click',refresh);refresh();setInterval(refresh,5000);
</script></body></html>"""


class Handler(BaseHTTPRequestHandler):
    def __init__(self, *args, root: Path, run_prefix: str, controller_pid: int, **kwargs):
        self.root = root
        self.run_prefix = run_prefix
        self.controller_pid = controller_pid
        super().__init__(*args, **kwargs)

    def do_GET(self) -> None:
        if self.path == "/":
            body = HTML.encode("utf-8")
            content_type = "text/html; charset=utf-8"
        elif self.path == "/api/status":
            data = summarize(
                self.root, self.run_prefix,
                controller_alive(self.controller_pid, self.run_prefix),
            )
            body = json.dumps(data, separators=(",", ":")).encode("utf-8")
            content_type = "application/json; charset=utf-8"
        else:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--run-prefix", required=True)
    parser.add_argument("--controller-pid", type=int, required=True)
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    if args.controller_pid <= 0 or not (1024 <= args.port <= 65535):
        parser.error("invalid PID or port")
    handler = partial(
        Handler, root=args.root.resolve(), run_prefix=args.run_prefix,
        controller_pid=args.controller_pid,
    )
    server = ThreadingHTTPServer(("127.0.0.1", args.port), handler)
    print(f"Tracker: http://127.0.0.1:{args.port}/", flush=True)
    try:
        server.serve_forever(poll_interval=0.5)
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
