import hashlib
import io
import json
import tarfile
from pathlib import Path

import pytest

from scripts.train.inspect_model_archive import verify, file_sha, EXPECTED


def fixture(tmp_path, extra=None, mutate=False):
    data=b'canonical model fixture'
    row={'path':'config.json','size':len(data),'git_oid':hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()}
    inventory=tmp_path/'inventory.json'
    inventory.write_text(json.dumps({'model_id':'Qwen/Qwen3.5-2B','revision':EXPECTED['model_revision'],'files':[row]}))
    archive=tmp_path/'model.tar.gz'
    with tarfile.open(archive,'w:gz') as handle:
        items=[('./config.json',b'x'*len(data) if mutate else data),
               ('._.',bytes.fromhex('0005160700020000')+bytes(155))]
        if extra: items.append(extra)
        for name,content in items:
            info=tarfile.TarInfo(name);info.size=len(content)
            handle.addfile(info,io.BytesIO(content))
    return archive,inventory


def test_verified_model_and_bounded_download_metadata(tmp_path):
    archive,inventory=fixture(tmp_path,('.cache/huggingface/download/config.json.metadata',b'fixture metadata'))
    result=verify(archive,inventory,file_sha(archive))
    assert list(result['verified_files'])==['config.json']
    assert len(result['metadata_only_appledouble_sidecars'])==1
    assert len(result['excluded_huggingface_download_cache'])==1


@pytest.mark.parametrize('extra',[('../escape',b'x'),('unknown.bin',b'x'),
                                   ('._config.json',bytes(163)),('.cache/huggingface/token',b'not admitted')])
def test_noncanonical_or_unsafe_extras_rejected(tmp_path,extra):
    archive,inventory=fixture(tmp_path,extra)
    with pytest.raises(ValueError): verify(archive,inventory,file_sha(archive))


def test_model_byte_change_rejected(tmp_path):
    archive,inventory=fixture(tmp_path,mutate=True)
    with pytest.raises(ValueError): verify(archive,inventory,file_sha(archive))


def test_materialization_keeps_only_canonical_bytes(tmp_path):
    archive,inventory=fixture(tmp_path,('.cache/huggingface/download/config.json.metadata',b'fixture metadata'))
    target=tmp_path/'canonical'
    result=verify(archive,inventory,file_sha(archive),target)
    assert result['canonical_materialization_performed'] is True
    assert [path.name for path in target.iterdir()]==['config.json']
    assert (target/'config.json').read_bytes()==b'canonical model fixture'


def test_materialization_never_overwrites_existing_data(tmp_path):
    archive,inventory=fixture(tmp_path)
    target=tmp_path/'canonical';target.mkdir();(target/'user-file').write_bytes(b'keep')
    with pytest.raises(ValueError): verify(archive,inventory,file_sha(archive),target)
    assert (target/'user-file').read_bytes()==b'keep'
