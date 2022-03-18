#!/usr/bin/env bash

sudo apt update
sudo apt install -y build-essential cmake python3-setuptools openjdk-8-jre openjdk-8-jdk maven

mkdir -p build
cd build
cmake .. && make -j