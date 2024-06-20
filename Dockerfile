FROM python:3.12

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    && apt-get clean
    
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python3","app.py" ]