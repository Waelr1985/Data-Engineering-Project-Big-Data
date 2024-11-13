import os
import sys
import logging
import zipfile
from gcloud import GCloud
from pyspark.sql import SparkSession
from pyspark.ml.classification import RandomForestClassificationModel
from pyspark.ml.feature import VectorAssembler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelPredictor:
    def __init__(self):
        self.gcloud = GCloud()
        self.model_dir = "/app/artifacts/imported_model"
        self.bucket_name = "skin-cancer-dataset-bucket"
        self.model_path = "model.zip"
        
        # Check directory exists and is writable
        if not os.path.exists(self.model_dir):
            os.makedirs(self.model_dir, exist_ok=True)
            logger.info(f"Created directory: {self.model_dir}")
        
        if not os.access(self.model_dir, os.W_OK):
            logger.error(f"Directory {self.model_dir} is not writable")
            raise PermissionError(f"Cannot write to {self.model_dir}")
            
        logger.info(f"Directory status - exists: {os.path.exists(self.model_dir)}, writable: {os.access(self.model_dir, os.W_OK)}")
        
        self.spark = (SparkSession.builder
            .appName("SkinSegmentation")
            .config("spark.driver.memory", "2g")
            .getOrCreate())
            
        self.assembler = VectorAssembler(
            inputCols=["R", "G", "B"],
            outputCol="features"
        )
        
        self.prediction_labels = {
            0.0: "Non-Skin Pixel",
            1.0: "Skin Pixel"
        }
    
    def download_model(self):
        try:
            zip_path = os.path.join(self.model_dir, self.model_path)
            logger.info(f"Attempting to download model to: {zip_path}")
            
            self.gcloud.sync_folder_from_gcloud(
                bucket_name=self.bucket_name,
                filename=self.model_path,
                destination=zip_path
            )
            logger.info("Model download completed successfully")
            
            # List directory contents before extraction
            logger.info(f"Directory contents before extraction: {os.listdir(self.model_dir)}")
            
            model_extract_path = os.path.join(self.model_dir, "model")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(model_extract_path)
            logger.info(f"Model extracted to {model_extract_path}")
            
            # List contents after extraction
            logger.info(f"Directory contents after extraction: {os.listdir(model_extract_path)}")
            
        except Exception as e:
            logger.error(f"Error in download_model: {str(e)}")
            raise

    def predict(self, r, g, b):
        try:
            data = [(float(r), float(g), float(b))]
            df = self.spark.createDataFrame(data, ["R", "G", "B"])
            df_assembled = self.assembler.transform(df)
            
            model_path = os.path.join(self.model_dir, "model")
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model directory not found at {model_path}")
                
            logger.info(f"Loading model from {model_path}")
            model = RandomForestClassificationModel.load(model_path)
            prediction = model.transform(df_assembled).select("prediction").collect()[0][0]
            
            result = {
                "numerical_prediction": float(prediction),
                "classification": self.prediction_labels.get(prediction, "Unknown"),
                "description": "Classification of pixel as skin or non-skin based on RGB values"
            }
            return result
            
        except Exception as e:
            logger.error(f"Error during prediction: {str(e)}")
            raise

if __name__ == "__main__":
    try:
        logger.info("Starting ModelPredictor...")
        predictor = ModelPredictor()
        
        logger.info("Verifying bucket access...")
        if not predictor.gcloud.verify_bucket_access(predictor.bucket_name):
            raise Exception(f"Cannot access bucket: {predictor.bucket_name}")
        
        logger.info("Downloading model...")
        predictor.download_model()
        
        try:
            r = int(os.environ.get('R'))
            g = int(os.environ.get('G'))
            b = int(os.environ.get('B'))
            
            if not all(0 <= val <= 255 for val in [r, g, b]):
                raise ValueError("RGB values must be between 0 and 255")
                
            logger.info(f"Analyzing pixel with RGB values - R:{r} G:{g} B:{b}")
            
            result = predictor.predict(r, g, b)
            logger.info("Analysis Results:")
            logger.info(f"Classification: {result['classification']}")
            logger.info(f"Raw Score: {result['numerical_prediction']}")
            
        except TypeError:
            logger.error("RGB values not provided. Please set R, G, and B environment variables")
            sys.exit(1)
        except ValueError as ve:
            logger.error(f"Invalid RGB values: {str(ve)}")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        sys.exit(1)