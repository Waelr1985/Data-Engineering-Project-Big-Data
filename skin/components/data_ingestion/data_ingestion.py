import os
import sys
from skin.configuration.gcloud import GCloud
from skin.constants import *
from pathlib import Path
from zipfile import ZipFile
from skin.logger import logging
from skin.exception import SkinException

class DataIngestion:
    def __init__(self):
        self.bucket_name = BUCKET_NAME
        self.zip_file_name = GCP_DATA_FILE_NAME
        self.file_url = "https://storage.googleapis.com/kaggle-data-sets/5999486/9790967/bundle/archive.zip?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com@kaggle-161607.iam.gserviceaccount.com/20241103/auto/storage/goog4_request&X-Goog-Date=20241103T001843Z&X-Goog-Expires=259200&X-Goog-SignedHeaders=host&X-Goog-Signature=510f1247d8b605eaf88d006725c2d7e145f640b9db4122939fddc8ca319c0c91338929ce1558c51e5fe3aab617d4dca2391d475734db43acbd4918eb0e224f5c6e98832cd4fc6c45c7619b6b6f45ab2497e30bc98fd58da89fe609a8da5edd239bede7dea39da59c64bb0d7d6a9f17495ac9b180c146ad27ac10f4aa69667579c34e1d86587ff6cd8243b71ba0542507cc642706c16acd99b7f30816109fe58e3b609478c9b6f21084964f1acdc015841f41aef20b8cb29f918c89df750522bc58de92c06002c494a491fd857cb0af87a61fd61c58517a28c2aed7e2afb5ce6942d28c27f10fb7d3ed9f95ee11c26a710012807798874328d51d378010f46b0c"
        self.gcloud = GCloud()
        
        # Create artifact directories
        self.artifacts_root = Path("artifacts")
        self.raw_data_dir = self.artifacts_root / "raw_data"
        self.extracted_data_dir = self.artifacts_root / "extracted_data"
        self._create_directories()

    def _create_directories(self):
        """Create necessary directories"""
        os.makedirs(self.artifacts_root, exist_ok=True)
        os.makedirs(self.raw_data_dir, exist_ok=True)
        os.makedirs(self.extracted_data_dir, exist_ok=True)
        logging.info(f"Created directories: {self.artifacts_root}, {self.raw_data_dir}, {self.extracted_data_dir}")

    def extract_data(self, input_file_path: str, output_file_path: str) -> None:
        """Extract the zip file"""
        logging.info("Extracting zip file")
        try:
            with ZipFile(input_file_path, "r") as zip_ref:
                zip_ref.extractall(path=output_file_path)
            logging.info(f"Successfully extracted zip to {output_file_path}")
        except Exception as e:
            logging.error(f"Error extracting zip file: {str(e)}")
            raise SkinException(e, sys) from e

    def upload_zip_to_gcloud_from_url(self):
        """Execute the data ingestion pipeline"""
        try:
            logging.info("Starting data ingestion pipeline")
            
            # Step 1: Download from URL and upload to GCloud
            self.gcloud.download_from_url_and_upload_to_gcloud(
                self.file_url, 
                self.bucket_name, 
                self.zip_file_name
            )
            
            # Step 2: Download from GCloud to local artifacts
            local_zip_path = self.raw_data_dir / self.zip_file_name
            self.gcloud.sync_folder_from_gcloud(
                self.bucket_name,
                self.zip_file_name,
                local_zip_path
            )
            
            # Step 3: Extract zip file
            self.extract_data(
                str(local_zip_path),
                str(self.extracted_data_dir)
            )
            
            logging.info("Data ingestion pipeline completed successfully")
            
        except Exception as e:
            logging.error(f"Error in data ingestion pipeline: {str(e)}")
            raise SkinException(e, sys) from e

if __name__ == "__main__":
    try:
        logging.info("Starting data ingestion process")
        uploader = DataIngestion()
        uploader.upload_zip_to_gcloud_from_url()
        logging.info("Data ingestion completed successfully")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise