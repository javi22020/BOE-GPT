FROM python:3.10

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git

COPY . /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN CMAKE_ARGS="-DGGML_CUDA=on" pip install llama-cpp-python

EXPOSE 4550

CMD ["python", "llm_api.py"]