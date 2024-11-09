# model_evaluation.py
import os
import logging
from pyspark.sql import SparkSession
from pyspark.ml.classification import RandomForestClassificationModel
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.feature import VectorAssembler
import json
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ModelEvaluator:
    def __init__(self):
        self.spark = SparkSession.builder \
            .appName("SkinModelEvaluation") \
            .config("spark.driver.memory", "4g") \
            .config("spark.executor.memory", "4g") \
            .getOrCreate()
        
        # Define paths
        self.artifacts_dir = os.path.abspath("artifacts")
        self.model_dir = os.path.join(self.artifacts_dir, "model")
        self.test_dir = os.path.join(self.artifacts_dir, "transformed_data/test")
        self.evaluation_dir = os.path.join(self.artifacts_dir, "evaluation")
        os.makedirs(self.evaluation_dir, exist_ok=True)
        
        logger.info("Initialized ModelEvaluator")

    def load_test_data(self):
        """Load and prepare test data"""
        try:
            test_path = os.path.join(self.test_dir, "test_data")
            logger.info(f"Loading test data from {test_path}")
            
            # Load CSV test data
            test_data = self.spark.read.csv(
                test_path,
                header=True,
                inferSchema=True
            )
            
            # Cast columns to proper types
            test_data = test_data.select(
                test_data.B.cast("double"),
                test_data.G.cast("double"),
                test_data.R.cast("double"),
                test_data.y.cast("double")
            )
            
            # Prepare feature vector
            assembler = VectorAssembler(
                inputCols=["B", "G", "R"],
                outputCol="features"
            )
            test_data = assembler.transform(test_data)
            
            logger.info(f"Loaded and prepared {test_data.count()} test records")
            return test_data
            
        except Exception as e:
            logger.error(f"Error loading test data: {str(e)}")
            raise

    def load_model(self):
        """Load the trained Random Forest model"""
        try:
            model_path = os.path.join(self.model_dir, "random_forest_model")
            logger.info(f"Loading model from {model_path}")
            model = RandomForestClassificationModel.load(model_path)
            logger.info("Model loaded successfully")
            return model
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise

    def evaluate_model(self, model, test_data):
        """Evaluate model performance"""
        try:
            # Make predictions
            predictions = model.transform(test_data)
            logger.info("Generated predictions on test data")

            # Initialize evaluator for different metrics
            evaluator = MulticlassClassificationEvaluator(
                labelCol="y",
                predictionCol="prediction"
            )

            # Calculate metrics
            metrics = {}
            
            # Accuracy
            evaluator.setMetricName("accuracy")
            metrics["accuracy"] = evaluator.evaluate(predictions)
            
            # Precision
            evaluator.setMetricName("weightedPrecision")
            metrics["precision"] = evaluator.evaluate(predictions)
            
            # Recall
            evaluator.setMetricName("weightedRecall")
            metrics["recall"] = evaluator.evaluate(predictions)
            
            # F1 Score
            evaluator.setMetricName("f1")
            metrics["f1_score"] = evaluator.evaluate(predictions)

            logger.info("Calculated evaluation metrics")
            return metrics, predictions
            
        except Exception as e:
            logger.error(f"Error evaluating model: {str(e)}")
            raise

    def save_evaluation_results(self, metrics):
        """Save evaluation results to file"""
        try:
            # Add timestamp to results
            results = {
                "evaluation_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "metrics": metrics
            }
            
            # Save results as JSON
            output_file = os.path.join(self.evaluation_dir, "evaluation_results.json")
            with open(output_file, "w") as f:
                json.dump(results, f, indent=4)
            
            logger.info(f"Saved evaluation results to {output_file}")
            
        except Exception as e:
            logger.error(f"Error saving evaluation results: {str(e)}")
            raise

    def run_evaluation(self):
        """Execute the full evaluation pipeline"""
        try:
            logger.info("Starting model evaluation pipeline")
            
            # Load test data
            test_data = self.load_test_data()
            
            # Load model
            model = self.load_model()
            
            # Evaluate model
            metrics, predictions = self.evaluate_model(model, test_data)
            
            # Save results
            self.save_evaluation_results(metrics)
            
            # Print metrics
            logger.info("Evaluation Results:")
            for metric, value in metrics.items():
                logger.info(f"{metric}: {value:.4f}")
            
            logger.info("Completed model evaluation pipeline")
            
        except Exception as e:
            logger.error(f"Evaluation pipeline failed: {str(e)}")
            raise
        finally:
            self.spark.stop()

if __name__ == "__main__":
    evaluator = ModelEvaluator()
    evaluator.run_evaluation()