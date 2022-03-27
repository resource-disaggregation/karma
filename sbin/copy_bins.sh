#!/usr/bin/env bash

sbin="`dirname "$0"`"
sbin="`cd "$sbin"; pwd`"

mkdir -p /home/ubuntu/deploy

cp $sbin/../scripts/driver4.py /home/ubuntu/deploy/
cp $sbin/../scripts/compute_allocations.py /home/ubuntu/deploy/
cp $sbin/* /home/ubuntu/deploy/
