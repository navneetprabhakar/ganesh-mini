#!/usr/bin/env bash
set -Eeuo pipefail

for name in GANESH_GCP_PROJECT GANESH_GCS_BUCKET GANESH_GCS_PREFIX GANESH_CUDA_IMAGE_ID GANESH_CUDA_IMAGE_REF GANESH_PRIOR_BACKUP_MANIFEST_URI GANESH_PRIOR_BACKUP_MANIFEST_SHA256 GANESH_SERIAL_RECOVERY_MANIFEST_URI GANESH_SERIAL_RECOVERY_MANIFEST_SHA256 GANESH_SERIAL_RECOVERY_FINDING_SHA256 GANESH_WORKSPACE_ARCHIVE_URI GANESH_WORKSPACE_ARCHIVE_SHA256 GANESH_WORKSPACE_GIT_COMMIT GANESH_BUILD_INPUTS_SHA256 GANESH_RESOURCE_NAME GANESH_RESOURCE_ID GANESH_CUMULATIVE_COST_USD GANESH_RESUME_COMPUTE_UPPER_USD GANESH_SUPPORT_RESERVE_USD; do
  [[ -n "${!name:-}" ]] || { echo "missing $name" >&2; exit 2; }
done
approved_prefix="ganesh-mini-1.0/gate0b/20260822T165734Z"
[[ "$GANESH_GCS_PREFIX" == "$approved_prefix" ]]
[[ "$GANESH_RESOURCE_NAME" == "ganesh-mini-prebuild-20260822t165734z" ]]
[[ "$GANESH_RESOURCE_ID" == "8798900559452333835" ]]
case "$GANESH_PRIOR_BACKUP_MANIFEST_URI" in *'#'[0-9]*) ;; *) echo "prior backup manifest URI must include a GCS generation" >&2; exit 40;; esac
case "$GANESH_SERIAL_RECOVERY_MANIFEST_URI" in *'#'[0-9]*) ;; *) echo "serial recovery manifest URI must include a GCS generation" >&2; exit 40;; esac
python3 - "$GANESH_CUMULATIVE_COST_USD" "$GANESH_RESUME_COMPUTE_UPPER_USD" "$GANESH_SUPPORT_RESERVE_USD" <<'PY'
from decimal import Decimal
import sys
values = [Decimal(value) for value in sys.argv[1:]]
if any(value < 0 for value in values) or values[1] <= 0:
    raise SystemExit("resume cost inputs must be nonnegative and resume upper positive")
if sum(values) >= Decimal("5"):
    raise SystemExit(f"resume cost ceiling is not below USD 5: {sum(values)}")
PY

source_evidence_dir="/var/lib/ganesh-mini-prebuild"
source_artifact_dir="$source_evidence_dir/artifacts"
evidence_dir="/var/lib/ganesh-mini-prebuild-attempt2"
artifact_dir="$evidence_dir/artifacts"
mkdir -p "$artifact_dir"
exec > >(tee -a "$evidence_dir/startup.stdout.log") 2> >(tee -a "$evidence_dir/startup.stderr.log" >&2)

