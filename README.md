Agent
-----

####Start agent:

 You should start agent in docker container:
 1. Build image: docker build -f agent.Dockerfile
 
 2. Run container: docker run -d -v /home/animecoinuser/.pastel:/opt/app/agent/container_db
 on linux you should add --add-host=host.docker.internal:host-gateway

By default the data will send on http://dobrushskiy.name:8020/
if you need to change the address you should set the environment variables
CUSTOM_DNS_NAME and CUSTOM_PORT
