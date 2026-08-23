#!/bin/sh
set -eu
probe_root="$(mktemp -d)"
trap 'rm -rf "$probe_root"' EXIT
tar -xzf /opt/typescript-5.5.4.tgz -C "$probe_root"
node "$probe_root/package/bin/tsc" --version
