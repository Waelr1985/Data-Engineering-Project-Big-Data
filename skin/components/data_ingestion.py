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
zip_file_name = GCP_DATA_FILE_NAME  

# Create an instance of the DataUploader class
uploader = DataUploader(bucket_name, local_directory, zip_file_name)

# Call the upload method
uploader.upload_zip_to_gcloud()


class DataIngestion:
    def __init__(
        self, data_ingestion_config: DataIngestionConfig, gcloud: GCloud
    ) -> None:
        self.data_ingestion_config = data_ingestion_config
        self.gcloud = gcloud


    def get_data_from_gcp(self, bucket_name: str, file_name: str, path: str) -> ZipFile:
        logging.info("Entered the get_data_from_gcp method of data ingestion class")
        try:
            self.gcloud.sync_folder_from_gcloud(
                gcp_bucket_url=bucket_name, filename=file_name, destination=path
            )
            logging.info("Exited the get_data_from_gcp method of data ingestion class")

        except Exception as e:
            raise SkinException(e, sys) from e


    def extract_data(self, input_file_path: str, output_file_path: str) -> None:
        logging.info("Entered the extract_data method of Data ingestion class")
        try:
            # loading the temp.zip and creating a zip object
            with ZipFile(input_file_path, "r") as zObject:

                # Extracting all the members of the zip
                # into a specific location.
                zObject.extractall(path=output_file_path)
            logging.info("Exited the extract_data method of Data ingestion class")

        except Exception as e:
            raise SkinException(e, sys) from e


    def initiate_data_ingestion(self) -> DataIngestionArtifacts:
        logging.info(
            "Entered the initiate_data_ingestion method of data ingestion class"
        )
        try:
            # Creating Data Ingestion Artifacts directory inside artifacts folder
            os.makedirs(
                self.data_ingestion_config.data_ingestion_artifacts_dir, exist_ok=True
            )
            logging.info(
                f"Created {os.path.basename(self.data_ingestion_config.data_ingestion_artifacts_dir)} directory."
            )

            # Getting data from GCP
            self.get_data_from_gcp(
                bucket_name=BUCKET_NAME,
                file_name=GCP_DATA_FILE_NAME,
                path=self.data_ingestion_config.gcp_data_file_path,
            )
            logging.info(
                f"Got the file from Google cloud storage. File name - {os.path.basename(self.data_ingestion_config.gcp_data_file_path)}"
            )

            # Extracting the data file
            self.extract_data(
                input_file_path=self.data_ingestion_config.gcp_data_file_path,
                output_file_path=self.data_ingestion_config.output_file_path,
            )
            logging.info(f"Extracted the data from zip file.")

            data_ingestion_artifact = DataIngestionArtifacts(
                zip_data_file_path=self.data_ingestion_config.gcp_data_file_path,
                csv_data_file_path=self.data_ingestion_config.csv_data_file_path,
            )
            logging.info("Exited the initiate_data_ingestion method of data ingestion class")
            return data_ingestion_artifact

        except Exception as e:
            raise SkinException(e, sys) from e