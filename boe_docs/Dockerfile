FROM nvidia/cuda:12.1.0-base-ubuntu22.04

COPY . app/

WORKDIR /app

ENV CMAKE_ARGS="-DGGML_CUDA=on"

RUN apt-get update && apt-get install -y \
    python3.10 \
    python3.10-venv \
    python3-pip \
    build-essential \
    cmake
    
RUN python3 -m venv venv
    
RUN . venv/bin/activate

RUN pip install llama-cpp-python \
--extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu121

RUN pip install -r requirements.txt

EXPOSE 6550:6550

CMD [ "python3", "api.py" ]



