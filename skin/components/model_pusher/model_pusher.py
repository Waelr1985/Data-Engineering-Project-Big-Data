import os
import logging
import shutil
from pathlib import Path
from skin.configuration.gcloud import GCloud

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ModelPusher:
    def __init__(self):
        self.gcloud = GCloud()
        self.artifacts_dir = Path("artifacts")
        self.model_dir = self.artifacts_dir / "model"
        self.bucket_name = "skin-cancer-dataset-bucket"
        
    def push_model_to_gcp(self):
        try:
            logger.info("Starting model pushing process")
            
            if not os.path.exists(self.model_dir):
                raise Exception(f"Model directory not found at {self.model_dir}")
            
            if not self.gcloud.verify_bucket_access(self.bucket_name):
                raise Exception(f"Cannot access bucket: {self.bucket_name}")
            
            # Create a temporary directory for zipping
            temp_dir = self.artifacts_dir / "temp"
            os.makedirs(temp_dir, exist_ok=True)
            
            # Create zip file of model
            model_path = self.model_dir / "random_forest_model"
            zip_path = temp_dir / "model.zip"
            
            if os.path.exists(model_path):
                shutil.make_archive(
                    str(temp_dir / "model"),  # prefix for the zip file
                    'zip',                    # archive format
                    model_path               # directory to zip
                )
                
                # Upload the zip file
                logger.info(f"Pushing zipped model to GCS")
                self.gcloud.sync_folder_to_gcloud(
                    bucket_name=self.bucket_name,
                    filepath=str(temp_dir),
                    filename="model.zip"
                )
                
                # Clean up
                if os.path.exists(zip_path):
                    os.remove(zip_path)
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
                    
                logger.info("Model pushing completed successfully")
                return True
            else:
                raise Exception(f"Model not found at {model_path}")
            
        except Exception as e:
            logger.error(f"Error in pushing model: {str(e)}")
            raise

if __name__ == "__main__":
    try:
        pusher = ModelPusher()
        pusher.push_model_to_gcp()
    except Exception as e:
        logger.error(f"Model pushing failed: {str(e)}")
        raise
