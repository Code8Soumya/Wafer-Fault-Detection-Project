FROM python:3.12

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    && apt-get clean
    
COPY . /app

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

ENV AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
ENV AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}

CMD [ "python3","app.py" ]