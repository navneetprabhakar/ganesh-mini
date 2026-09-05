"""Minimal GCS transfer client using the VM's attached service identity."""
import hashlib
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path


def request(url, method="GET", data=None):
    token_request = urllib.request.Request(
        "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token",
        headers={"Metadata-Flavor": "Google"})
    with urllib.request.urlopen(token_request, timeout=30) as response:
        token = json.load(response)["access_token"]
    return urllib.request.urlopen(urllib.request.Request(url, data=data, method=method,
        headers={"Authorization": "Bearer " + token, "Content-Type": "application/octet-stream"}), timeout=300)


def main():
    mode, bucket, key, local = sys.argv[1:5]
    if mode == "download":
        url = "https://storage.googleapis.com/storage/v1/b/" + bucket + "/o/" + urllib.parse.quote(key, safe="") + "?alt=media"
        h = hashlib.sha256()
        with request(url) as source, open(local, "wb") as target:
            while chunk := source.read(4*1024*1024):
                h.update(chunk)
                target.write(chunk)
        if h.hexdigest() != sys.argv[5]:
            raise RuntimeError("download SHA-256 mismatch: " + key)
    elif mode == "upload":
        url = "https://storage.googleapis.com/upload/storage/v1/b/"+bucket+"/o?uploadType=media&name="+urllib.parse.quote(key, safe="")
        with request(url, method="POST", data=Path(local).read_bytes()) as response:
            metadata = json.load(response)
        print(json.dumps({"name": metadata["name"], "generation": metadata["generation"], "size": metadata["size"]}))
    else:
        raise ValueError("unknown transfer mode")


if __name__ == "__main__":
    main()
