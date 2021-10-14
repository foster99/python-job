#!/usr/bin/env bash

if [ $# -eq 1 ]; then
    docker exec -ti $1 bash
else
    echo "ERROR: You must specify the service"
fi
