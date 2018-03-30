#!/bin/bash

PROXY=http://172.16.2.30:8080

export https_proxy=$PROXY
export http_proxy=$PROXY

sudo add-apt-repository universe
sudo -E apt-get update
sudo -E apt-get install build-essential -y
sudo -E apt-get install python3-dev -y
sudo -E apt-get install python3-setuptools -y
sudo -E apt-get install python3-pip -y
sudo pip3 --proxy=$PROXY install flask
sudo pip3 --proxy=$PROXY install boto3
sudo pip3 --proxy=$PROXY install requests
sudo pip3 --proxy=$PROXY install json2html
sudo pip3 --proxy=$PROXY install fpdf
sudo pip3 --proxy=$PROXY install pattern
sudo -E apt-get install python3-opencv
