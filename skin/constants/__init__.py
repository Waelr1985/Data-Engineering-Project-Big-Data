import os
from datetime import datetime

TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")


file_url = "https://storage.googleapis.com/kaggle-data-sets/5999486/9790967/bundle/archive.zip?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com@kaggle-161607.iam.gserviceaccount.com/20241103/auto/storage/goog4_request&X-Goog-Date=20241103T001843Z&X-Goog-Expires=259200&X-Goog-SignedHeaders=host&X-Goog-Signature=510f1247d8b605eaf88d006725c2d7e145f640b9db4122939fddc8ca319c0c91338929ce1558c51e5fe3aab617d4dca2391d475734db43acbd4918eb0e224f5c6e98832cd4fc6c45c7619b6b6f45ab2497e30bc98fd58da89fe609a8da5edd239bede7dea39da59c64bb0d7d6a9f17495ac9b180c146ad27ac10f4aa69667579c34e1d86587ff6cd8243b71ba0542507cc642706c16acd99b7f30816109fe58e3b609478c9b6f21084964f1acdc015841f41aef20b8cb29f918c89df750522bc58de92c06002c494a491fd857cb0af87a61fd61c58517a28c2aed7e2afb5ce6942d28c27f10fb7d3ed9f95ee11c26a710012807798874328d51d378010f46b0c"  
ARTIFACTS_DIR = os.path.join("artifacts", TIMESTAMP)
LOGS_DIR = "logs"
LOGS_FILE_NAME = "skin.log"
MODELS_DIR = "models"
BEST_MODEL_DIR = "best_model"

# data ingestion 
BUCKET_NAME = "skin-cancer-dataset-bucket"
GCP_DATA_FILE_NAME = "skin.zip"
CSV_DATA_FILE_NAME = "skin.csv"
GCP_MODEL_NAME = "model.pt"

DATA_INGESTION_ARTIFACTS_DIR = "DataIngestionArtifacts"