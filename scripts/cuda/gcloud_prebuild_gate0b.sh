#!/usr/bin/env bash
set -Eeuo pipefail

for name in GANESH_GCP_PROJECT GANESH_GCS_BUCKET GANESH_GCS_PREFIX GANESH_WORKSPACE_ARCHIVE_URI GANESH_WORKSPACE_ARCHIVE_SHA256 GANESH_WORKSPACE_ARCHIVE_SIZE GANESH_CUMULATIVE_COST_USD GANESH_BUILDER_HOURLY_USD GANESH_SUPPORT_RESERVE_USD; do
  [[ -n "${!name:-}" ]] || { echo "missing $name" >&2; exit 2; }
done
case "$GANESH_WORKSPACE_ARCHIVE_URI" in *'#'[0-9]*) ;; *) echo "workspace URI must include a GCS generation" >&2; exit 40;; esac
python3 - "$GANESH_CUMULATIVE_COST_USD" "$GANESH_BUILDER_HOURLY_USD" "$GANESH_SUPPORT_RESERVE_USD" <<'PY'
from decimal import Decimal
import sys
total = Decimal(sys.argv[1]) + Decimal(sys.argv[2]) + Decimal(sys.argv[3])
if any(Decimal(value) < 0 for value in sys.argv[1:]) or Decimal(sys.argv[2]) <= 0:
    raise SystemExit("cost inputs must be nonnegative and builder hourly rate positive")
if total >= Decimal("5"): raise SystemExit(f"prebuild cost ceiling is not below USD 5: {total}")
PY

work_dir="/opt/ganesh-mini-prebuild"
evidence_dir="/var/lib/ganesh-mini-prebuild"
artifact_dir="$evidence_dir/artifacts"
bundle_dir="$artifact_dir/docker-bundle"
mkdir -p "$work_dir" "$artifact_dir" "$bundle_dir/debs/partial"
exec > >(tee -a "$evidence_dir/startup.stdout.log") 2> >(tee -a "$evidence_dir/startup.stderr.log" >&2)
started_epoch="$(date +%s)"; hard_deadline_epoch="$((started_epoch + 3600))"; operation_deadline_epoch="$((started_epoch + 3300))"
deadline_epoch="$operation_deadline_epoch"
printf '%s\n' "$deadline_epoch" > "$evidence_dir/prebuild-deadline-epoch.txt"
( sleep 3590; shutdown -h now ) & watchdog_pid="$!"
remaining() { local value=$((operation_deadline_epoch - $(date +%s))); (( value > 0 )) || return 1; printf '%s\n' "$value"; }
backup_remaining() { local value=$((hard_deadline_epoch - 20 - $(date +%s))); (( value > 0 )) || return 1; printf '%s\n' "$value"; }
inventory_remaining() { local value=$((hard_deadline_epoch - 240 - $(date +%s))); (( value > 0 )) || return 1; printf '%s\n' "$value"; }
phase_timeout() { local cap="$1" left; left="$(remaining)" || return 1; (( left < cap )) && printf '%s\n' "$left" || printf '%s\n' "$cap"; }
checkpoint() {
  local stamp; stamp="$(date -u +%Y%m%dT%H%M%S%NZ)-$$-$RANDOM"
  timeout 300s gcloud storage rsync "$evidence_dir" "gs://$GANESH_GCS_BUCKET/$GANESH_GCS_PREFIX/prebuild-checkpoints/$stamp" --recursive --project="$GANESH_GCP_PROJECT" >> "$evidence_dir/gcs-backup.log" 2>&1 || true
}
final_backup() {
  timeout "$(backup_remaining)" gcloud storage rsync "$evidence_dir" "gs://$GANESH_GCS_BUCKET/$GANESH_GCS_PREFIX/prebuild-terminal" --recursive --project="$GANESH_GCP_PROJECT" > /var/log/ganesh-prebuild-final-backup.log 2>&1
}
inventory_attempted=0
write_inventory() {
  inventory_attempted=1
  local budget; budget="$(inventory_remaining)" || return 1
  timeout "$budget" bash -c 'set -o pipefail; cd "$1"; find . -type f ! -name runtime-files.sha256 ! -name .runtime-files.sha256.tmp -print0 | sort -z | xargs -0 sha256sum > .runtime-files.sha256.tmp && mv .runtime-files.sha256.tmp runtime-files.sha256' _ "$evidence_dir"
}
finish() { local status="$?"; trap - EXIT; printf '%s\n' "$status" > "$evidence_dir/startup-exit-code.txt"; if (( inventory_attempted == 0 )) && ! write_inventory; then rm -f "$evidence_dir/.runtime-files.sha256.tmp"; printf 'terminal inventory failed\n' > "$evidence_dir/terminal-inventory-failure.txt"; status=91; fi; final_backup || status=90; kill "$watchdog_pid" 2>/dev/null || true; exit "$status"; }
trap finish EXIT

