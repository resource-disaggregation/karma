#!/usr/bin/env bash

sudo apt update
sudo apt install -y build-essential cmake python3-setuptools python3-pip python-pip openjdk-8-jre openjdk-8-jdk maven

python3 -m pip install thrift
sudo python -m pip install thrift
python3 -m pip install 'pytest-runner==3.0'
sudo python -m pip install 'pytest-runner==3.0'

mkdir -p build
cd build
cmake .. && make -j && cd pyjiffy/ && python3 -m pip install .