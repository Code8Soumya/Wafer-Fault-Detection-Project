import os
import sys
import boto3
from src.exception import CustomException
from src.logger import logging
from dotenv import load_dotenv
load_dotenv()


try:
    logging.info("Getting aws cradentials from env file")
    os.environ["AWS_ACCESS_KEY_ID"] = os.getenv("AWS_ACCESS_KEY_ID")
    os.environ["AWS_SECRET_ACCESS_KEY"] = os.getenv("AWS_SECRET_ACCESS_KEY")
    logging.info("Successfully got aws cradentials from env file")
except Exception as e:
    logging.info("Failed to get aws cradentials from env file")
else:
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

def s3_client():
    try:
        logging.info("Creating s3 client")
        client = boto3.client('s3')
        logging.info("Successfully created s3 client")
        return client
    except Exception as e:
        raise CustomException(e, sys) from e
    
client = s3_client()