FROM python:3.11.3-alpine3.16

COPY requirements.txt /requirements.txt
COPY project /project

WORKDIR /project
EXPOSE 8000

RUN apk add postgresql-client build-base postgresql-dev
RUN pip install -r ../requirements.txt

RUN addgroup -S projectuser
RUN adduser --disabled-password -S projectuser -G projectuser

RUN chown -R projectuser:projectuser /project
USER projectuser