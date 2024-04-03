FROM python:3.11
WORKDIR /usr/src/app
COPY aislr4api ./
RUN pip install -r requirements.txt