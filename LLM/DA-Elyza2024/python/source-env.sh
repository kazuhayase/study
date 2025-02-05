#/bin/bash +x
    while [ ! -f "/root/_home/.env" ]; do
	sleep 1
    done
source "/root/_home/.env"