timeout "$(phase_timeout 600)" gcloud storage cp "$GANESH_WORKSPACE_ARCHIVE_URI" "$work_dir/workspace.tar.gz" --project="$GANESH_GCP_PROJECT"
[[ "$(stat -c %s "$work_dir/workspace.tar.gz")" == "$GANESH_WORKSPACE_ARCHIVE_SIZE" ]]
printf '%s  %s\n' "$GANESH_WORKSPACE_ARCHIVE_SHA256" "$work_dir/workspace.tar.gz" | sha256sum -c -
mkdir "$work_dir/workspace"
timeout "$(phase_timeout 180)" tar -xzf "$work_dir/workspace.tar.gz" -C "$work_dir/workspace"
timeout "$(phase_timeout 30)" bash -c "set -o pipefail; dpkg-query -W -f='\${Package}\\t\${Version}\\n' | sort" > "$bundle_dir/base-dpkg-packages.tsv"
timeout "$(phase_timeout 10)" uname -a > "$evidence_dir/uname.txt"
docker_package_version="29.1.3-0ubuntu3~22.04.2"
timeout "$(phase_timeout 300)" apt-get update > "$evidence_dir/apt-update.log" 2>&1
apt-cache policy docker.io > "$evidence_dir/docker-apt-policy.txt"
grep -Fq "$docker_package_version" "$evidence_dir/docker-apt-policy.txt"
DEBIAN_FRONTEND=noninteractive timeout "$(phase_timeout 600)" apt-get -o "Dir::Cache::archives=$bundle_dir/debs" install --download-only -y --no-install-recommends "docker.io=$docker_package_version" zstd > "$evidence_dir/docker-download.log" 2>&1
find "$bundle_dir/debs" -maxdepth 1 -name '*.deb' -print -quit | grep -q .
(cd "$bundle_dir" && find . -type f ! -name bundle-files.sha256 -print0 | sort -z | xargs -0 sha256sum > bundle-files.sha256)
DEBIAN_FRONTEND=noninteractive timeout "$(phase_timeout 600)" apt-get install -y --no-install-recommends "docker.io=$docker_package_version" zstd > "$evidence_dir/docker-install.log" 2>&1
timeout "$(phase_timeout 30)" bash -c "set -o pipefail; dpkg-query -W -f='\${Package}\\t\${Version}\\n' | sort" > "$evidence_dir/builder-dpkg-packages.tsv"
timeout "$(phase_timeout 30)" docker version > "$evidence_dir/docker-version.txt" 2>&1
chmod +x "$work_dir/workspace/scripts/cuda/prebuild_cuda_image.sh"
GANESH_PREBUILD_DEADLINE_EPOCH="$deadline_epoch" "$work_dir/workspace/scripts/cuda/prebuild_cuda_image.sh" "$work_dir/workspace" "$artifact_dir"
timeout "$(remaining)" tar -czf "$artifact_dir/docker-bundle.tar.gz" -C "$artifact_dir" docker-bundle
timeout "$(remaining)" sha256sum "$artifact_dir/docker-bundle.tar.gz" > "$artifact_dir/docker-bundle.tar.gz.sha256"
timeout "$(remaining)" python3 - "$artifact_dir" "$GANESH_WORKSPACE_ARCHIVE_URI" "$GANESH_WORKSPACE_ARCHIVE_SHA256" <<'PY'
import hashlib, json, sys
from pathlib import Path
root=Path(sys.argv[1]); files=[]
for path in sorted(root.rglob("*")):
    if path.is_file() and path.name != "prebuild-manifest.json":
        digest=hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda:handle.read(1024*1024),b""): digest.update(chunk)
        h=digest.hexdigest()
        files.append({"path":str(path.relative_to(root)),"size":path.stat().st_size,"sha256":h})
value={"schema_version":"ganesh-mini-cuda-prebuild/v2","status":"built","workspace_uri":sys.argv[2],"workspace_sha256":sys.argv[3],"image_ref":(root/"image-ref.txt").read_text().strip(),"image_id":(root/"image-id.txt").read_text().strip(),"files":files}
value["evidence_sha256"]=hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",",":")).encode()).hexdigest()
(root/"prebuild-manifest.json").write_text(json.dumps(value,indent=2,sort_keys=True)+"\n")
PY
printf '%s\n' 0 > "$evidence_dir/startup-exit-code.txt"
timeout "$(remaining)" gcloud storage rsync "$artifact_dir" "gs://$GANESH_GCS_BUCKET/$GANESH_GCS_PREFIX/prebuild" --recursive --project="$GANESH_GCP_PROJECT" > "$evidence_dir/gcs-artifact-upload.log" 2>&1
if ! write_inventory; then
  rm -f "$evidence_dir/.runtime-files.sha256.tmp"
  printf 'terminal inventory failed\n' > "$evidence_dir/terminal-inventory-failure.txt"
  exit 91
fi
final_backup
trap - EXIT
kill "$watchdog_pid" 2>/dev/null || true
exit 0
