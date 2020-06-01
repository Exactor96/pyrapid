FROM python:3.8.2-alpine3.11
RUN mkdir /executor
RUN pip3 install cloudpickle
COPY async_test_server.py /executor/server.py
WORKDIR /executor
EXPOSE 8888
ENTRYPOINT python3 /executor/server.py