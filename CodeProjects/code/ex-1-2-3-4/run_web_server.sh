#!/usr/bin/env bash

# set python environment

source ./python-database-env/bin/activate

python ./webApp/app/manage.py runserver
