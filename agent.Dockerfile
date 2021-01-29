FROM python:3.8.5-buster

RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/agent
RUN mkdir -p /opt/app/agent/container_db
COPY agent /opt/app/agent
COPY start-agent.sh /opt/app/agent/start-agent.sh
WORKDIR /opt/app/agent/
RUN pip install -r requirements.txt


CMD [ "python", "./agent.py"]
