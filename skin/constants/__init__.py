import os
from datetime import datetime

TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")


local_directory = "E:\\"
ARTIFACTS_DIR = os.path.join("artifacts", TIMESTAMP)
LOGS_DIR = "logs"
LOGS_FILE_NAME = "skin.log"
MODELS_DIR = "models"
BEST_MODEL_DIR = "best_model"

# data ingestion 
BUCKET_NAME = "skin-segmentation"
GCP_DATA_FILE_NAME = "skin.zip"
CSV_DATA_FILE_NAME = "skin.csv"
GCP_MODEL_NAME = "model.pt"

DATA_INGESTION_ARTIFACTS_DIR = "DataIngestionArtifacts"