import sys
from skin.components.data_ingestion.data_ingestion import DataIngestion
#from skin.components.data_transforamation import DataTransformation
#from skin.components.model_training import ModelTraining
#from skin.components.model_evaluation import ModelEvaluation
#from skin.components.model_pusher import ModelPusher
from skin.configuration.gcloud import GCloud
from skin.constants import *


from skin.entity.artifact_entity import (
    DataIngestionArtifacts
    
    )


from skin.entity.config_entity import (
    DataIngestionConfig
    
    
)

from skin.exception import SkinException
from skin.logger import logging


class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        
        self.gcloud = GCloud()

    
     # This method is used to start the data ingestion
    def start_data_ingestion(self) -> DataIngestionArtifacts:
        logging.info("Entered the start_data_ingestion method of TrainPipeline class")
        try:
            logging.info("Getting the data from Google cloud storage")
            data_ingestion = DataIngestion(
                data_ingestion_config=self.data_ingestion_config, gcloud=self.gcloud
            )
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Got the data from Google cloud storage")
            logging.info(
                "Exited the start_data_ingestion method of TrainPipeline class"
            )
            return data_ingestion_artifact

        except Exception as e:
            raise SkinException(e, sys) from e
        
    # This method is used to start the training pipeline
    def run_pipeline(self) -> None:
        try:
            logging.info("Started Model training >>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            data_ingestion_artifact = self.start_data_ingestion()
            

        except Exception as e:
            raise SkinException(e, sys) from e