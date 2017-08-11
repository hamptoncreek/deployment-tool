FROM python:3.5
RUN apt-get update
RUN apt-get install mysql-client -y
RUN pip install --upgrade pip
COPY ./docker/jenkins/code /code
RUN pip install -r /code/requirements.txt