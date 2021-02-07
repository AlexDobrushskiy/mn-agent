FROM python:3.8.5-buster

RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/agent
RUN mkdir -p /opt/app/agent/container_db
COPY agent /opt/app/agent
WORKDIR /opt/app/agent/
RUN pip install -r requirements.txt


CMD [ "python", "./agent.py"]
