import sys
from src.constant import *
from src.configuration.s3_client import client
from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    s3_bucket_name: str= S3_BUCKET_NAME
    artifact_folder: str = ARTIFACTS_FOLDER
    
class DataIngestion:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.s3_client = client
        
    def initiate_data_ingestion(self) -> str:
        try:
            logging.info("Data ingestion started and downloading data from s3")
            self.s3_client.download_file(
                Bucket = self.data_ingestion_config.s3_bucket_name,
                Key = f'{self.data_ingestion_config.artifact_folder}/training/wafers.csv',
                Filename = f'{self.data_ingestion_config.artifact_folder}/training/wafers.csv',
            )
            logging.info("Data ingestion completed and downloaded data from s3")
            raw_file_path = f'{self.data_ingestion_config.artifact_folder}/training/wafers.csv'
            return raw_file_path
        except Exception as e:
            raise CustomException(e, sys) from e
        


