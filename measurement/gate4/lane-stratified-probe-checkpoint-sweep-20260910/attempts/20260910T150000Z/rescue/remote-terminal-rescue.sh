#!/usr/bin/env bash
set -Eeuo pipefail

evidence=/var/lib/ganesh-mini-checkpoint-sweep
project=executespecv1
bucket=ganesh-gate0-model-transfer-1061994342941
prefix=ganesh-mini-1.0/evaluation/checkpoint-sweep-v1/attempts/20260910T150000Z/rescue-terminal-20260910T150000Z

test "$(cat "$evidence/startup-exit-code.txt")" = "0"
test -f "$evidence/output/campaign-result.json"
test -f "$evidence/output/checkpoint-sweep-result.json"
test -f "$evidence/output/results/tokens-000000389093/tasks/dev-t1-typescript-clamp-window.json"

date -u +%FT%TZ > "$evidence/rescue-captured-at-utc.txt"
uname -a > "$evidence/rescue-uname.txt"
ps -eo pid,ppid,etimes,stat,cmd --sort=pid > "$evidence/rescue-process-tree.txt"
systemctl status google-startup-scripts.service --no-pager -l > "$evidence/rescue-startup-service.txt" 2>&1 || true
journalctl -u google-startup-scripts.service --no-pager > "$evidence/rescue-startup-journal.txt" 2>&1 || true
find "$evidence" -type f -printf '%P\t%s\t%TY-%Tm-%TdT%TH:%TM:%TSZ\n' | sort > "$evidence/rescue-file-inventory.tsv"

(
  cd "$evidence"
  find . -type f ! -name runtime-files.sha256 -print0 | sort -z | xargs -0 sha256sum > runtime-files.sha256
)

timeout --kill-after=30 900 gcloud storage rsync "$evidence" "gs://$bucket/$prefix" --recursive --project="$project"
