FROM python:3.11

WORKDIR /play_with_image

ENV PYTHONDONTWRITEBYTECODE=1\
    PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

COPY "./requirements.txt" .

RUN pip install -r requirements.txt

COPY /play_with_image/. .