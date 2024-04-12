FROM python:3.11.6-alpine3.18

WORKDIR /home

ARG UNAME=e2l
ARG UID=1001
ARG GID=1001
RUN addgroup --gid ${GID} ${UNAME}
RUN adduser --home /home/e2l --uid ${UID} -G ${UNAME} --disabled-password e2l && \
    apk update && apk add --no-cache make protobuf-dev g++ python3-dev libffi-dev openssl-dev && \
    mkdir /home/e2l/e2l-sink && \
    chown -R ${UNAME}:${UNAME} /home/e2l 

USER ${UNAME} 
WORKDIR /home/e2l/e2l-sink

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt && \
    mkdir device_files

COPY e2gw_rpc_client/ e2gw_rpc_client/
COPY e2l_module/ e2l_module/
COPY mqtt_module/ mqtt_module/
COPY protos/ protos/
COPY rpc_module/ rpc_module/
COPY main.py main.py
COPY VERSION VERSION

ENV DEBUG=0

CMD ["python3", "main.py"]
