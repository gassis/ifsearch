#!/bin/sh

set -e pipefail

echo "ElasticSearch server setup..."
while true
do
    echo "Testando acesso ao ES."
    if nc -zv elasticsearch 9200 ; then
        if health="$(curl -XGET "http://elasticsearch:9200/?pretty"")"; then
            echo $health
            # trim whitespace (otherwise we'll have "green ")
            health="$(echo "$health" | sed -r 's/^[[:space:]]+|[[:space:]]+$//g')" 
    	    if [ "$health" = 'green' ]; then
  	        echo "Elasticsearch running..."
                break
   	    fi
	    echo "Unexpected ES health status: $health"
    	    sleep 1
    	fi
    fi
    sleep 2
done
exit 0

