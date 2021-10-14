#!/usr/bin/env bash

echo -e "\033[34;47m                      CLEANING DOCKER GARBAGE                                 \033[0m"
docker system prune
docker system df
