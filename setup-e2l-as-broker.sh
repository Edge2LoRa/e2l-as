 #!/bin/bash

DATA_DIRECTORY="e2l-as-broker/data"
LOG_DIRECTORY="e2l-as-broker/log"

mkdir ${DATA_DIRECTORY} > /dev/null 2>&1
ret=$?
if [ "$ret" == "0" ]
then
    echo "e2l as broker data directory created"
else
    echo "e2l as broker data directory already exixts"
fi

mkdir ${LOG_DIRECTORY} > /dev/null 2>&1
ret=$?
if [ "$ret" == "0" ]
then
    echo "e2l as broker log directory created"
else
    echo "e2l as broker log directory already exixts"
fi
