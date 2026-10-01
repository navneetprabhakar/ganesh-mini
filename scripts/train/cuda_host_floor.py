"""Versioned Gate 3 CUDA-visible memory contract for nominal 24-GB L4."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

L4_USABLE_BYTES = 22 * 1024**3
OTHER_GPU_BYTES = 24_000_000_000
CONTRACT = 'ganesh-mini-gate3-l4-usable-v1'


def assess_cuda_host(torch, output: Path | None = None) -> dict:
    available = bool(torch.cuda.is_available())
    count = int(torch.cuda.device_count()) if available else 0
    props = torch.cuda.get_device_properties(0) if count == 1 else None
    name = props.name if props is not None else None
    actual = int(props.total_memory) if props is not None else None
    bf16 = bool(torch.cuda.is_bf16_supported()) if props is not None else False
    required = L4_USABLE_BYTES if name == 'NVIDIA L4' else OTHER_GPU_BYTES
    rule = 'nominal-24gb-l4-usable-22gib' if name == 'NVIDIA L4' else 'other-gpu-literal-24gb'
    passed = count == 1 and bf16 and actual is not None and actual >= required
    report = {'schema_version': CONTRACT, 'status': 'passed' if passed else 'failed',
              'cuda_available': available, 'cuda_device_count': count,
              'gpu_name': name, 'cuda_visible_memory_bytes': actual,
              'bf16_supported': bf16, 'required_usable_memory_bytes': required,
              'selected_rule': rule,
              'scope': 'hardware preflight only; not model capacity or quality'}
    report['evidence_sha256'] = hashlib.sha256(json.dumps(report, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    if output is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open('x', encoding='utf-8') as handle:
            json.dump(report, handle, indent=2, sort_keys=True)
            handle.write('\n')
    if not passed:
        raise RuntimeError(f"CUDA host failed {CONTRACT}: {name}, {actual} visible bytes, BF16={bf16}, required={required}")
    return report
