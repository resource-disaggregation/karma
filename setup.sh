#!/usr/bin/env bash

sudo apt update
sudo apt install build-essential
sudo apt install cmake
sudo apt-get install python3-setuptools
sudo apt install default-jdk
sudo apt install maven

git clone https://github.com/webglider/jiffy
git checkout asplos23

mkdir -p build
cd build
cmake .. && make -j