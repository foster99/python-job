#!/usr/bin/env bash

# Ejecutar un comanodo dentro de un container (HECHO PARA JENKINS)

function docker_cleanup {
    docker exec $IMAGE bash -c "if [ -f $PIDFILE ]; then kill -TERM -\$(cat $PIDFILE); rm $PIDFILE; fi"
}

IMAGE=$1
PIDFILE=/tmp/docker-exec-$$
shift
trap 'kill $PID; docker_cleanup $IMAGE $PIDFILE' TERM INT
docker exec $IMAGE bash -c "echo \"\$\$\" > $PIDFILE; exec $*" &
PID=$!
wait $PID
trap - TERM INT
wait $PID

