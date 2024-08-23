FROM ubuntu:22.04

COPY . app/

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

RUN apt-get update && apt-get install -y \
    python3.10 \
    python3.10-venv \
    python3-pip \
    build-essential \
    cmake \
    ccache \
    curl \
    git \
    pkg-config \
    libopenblas-dev \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv venv

ENV PATH="/app/venv/bin:$PATH"

RUN pip install --upgrade pip setuptools wheel

# Install llama-cpp-python from source
RUN CMAKE_ARGS="-DGGML_BLAS=ON -DGGML_BLAS_VENDOR=OpenBLAS" pip install llama-cpp-python --no-binary llama-cpp-python

# Install other requirements
RUN pip install -r requirements.txt

EXPOSE 6550:6550

CMD ["python3", "api.py"]