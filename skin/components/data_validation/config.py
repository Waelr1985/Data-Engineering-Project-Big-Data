import os

class DataValidationConfig:
    def __init__(self):
        # Base directory for artifacts
        self.artifacts_dir = os.path.abspath("artifacts")
        
        # Input data directory
        self.extracted_data_dir = os.path.join(self.artifacts_dir, "extracted_data")
        
        # Directories and paths within the artifacts directory
        self.data_validation_dir = os.path.join(self.artifacts_dir, "data_validation")
        self.drift_report_dir = os.path.join(self.data_validation_dir, "drift_report")
        self.valid_data_dir = os.path.join(self.data_validation_dir, "validated")
        self.invalid_data_dir = os.path.join(self.data_validation_dir, "invalid")
        
        # File paths for reports
        self.validation_report_file_path = os.path.join(self.data_validation_dir, "validation_report.txt")
        self.validation_report_page_file_path = os.path.join(self.drift_report_dir, "drift_report.html")

        # Ensure directories exist
        os.makedirs(self.data_validation_dir, exist_ok=True)
        os.makedirs(self.drift_report_dir, exist_ok=True)
        os.makedirs(self.valid_data_dir, exist_ok=True)
        os.makedirs(self.invalid_data_dir, exist_ok=True)