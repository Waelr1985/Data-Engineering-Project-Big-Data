# data_transformation.py
import os
import logging
from pyspark.sql import SparkSession, DataFrame
from typing import Tuple
from config import DataTransformationConfig

class DataTransformationService:
    def __init__(self):
        """Initialize service with config and spark session"""
        self.logger = logging.getLogger(__name__)
        self.config = DataTransformationConfig()
        self.spark = self._create_spark_session()
        
    def _create_spark_session(self) -> SparkSession:
        """Create and configure Spark session"""
        self.logger.info("Creating Spark session")
        return (SparkSession.builder
                .appName("SkinDataTransformation")
                .config("spark.driver.memory", "4g")
                .getOrCreate())
    
    def load_data(self) -> DataFrame:
        """Load data from CSV files in extracted_data directory"""
        try:
            self.logger.info("Loading data...")
            
            # Get CSV files from extracted_data directory
            csv_files = [f for f in os.listdir(self.config.extracted_data_dir) 
                        if f.endswith('.csv')]
            
            if not csv_files:
                raise FileNotFoundError("No CSV files found in extracted_data directory")
            
            # Load first CSV file
            data_path = os.path.join(self.config.extracted_data_dir, csv_files[0])
            df = self.spark.read.csv(
                data_path,
                header=True,
                inferSchema=True
            )
            
            self.logger.info(f"Loaded {df.count()} rows and {len(df.columns)} columns")
            return df
            
        except Exception as e:
            self.logger.error(f"Error loading data: {str(e)}")
            raise
    
    def _split_data(self, df: DataFrame) -> Tuple[DataFrame, DataFrame]:
        """Split dataframe into train and test sets"""
        train_df, test_df = df.randomSplit(
            [self.config.train_ratio, 1.0 - self.config.train_ratio], 
            seed=42
        )
        self.logger.info(f"Split data - Training: {train_df.count()}, Testing: {test_df.count()} rows")
        return train_df, test_df
    
    def transform_and_save(self):
        """Main transformation pipeline"""
        try:
            self.logger.info("Starting transformation pipeline...")
            
            # Load data
            df = self.load_data()
            
            # Split data
            train_df, test_df = self._split_data(df)
            
            # Save splits to configured directories
            train_path = os.path.join(self.config.train_dir, "train_data")
            test_path = os.path.join(self.config.test_dir, "test_data")
            
            train_df.write.mode("overwrite").csv(train_path, header=True)
            test_df.write.mode("overwrite").csv(test_path, header=True)
            
            self.logger.info(f"Saved train data to: {train_path}")
            self.logger.info(f"Saved test data to: {test_path}")
            
        except Exception as e:
            self.logger.error(f"Error in transformation pipeline: {str(e)}")
            raise
        finally:
            self.logger.info("Stopping Spark session")
            self.spark.stop()

def main():
    """Main execution function"""
    try:
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Run transformation
        service = DataTransformationService()
        service.transform_and_save()
        
    except Exception as e:
        logging.error(f"Error in main execution: {str(e)}")
        raise

if __name__ == "__main__":
    main()