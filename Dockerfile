FROM python:3.9

WORKDIR /app

RUN pip install pymongo

COPY ./app-python /app

CMD ["python", "app.py"]