# Data-Engineering-Project-Big-Data

This repository contains Microservices for Skin Segmentation Machine Learning Application. The dataset is designed for skin detection and segmentation in computer vision applications. It contains RGB color values extracted from face images of individuals across different age groups, races, and genders.

## Folder structure

![alt text](<folder structure.png>)

=====================================

## Prerequisites
- [Docker](https://www.docker.com/get-started)
- [Python 3.7+](https://www.python.org/downloads/) (only for local development)
- Google Cloud Platform Account
- GCP Service Account with necessary permissions

## GCP Setup Instructions

![alt text](<GCP Bucket.png>)
=====================================
### 1. Create a GCP Project
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Click "New Project" and create a project
3. Note your Project ID (you'll need this later)

### 2. Create a Storage Bucket
1. Navigate to Cloud Storage in GCP Console
2. Click "Create Bucket"
3. Choose a unique name for your bucket
4. Select your preferred location
5. Choose storage class (Standard recommended)
6. Click "Create"

### 3. Set Up Authentication
1. Navigate to "IAM & Admin" > "Service Accounts"
2. Click "Create Service Account"
3. Name your service account and click "Create"
4. Add roles:
   - Storage Object Viewer
   - Storage Object Creator
5. Click "Create Key"
   - Choose JSON format
   - Save the downloaded key.json file
6. Move the key.json file to your project root directory

## Microservices Setup and Deployment

## Microservices Architecture Overview

### What is Microservices Architecture?
This project implements a microservices architecture, where the application is structured as a collection of loosely coupled, independently deployable services. Each service handles a specific task capability and communicates with other services through well-defined APIs.

### Architecture Components

#### 1. Data Pipeline Services
- **Data Ingestion Service**: Handles initial data collection and storage using GCP
- **Data Validation Service**: Ensures data quality and consistency
- **Data Transformation Service**: Preprocesses and transforms raw data
- **Model Training Service**: Manages ML model training process
- **Model Evaluation Service**: Assesses model performance
- **Model Pusher Service**: Deploys trained models to GCP
- **Model Predictor Service**: Handles the predictions

#### 2. API Service
- **FastAPI Application**: Provides RESTful API endpoints for client interactions

### Key Benefits of Our Architecture
1. **Independent Deployment**
   - Each service can be deployed independently
   - Enables continuous deployment and integration
   - Reduces deployment risks

2. **Scalability**
   - Services can scale independently based on demand
   - Efficient resource utilization
   - Better handling of varying workloads

3. **Technology Flexibility**
   - Each service can use the most appropriate technology stack
   - Independent development and testing
   - Easier maintenance and updates

4. **Fault Isolation**
   - Issues in one service don't directly affect others
   - Enhanced system reliability
   - Easier debugging and maintenance

### Service Communication
![alt text](<flow charts.png>)

# Start all services
docker-compose up
this command will start all the services and we can access the app service by going to http://localhost:8000 in the browser.


# Start specific service
docker-compose up <service_name>

# Start in detached mode
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs

# View logs for specific service
docker-compose logs <service_name>

# Remove all containers and networks
docker-compose down --volumes

# Check service status
docker-compose ps


---

## Service Architecture Overview
This application consists of multiple microservices that work together to create an end-to-end machine learning pipeline. Each service can be built and run individually using Docker containers.


## Services

**Build the Service:**


### Data Ingestion Service
The Data Ingestion Service is responsible for downloading data from GCP after uploading it from external resource (e.g., Kaggle), and in local machine it will be saved in artifacts folder

```bash
# Build Docker image
docker build -t data-ingestion-service -f skin/components/data_ingestion/Dockerfile .


# Push to Docker Hub
docker tag data-ingestion-service waelr1985/data-ingestion-service:latest
docker push waelr1985/data-ingestion-service:latest

# Run Data Ingestion container
docker run -it --rm \
    --name data-ingestion-container-new \
    -v "${PWD}/key.json:/app/key.json:ro" \
    -v "${PWD}/artifacts:/app/artifacts" \
    -e GOOGLE_APPLICATION_CREDENTIALS=/app/key.json \
    -e GOOGLE_CLOUD_PROJECT=starlit-byway-436420-s9 \
    waelr1985/data-ingestion-service

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


## How to use this container
# just need to run this command:
docker pull waelr1985/data-ingestion-service:latest
```

### Data Validation Service
Check the quality of the data including data drift, and saving the report in artifacts folder

```bash
# Build Docker image
docker build -t data-validation-service -f skin/components/data_validation/Dockerfile .


# Push to Docker Hub
docker tag data-validation-service waelr1985/data-validation-service
docker push waelr1985/data-validation-service:latest

#### Run the Data Validation Container
docker run -it \
    -v "D:\Data-Engineering-Project-Big-Data\artifacts:/app/artifacts" \
    -v "D:\Data-Engineering-Project-Big-Data\config:/app/config" \
    --name data-validation waelr1985/data-validation-service

## How to use this container
# just need to run this command:
docker pull waelr1985/data-validation-service:latest
```

#### Data Transformation Service
Splitting the dataset into train and test sets for building Machine Learning Model, and saving the splitted data in artifacts folder.

```bash
# Build Docker image
docker build -t waelr1985/data-transformation-service -f skin/components/data_transformation/Dockerfile .

# Push to Docker Hub
docker tag data-transformation-service waelr1985/data-transformation-service:latest
docker push waelr1985/data-transformation-service:latest


#### Run the Data Transformation Container
docker run -v "D:/Data-Engineering-Project-Big-Data/artifacts:/app/artifacts" waelr1985/data-transformation-service

## How to use this container
# just need to run this command:
docker pull waelr1985/data-transformation-service:latest
```


#### Model Training Service
Using train dataset from artifacts folder to build ML model

```bash
# Build Docker image
docker build -t model-training-service -f skin/components/model_training/Dockerfile .

# Push to Docker Hub 
docker tag model-training-service waelr1985/model-training-service:latest
docker push waelr1985/model-training-service:latest


#### Run the Model Training Container
docker run -v "D:/Data-Engineering-Project-Big-Data/artifacts:/app/artifacts" waelr1985/model-training-service

## How to use this container
# just need to run this command:
docker pull waelr1985/model-training-service:latest
```

####  Model Evalaution Service
Evaluate the model and saving the evalaution metrics in artifacts folder

```bash
# Build Docker image
docker build -t model-evaluation-service -f skin/components/model_evaluation/Dockerfile .

# Push to Docker Hub 
docker tag model-evaluation-service waelr1985/model-evaluation-service:latest
docker push waelr1985/model-evaluation-service:latest

#### Run the Model Evaluation Container
docker run -v "D:/Data-Engineering-Project-Big-Data/artifacts:/app/artifacts" waelr1985/model-evaluation-service


## How to use this container
# just need to run this command:
docker pull waelr1985/model-evaluation-service:latest


Performance Metrics
The model achieves the following performance on the test set:
Accuracy: 97.23%
Precision: 97.32%
Recall: 97.23%
F1 Score: 97.26%
```

#### Model Pusher Service
Pusing the model from local machine (in artifacts folder) to GCP storage

```bash
# Build Docker image
docker build -t model-pusher-service -f skin/components/model_pusher/Dockerfile .

# Push to Docker Hub
docker tag model-pusher-service waelr1985/model-pusher-service
docker push waelr1985/model-pusher-service:latest


#### Run the Model Pusher Container
docker run -v "$(pwd)/artifacts:/app/artifacts" \
          -v "${PWD}/key.json:/app/key.json:ro"\
          -e GOOGLE_APPLICATION_CREDENTIALS=/app/key.json \
          -e GOOGLE_CLOUD_PROJECT=starlit-byway-436420-s9 \
          waelr1985/model-pusher-service


## How to use this container
# just need to run this command:
docker pull waelr1985/model-pusher-service:latest
```

#### Model Predictor Service
Downloading model from GCP to use it for prediction

```bash
# Build Docker image
docker build --no-cache -t model-predictor-service -f skin/components/model_predictor/Dockerfile .

# Push to Docker Hub
docker tag model-predictor-service waelr1985/model-predictor:latest
docker push waelr1985/model-predictor:latest


#### Run the Model Predictor Container
docker run -d --name model-predictor -e GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/key.json -v "D:\Data-Engineering-Project-Big-Data\key.json:/app/credentials/key.json" -v D:\Data-Engineering-Project-Big-Data\artifacts:/app/artifacts --env B=150 --env G=100 --env R=200 model-predictor-service



## How to use this container
# just need to run this command:
docker pull waelr1985/model-predictor:latest
```

#### app service
API for all services

```bash
# Build Docker image
docker build -t app .
OR 
docker build --no-cache -t app .

# Push to Docker Hub
docker tag app waelr1985/app
docker push waelr1985/app


#### Run APP Service Container                        
docker run -d -p 8000:8000 -v ${PWD}:/app/config -e GOOGLE_APPLICATION_CREDENTIALS=/app/key.json -e GOOGLE_CLOUD_PROJECT=starlit-byway-436420-s9 waelr1985/app:latest 


## How to use this container
# just need to run this command:
docker pull waelr1985/app:latest 
```
