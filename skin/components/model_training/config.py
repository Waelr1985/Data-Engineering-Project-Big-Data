# config.py
import os

class ModelTrainingConfig:
    def __init__(self):
        self.artifacts_dir = os.path.abspath("artifacts")
        self.extracted_data_dir = os.path.join(self.artifacts_dir, "extracted_data") 
        self.transformed_data_dir = os.path.join(self.artifacts_dir, "transformed_data")
        self.model_dir = os.path.join(self.artifacts_dir, "model")
        self.train_dir = os.path.join(self.transformed_data_dir, "train")
        self.test_dir = os.path.join(self.transformed_data_dir, "test")
        
        # Create directories
        os.makedirs(self.extracted_data_dir, exist_ok=True)
        os.makedirs(self.transformed_data_dir, exist_ok=True)  # Add this line
        os.makedirs(self.train_dir, exist_ok=True)
        os.makedirs(self.test_dir, exist_ok=True)
        os.makedirs(self.model_dir, exist_ok=True)