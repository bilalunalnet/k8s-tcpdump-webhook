FROM python:3.13.0a4-alpine

WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app /code/app

EXPOSE 8443

USER 1001:1001

CMD [ "/usr/local/bin/gunicorn", "app:app", "--certfile=/ssl/server.crt", "--keyfile=/ssl/server.key", "--bind", "0.0.0.0:8443", "--keep-alive", "1" ]