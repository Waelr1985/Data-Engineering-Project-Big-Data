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
file_url = "https://storage.googleapis.com/kaggle-data-sets/5999486/9790967/bundle/archive.zip?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com@kaggle-161607.iam.gserviceaccount.com/20241123/auto/storage/goog4_request&X-Goog-Date=20241123T233623Z&X-Goog-Expires=259200&X-Goog-SignedHeaders=host&X-Goog-Signature=0e7a735a913bc83b88f88e6011a23e0765de070dcfcfac3f6942b858b30b53848ae6735255109c47305700e8476cce47e1cd1b239790e9945828deae664db17336e877303f0f3fee3977a3ea1b334abbd7f8e84097765226dfd021652f58cf48092a9a84a6b4634992054edf47b4d95bd8a888fc64947e8d490e4101285feb2c911f14bcc3aeced2baa5c5328de603abf1e311d24080483d823ed1cb04fd7d023b8d439c0b914c2608adf9d92a92fe5a5cec552131749549c3843a7d667e2113519f095eacd26144daaac84ad0388853cf497687e0aab12747f50a1838385b913a24f060f6768bdc02a8cdbb9ac015ee19510281f824659e3e92c1b039562a4a"
