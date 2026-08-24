# syntax=docker/dockerfile:1.8
ARG CUDA_IMAGE=docker.io/nvidia/cuda:13.0.1-cudnn-devel-ubuntu24.04@sha256:8b2705ea7a8653ad3451b46ab835eced92d77b44e671b9cf3ad4f95fbb2efe5e
FROM ${CUDA_IMAGE}

ARG UV_VERSION=0.11.11
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    UV_PROJECT_ENVIRONMENT=/opt/ganesh-venv \
    MAX_JOBS=1 \
    TORCH_CUDA_ARCH_LIST=8.0+PTX \
    PATH=/opt/ganesh-venv/bin:${PATH}

RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential ca-certificates git ninja-build python3.12 python3.12-dev python3-pip \
    && rm -rf /var/lib/apt/lists/* \
    && python3.12 -m pip install --break-system-packages --no-cache-dir "uv==${UV_VERSION}"

WORKDIR /opt/ganesh-build
COPY pyproject.toml uv.lock ./
# uv.lock is the package lock. Keeping compilation in this CUDA devel image is
# necessary for causal-conv1d; runtime qualification records the resulting
# package and CUDA identities before accepting any result.
RUN uv sync --frozen --no-dev --no-install-project --extra train-candidate \
      --no-install-package causal-conv1d \
    && uv pip install --no-build-isolation --no-deps \
      'https://files.pythonhosted.org/packages/f4/d1/eba27735f31bd5527d39a3c7f693e6ded7b844cab275db719a15ad37b6cd/causal_conv1d-1.7.0.tar.gz#sha256=3202758494eaa7b597ce1c282dfa188889506bfcb92cad3c407d26736bfcd32b' \
    && python - <<'PY'
from importlib.metadata import version
expected = {
    "torch": "2.13.0",
    "torchvision": "0.28.0",
    "transformers": "5.15.1",
    "peft": "0.19.1",
    "ms-swift": "4.5.2",
    "bitsandbytes": "0.49.2",
    "flash-linear-attention": "0.5.2",
    "causal-conv1d": "1.7.0",
    "liger-kernel": "0.8.2",
}
observed = {name: version(name) for name in expected}
assert observed == expected, (observed, expected)
import torchvision
import qwen_vl_utils
from liger_kernel.transformers import apply_liger_kernel_to_qwen3_5
from peft import LoraConfig
from swift.model import get_model_info_meta
from transformers import AutoModelForImageTextToText
assert torchvision.__version__.split('+', 1)[0] == expected["torchvision"]
assert qwen_vl_utils and apply_liger_kernel_to_qwen3_5 and LoraConfig and get_model_info_meta and AutoModelForImageTextToText
PY

WORKDIR /workspace
ENTRYPOINT ["python", "/workspace/scripts/cuda/qualify.py"]
