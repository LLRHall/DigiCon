#!/bin/bash

PROXY=http://172.16.2.30:8080

sudo add-apt-repository universe
sudo -E apt-get update
sudo -E apt-get install build-essential -y
sudo -E apt-get install python-dev -y
sudo -E apt-get install python-setuptools -y
sudo -E apt-get install python-pip -y
sudo pip --proxy=$PROXY install flask


