#!/usr/bin/env bash

sbin="`dirname "$0"`"
sbin="`cd "$sbin"; pwd`"

hosts_csv=$1
shift;

l1_hosts=($(cat $hosts_csv))

for i in "${!l1_hosts[@]}"; do 
    SERVERLIST="${l1_hosts[$i]}" $sbin/hosts.sh /home/ubuntu/deploy/start_drivers4.sh "$@" "${!l1_hosts[@]}" $i
done