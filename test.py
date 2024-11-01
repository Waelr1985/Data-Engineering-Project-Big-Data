import os
import sys
from zipfile import ZipFile
from skin.configuration.gcloud import GCloud
from skin.constants import *
from skin.entity.artifact_entity import DataIngestionArtifacts
from skin.entity.config_entity import DataIngestionConfig
from skin.exception import SkinException
from skin.logger import logging
import logging


class DataUploader:
    def __init__(self, bucket_name: str, local_directory: str, zip_file_name: str):
        self.bucket_name = bucket_name
        self.local_directory = local_directory
        self.zip_file_name = zip_file_name
        self.gcloud = GCloud()

    def upload_zip_to_gcloud(self):
        logging.info(f"Starting upload of {self.zip_file_name} to bucket {self.bucket_name}")
        self.gcloud.sync_folder_to_gcloud(self.bucket_name, self.local_directory, self.zip_file_name)
        logging.info(f"Upload of {self.zip_file_name} completed successfully")

# Example usage
bucket_name = BUCKET_NAME  
zip_file_name = "skin1.zip"  

# Create an instance of the DataUploader class
uploader = DataUploader(bucket_name, local_directory1, zip_file_name)

# Call the upload method
uploader.upload_zip_to_gcloud()