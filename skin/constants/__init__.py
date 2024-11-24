import os
from datetime import datetime

TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

# Logging constants
LOGS_DIR = "logs"
LOGS_FILE_NAME = "running_logs.log"

# GCP constants
BUCKET_NAME = "skin-cancer-dataset-bucket"
GCP_DATA_FILE_NAME = "skin.zip"
CSV_DATA_FILE_NAME = "skin.csv"
GCP_MODEL_NAME = "model.zip"

# Artifacts
ARTIFACTS_DIR = os.path.join("artifacts", TIMESTAMP)
MODELS_DIR = "model"

# Data URL
file_url = "https://www.kaggle.com/api/v1/datasets/download/waelr1985/skin-segmentation?dataset_version_number=1"
