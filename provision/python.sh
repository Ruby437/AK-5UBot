#!/usr/bin/env bash

apt-get update
apt-get install -y python3
apt-get install -y python3-pip
pip3 install libxml2
pip3 install discord
pip3 install urllib
pip3 install pyquery

cd
git pull
python3 main.py