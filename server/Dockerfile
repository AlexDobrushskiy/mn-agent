# Dockerfile

FROM python:3.9.1-buster

RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/pip_cache
COPY * /opt/app/
WORKDIR /opt/app
RUN pip install -r requirements.txt --cache-dir /opt/app/pip_cache
RUN chown -R www-data:www-data /opt/app
