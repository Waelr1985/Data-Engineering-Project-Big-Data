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
file_url = "https://storage.googleapis.com/kaggle-data-sets/5999486/9790967/bundle/archive.zip?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com@kaggle-161607.iam.gserviceaccount.com/20241119/auto/storage/goog4_request&X-Goog-Date=20241119T100952Z&X-Goog-Expires=259200&X-Goog-SignedHeaders=host&X-Goog-Signature=7c652ffb81840a338c2b3eb1f878c5b7f832cbba49627371130e68bf15fbafd9fbe00a222de304461334b9c28ece64cd86fec9601c01a9d2c1719eb034175848162b39d94bc3ced9ffcfda1909e928f9682f4c174abfe10949dfdc8d97eff552c6e65e469898a6dcfacb65163ffeb29432975fd4a748fab02e613148e9f0f6c5b8f9fcbbb9d07830218e0159ef8ecec1f2fc7b92cf5321967ee9aa5733b7d2cd3a7ecf311287ed62e9b8baa365d97df42971239a08ef9f14784249e5f4c0d89b387a78f48ffc6a41f37f7e9a404309750208fcc894f41c02fd1004b1d0dba2bba26e5f78661efc14265c15c984311b7e1a839e6cf6e43b543957e54b5d2bd4cc"
