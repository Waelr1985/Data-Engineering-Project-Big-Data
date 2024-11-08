# config.py
import os

class DataTransformationConfig:
    def __init__(self):
        self.artifacts_dir = os.path.abspath("artifacts")
        self.extracted_data_dir = os.path.join(self.artifacts_dir, "extracted_data")
        self.transformed_data_dir = os.path.join(self.artifacts_dir, "transformed_data")
        self.train_dir = os.path.join(self.transformed_data_dir, "train")
        self.test_dir = os.path.join(self.transformed_data_dir, "test")
        self.train_ratio = 0.8
        
        os.makedirs(self.extracted_data_dir, exist_ok=True)
        os.makedirs(self.train_dir, exist_ok=True)
        os.makedirs(self.test_dir, exist_ok=True)