import os
import sys
import logging
import zipfile
import shutil
from skin.configuration.gcloud import GCloud
from pyspark.sql import SparkSession
from pyspark.ml.classification import RandomForestClassificationModel
from pyspark.ml.feature import VectorAssembler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelPredictor:
    def __init__(self):
        self.gcloud = GCloud()
        self.base_dir = "/app/artifacts"
        self.model_dir = os.path.join(self.base_dir, "imported_model")
        self.bucket_name = "skin-cancer-dataset-bucket"
        self.model_path = "model.zip"
        
        # Create all necessary directories
        os.makedirs(self.base_dir, exist_ok=True)
        os.makedirs(self.model_dir, exist_ok=True)
        
        # Initialize Spark
        self.spark = (SparkSession.builder
            .appName("SkinSegmentation")
            .config("spark.driver.memory", "2g")
            .config("spark.driver.maxResultSize", "1g")
            .config("spark.sql.shuffle.partitions", "2")
            .config("spark.memory.offHeap.enabled", "true")
            .config("spark.memory.offHeap.size", "1g")
            .config("spark.driver.host", "localhost")
            .config("spark.driver.bindAddress", "0.0.0.0")
            .getOrCreate())
            
        self.assembler = VectorAssembler(
            inputCols=["R", "G", "B"],
            outputCol="features"
        )
        
        self.prediction_labels = {
            0.0: "Non-Skin",
            1.0: "Skin"
        }
        
        # Download and extract model at initialization
        self.ensure_model_ready()
    
    def ensure_model_ready(self):
        """Download and extract model if not already present"""
        try:
            # Define paths
            model_dir = os.path.join(self.model_dir, "model")
            metadata_path = os.path.join(model_dir, "metadata")
            zip_path = os.path.join(self.model_dir, self.model_path)
            
            # Log current directory structure
            logger.info(f"Current directory structure:")
            logger.info(f"Base dir: {self.base_dir}")
            logger.info(f"Model dir: {self.model_dir}")
            logger.info(f"Zip path: {zip_path}")
            
            # Clean up existing files if metadata is missing
            if os.path.exists(model_dir) and not os.path.exists(metadata_path):
                logger.info("Cleaning up incomplete model files...")
                shutil.rmtree(model_dir)
            
            # If model already extracted and ready, skip download
            if os.path.exists(metadata_path):
                logger.info("Model already present and extracted")
                return
                
            # Download fresh model
            logger.info(f"Downloading model from GCloud to: {zip_path}")
            try:
                self.gcloud.sync_folder_from_gcloud(
                    bucket_name=self.bucket_name,
                    filename=self.model_path,
                    destination=zip_path
                )
                logger.info("Model download completed")
            except Exception as e:
                logger.error(f"Error downloading model: {str(e)}")
                raise
            
            # Verify zip exists
            if not os.path.exists(zip_path):
                raise Exception(f"Model zip not found at {zip_path} after download")
            
            # Create fresh model directory
            os.makedirs(model_dir, exist_ok=True)
            
            # Extract model zip
            logger.info(f"Extracting model from {zip_path} to {model_dir}")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # List contents before extraction
                logger.info("Zip contents:")
                for file in zip_ref.namelist():
                    logger.info(f"- {file}")
                    
                # Extract files directly to model directory
                zip_ref.extractall(model_dir)
            logger.info("Model extraction completed")
            
            # List extracted contents
            logger.info("Extracted contents:")
            for root, dirs, files in os.walk(model_dir):
                logger.info(f"Directory: {root}")
                logger.info(f"Files: {files}")
            
            # Verify extraction
            if os.path.exists(metadata_path):
                logger.info("Model files verified successfully")
            else:
                raise Exception(f"Model metadata not found at {metadata_path} after extraction")
            
        except Exception as e:
            logger.error(f"Error preparing model: {str(e)}")
            raise
    
    def predict(self, r: int, g: int, b: int):
        """Predict skin classification from RGB values"""
        try:
            # Ensure model is ready
            self.ensure_model_ready()
            
            # Create DataFrame with single row
            data = [(r, g, b)]
            df = self.spark.createDataFrame(data, ["R", "G", "B"])
            df_assembled = self.assembler.transform(df)
            
            # Load model and predict
            model_dir = os.path.join(self.model_dir, "model")
            logger.info(f"Loading model from: {model_dir}")
            
            model = RandomForestClassificationModel.load(model_dir)
            prediction = model.transform(df_assembled)
            
            # Get prediction and probability
            pred_value = float(prediction.select("prediction").collect()[0][0])
            probabilities = prediction.select("probability").collect()[0][0]
            confidence = float(probabilities[int(pred_value)])
            
            return {
                "prediction": int(pred_value),
                "prediction_label": self.prediction_labels.get(pred_value, "Unknown"),
                "confidence": confidence,
                "input_features": {"R": r, "G": g, "B": b}
            }
            
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            raise

if __name__ == "__main__":
    try:
        logger.info("Starting ModelPredictor...")
        predictor = ModelPredictor()
        logger.info("ModelPredictor initialized successfully")
        
        # Test prediction with sample values
        r, g, b = 150, 120, 100
        result = predictor.predict(r, g, b)
        logger.info(f"Prediction for RGB({r},{g},{b}): {result}")
        
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        sys.exit(1)