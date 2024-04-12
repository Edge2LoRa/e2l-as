!/bin/bash

python3 -m grpc_tools.protoc \
    -Iprotos --python_out=rpc_module/__private__ \
    --pyi_out=rpc_module/__private__ \
    --grpc_python_out=rpc_module/__private__ ./protos/edge2applicationserver.proto
    
python3 -m grpc_tools.protoc \
    -Iprotos --python_out=e2l_module/__private__ \
    --pyi_out=e2l_module/__private__ \
    --grpc_python_out=e2l_module/__private__ ./protos/demo.proto

python3 -m grpc_tools.protoc \
    -Iprotos --python_out=e2gw_rpc_client \
    --pyi_out=e2gw_rpc_client \
    --grpc_python_out=e2gw_rpc_client ./protos/edge2gateway.proto
