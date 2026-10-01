#!/usr/bin/env python3
"""Offline pinned model-byte verification; classify excluded download metadata."""
import argparse
import hashlib
import json
import tarfile
from pathlib import Path, PurePosixPath

from scripts.train.preflight_gate3_capability_pilot import canonical_sha, file_sha, EXPECTED


def verify(archive, inventory_path, archive_sha256, materialize_dir=None):
    if file_sha(archive)!=archive_sha256: raise ValueError('archive identity differs')
    if materialize_dir is not None:
        if materialize_dir.exists() and any(materialize_dir.iterdir()):
            raise ValueError('empty canonical model directory required')
        materialize_dir.mkdir(parents=True,exist_ok=True)
    inventory=json.loads(inventory_path.read_text())
    if inventory['model_id']!='Qwen/Qwen3.5-2B' or inventory['revision']!=EXPECTED['model_revision']:
        raise ValueError('model identity differs')
    expected={row['path']:row for row in inventory['files']}
    seen={}; sidecars=[]; cache=[]
    cache_dirs={'.cache','.cache/huggingface','.cache/huggingface/download','.cache/huggingface/trees'}
    cache_names={'.cache/huggingface/CACHEDIR.TAG','.cache/huggingface/.gitignore',
                 '.cache/huggingface/trees/'+EXPECTED['model_revision']+'.json'}
    cache_names.update('.cache/huggingface/download/'+name+suffix for name in expected for suffix in ('.lock','.metadata'))
    with tarfile.open(archive,mode='r|gz') as members:
        for member in members:
            path=PurePosixPath(member.name)
            if path.is_absolute() or '..' in path.parts: raise ValueError('unsafe model member')
            name=path.as_posix()
            if member.isdir():
                if name!='.' and name not in cache_dirs: raise ValueError('unexpected model directory: '+name)
                continue
            if not member.isfile(): raise ValueError('nonregular model member')
            content=members.extractfile(member)
            if path.name.startswith('._'):
                target='.' if name=='._.' else path.with_name(path.name[2:]).as_posix()
                if target!='.' and target not in expected and target not in cache_dirs and target not in cache_names:
                    raise ValueError('unbound sidecar: '+name)
                if member.size<26 or member.size>65536: raise ValueError('unbounded sidecar')
                data=content.read()
                if data[:8]!=bytes.fromhex('0005160700020000'): raise ValueError('not AppleDouble metadata')
                sidecars.append({'name':name,'size':member.size,'sha256':hashlib.sha256(data).hexdigest()})
                continue
            if name.startswith('.cache/huggingface/'):
                if name not in cache_names: raise ValueError('unexpected cache file: '+name)
                if member.size>1048576: raise ValueError('unbounded cache metadata')
                data=content.read()
                cache.append({'name':name,'size':member.size,'sha256':hashlib.sha256(data).hexdigest()})
                continue
            if len(path.parts)!=1: raise ValueError('non-flat model member')
            if name not in expected or name in seen: raise ValueError('unexpected/duplicate model file')
            row=expected[name]
            if member.size!=row['size']: raise ValueError('model size differs: '+name)
            sha256=hashlib.sha256(); git=hashlib.sha1(f"blob {member.size}\0".encode())
            output=(materialize_dir/name).open('xb') if materialize_dir is not None else None
            try:
                for chunk in iter(lambda:content.read(8*1024*1024),b''):
                    sha256.update(chunk); git.update(chunk)
                    if output is not None: output.write(chunk)
            finally:
                if output is not None: output.close()
            claimed=row.get('sha256') or row['git_oid']
            observed=sha256.hexdigest() if row.get('sha256') else git.hexdigest()
            if observed!=claimed: raise ValueError('model bytes differ: '+name)
            seen[name]={'archive_member':member.name,'size':member.size,'sha256':sha256.hexdigest(),'git_blob_sha1':git.hexdigest()}
    if set(seen)!=set(expected): raise ValueError('model inventory incomplete')
    result={'schema_version':'ganesh-mini-model-archive-inventory/v1','status':'passed',
            'model_revision':inventory['revision'],'archive_sha256':archive_sha256,
            'inventory_sha256':file_sha(inventory_path),'verified_files':seen,
            'metadata_only_appledouble_sidecars':sidecars,
            'excluded_huggingface_download_cache':cache,
            'canonical_materialization_performed':materialize_dir is not None,
            'scope':'CPU archive byte verification only; no model loading or training'}
    result['evidence_sha256']=canonical_sha(result)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive',type=Path,required=True)
    parser.add_argument('--inventory',type=Path,required=True)
    parser.add_argument('--archive-sha256',required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--materialize-dir',type=Path)
    args=parser.parse_args()
    if args.output.exists(): raise ValueError('unused evidence path required')
    record=verify(args.archive,args.inventory,args.archive_sha256,args.materialize_dir)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open('x') as handle: json.dump(record,handle,indent=2,sort_keys=True);handle.write('\n')
    print(json.dumps({'status':'passed','files_verified':len(record['verified_files']),
                      'metadata_sidecars':len(record['metadata_only_appledouble_sidecars']),
                      'evidence_sha256':record['evidence_sha256']}))
