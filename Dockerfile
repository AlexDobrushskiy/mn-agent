# Dockerfile

FROM python:3.8.5-buster
RUN apt-get update && apt-get install nginx vim -y --no-install-recommends
COPY nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/server
RUN mkdir -p /opt/app/server/container_db
RUN chown -R www-data:www-data /opt/app/server/
COPY server /opt/app/server
COPY start-server.sh /opt/app/server/start-server.sh
WORKDIR /opt/app/server/
RUN pip install -r requirements.txt

EXPOSE 8020
STOPSIGNAL SIGTERM
#CMD ["gunicorn",  "server.wsgi", "--bind", "0.0.0.0:8020", "--workers", "3"]
CMD ["/opt/app/server/start-server.sh"]
