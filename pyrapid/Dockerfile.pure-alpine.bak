FROM alpine:latest
RUN apk add --no-cache python3 python3-dev py3-pip
RUN mkdir /executor
COPY async_test_server.py /executor/server.py
COPY requirements.txt /executor/requirements.txt
WORKDIR /executor
RUN pip3 install -r requirements.txt
EXPOSE 8888
ENTRYPOINT python3 /executor/server.py
