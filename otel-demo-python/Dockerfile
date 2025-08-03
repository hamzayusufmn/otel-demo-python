FROM python:3.8-slim-bookworm

WORKDIR /python-docker

COPY requirements.txt .

RUN apt-get update && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir -r requirements.txt

RUN opentelemetry-bootstrap -a install

COPY . .

CMD ["opentelemetry-instrument", "flask", "run" , "-h", "0.0.0.0", "-p", "3000"]
