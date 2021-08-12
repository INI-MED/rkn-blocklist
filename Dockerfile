FROM python:3.9-alpine

WORKDIR /rkn

COPY requirements.txt .

RUN pip install -r requirements.txt
COPY . .

EXPOSE 5000
