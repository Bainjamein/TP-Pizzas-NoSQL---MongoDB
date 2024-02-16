FROM python:3.9

WORKDIR /app

RUN pip install pymongo
RUN pip install Flask 
RUN pip install flask_pymongo
RUN pip install flask_bcrypt
RUN pip install PyJWT

COPY ./app-python /app

CMD ["python", "pizzas_shop_api.py"]

EXPOSE 5001
EXPOSE 5002
EXPOSE 5003
