FROM nvidia/cuda:12.4.0-runtime-ubuntu22.04

COPY . app/

WORKDIR /app

ENV CUDAToolkit_ROOT="/usr/local/cuda-12.4/bin/nvcc"

ENV CMAKE_ARGS="-DGGML_CUDA=on"

ENV GGML_CUDA="on"

RUN apt-get update && apt-get install -y \
    python3.10 \
    python3.10-venv \
    python3-pip \
    build-essential \
    cmake \
    ccache \
    curl
    
RUN python3 -m venv venv
    
RUN . venv/bin/activate && pip install llama-cpp-python \
--extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu124 \
&& pip install -r requirements.txt

EXPOSE 3550:3550

CMD . venv/bin/activate && python3 api.py