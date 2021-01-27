#!/bin/sh
set -e
 
host="$1"
shift
cmd="$@"

while :
do
    if health="$(curl -fsSL "http://$host:9200/_cat/health?h=status")"; then
        # trim whitespace (otherwise we'll have "green ")
        health="$(echo "$health" | sed -r 's/^[[:space:]]+|[[:space:]]+$//g')" 
	if [ "$health" = 'green' ]; then
	        >&2 echo "Elasticsearch running..."
	        exec $cmd
                break
	fi
	>&2 echo "Unexpected ES health status: $health"
	sleep 1
    fi
done
exit 0

