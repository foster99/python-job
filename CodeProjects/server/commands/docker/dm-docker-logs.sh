#!/usr/bin/env bash

if [ $# -eq 1 ]; then
    docker-compose -f /root/delectame/server/containers/docker-compose.yml logs | grep $1
else
    echo "ERROR: You must specify the service"
fi