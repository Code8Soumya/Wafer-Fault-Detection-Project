import sys
import os
import csv
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.impute import KNNImputer
from sklearn.preprocessing import RobustScaler
from imblearn.combine import SMOTETomek
from imblearn.over_sampling import SMOTE
from sklearn.pipeline import Pipeline
from src.constant import *
from src.configuration.s3_client import client
from src.exception import CustomException
from src.logger import logging
from src.utils.main_utils import MainUtils
from dataclasses import dataclass

@dataclass
class DataTransformationConfig:
    file_path = os.path.join(ARTIFACTS_FOLDER, 'training')
    transformed_train_file_path=os.path.join(file_path, 'train.npy')
    transformed_test_file_path=os.path.join(file_path, 'test.npy') 
    transformer_object_file_path=os.path.join(ARTIFACTS_FOLDER, 'models', 'preprocessor.pkl')
    
class DataTransformation:
    def __init__(self,raw_file_path):
        self.raw_file_path = raw_file_path
        self.data_transformation_config = DataTransformationConfig()
        self.utils =  MainUtils()
        self.s3_client = client
        
    @staticmethod
    def get_data(raw_file_path: str) -> pd.DataFrame:
        try:
            logging.info("Reading csv file from the source")
            data = pd.read_csv(raw_file_path)
            logging.info("Reading csv file from the source completed")
            return data
        except Exception as e:
            raise CustomException(e,sys) from e
        
    def get_data_transformer_object(self):
        try:
            logging.info("Initiating data transformer pipeline")
            imputer_step = ('imputer', KNNImputer(n_neighbors=5))
            scaler_step = ('scaler', RobustScaler())
            preprocessor = Pipeline(steps=[imputer_step,scaler_step])
            logging.info("Data transformer pipeline initiated")
            return preprocessor
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def get_cols_with_zero_std_dev(self, df: pd.DataFrame) -> list:
        cols_to_drop = []
        for col in df.columns:
            if df[col].std() == 0:
                cols_to_drop.append(col)
        return cols_to_drop
    
    def get_redundant_cols(self, df: pd.DataFrame, missing_thresh=.7) -> list:
        cols_missing_ratios = df.isna().sum().div(df.shape[0])
        cols_to_drop = list(cols_missing_ratios[cols_missing_ratios > missing_thresh].index)
        return cols_to_drop 
    
    def initiate_data_transformation(self):
        try:
            logging.info("Initiating data transformation")
            df = self.get_data(raw_file_path=self.raw_file_path)
            y = np.where(df[TARGET_COLUMN] == -1,0,1)
            cols_to_drop = [TARGET_COLUMN,"Unnamed: 0"]
            df.drop(columns = cols_to_drop, axis=1, inplace=True)
            cols_to_drop = self.get_cols_with_zero_std_dev(df)+self.get_redundant_cols(df)
            x = df.drop(columns = cols_to_drop, axis=1)
            cols_to_drop  = ['cols_to_drop', 'Unnamed: 0'] + cols_to_drop 
            cols_to_drop_path = os.path.join(self.data_transformation_config.file_path, 'cols_to_drop.csv')
            with open(cols_to_drop_path, 'w', newline='') as file:
                writer = csv.writer(file)
                for item in cols_to_drop:
                    writer.writerow([item])
            self.s3_client.upload_file(
                cols_to_drop_path,
                S3_BUCKET_NAME,
                'artifacts/training/cols_to_drop.csv',
            )
            logging.info("Train_test splitting the data")
            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2)
            preprocessor = self.get_data_transformer_object()
            logging.info("Fitting and transforming the data")
            x_train_scaled =  preprocessor.fit_transform(x_train)
            x_test_scaled  =  preprocessor.transform(x_test)
            logging.info("Saving preprocessor object")
            preprocessor_path = self.data_transformation_config.transformer_object_file_path
            os.makedirs(os.path.dirname(preprocessor_path), exist_ok=True)
            self.utils.save_object(file_path=preprocessor_path,obj=preprocessor)
            self.s3_client.upload_file(
                self.data_transformation_config.transformer_object_file_path,
                S3_BUCKET_NAME,
                'artifacts/models/preprocessor.pkl',
            )
            logging.info("Oversampling the data")
            resampler = SMOTETomek(smote=SMOTE(k_neighbors=2),sampling_strategy='auto')
            x_train_scaled_res, y_train_res = resampler.fit_resample(x_train_scaled, y_train) 
            logging.info("Saving transformed data")
            train_arr = np.c_[x_train_scaled_res, np.array(y_train_res) ]
            test_arr = np.c_[x_test_scaled, np.array(y_test) ]
            np.save(self.data_transformation_config.transformed_train_file_path, train_arr)
            np.save(self.data_transformation_config.transformed_test_file_path, test_arr)
            logging.info("Data transformation completed")
            return (train_arr, test_arr, preprocessor_path)
        except Exception as e:
            raise CustomException(e, sys) from e
