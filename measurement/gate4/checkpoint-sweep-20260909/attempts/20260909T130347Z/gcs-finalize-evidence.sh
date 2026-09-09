#!/usr/bin/env bash
set -Eeuo pipefail

bucket="ganesh-gate0-model-transfer-1061994342941"
prefix="ganesh-mini-1.0/evaluation/checkpoint-sweep-v1/attempts/20260909T130347Z/finalization"
attempt_dir="measurement/gate4/checkpoint-sweep-20260909/attempts/20260909T130347Z"
artifact_dir="artifacts/eval/checkpoint-sweep-20260909T130347Z"
archive="${artifact_dir}/checkpoint-sweep-evidence.tar.gz"
roundtrip_dir="${attempt_dir}/gcs-roundtrip"
mkdir -p "${artifact_dir}" "${roundtrip_dir}"

COPYFILE_DISABLE=1 tar -czf "${archive}" \
  -C "$(dirname "${attempt_dir}")" "$(basename "${attempt_dir}")"

access_token="$(gcloud auth print-access-token)"
upload_create_only() {
  local source="$1"
  local object_name="$2"
  local metadata_path="$3"
  local encoded_name
  encoded_name="$(jq -rn --arg v "${object_name}" '$v|@uri')"
  curl --fail --silent --show-error -X POST \
    -H "Authorization: Bearer ${access_token}" \
    -H 'Content-Type: application/octet-stream' \
    --data-binary "@${source}" \
    "https://storage.googleapis.com/upload/storage/v1/b/${bucket}/o?uploadType=media&ifGenerationMatch=0&name=${encoded_name}" \
    -o "${metadata_path}"
  local generation
  generation="$(jq -r '.generation' "${metadata_path}")"
  curl --fail --silent --show-error \
    -H "Authorization: Bearer ${access_token}" \
    "https://storage.googleapis.com/download/storage/v1/b/${bucket}/o/${encoded_name}?alt=media&generation=${generation}" \
    -o "${roundtrip_dir}/$(basename "${source}")"
  cmp "${source}" "${roundtrip_dir}/$(basename "${source}")"
}

upload_create_only "${attempt_dir}/interruption-receipt.json" \
  "${prefix}/interruption-receipt.json" "${attempt_dir}/provider/gcs-interruption-upload.json"
upload_create_only "${attempt_dir}/teardown-receipt.json" \
  "${prefix}/teardown-receipt.json" "${attempt_dir}/provider/gcs-teardown-upload.json"
upload_create_only "${archive}" \
  "${prefix}/checkpoint-sweep-evidence.tar.gz" "${attempt_dir}/provider/gcs-archive-upload.json"

python3 - "${attempt_dir}" "${archive}" <<'PY'
import hashlib, json, pathlib, sys

attempt = pathlib.Path(sys.argv[1])
archive = pathlib.Path(sys.argv[2])

def digest(path):
    value = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b''):
            value.update(chunk)
    return value.hexdigest()

def canonical(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode()).hexdigest()

rows = []
for label, source, metadata in (
    ('interruption_receipt', attempt / 'interruption-receipt.json', attempt / 'provider/gcs-interruption-upload.json'),
    ('teardown_receipt', attempt / 'teardown-receipt.json', attempt / 'provider/gcs-teardown-upload.json'),
    ('evidence_archive', archive, attempt / 'provider/gcs-archive-upload.json'),
):
    uploaded = json.loads(metadata.read_text())
    rows.append({
        'label': label,
        'name': uploaded['name'],
        'generation': uploaded['generation'],
        'size_bytes': source.stat().st_size,
        'sha256': digest(source),
        'exact_generation_roundtrip': True,
    })
receipt = {
    'schema_version': 'ganesh-mini-checkpoint-sweep-gcs-finalization/v1',
    'status': 'evidence-preserved',
    'attempt_id': attempt.name,
    'objects': rows,
}
receipt['receipt_sha256'] = canonical(receipt)
(attempt / 'gcs-finalization-receipt.json').write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
PY

upload_create_only "${attempt_dir}/gcs-finalization-receipt.json" \
  "${prefix}/gcs-finalization-receipt.json" "${attempt_dir}/provider/gcs-finalization-upload.json"

jq '{status,receipt_sha256,objects}' "${attempt_dir}/gcs-finalization-receipt.json"
