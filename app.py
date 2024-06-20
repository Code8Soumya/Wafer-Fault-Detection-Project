from flask import Flask, render_template, request, send_file
from src.exception import CustomException
from src.logger import logging 
import sys
from src.pipeline.train_pipeline import TraininingPipeline
from src.pipeline.predict_pipeline import PredictionPipeline

app = Flask(__name__)
@app.route("/")
def home():
    return "Welcome to my application"

@app.route("/train")
def train_route():
    try:
        train_pipeline = TraininingPipeline()
        train_pipeline.run_pipeline()
        return "Training Completed"
    except Exception as e:
        raise CustomException(e,sys) from e

@app.route('/predict', methods=['POST', 'GET'])
def upload():
    try:
        if request.method == 'POST':
            prediction_pipeline = PredictionPipeline(request)
            prediction_file_detail = prediction_pipeline.run_pipeline()
            logging.info("prediction completed\nDownloading prediction file")
            return send_file(
                prediction_file_detail.pred_output_path,
                download_name = 'output.csv',
                as_attachment = True,
            )
        else:
            return render_template('upload_file.html')
    except Exception as e:
        raise CustomException(e,sys) from e
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)