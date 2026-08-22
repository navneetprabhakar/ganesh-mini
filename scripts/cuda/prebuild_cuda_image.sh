#!/usr/bin/env bash
set -Eeuo pipefail

if [[ "$(uname -s)" != "Linux" || "$(uname -m)" != "x86_64" ]]; then
  echo "CUDA image prebuild requires a Linux x86_64 builder" >&2
  exit 2
fi
if [[ $# -ne 2 ]]; then
  echo "usage: $0 REPOSITORY_DIR OUTPUT_DIR" >&2
  exit 2
fi
repo_dir="$(realpath "$1")"
output_dir="$(mkdir -p "$2" && realpath "$2")"
image_ref="${GANESH_CUDA_IMAGE_REF:-ganesh-mini-cuda-gate0:torch2.13.0-cu13.0.1}"
deadline_epoch="${GANESH_PREBUILD_DEADLINE_EPOCH:-$(( $(date +%s) + 3600 ))}"
remaining=$((deadline_epoch - $(date +%s)))
if (( remaining <= 0 || remaining > 3600 )); then
  echo "prebuild deadline must be within the next 3,600 seconds" >&2
  exit 2
fi
timeout --signal=TERM --kill-after=30s "$remaining" \
  docker build --platform linux/amd64 --pull=false --network=default \
    --file "$repo_dir/containers/cuda/Dockerfile" --tag "$image_ref" "$repo_dir" \
    > >(tee "$output_dir/docker-build.stdout.log") \
    2> >(tee "$output_dir/docker-build.stderr.log" >&2)
image_id="$(docker image inspect --format '{{.Id}}' "$image_ref")"
docker image inspect "$image_ref" > "$output_dir/docker-image-inspect.json"
docker history --no-trunc "$image_ref" > "$output_dir/docker-history.txt"
printf '%s\n' "$image_ref" > "$output_dir/image-ref.txt"
printf '%s\n' "$image_id" > "$output_dir/image-id.txt"
sha256sum "$repo_dir/containers/cuda/Dockerfile" "$repo_dir/pyproject.toml" "$repo_dir/uv.lock" > "$output_dir/build-inputs.sha256"
remaining=$((deadline_epoch - $(date +%s)))
timeout --signal=TERM --kill-after=30s "$remaining" bash -c 'set -o pipefail; docker save "$1" | zstd --quiet -T0 -10 -o "$2"' _ "$image_ref" "$output_dir/cuda-image.docker.tar.zst"
remaining=$((deadline_epoch - $(date +%s)))
timeout "$remaining" sha256sum "$output_dir/cuda-image.docker.tar.zst" > "$output_dir/cuda-image.docker.tar.zst.sha256"
remaining=$((deadline_epoch - $(date +%s))); (( remaining > 0 )); (( remaining < 60 )) && cap="$remaining" || cap=60
timeout "$cap" docker run --rm --pull=never --network none --entrypoint /bin/bash "$image_ref" -c \
  "set -o pipefail; dpkg-query -W -f='\${Package}\\t\${Version}\\n' | sort" > "$output_dir/container-dpkg-packages.tsv"
remaining=$((deadline_epoch - $(date +%s))); (( remaining > 0 )); (( remaining < 60 )) && cap="$remaining" || cap=60
timeout "$cap" docker run --rm --pull=never --network none --entrypoint /bin/bash "$image_ref" -c \
  "set -o pipefail; uv pip freeze --python /opt/ganesh-venv/bin/python | sort" > "$output_dir/container-python-packages.txt"
