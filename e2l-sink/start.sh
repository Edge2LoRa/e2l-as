#!/bin/bash

export DEBUG=1
if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
    . venv/bin/activate && python3 main.py 
  else
    . venv/bin/activate && python3 main.py $1
fi
