#/bin/bash +x
source /root/_home/.env
uvicorn main:app --host 0.0.0.0 --port 9000 >> /tmp/rag.log 2>&1
