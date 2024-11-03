import os
from pathlib import Path
import time
import requests
import logging
from google.cloud import storage
import tempfile

class GCloud:
    def __init__(self):
        self.artifacts_root = Path("artifacts")
        self.raw_data_dir = self.artifacts_root / "raw_data"
        self.create_artifact_dirs()
        self._verify_gcp_auth()
        
    def create_artifact_dirs(self):
        """Create the necessary artifact directories"""
        os.makedirs(self.artifacts_root, exist_ok=True)
        os.makedirs(self.raw_data_dir, exist_ok=True)
        logging.info(f"Created artifact directories at {self.artifacts_root}")

    def _verify_gcp_auth(self):
        """Verify GCP authentication"""
        try:
            credentials_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
            if not credentials_path:
                raise Exception("GOOGLE_APPLICATION_CREDENTIALS environment variable not set")
            if not os.path.exists(credentials_path):
                raise Exception(f"Credentials file not found at {credentials_path}")
            
            storage_client = storage.Client()
            logging.info("Successfully authenticated with GCP using service account")
        except Exception as e:
            logging.error(f"GCP Authentication failed: {str(e)}")
            raise

    def sync_folder_to_gcloud(self, bucket_name, filepath, filename):
        """Upload file to GCS bucket"""
        try:
            logging.info(f"Uploading {filename} to GCS bucket: {bucket_name}")
            storage_client = storage.Client()
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(filename)
            
            full_path = os.path.join(filepath, filename)
            blob.upload_from_filename(full_path)
            logging.info(f"Successfully uploaded to GCS bucket: {bucket_name}")
        except Exception as e:
            logging.error(f"Error in sync_folder_to_gcloud: {str(e)}")
            raise

    def sync_folder_from_gcloud(self, bucket_name, filename, destination):
        """Download file from GCS bucket"""
        try:
            logging.info(f"Downloading {filename} from GCS bucket: {bucket_name}")
            storage_client = storage.Client()
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(filename)
            
            blob.download_to_filename(destination)
            logging.info(f"Successfully downloaded from GCS to: {destination}")
        except Exception as e:
            logging.error(f"Error in sync_folder_from_gcloud: {str(e)}")
            raise

    def download_from_url_and_upload_to_gcloud(self, file_url, bucket_name, filename):
        """Download from URL and upload to GCS"""
        try:
            logging.info(f"Downloading from URL: {file_url}")
            response = requests.get(file_url)
            response.raise_for_status()
            
            # Create temp directory
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_file = os.path.join(temp_dir, filename)
                
                # Save to temp file
                with open(temp_file, 'wb') as f:
                    f.write(response.content)
                logging.info(f"Downloaded to temporary file: {temp_file}")
                
                # Upload to GCS
                self.sync_folder_to_gcloud(bucket_name, temp_dir, filename)
                logging.info("Upload to GCS completed")
                
        except Exception as e:
            logging.error(f"Error in download_from_url_and_upload_to_gcloud: {str(e)}")
            raise

    def verify_bucket_access(self, bucket_name):
        """Verify bucket exists and is accessible"""
        try:
            storage_client = storage.Client()
            bucket = storage_client.bucket(bucket_name)
            if not bucket.exists():
                logging.warning(f"Bucket {bucket_name} does not exist")
                return False
            return True
        except Exception as e:
            logging.error(f"Error verifying bucket access: {str(e)}")
            return False