import sys
import os
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from src.constant import *
from src.exception import CustomException
from src.logger import logging
from src.utils.main_utils import MainUtils
from src.configuration.s3_client import client
from dataclasses import dataclass

@dataclass
class ModelTrainerConfig:
    trained_model_path= os.path.join(ARTIFACTS_FOLDER, "models", "model.pkl" )
    model_config_file_path= os.path.join('config', 'model.yaml')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
        self.utils = MainUtils()
        self.model = RandomForestClassifier()
        self.s3_client = client

    def train_model(self, x_train, y_train) -> object: 
        try:
            model_param_grid = self.utils.read_yaml_file(self.model_trainer_config.model_config_file_path)["model"]["RandomForestClassifier"]["search_param_grid"]
            grid_search = GridSearchCV(self.model, param_grid=model_param_grid, cv=5, n_jobs=-1, verbose=1)
            grid_search.fit(x_train, y_train)
            best_params = grid_search.best_params_
            print("Best params are:", best_params)
            finetuned_model = self.model.set_params(**best_params)
            return finetuned_model
        except Exception as e:
            raise CustomException(e,sys)

    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info(f"Splitting training and testing input and target feature")
            x_train, y_train, x_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1],
            )
            finetuned_model = self.train_model(x_train,y_train)
            finetuned_model.fit(x_train, y_train)
            y_pred = finetuned_model.predict(x_test)
            best_model_score = accuracy_score(y_test, y_pred)
            logging.info(f"Saving model at path: {self.model_trainer_config.trained_model_path}")
            os.makedirs(os.path.dirname(self.model_trainer_config.trained_model_path), exist_ok=True)
            self.utils.save_object(
                file_path=self.model_trainer_config.trained_model_path,
                obj=finetuned_model
            )
            self.s3_client.upload_file(
                self.model_trainer_config.trained_model_path,
                S3_BUCKET_NAME,
                'artifacts/models/model.pkl',
            )
            return best_model_score
        except Exception as e:
            raise CustomException(e, sys) from e