started_epoch="$(date +%s)"
hard_deadline_epoch="$((started_epoch + 1800))"
operation_deadline_epoch="$((started_epoch + 1500))"
printf '%s\n' "$operation_deadline_epoch" > "$evidence_dir/prebuild-deadline-epoch.txt"
( sleep 1790; shutdown -h now ) & watchdog_pid="$!"
remaining() { local value=$((operation_deadline_epoch - $(date +%s))); (( value > 0 )) || return 1; printf '%s\n' "$value"; }
backup_remaining() { local value=$((hard_deadline_epoch - 20 - $(date +%s))); (( value > 0 )) || return 1; printf '%s\n' "$value"; }
inventory_remaining() { local value=$((hard_deadline_epoch - 240 - $(date +%s))); (( value > 0 )) || return 1; printf '%s\n' "$value"; }
inventory_attempted=0
phase_timeout() { local cap="$1" left; left="$(remaining)" || return 1; (( left < cap )) && printf '%s\n' "$left" || printf '%s\n' "$cap"; }
write_inventory() {
  inventory_attempted=1
  local budget; budget="$(inventory_remaining)" || return 1
  timeout "$budget" bash -c 'set -o pipefail; cd "$1"; find . -type f ! -name runtime-files.sha256 ! -name .runtime-files.sha256.tmp -print0 | sort -z | xargs -0 sha256sum > .runtime-files.sha256.tmp && mv .runtime-files.sha256.tmp runtime-files.sha256' _ "$evidence_dir"
}
final_backup() {
  timeout "$(backup_remaining)" gcloud storage rsync "$evidence_dir" \
    "gs://$GANESH_GCS_BUCKET/$GANESH_GCS_PREFIX/prebuild-terminal-attempt2" \
    --recursive --project="$GANESH_GCP_PROJECT" > /var/log/ganesh-prebuild-attempt2-final-backup.log 2>&1
}
finish() {
  local status="$?"
  trap - EXIT
  printf '%s\n' "$status" > "$evidence_dir/startup-exit-code.txt"
  if (( inventory_attempted == 0 )) && ! write_inventory; then
    rm -f "$evidence_dir/.runtime-files.sha256.tmp"
    printf 'terminal inventory failed\n' > "$evidence_dir/terminal-inventory-failure.txt"
    status=91
  fi
  final_backup || status=90
  kill "$watchdog_pid" 2>/dev/null || true
  exit "$status"
}
trap finish EXIT

if gcloud storage ls "gs://$GANESH_GCS_BUCKET/$GANESH_GCS_PREFIX/prebuild-attempt2/**" --project="$GANESH_GCP_PROJECT" >/dev/null 2>&1 || \
   gcloud storage ls "gs://$GANESH_GCS_BUCKET/$GANESH_GCS_PREFIX/prebuild-terminal-attempt2/**" --project="$GANESH_GCP_PROJECT" >/dev/null 2>&1; then
  echo "attempt 2 GCS destinations must be empty" >&2
  exit 41
