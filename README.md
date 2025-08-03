# otel-demo-python

### 1. Build and run the Flask app

1. **Build the Docker image** for the app.  This will install the Python dependencies and set up the OpenTelemetry bootstrap process:

   docker build -t flaskapp:v1 .

   docker run -dit -p 3000:3000 flaskapp:v1

   docker network create my-net

docker run -dit \
  --name otel-lgtm \
  --network my-net \
  -p 3000:3000  # Grafana UI
  -p 4317:4317  # OTLP/gRPC
  -p 4318:4318  # OTLP/HTTP
  grafana/otel-lgtm


docker run -dit \
  --name flask \
  --network my-net \
  -p 3010:3000  # expose app at localhost:3010
  -e OTEL_TRACES_EXPORTER=otlp \
  -e OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=http://otel-lgtm:4317 \
  -e OTEL_METRICS_EXPORTER=otlp \
  -e OTEL_EXPORTER_OTLP_METRICS_ENDPOINT=http://otel-lgtm:4317 \
  -e OTEL_LOGS_EXPORTER=otlp \
  -e OTEL_EXPORTER_OTLP_LOGS_ENDPOINT=http://otel-lgtm:4317 \
  -e OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true \
  -e OTEL_SERVICE_NAME=flask-app \
  flaskapp:v1

