#!/usr/bin/env bash

sbin="`dirname "$0"`"
sbin="`cd "$sbin"; pwd`"

mkdir -p /home/ubunu/deploy

cp $sbin/../build/storage/storaged /home/ubunu/deploy/
cp $sbin/../build/directory/directoryd /home/ubunu/deploy/
cp $sbin/../scripts/driver4.py /home/ubunu/deploy/
cp $sbin/* /home/ubunu/deploy/
