import json
from types import SimpleNamespace
import pytest

from scripts.train.cuda_host_floor import assess_cuda_host, L4_USABLE_BYTES


def cuda(name='NVIDIA L4', memory=23_659_151_360, bf16=True, count=1):
    device=SimpleNamespace(name=name,total_memory=memory)
    return SimpleNamespace(cuda=SimpleNamespace(is_available=lambda: count>0,
        device_count=lambda: count, get_device_properties=lambda _: device,
        is_bf16_supported=lambda: bf16))


def test_l4_uses_explicit_visible_22_gib_floor(tmp_path):
    path=tmp_path/'hardware.json'
    report=assess_cuda_host(cuda(memory=L4_USABLE_BYTES),path)
    assert report['required_usable_memory_bytes']==L4_USABLE_BYTES
    assert report['status']=='passed' and json.loads(path.read_text())==report


@pytest.mark.parametrize('torch',[
    cuda(memory=L4_USABLE_BYTES-1),cuda(bf16=False),cuda(count=2),
    cuda(name='NVIDIA A100',memory=23_999_999_999),cuda(count=0)])
def test_failed_guard_preserves_separate_operands(tmp_path,torch):
    path=tmp_path/'hardware.json'
    with pytest.raises(RuntimeError,match='CUDA host failed'):
        assess_cuda_host(torch,path)
    body=json.loads(path.read_text())
    assert body['status']=='failed' and 'bf16_supported' in body and 'cuda_visible_memory_bytes' in body
