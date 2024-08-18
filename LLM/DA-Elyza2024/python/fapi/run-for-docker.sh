#/bin/bash +x
    while [ ! -f "/root/_home/.env" ]; do
	sleep 1
    done
source "/root/_home/.env"
#uvicorn main:app --host 0.0.0.0 --port 9000 >> /tmp/rag.log 2>&1
uvicorn main:app --host 0.0.0.0 --port 9000 >> /tmp/rag.log 
while 1; do
    sleep 100
done
