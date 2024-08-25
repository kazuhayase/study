#/bin/bash +x
# replace to secrets # while [ ! -f "/root/_home/.env" ]; do
# replace to secrets #     sleep 1
# replace to secrets # done
# replace to secrets # source "/root/_home/.env"
source "/run/secrets/.env"

#python3 llama_mkvec.py
#cd fapi
uvicorn main:app --host 0.0.0.0 --port 9000 >> /tmp/rag.log 2>&1
#uvicorn main:app --host 0.0.0.0 --port 9000 >> /tmp/rag.log 
