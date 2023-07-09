#!/usr/bin/env bash

sbin="`dirname "$0"`"
sbin="`cd "$sbin"; pwd`"

config=$1


JIFFY_SERVERS=~/karma-clients.txt $sbin/hosts.sh cat ~/karma-eval/$config.tenant* | grep -i error
JIFFY_SERVERS=~/karma-clients.txt $sbin/hosts.sh cat ~/karma-eval/$config.tenant* | grep -i exception

echo "Number of users that returned"
JIFFY_SERVERS=~/karma-clients.txt $sbin/hosts.sh cat ~/karma-eval/$config.tenant* | grep -i throughput | wc -l

JIFFY_SERVERS=~/karma-clients.txt $sbin/hosts.sh cat ~/karma-eval/$config.tenant* > ~/karma-eval/$config.results
echo "Done"