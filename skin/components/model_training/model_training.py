
# Import required libraries
import os
import json
import yaml
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml import Pipeline
from pyspark.ml.classification import RandomForestClassifier, RandomForestClassificationModel
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from skin.logger import logging

# Model Training Service
class ModelTrainingService:
    def __init__(self, config_path: str = 'config.yaml'):
        logging.info(f"Initializing ModelTrainingService with config: {config_path}")
        self.config = self._load_config(config_path)
        self.spark = self._create_spark_session()
        
    def _load_config(self, config_path: str) -> dict:
        logging.info(f"Loading configuration from {config_path}")
        try:
            with open(config_path, 'r') as file:
                config = yaml.safe_load(file)
            logging.info("Configuration loaded successfully")
            return config
        except Exception as e:
            logging.error(f"Error loading configuration: {str(e)}")
            raise
    
    def _create_spark_session(self) -> SparkSession:
        logging.info("Creating Spark session for model training")
        return SparkSession.builder \
            .appName("ModelTraining") \
            .getOrCreate()
    
    def train_and_save(self, artifact_path: str):
        try:
            logging.info(f"Starting model training process using artifacts from: {artifact_path}")
            
            # Load training data
            logging.info("Loading training data from parquet")
            train_data = self.spark.read.parquet(f"{artifact_path}/train_data")
            logging.info(f"Training data loaded. Number of records: {train_data.count()}")
            
            # Configure Random Forest
            logging.info("Configuring Random Forest classifier")
            rf_params = {
                'labelCol': self.config['label_column'],
                'featuresCol': "features",
                'numTrees': self.config['model_params']['numTrees'],
                'maxDepth': self.config['model_params']['maxDepth']
            }
            logging.info(f"Random Forest parameters: {rf_params}")
            
            rf = RandomForestClassifier(**rf_params)
            
            # Train model
            logging.info("Training Random Forest model...")
            model = rf.fit(train_data)
            logging.info("Model training completed")
            
            # Log feature importances
            feature_importance = model.featureImportances
            logging.info(f"Feature importances: {feature_importance}")
            
            # Save model
            model_path = f"{artifact_path}/trained_model"
            logging.info(f"Saving trained model to: {model_path}")
            model.save(model_path)
            logging.info("Model saved successfully")
            
        except Exception as e:
            logging.error(f"Error in model training: {str(e)}")
            raise
        finally:
            logging.info("Stopping Spark session")
            self.spark.stop()

logging.info("Model Training Service defined successfully")