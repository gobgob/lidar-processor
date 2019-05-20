#!/bin/bash

scp src/main/* pi@172.24.1.1:/home/pi/lidar-processor/

scp retrieve_packages.sh pi@172.24.1.1:/home/pi/lidar-processor/
# scp Python-3.7.3.tgz pi@172.24.1.1:/home/pi/lidar-processor/
