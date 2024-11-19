import sys 
import os
import pandas as pd
import numpy as np
from datetime import datetime
import json
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
from skin.components.data_validation.config import DataValidationConfig
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CustomException(Exception):
    def __init__(self, error_msg, error_detail):
        super().__init__(error_msg)
        self.error_msg = error_msg
        self.error_detail = error_detail
    
    def __str__(self):
        return self.error_msg

def test_imports():
    """Test all required imports"""
    required_packages = [
        'pandas', 'numpy', 'evidently', 'json', 'datetime', 'os'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            logger.info(f"{package} successfully imported")
        except ImportError as e:
            missing_packages.append(package)
            logger.error(f"Failed to import {package}: {str(e)}")
    
    if missing_packages:
        logger.error("Missing packages: " + ", ".join(missing_packages))
        sys.exit(1)
    logger.info("All imports successful!")

class DataValidation:
    def __init__(self, config):
        self.config = config
        self.artifacts_dir = config.artifacts_dir
        self._setup_directories()
        
    def _setup_directories(self):
        """Create necessary directories"""
        try:
            os.makedirs(self.config.data_validation_dir, exist_ok=True)
            os.makedirs(self.config.drift_report_dir, exist_ok=True)
            os.makedirs(self.config.valid_data_dir, exist_ok=True)
            os.makedirs(self.config.invalid_data_dir, exist_ok=True)
            logger.info("Necessary directories set up successfully.")
        except Exception as e:
            raise CustomException(f"Error setting up directories: {str(e)}", sys)
        
    def load_data(self):
        """Load and validate data"""
        try:
            logger.info("Loading data...")
            # Get all CSV files from extracted_data directory
            csv_files = [f for f in os.listdir(self.config.extracted_data_dir) 
                        if f.endswith('.csv')]
            
            if not csv_files:
                raise FileNotFoundError("No CSV files found in extracted_data directory")
            
            # Load the first CSV file (you might want to modify this based on your needs)
            data_path = os.path.join(self.config.extracted_data_dir, csv_files[0])
            self.data = pd.read_csv(data_path)
            logger.info(f"Loaded data shape: {self.data.shape}")
            return self.data
        except Exception as e:
            raise CustomException(f"Error loading data: {str(e)}", sys)
        
    def validate_schema(self):
        """Validate schema"""
        try:
            # Check if required columns exist
            required_columns = {'B', 'G', 'R', 'y'}
            current_columns = set(self.data.columns)
            
            if not required_columns.issubset(current_columns):
                missing_cols = required_columns - current_columns
                logger.error(f"Missing required columns: {missing_cols}")
                return False
                
            # Check data types
            for col in ['B', 'G', 'R']:
                if not pd.api.types.is_numeric_dtype(self.data[col]):
                    logger.error(f"Column {col} is not numeric")
                    return False
                    
            if not pd.api.types.is_numeric_dtype(self.data['y']):
                logger.error("Target column 'y' is not numeric")
                return False
                
            return True
        except Exception as e:
            raise CustomException(f"Error validating schema: {str(e)}", sys)
        
    def check_data_drift(self):
        """Check for data drift"""
        try:
            # Basic data drift check using evidently
            report = Report(metrics=[DataDriftPreset()])
            # Split data into reference and current
            mid_point = len(self.data) // 2
            reference_data = self.data.iloc[:mid_point]
            current_data = self.data.iloc[mid_point:]
            
            report.run(reference_data=reference_data, current_data=current_data)
            
            # Save drift report
            report.save_html(self.config.validation_report_page_file_path)
            return True
        except Exception as e:
            raise CustomException(f"Error checking data drift: {str(e)}", sys)
        
    def save_validation_report(self, results):
        """Save validation results"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_path = os.path.join(self.config.data_validation_dir, 
                                     f'validation_report_{timestamp}.json')
            
            with open(report_path, 'w') as f:
                json.dump(results, f, indent=4)
            logger.info(f"Validation report saved to: {report_path}")
            return report_path
        except Exception as e:
            raise CustomException(f"Error saving validation report: {str(e)}", sys)
        
    def initiate_data_validation(self):
        """Run full validation"""
        try:
            logger.info("Starting validation process...")
            
            # Load data
            self.load_data()
            
            results = {
                'timestamp': datetime.now().isoformat(),
                'data_shape': self.data.shape,
                'checks': {}
            }
            
            # Run schema validation
            results['checks']['schema_valid'] = self.validate_schema()
            if not results['checks']['schema_valid']:
                logger.error("Validation failed: Invalid schema")
                self.save_validation_report(results)
                return False
            
            # Check data drift
            results['checks']['no_drift'] = self.check_data_drift()
            
            # Overall validation result
            validation_passed = all(results['checks'].values())
            results['validation_passed'] = validation_passed
            
            # Save the full report
            self.save_validation_report(results)
            logger.info(f"Validation {'passed' if validation_passed else 'failed'}")
            
            return validation_passed
        except Exception as e:
            raise CustomException(f"Error in validation process: {str(e)}", sys)

if __name__ == "__main__":
    # First test imports
    logger.info("Testing imports...")
    test_imports()
    
    logger.info("Initiating data validation...")
    config = DataValidationConfig()
    validator = DataValidation(config)
    validator.initiate_data_validation()