fi
timeout "$(phase_timeout 120)" gcloud storage cp "$GANESH_PRIOR_BACKUP_MANIFEST_URI" "$evidence_dir/prior-backup-manifest.json" --project="$GANESH_GCP_PROJECT" > "$evidence_dir/prior-backup-download.log" 2>&1
printf '%s  %s\n' "$GANESH_PRIOR_BACKUP_MANIFEST_SHA256" "$evidence_dir/prior-backup-manifest.json" | sha256sum -c -
timeout "$(phase_timeout 120)" gcloud storage cp "$GANESH_SERIAL_RECOVERY_MANIFEST_URI" "$evidence_dir/serial-recovery-manifest.json" --project="$GANESH_GCP_PROJECT" > "$evidence_dir/serial-recovery-download.log" 2>&1
printf '%s  %s\n' "$GANESH_SERIAL_RECOVERY_MANIFEST_SHA256" "$evidence_dir/serial-recovery-manifest.json" | sha256sum -c -
timeout "$(remaining)" python3 - "$evidence_dir/prior-backup-manifest.json" "$source_evidence_dir" "$GANESH_GCS_BUCKET" "$GANESH_GCS_PREFIX" <<'PY'
import hashlib, json, sys
from pathlib import Path
manifest_path, source_root, bucket, prefix = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], sys.argv[4]
def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
manifest = json.loads(manifest_path.read_text())
claimed = manifest.pop("evidence_sha256", None)
observed = hashlib.sha256(json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
if claimed != observed or manifest.get("status") != "verified":
    raise SystemExit("prior backup manifest seal or status mismatch")
expected_prefix = f"gs://{bucket}/{prefix}/prebuild-terminal"
if manifest.get("prefix") != expected_prefix:
    raise SystemExit("prior backup manifest prefix mismatch")
rows = {row["object_uri"].removeprefix(expected_prefix + "/"): row for row in manifest["objects"]}
inventory_path = source_root / "runtime-files.sha256"
inventory_hash = file_hash(inventory_path)
if rows.get("runtime-files.sha256", {}).get("downloaded_sha256") != inventory_hash:
    raise SystemExit("source runtime inventory is not bound to the prior backup")
for line in inventory_path.read_text().splitlines():
    digest, relative = line.split(None, 1)
    relative = relative.lstrip("*").removeprefix("./")
    path = source_root / relative
    if not path.is_file():
        raise SystemExit(f"source file missing: {relative}")
    local = file_hash(path)
    if local != digest or rows.get(relative, {}).get("downloaded_sha256") != digest:
        raise SystemExit(f"source file is not identical to sealed backup: {relative}")
if (source_root / "startup-exit-code.txt").read_text().strip() != "141":
    raise SystemExit("prior attempt did not fail with the expected exit 141")
PY
timeout "$(remaining)" python3 - "$evidence_dir/serial-recovery-manifest.json" "$GANESH_GCS_BUCKET" "$GANESH_GCS_PREFIX" "$GANESH_SERIAL_RECOVERY_FINDING_SHA256" <<'PY'
import hashlib, json, sys
from pathlib import Path
manifest = json.loads(Path(sys.argv[1]).read_text())
claimed = manifest.pop("evidence_sha256", None)
observed = hashlib.sha256(json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
expected_prefix = f"gs://{sys.argv[2]}/{sys.argv[3]}/prebuild-attempt1-serial-recovery"
if claimed != observed or manifest.get("status") != "verified" or manifest.get("prefix") != expected_prefix:
    raise SystemExit("serial recovery manifest seal, status, or prefix mismatch")
serial = [row for row in manifest.get("objects", []) if row["object_uri"].endswith("/provider/serial-port.log")]
if len(serial) != 1 or not serial[0].get("verified") or int(serial[0].get("size", 0)) <= 0:
    raise SystemExit("serial recovery manifest lacks nonempty verified serial output")
finding = [row for row in manifest.get("objects", []) if row["object_uri"].endswith("/recovery-finding.json")]
if len(finding) != 1 or not finding[0].get("verified") or finding[0].get("downloaded_sha256") != sys.argv[4]:
    raise SystemExit("serial recovery limitation finding is not bound")
PY

observed_image_id="$(timeout "$(phase_timeout 30)" docker image inspect --format '{{.Id}}' "$GANESH_CUDA_IMAGE_REF")"
[[ "$observed_image_id" == "$GANESH_CUDA_IMAGE_ID" ]]
[[ -f "$source_artifact_dir/image-id.txt" ]]
[[ "$(<"$source_artifact_dir/image-id.txt")" == "$GANESH_CUDA_IMAGE_ID" ]]
printf '%s  %s\n' "$GANESH_BUILD_INPUTS_SHA256" "$source_artifact_dir/build-inputs.sha256" | sha256sum -c -

for file in build-inputs.sha256 docker-build.stderr.log docker-build.stdout.log docker-history.txt docker-image-inspect.json image-id.txt image-ref.txt; do
  cp -a "$source_artifact_dir/$file" "$artifact_dir/$file"
done
cp -a "$source_artifact_dir/docker-bundle" "$artifact_dir/docker-bundle"
cp -a "$source_evidence_dir/builder-dpkg-packages.tsv" "$evidence_dir/builder-dpkg-packages.tsv"
cp -a "$source_evidence_dir/docker-version.txt" "$evidence_dir/docker-version.txt"
timeout "$(remaining)" bash -c 'set -o pipefail; docker save "$1" | zstd --quiet -T0 -10 -o "$2"' _ \
  "$GANESH_CUDA_IMAGE_REF" "$artifact_dir/cuda-image.docker.tar.zst"
timeout "$(remaining)" sha256sum "$artifact_dir/cuda-image.docker.tar.zst" > "$artifact_dir/cuda-image.docker.tar.zst.sha256"
timeout "$(phase_timeout 60)" docker run --rm --pull=never --network none --entrypoint /bin/bash "$GANESH_CUDA_IMAGE_REF" -c \
  "set -o pipefail; dpkg-query -W -f='\${Package}\\t\${Version}\\n' | sort" > "$artifact_dir/container-dpkg-packages.tsv"
timeout "$(phase_timeout 60)" docker run --rm --pull=never --network none --entrypoint /bin/bash "$GANESH_CUDA_IMAGE_REF" -c \
  "set -o pipefail; uv pip freeze --python /opt/ganesh-venv/bin/python | sort" > "$artifact_dir/container-python-packages.txt"
timeout "$(remaining)" tar -czf "$artifact_dir/docker-bundle.tar.gz" -C "$artifact_dir" docker-bundle
timeout "$(remaining)" sha256sum "$artifact_dir/docker-bundle.tar.gz" > "$artifact_dir/docker-bundle.tar.gz.sha256"
timeout "$(remaining)" python3 - "$artifact_dir" "$GANESH_WORKSPACE_ARCHIVE_URI" "$GANESH_WORKSPACE_ARCHIVE_SHA256" "$GANESH_PRIOR_BACKUP_MANIFEST_SHA256" "$GANESH_SERIAL_RECOVERY_MANIFEST_SHA256" "$GANESH_SERIAL_RECOVERY_FINDING_SHA256" "$GANESH_RESOURCE_NAME" "$GANESH_RESOURCE_ID" "$GANESH_WORKSPACE_GIT_COMMIT" <<'PY'
import hashlib, json, sys
from pathlib import Path
root = Path(sys.argv[1])
files = []
for path in sorted(root.rglob("*")):
    if path.is_file() and path.name != "prebuild-manifest.json":
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        files.append({"path": str(path.relative_to(root)), "size": path.stat().st_size, "sha256": digest.hexdigest()})
value = {
    "schema_version": "ganesh-mini-cuda-prebuild/v2",
    "status": "built",
    "attempt_id": "prebuild-attempt2",
    "resumed_from_failed_attempt": "prebuild-terminal",
    "workspace_uri": sys.argv[2],
    "workspace_sha256": sys.argv[3],
    "prior_backup_manifest_sha256": sys.argv[4],
    "serial_recovery_manifest_sha256": sys.argv[5],
    "serial_recovery_finding_sha256": sys.argv[6],
    "resource_name": sys.argv[7],
    "resource_id": sys.argv[8],
    "workspace_git_commit": sys.argv[9],
    "build_inputs_sha256": hashlib.sha256((root / "build-inputs.sha256").read_bytes()).hexdigest(),
    "image_ref": (root / "image-ref.txt").read_text().strip(),
    "image_id": (root / "image-id.txt").read_text().strip(),
    "files": files,
}
value["evidence_sha256"] = hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
(root / "prebuild-manifest.json").write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
PY
printf '%s\n' 0 > "$evidence_dir/startup-exit-code.txt"
timeout "$(remaining)" gcloud storage rsync "$artifact_dir" \
  "gs://$GANESH_GCS_BUCKET/$GANESH_GCS_PREFIX/prebuild-attempt2" --recursive --project="$GANESH_GCP_PROJECT" > "$evidence_dir/gcs-artifact-upload.log" 2>&1
if ! write_inventory; then
  rm -f "$evidence_dir/.runtime-files.sha256.tmp"
  printf 'terminal inventory failed\n' > "$evidence_dir/terminal-inventory-failure.txt"
  exit 91
fi
final_backup
trap - EXIT
kill "$watchdog_pid" 2>/dev/null || true
