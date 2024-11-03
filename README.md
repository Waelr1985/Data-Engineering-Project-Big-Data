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


# Data Ingestion Service

## How to use this container

# just need to run this command:
docker pull waelr1985/data-ingestion-service:latest


1. Download your Google Cloud service account key as `key.json`

2. Run the container:
```bash
docker run -it --rm \
    --name data-ingestion-container-new \
    -v "/your/path/to/key.json:/app/key.json:ro" \
    -v "/your/path/to/artifacts:/app/artifacts" \
    -e GOOGLE_APPLICATION_CREDENTIALS=/app/key.json \
    -e GOOGLE_CLOUD_PROJECT=your-project-id \
    yourusername/data-ingestion-service


Requirements:

Docker installed
Google Cloud service account key
Access to Google Cloud Storage