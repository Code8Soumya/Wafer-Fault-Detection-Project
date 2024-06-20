import os
import sys
import boto3
from src.exception import CustomException
from src.logger import logging
from dotenv import load_dotenv
load_dotenv()

try:
    logging.info("Getting aws cradentials from env file")
    os.environ["AWS_ACCESS_KEY_ID"] = os.getenv("aws_access_key_id")
    os.environ["AWS_SECRET_ACCESS_KEY"] = os.getenv("aws_secret_access_key")
    logging.info("Successfully got aws cradentials from env file")
except Exception as e:
    raise CustomException(e, sys) from e

def s3_client():
    try:
        logging.info("Creating s3 client")
        client = boto3.client('s3')
        logging.info("Successfully created s3 client")
        return client
    except Exception as e:
        raise CustomException(e, sys) from e
    
client = s3_client()