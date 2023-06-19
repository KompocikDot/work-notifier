FROM python:3.11.4-alpine3.18

COPY .. /workifier
WORKDIR /workifier
RUN pip3 install pre-commit
RUN pip3 install -r requirements.txt

CMD python3 app/main.py
