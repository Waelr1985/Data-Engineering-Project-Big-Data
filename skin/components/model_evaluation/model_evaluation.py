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

# Model Evaluation Service
class ModelEvaluationService:
    def __init__(self, config_path: str = 'config.yaml'):
        logging.info(f"Initializing ModelEvaluationService with config: {config_path}")
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
        logging.info("Creating Spark session for model evaluation")
        return SparkSession.builder \
            .appName("ModelEvaluation") \
            .getOrCreate()
    
    def evaluate(self, artifact_path: str):
        try:
            logging.info(f"Starting model evaluation process using artifacts from: {artifact_path}")
            
            # Load test data and model
            logging.info("Loading test data from parquet")
            test_data = self.spark.read.parquet(f"{artifact_path}/test_data")
            logging.info(f"Test data loaded. Number of records: {test_data.count()}")
            
            logging.info("Loading trained model")
            model = RandomForestClassificationModel.load(f"{artifact_path}/trained_model")
            logging.info("Model loaded successfully")
            
            # Make predictions
            logging.info("Making predictions on test data")
            predictions = model.transform(test_data)
            logging.info(f"Predictions generated for {predictions.count()} records")
            
            # Calculate metrics
            logging.info("Calculating evaluation metrics")
            evaluator = MulticlassClassificationEvaluator(
                labelCol=self.config['label_column'],
                predictionCol="prediction"
            )
            
            metrics = {}
            for metric in ['accuracy', 'weightedPrecision', 'weightedRecall', 'f1']:
                logging.info(f"Calculating {metric}")
                evaluator.setMetricName(metric)
                metric_value = evaluator.evaluate(predictions)
                metrics[metric] = metric_value
                logging.info(f"{metric}: {metric_value}")
            
            # Calculate confusion matrix
            logging.info("Calculating confusion matrix")
            confusion_matrix = predictions.groupBy("label", "prediction").count()
            logging.info("Confusion matrix calculated")
            logging.info(f"Confusion Matrix:\\
{confusion_matrix.toPandas().to_string()}")
            
            # Save metrics
            metrics_path = f"{artifact_path}/metrics.json"
            logging.info(f"Saving metrics to: {metrics_path}")
            with open(metrics_path, 'w') as f:
                json.dump(metrics, f, indent=4)
            logging.info("Metrics saved successfully")
            
            # Log detailed model performance summary
            logging.info("Model Performance Summary:")
            for metric, value in metrics.items():
                logging.info(f"{metric}: {value:.4f}")
            
        except Exception as e:
            logging.error(f"Error in model evaluation: {str(e)}")
            raise
        finally:
            logging.info("Stopping Spark session")
            self.spark.stop()

logging.info("Model Evaluation Service defined successfully")

# Create example configuration
example_config = """
feature_columns:
  - "B"
  - "G"
  - "R"

label_column: "y"

train_test_split:
  train_ratio: 0.8
  test_ratio: 0.2
  seed: 42

model_params:
  numTrees: 100
  maxDepth: 10
  seed: 42

artifact_path: "./artifacts"
"""

# Save configuration
with open('config.yaml', 'w') as f:
    f.write(example_config)

print("\
Configuration saved to config.yaml")

# Example usage
print("\
Example usage:")
print("""
# 1. Data Transformation
data_transformer = DataTransformationService('config.yaml')
data_transformer.transform_and_save('skin.csv', './artifacts')

# 2. Model Training
model_trainer = ModelTrainingService('config.yaml')
model_trainer.train_and_save('./artifacts')

# 3. Model Evaluation
model_evaluator = ModelEvaluationService('config.yaml')
model_evaluator.evaluate('./artifacts')
""")