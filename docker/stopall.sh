#!/bin/bash

# stop all containers
sudo docker stop $(sudo docker ps -a -q)


