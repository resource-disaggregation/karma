#!/usr/bin/env bash

sudo apt update
sudo apt install build-essential
sudo apt install cmake
sudo apt-get install python3-setuptools
sudo apt install default-jdk
sudo apt install maven

mkdir -p build
cd build
cmake .. && make -j