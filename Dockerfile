FROM python:3.11.4-alpine3.18

COPY ../ /app

CMD python3 /app/main.py