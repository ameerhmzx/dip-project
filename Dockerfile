FROM python:3.8

#RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt && rm -rf requirements.txt

WORKDIR /photos
