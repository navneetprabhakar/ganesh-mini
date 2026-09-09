#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 3 || $# -gt 4 ]]; then
  printf '%s\n' \
    'Usage: resumable_gcs_upload.sh SOURCE BUCKET OBJECT [SESSION_FILE]' \
    'Uploads SOURCE with a create-only GCS JSON resumable session.' \
    'The SESSION_FILE may be reused after a transport failure.' >&2
  exit 2
fi

source_file=$1
bucket=$2
object=$3
session_file=${4:-/tmp/ganesh-gcs-resumable-session}
chunk_bytes=$((64 * 1024 * 1024))
alignment=$((256 * 1024))

[[ -f "$source_file" ]] || { echo "missing source: $source_file" >&2; exit 2; }
command -v curl >/dev/null
command -v gcloud >/dev/null
command -v jq >/dev/null

if stat -f %z "$source_file" >/dev/null 2>&1; then
  total_bytes=$(stat -f %z "$source_file")
else
  total_bytes=$(stat -c %s "$source_file")
fi

headers=$(mktemp /tmp/ganesh-gcs-upload-headers.XXXXXX)
body=$(mktemp /tmp/ganesh-gcs-upload-body.XXXXXX)
trap 'rm -f "$headers" "$body"' EXIT

new_session() {
  local token encoded location
  token=$(gcloud auth print-access-token)
  encoded=$(jq -rn --arg value "$object" '$value|@uri')
  : >"$headers"
  : >"$body"
  curl -fsS --max-time 30 -D "$headers" -o "$body" -X POST \
    -H "Authorization: Bearer $token" \
    -H "X-Upload-Content-Type: application/octet-stream" \
    -H "X-Upload-Content-Length: $total_bytes" \
    -H "Content-Length: 0" \
    "https://storage.googleapis.com/upload/storage/v1/b/${bucket}/o?uploadType=resumable&ifGenerationMatch=0&name=${encoded}"
  location=$(awk 'BEGIN{IGNORECASE=1} /^location:/ {sub(/^[^:]*:[[:space:]]*/, ""); sub(/\r$/, ""); print; exit}' "$headers")
  [[ -n "$location" ]] || { cat "$body" >&2; echo "missing resumable session location" >&2; exit 1; }
  printf '%s\n' "$location" >"$session_file"
}

query_offset() {
  local session status range
  session=$(<"$session_file")
  : >"$headers"
  : >"$body"
  curl -sS --max-time 30 -D "$headers" -o "$body" -X PUT \
    -H "Content-Length: 0" \
    -H "Content-Range: bytes */$total_bytes" \
    "$session" || return 1
  status=$(awk 'toupper($1) ~ /^HTTP\// {code=$2} END {print code}' "$headers")
  if [[ "$status" == 200 || "$status" == 201 ]]; then
    echo "$total_bytes"
    return 0
  fi
  [[ "$status" == 308 ]] || { cat "$body" >&2; echo "unexpected status query response: $status" >&2; return 1; }
  range=$(awk 'BEGIN{IGNORECASE=1} /^range:/ {sub(/^[^:]*:[[:space:]]*bytes=0-/, ""); sub(/\r$/, ""); print; exit}' "$headers")
  if [[ -n "$range" ]]; then
    echo $((range + 1))
  else
    echo 0
  fi
}

[[ -s "$session_file" ]] || new_session

while true; do
  if ! offset=$(query_offset); then
    echo "session query failed; creating a new create-only session" >&2
    rm -f "$session_file"
    new_session
    offset=0
  fi
  if (( offset >= total_bytes )); then
    echo "upload complete: bytes=$total_bytes"
    exit 0
  fi
  (( offset % alignment == 0 )) || { echo "server offset is not 256 KiB aligned: $offset" >&2; exit 1; }
  remaining=$((total_bytes - offset))
  length=$chunk_bytes
  (( remaining < length )) && length=$remaining
  end=$((offset + length - 1))
  blocks=$(((length + alignment - 1) / alignment))
  skip_blocks=$((offset / alignment))
  session=$(<"$session_file")
  : >"$headers"
  : >"$body"
  echo "uploading bytes $offset-$end of $total_bytes" >&2
  set +e
  dd if="$source_file" bs=$alignment skip=$skip_blocks count=$blocks status=none | \
    curl -sS --max-time 300 -D "$headers" -o "$body" -X PUT \
      -H "Content-Length: $length" \
      -H "Content-Range: bytes $offset-$end/$total_bytes" \
      -H "Content-Type: application/octet-stream" \
      --data-binary @- "$session"
  curl_status=${PIPESTATUS[1]}
  set -e
  status=$(awk 'toupper($1) ~ /^HTTP\// {code=$2} END {print code}' "$headers")
  if [[ "$curl_status" == 0 && ( "$status" == 200 || "$status" == 201 ) ]]; then
    cat "$body"
    echo
    echo "upload complete: bytes=$total_bytes"
    exit 0
  fi
  if [[ "$curl_status" == 0 && "$status" == 308 ]]; then
    continue
  fi
  echo "chunk transport/status failure: curl=$curl_status http=${status:-none}; recovering from server offset" >&2
  sleep 2
done
