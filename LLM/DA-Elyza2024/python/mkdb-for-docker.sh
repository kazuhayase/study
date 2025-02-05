#while [ ! -f "/root/_home/.env" ]; do
#    sleep 1
#done
ls "/run"
ls "/run/secrets"
#source "/root/_home/.env"
#source "/run/secrets/env"
source "/run/secrets/.env"
env | grep -i key
/usr/local/bin/python3 llama_mkvec.py >> /tmp/mkvec.log 2>&1
