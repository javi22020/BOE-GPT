FROM python:3.10-slim

FROM nvidia/cuda:12.6.0-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

COPY . /app

ENV PATH=/usr/local/cuda/bin:${PATH}
ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:${LD_LIBRARY_PATH}
ENV CUDAToolkit_ROOT=/opt/cuda/bin/nvcc

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3.10-venv \
    build-essential \
    cmake \
    ccache \
    git \
    && rm -rf /var/lib/apt/lists/*

ENV CMAKE_ARGS="-DGGML_CUDA=on"

RUN python3 -m venv venv

RUN . venv/bin/activate

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5550:5550

CMD ["python3", "chroma_server.py"]