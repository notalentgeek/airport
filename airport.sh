#!/bin/bash

# Start the web application when system starts. This file needs to corresponds
# with airport.service.

cd /root/airport
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker rmi -f $(docker images -a -q)
./utility_scripts/remove_and_reset.sh
./utility_scripts/utility.sh
docker-compose stop &&
yes | docker-compose rm &&
yes | docker-compose rm nginx &&
yes | docker-compose rm web &&
docker-compose build &&
docker-compose up -d &&
docker-compose up