#!/usr/bin/env bash
set -Eeuo pipefail

project=executespecv1
bucket=ganesh-gate0-model-transfer-1061994342941
prefix=ganesh-mini-1.0/gate0b/20260822T165734Z
resource_id=8798900559452333835
source_root=/var/lib/ganesh-mini-prebuild-attempt2
evidence_dir=/var/lib/ganesh-mini-prebuild-verification-attempt2
download_dir=/var/lib/ganesh-mini-prebuild-verification-attempt2-downloads
mkdir -p "$evidence_dir" "$download_dir"
echo "GANESH_PREBUILD_VERIFICATION_BEGIN 20260822T165734Z"
exec >"$evidence_dir/startup.stdout.log" 2>"$evidence_dir/startup.stderr.log"

started_epoch="$(date +%s)"
hard_deadline_epoch="$((started_epoch + 750))"
operation_deadline_epoch="$((started_epoch + 500))"
( sleep 740; shutdown -h now ) & watchdog_pid="$!"
remaining() { local value=$((operation_deadline_epoch - $(date +%s))); (( value > 0 )) || return 1; printf '%s\n' "$value"; }
backup_remaining() { local value=$((hard_deadline_epoch - 20 - $(date +%s))); (( value > 0 )) || return 1; printf '%s\n' "$value"; }
write_inventory() {
  (cd "$evidence_dir" && find . -type f ! -name runtime-files.sha256 -print0 | sort -z | xargs -0 sha256sum > runtime-files.sha256)
}
final_backup() {
  timeout "$(backup_remaining)" gcloud storage rsync "$evidence_dir" "gs://$bucket/$prefix/prebuild-verification-terminal-attempt2" --recursive --project="$project" >/var/log/ganesh-prebuild-verification-attempt2-backup.log 2>&1
}
finish() {
  local status="$?"
  trap - EXIT
  printf '%s\n' "$status" >"$evidence_dir/startup-exit-code.txt"
  write_inventory || status=91
  final_backup || status=90
  kill "$watchdog_pid" 2>/dev/null || true
  exit "$status"
}
trap finish EXIT

observed_id="$(curl -fsS -H 'Metadata-Flavor: Google' http://metadata.google.internal/computeMetadata/v1/instance/id)"
[[ "$observed_id" == "$resource_id" ]]
for suffix in prebuild-verification-attempt2 prebuild-verification-terminal-attempt2; do
  if gcloud storage ls "gs://$bucket/$prefix/$suffix/**" --project="$project" >/dev/null 2>&1; then
    echo "verification destination is not empty: $suffix" >&2
    exit 41
  fi
done

verifier=/opt/ganesh-gcloud-backup-manifest.py
timeout 120 gcloud storage cp 'gs://ganesh-gate0-model-transfer-1061994342941/ganesh-mini-1.0/gate0b/20260822T165734Z/preflight/gcloud-backup-manifest-attempt2.py#1787429756830586' "$verifier" --project="$project"
printf '%s  %s\n' b1829776353b8bced319144cf9cac9930ae74e85a0a995616b10741cf5761ac0 "$verifier" | sha256sum -c -

timeout "$(remaining)" python3 "$verifier" \
  --project "$project" \
  --prefix "gs://$bucket/$prefix/prebuild-terminal-attempt2" \
  --output "$evidence_dir/backup-manifest.json" \
  --download-dir "$download_dir" \
  --map "artifacts=$source_root/artifacts" \
  --map "builder-dpkg-packages.tsv=$source_root/builder-dpkg-packages.tsv" \
  --map "docker-version.txt=$source_root/docker-version.txt" \
  --map "gcs-artifact-upload.log=$source_root/gcs-artifact-upload.log" \
  --map "prebuild-deadline-epoch.txt=$source_root/prebuild-deadline-epoch.txt" \
  --map "prior-backup-download.log=$source_root/prior-backup-download.log" \
  --map "prior-backup-manifest.json=$source_root/prior-backup-manifest.json" \
  --map "runtime-files.sha256=$source_root/runtime-files.sha256" \
  --map "serial-recovery-download.log=$source_root/serial-recovery-download.log" \
  --map "serial-recovery-manifest.json=$source_root/serial-recovery-manifest.json" \
  --map "startup-exit-code.txt=$source_root/startup-exit-code.txt" \
  --map "startup.stderr.log=$source_root/startup.stderr.log" \
  --map "startup.stdout.log=$source_root/startup.stdout.log"

printf '%s\n' 0 >"$evidence_dir/startup-exit-code.txt"
write_inventory
timeout "$(remaining)" gcloud storage rsync "$evidence_dir" "gs://$bucket/$prefix/prebuild-verification-attempt2" --recursive --project="$project" >"$evidence_dir/gcs-upload.log" 2>&1
write_inventory
final_backup
trap - EXIT
kill "$watchdog_pid" 2>/dev/null || true
