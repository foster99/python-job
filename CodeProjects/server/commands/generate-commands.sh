#!/usr/bin/env bash

echo "\033[30;42m REMOVING OLD COMMANDS \033[0m"
rm -rf /usr/bin/dm-*

echo "\033[30;42m GENERATING COMMANDS \033[0m"
mkdir -p /root/delectame/server/commands/generated
ENT="$1"
COMMANDS_ROOT="/root/delectame/server/commands/"
DOCKER_COMMANDS_ROOT=$COMMANDS_ROOT"docker/"
TOOLS_COMMANDS_ROOT=$COMMANDS_ROOT"tools/"

# COMMANDS TO DO DOCKER PROCESSES
cp "$DOCKER_COMMANDS_ROOT"dm-docker-down.sh "$COMMANDS_ROOT"generated/dm-docker-down.sh
cp "$DOCKER_COMMANDS_ROOT"dm-docker-logs.sh "$COMMANDS_ROOT"generated/dm-docker-logs.sh
cp "$DOCKER_COMMANDS_ROOT"dm-docker-ps.sh "$COMMANDS_ROOT"generated/dm-docker-ps.sh
cp "$DOCKER_COMMANDS_ROOT"dm-docker-rebuild.sh "$COMMANDS_ROOT"generated/dm-docker-rebuild.sh
cp "$DOCKER_COMMANDS_ROOT"dm-docker-ssh.sh "$COMMANDS_ROOT"generated/dm-docker-ssh.sh
cp "$DOCKER_COMMANDS_ROOT"dm-docker-up.sh "$COMMANDS_ROOT"generated/dm-docker-up.sh
cp "$DOCKER_COMMANDS_ROOT"dm-docker-exec.sh "$COMMANDS_ROOT"generated/dm-docker-exec.sh
cp "$DOCKER_COMMANDS_ROOT"dm-docker-group-up.sh "$COMMANDS_ROOT"generated/dm-docker-group-up.sh
cp "$DOCKER_COMMANDS_ROOT"dm-docker-clean.sh "$COMMANDS_ROOT"generated/dm-docker-clean.sh

echo "\033[30;42m COPYING COMMANDS TO /usr/bin \033[0m"
cp "$COMMANDS_ROOT"generated/dm-docker-clean.sh /usr/bin/dm-docker-clean
cp "$COMMANDS_ROOT"generated/dm-docker-down.sh /usr/bin/dm-docker-down
cp "$COMMANDS_ROOT"generated/dm-docker-logs.sh /usr/bin/dm-docker-logs
cp "$COMMANDS_ROOT"generated/dm-docker-ps.sh /usr/bin/dm-docker-ps
cp "$COMMANDS_ROOT"generated/dm-docker-rebuild.sh /usr/bin/dm-docker-rebuild
cp "$COMMANDS_ROOT"generated/dm-docker-ssh.sh /usr/bin/dm-docker-ssh
cp "$COMMANDS_ROOT"generated/dm-docker-up.sh /usr/bin/dm-docker-up
cp "$COMMANDS_ROOT"generated/dm-docker-exec.sh /usr/bin/dm-docker-exec
cp "$COMMANDS_ROOT"generated/dm-docker-group-up.sh /usr/bin/dm-docker-group-up

echo "\033[30;42m CHANGING PERMISSIONS \033[0m"
chmod 755 /usr/bin/dm-docker-clean
chmod 755 /usr/bin/dm-docker-down
chmod 755 /usr/bin/dm-docker-logs
chmod 755 /usr/bin/dm-docker-ps
chmod 755 /usr/bin/dm-docker-rebuild
chmod 755 /usr/bin/dm-docker-ssh
chmod 755 /usr/bin/dm-docker-up
chmod 755 /usr/bin/dm-docker-exec
chmod 755 /usr/bin/dm-docker-group-up

echo "\033[30;42m DELETING DEBRIS \033[0m"
rm -rf /root/delectame/server/commands/generated