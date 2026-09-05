#!/bin/bash
set -Eeuo pipefail
root=/opt/ganesh-cutoff5885
bucket=ganesh-gate0-model-transfer-1061994342941
prefix=ganesh-mini-1.0/verification/cutoff5885-20260905
mkdir -p "$root/results"
cd "$root"
exec > >(tee -a "$root/bootstrap.log") 2>&1

finish() {
  result=$?
  trap - EXIT
  set +e
  if [[ -n "${progress_pid:-}" ]]; then kill "$progress_pid"; fi
  python3 -c 'import json,sys; print(json.dumps({"exit_code":int(sys.argv[1])}))' "$result" > "$root/results/terminal.json"
  for file in "$root"/results/* "$root/bootstrap.log"; do
    [[ -f "$file" ]] || continue
    for attempt in 1 2 3; do
      python3 "$root/storage.py" upload "$bucket" "$prefix/results/$(basename "$file")" "$file" && break
      sleep 3
    done
  done
  sync
  /sbin/poweroff
}
trap finish EXIT
curl --fail --silent --show-error --retry 3 -H 'Metadata-Flavor: Google' \
  http://metadata.google.internal/computeMetadata/v1/instance/attributes/storage-client -o storage.py
echo '71e0f16f509c4a7ff0f442edd58c67d13dadc273408319a5ecb6f9077d2792bb  storage.py' | sha256sum -c -
python3 storage.py download "$bucket" "$prefix/input/workspace.tar.gz" workspace.tar.gz 608c825ee965a3b79fe6aa1ad77c7ab100295112a6f847a08fa016a9c5622b9b
python3 storage.py download "$bucket" ganesh-mini-1.0/gate3/20260827T113051Z/input/docker-bundle.tar.gz docker-bundle.tar.gz 2de5e2625e77f38d895d32bb69592970d017dcdc6494ca807421eb8ff0065245
python3 storage.py download "$bucket" ganesh-mini-1.0/gate3/20260827T113051Z/input/verifier-images-amd64-v1.tar verifier-images.tar 1c5c8196cdcc595d755ea506f774dee8a5699e495fe67d7c4441e7a06c21b972
tar -xzf workspace.tar.gz
tar -xzf docker-bundle.tar.gz
(cd docker-bundle && sha256sum -c bundle-files.sha256)
dpkg -i docker-bundle/debs/*.deb || dpkg -i docker-bundle/debs/*.deb
dpkg --audit > results/dpkg-audit.txt
test ! -s results/dpkg-audit.txt
systemctl start docker
docker load -i verifier-images.tar
docker info --format '{{json .}}' > results/docker-info.json
uname -a > results/host.txt
(
  while sleep 60; do
    for name in progress.json qualification.json qualification-1.json qualification-4.json qualification-8.json; do
      [[ -f "$root/results/$name" ]] && python3 "$root/storage.py" upload "$bucket" "$prefix/results/$name" "$root/results/$name" || true
    done
  done
) &
progress_pid=$!
timeout --signal=TERM --kill-after=30 25000 python3 -m scripts.data.vm_cutoff_verify
