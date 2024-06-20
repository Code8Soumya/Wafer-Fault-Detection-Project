import sys
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.exception import CustomException


class TraininingPipeline:
    def start_data_ingestion(self):
        try:
            data_ingestion = DataIngestion()
            raw_file_path = data_ingestion.initiate_data_ingestion()
            return raw_file_path
        except Exception as e:
            raise CustomException(e,sys) from e
    
    def start_data_transformation(self, raw_file_path):
        try:
            data_transformation = DataTransformation(raw_file_path)
            train_arr, test_arr, preprocessor_path = data_transformation.initiate_data_transformation()
            return train_arr, test_arr, preprocessor_path
        except Exception as e:
            raise CustomException(e,sys) from e

    def start_model_training(self, train_arr, test_arr):
        try:
            model_trainer = ModelTrainer()
            model_score = model_trainer.initiate_model_trainer(train_arr, test_arr)
            return model_score
        except Exception as e:
            raise CustomException(e,sys) from e
        
    def run_pipeline(self):
        try:
            raw_file_path = self.start_data_ingestion()
            train_arr, test_arr, preprocessor_path = self.start_data_transformation(raw_file_path)
            score = self.start_model_training(train_arr, test_arr)
            print("Training completed\nTrained model score : ", score)
        except Exception as e:
            raise CustomException(e, sys) from e
