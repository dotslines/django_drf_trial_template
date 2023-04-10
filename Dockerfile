FROM python:3.11.3-alpine3.16

COPY requirements.txt /requirements.txt
COPY project /project

WORKDIR /project
EXPOSE 8000

RUN apk add postgresql-client build-base postgresql-dev
RUN pip install -r ../requirements.txt
RUN adduser --disabled-password project-user

USER project-user
