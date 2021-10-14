#!/usr/bin/env bash

if [ $# -eq 1 ]; then
    docker stop $1
    docker rm $1
else
    docker-compose -f /root/delectame/server/containers/docker-compose.yml down
fi