import os
import sys
import pandas as pd
import numpy as np
from src.logger import logging
from src.exception import CustomException
from src.constant import *
from src.utils.main_utils import MainUtils
from dataclasses import dataclass
        
        
@dataclass
class PredictionPipelineConfig:
    pred_dirname: str = os.path.join(ARTIFACTS_FOLDER, 'prediction')
    pred_input_path = os.path.join(pred_dirname, 'input.csv')
    pred_output_path = os.path.join(pred_dirname, 'output.csv')
    model_file_path: str = os.path.join(ARTIFACTS_FOLDER, 'models', 'model.pkl')
    preprocessor_path: str = os.path.join(ARTIFACTS_FOLDER,'models', 'preprocessor.pkl')
    cols_to_drop_file_path: str = os.path.join(ARTIFACTS_FOLDER, 'training', 'cols_to_drop.csv')
    
class PredictionPipeline:
    def __init__(self, request):
        self.request = request
        self.utils = MainUtils()
        self.prediction_pipeline_config = PredictionPipelineConfig()

    def save_input_files(self) -> str:
        try:
            os.makedirs(self.prediction_pipeline_config.pred_dirname, exist_ok=True)
            input_csv_file = self.request.files['file']
            logging.info(input_csv_file.filename)
            df = pd.read_csv(input_csv_file)
            df.to_csv(self.prediction_pipeline_config.pred_input_path, index=False)
            return self.prediction_pipeline_config.pred_input_path
        except Exception as e:
            raise CustomException(e,sys) from e

    def predict(self, prediction_file_path):
            try:
                model = self.utils.load_object(self.prediction_pipeline_config.model_file_path)
                preprocessor = self.utils.load_object(file_path=self.prediction_pipeline_config.preprocessor_path)
                cols_to_drop = np.squeeze(np.array(pd.read_csv(self.prediction_pipeline_config.cols_to_drop_file_path)), axis=-1)
                to_predict = pd.read_csv(prediction_file_path)
                to_predict.drop(labels=cols_to_drop, axis=1, inplace=True)
                to_predict_trans = preprocessor.transform(to_predict)
                pred = model.predict(to_predict_trans)
                return pred
            except Exception as e:
                raise CustomException(e, sys) from e
        
    def get_predicted_dataframe(self, prediction_file_path: str):
        try:
            logging.info("Initiating prediction pipeline")
            input_dataframe = pd.read_csv(prediction_file_path)
            predictions = self.predict(prediction_file_path)
            input_dataframe[TARGET_COLUMN] = [pred for pred in predictions]
            target_column_mapping = {0:'bad', 1:'good'}
            input_dataframe[TARGET_COLUMN] = input_dataframe[TARGET_COLUMN].map(target_column_mapping)
            os.makedirs(self.prediction_pipeline_config.pred_dirname, exist_ok=True)
            input_dataframe.to_csv(self.prediction_pipeline_config.pred_output_path, index=False)
            logging.info("Prediction pipeline completed")
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def run_pipeline(self) -> None:
        try:
            input_csv_path = self.save_input_files()
            self.get_predicted_dataframe(input_csv_path)
            return self.prediction_pipeline_config
        except Exception as e:
            raise CustomException(e,sys) from e
            
        

 
        

        
