#!/usr/bin/env bash

# Tested on Ubuntu 18.04
sudo apt update
sudo apt install -y build-essential cmake python3-setuptools python3-pip python-pip openjdk-8-jre openjdk-8-jdk maven libssl-dev

python3 -m pip install thrift
sudo python -m pip install thrift
python3 -m pip install 'pytest-runner==3.0'
sudo python -m pip install 'pytest-runner==3.0'

sudo update-alternatives --set java /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java

# install latest cmake (for 18.04)
wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | gpg --dearmor - | sudo tee /etc/apt/trusted.gpg.d/kitware.gpg >/dev/null
sudo apt-add-repository 'deb https://apt.kitware.com/ubuntu/ bionic main'
sudo apt update
sudo apt install cmake

mkdir -p build
cd build
cmake .. && make -j && cd pyjiffy/ && python3 -m pip install .