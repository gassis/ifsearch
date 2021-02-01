FROM python:3.8-alpine
WORKDIR /code
COPY requirements.txt requirements.txt
COPY wait-for-it.sh wait-for-it.sh
COPY monitor.py monitor.py
COPY create_index.py create_index.py
RUN chmod 755 wait-for-it.sh
RUN apk add poppler-utils
RUN apk add --update curl
RUN apk add --update --no-cache g++ gcc libxslt-dev
RUN apk add --no-cache jpeg-dev zlib-dev
RUN apk add --no-cache --virtual .build-deps build-base linux-headers && pip install Pillow
RUN apk add tesseract-ocr
RUN pip install -r requirements.txt
RUN apk update && apk add bash
