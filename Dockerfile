FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

ENV AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
ENV AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}

CMD [ "python3","app.py" ]