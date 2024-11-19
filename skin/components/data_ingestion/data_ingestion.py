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
        self.file_url = file_url
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

    def initiate_data_ingestion(self):
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
        uploader.initiate_data_ingestion()
        logging.info("Data ingestion completed successfully")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise