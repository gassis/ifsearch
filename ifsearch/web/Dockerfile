FROM python:3.8-alpine
WORKDIR /code
COPY requirements.txt requirements.txt
COPY . .
RUN pip install -r requirements.txt
CMD ["gunicorn", "--config", "/code/gunicorn_config.py", "flask_app:app"]
EXPOSE 5000

