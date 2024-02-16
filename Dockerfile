FROM python:3.9

WORKDIR /app

RUN pip install pymongo
RUN pip install Flask 
RUN pip install flask_pymongo

COPY ./app-python /app

CMD ["python", "app_pizza_menu_api.py"]

EXPOSE 5000