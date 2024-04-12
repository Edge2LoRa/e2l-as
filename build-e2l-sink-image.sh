 #!/bin/bash

if [ -z "$1" ]
then
    echo "Please, provide the image tag"
    exit 1
fi

image_tag=$1

docker build -t e2l-sink:$image_tag -f e2l-sink.Dockerfile ./e2l-sink/