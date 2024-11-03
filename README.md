# Data-Engineering-Project-Big-Data



# Data Engineering Project - Docker Services

## Building and Running Docker Services

### 1. Data Ingestion Service

#### Build the Docker Image
```bash
docker build -t data-ingestion-service -f skin/components/data_ingestion/Dockerfile .

#### Run the Data Ingestion Container
docker run -it --rm \
    --name data-ingestion-container-new \
    -v "${PWD}/key.json:/app/key.json:ro" \
    -v "${PWD}/artifacts:/app/artifacts" \
    -e GOOGLE_APPLICATION_CREDENTIALS=/app/key.json \
    -e GOOGLE_CLOUD_PROJECT=starlit-byway-436420-s9 \
    data-ingestion-service


Parameters Explained:
-it: Interactive terminal
--rm: Remove container after execution
--name: Container name
-v: Volume mounts
    key.json: Google Cloud credentials (read-only)
    artifacts: Output directory for processed data
-e: Environment variables
GOOGLE_APPLICATION_CREDENTIALS: Path to credentials inside container
GOOGLE_CLOUD_PROJECT: Your Google Cloud project ID
