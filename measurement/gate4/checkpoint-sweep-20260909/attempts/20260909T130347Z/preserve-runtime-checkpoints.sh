#!/usr/bin/env bash
set -Eeuo pipefail

bucket="ganesh-gate0-model-transfer-1061994342941"
prefix="ganesh-mini-1.0/evaluation/checkpoint-sweep-v1/attempts/20260909T130347Z/"
attempt_dir="measurement/gate4/checkpoint-sweep-20260909/attempts/20260909T130347Z"
listing="${attempt_dir}/provider/runtime-checkpoint-listing.json"
mirror="${attempt_dir}/runtime-checkpoint-mirror"

mkdir -p "${attempt_dir}/provider" "${mirror}"
access_token="$(gcloud auth print-access-token)"
encoded_prefix="$(jq -rn --arg v "${prefix}" '$v|@uri')"
curl --fail --silent --show-error \
  -H "Authorization: Bearer ${access_token}" \
  "https://storage.googleapis.com/storage/v1/b/${bucket}/o?prefix=${encoded_prefix}" \
  -o "${listing}"

export access_token bucket prefix mirror
jq -r '.items[] | [.name, .generation] | @base64' "${listing}" | \
  xargs -P 8 -n 1 bash -c '
    row="$(printf "%s" "$1" | base64 --decode)"
    name="$(printf "%s" "${row}" | jq -r ".[0]")"
    generation="$(printf "%s" "${row}" | jq -r ".[1]")"
    relative="${name#${prefix}}"
    destination="${mirror}/${relative}"
    mkdir -p "$(dirname "${destination}")"
    encoded_name="$(jq -rn --arg v "${name}" "\$v|@uri")"
    curl --fail --silent --show-error \
      -H "Authorization: Bearer ${access_token}" \
      "https://storage.googleapis.com/download/storage/v1/b/${bucket}/o/${encoded_name}?alt=media&generation=${generation}" \
      -o "${destination}"
  ' _

failures=0
while IFS=$'\t' read -r relative expected_size expected_md5; do
  path="${mirror}/${relative}"
  actual_size="$(stat -f '%z' "${path}")"
  actual_md5="$(openssl dgst -md5 -binary "${path}" | base64)"
  if [[ "${actual_size}" != "${expected_size}" || "${actual_md5}" != "${expected_md5}" ]]; then
    printf 'mismatch\t%s\t%s\t%s\t%s\t%s\n' \
      "${relative}" "${expected_size}" "${actual_size}" "${expected_md5}" "${actual_md5}" >&2
    failures=$((failures + 1))
  fi
done < <(jq -r --arg prefix "${prefix}" '.items[] | [(.name | ltrimstr($prefix)), .size, .md5Hash] | @tsv' "${listing}")

if (( failures != 0 )); then
  printf 'verification failed: %d object(s)\n' "${failures}" >&2
  exit 1
fi

count="$(jq '.items | length' "${listing}")"
bytes="$(jq '[.items[].size | tonumber] | add' "${listing}")"
listing_sha256="$(shasum -a 256 "${listing}" | awk '{print $1}')"
printf 'verified_objects=%s\nverified_bytes=%s\nlisting_sha256=%s\n' \
  "${count}" "${bytes}" "${listing_sha256}"
