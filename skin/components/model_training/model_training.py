# model_training.py
import os
import logging
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import RandomForestClassifier
from config import ModelTrainingConfig

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ModelTrainer:
    def __init__(self):
        self.config = ModelTrainingConfig()
        self.spark = SparkSession.builder \
            .appName("SkinModelTraining") \
            .config("spark.driver.memory", "4g") \
            .config("spark.executor.memory", "4g") \
            .getOrCreate()
        logger.info("Created Spark session")

    def load_data(self):
        """Load training data from CSV files"""
        try:
            train_path = os.path.join(self.config.train_dir, "train_data")
            logger.info(f"Loading training data from {train_path}")
            
            # Changed from parquet to csv
            train_data = self.spark.read.csv(
                train_path,
                header=True,
                inferSchema=True
            )
            
            # Convert column names to match expected format
            train_data = train_data.select(
                train_data.B.cast("double"),
                train_data.G.cast("double"),
                train_data.R.cast("double"),
                train_data.y.cast("double")
            )
            
            return train_data
        except Exception as e:
            logger.error(f"Error loading training data: {str(e)}")
            raise

    def prepare_features(self, data):
        """Prepare feature vector for training"""
        try:
            feature_cols = ["B", "G", "R"]
            assembler = VectorAssembler(
                inputCols=feature_cols,
                outputCol="features"
            )
            data_with_features = assembler.transform(data)
            logger.info("Prepared feature vectors")
            return data_with_features
        except Exception as e:
            logger.error(f"Error preparing features: {str(e)}")
            raise

    def train_model(self, data):
        """Train Random Forest model"""
        try:
            rf = RandomForestClassifier(
                labelCol="y",
                featuresCol="features",
                numTrees=100,
                maxDepth=10,
                seed=42
            )
            
            model = rf.fit(data)
            logger.info("Trained Random Forest model")
            return model
        except Exception as e:
            logger.error(f"Error training model: {str(e)}")
            raise

    def save_model(self, model):
        """Save the trained model"""
        try:
            model_path = os.path.join(self.config.model_dir, "random_forest_model")
            model.save(model_path)
            logger.info(f"Saved model to {model_path}")
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")
            raise

    def run_training_pipeline(self):
        """Execute the full training pipeline"""
        try:
            logger.info("Starting model training pipeline")
            
            # Load data
            train_data = self.load_data()
            logger.info(f"Loaded {train_data.count()} training records")
            
            # Prepare features
            data_prepared = self.prepare_features(train_data)
            
            # Train model
            model = self.train_model(data_prepared)
            
            # Save model
            self.save_model(model)
            
            logger.info("Completed model training pipeline")
            
        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}")
            raise
        finally:
            self.spark.stop()

if __name__ == "__main__":
    trainer = ModelTrainer()
    trainer.run_training_pipeline()