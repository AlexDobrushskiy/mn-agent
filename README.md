Agent

Start agent:
you should start agent in docker container
1)Build image: docker build -f agent.Dockerfile
2)Run container: docker run
by default the data will send on http://dobrushskiy.name:8020/
if you need to change the address you should set the environment variables
CUSTOM_DNS_NAME and CUSTOM_PORT