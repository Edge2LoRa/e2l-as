 #!/bin/bash

DATA_DIRECTORY="e2l-as-broker/data"
LOG_DIRECTORY="e2l-as-broker/log"
LOG_FILE="mosquitto.log"
LOG_FILE_PATH=${LOG_DIRECTORY}/${LOG_FILE}

mkdir ${DATA_DIRECTORY} > /dev/null 2>&1
ret=$?
if [ "$ret" == "0" ]
then
    echo "e2l as broker data directory created"
else
    echo "e2l as broker data directory already exixts"
fi
sudo chown 1883:1883 ${DATA_DIRECTORY} -R

mkdir ${LOG_DIRECTORY} > /dev/null 2>&1
ret=$?
if [ "$ret" == "0" ]
then
    echo "e2l as broker log directory created"
    touch ${LOG_FILE_PATH}
    echo "e2l as broker log file created"
else
    echo "e2l as broker log directory already exixts"
fi
chmod o+r ${LOG_FILE_PATH}
sudo chown 1883:1883 ${LOG_DIRECTORY} -R

docker build -t e2l-as-broker:v1.0.0 -f e2l-as-broker.Dockerfile .