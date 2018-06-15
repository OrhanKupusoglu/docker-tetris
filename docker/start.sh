#!/bin/bash

#set -ex

source .env

arg=$1

DIR_RUN="$(cd "$(dirname "$0")" && pwd)"
cd $DIR_RUN

# activate virtual env first
source .venv/bin/activate

if [[ "$arg" == "mod" ]]
then
    export TETRIS_SERVER_SETTINGS="${DIR_RUN}/settings.cfg"
fi

export FLASK_APP=tetris-server/app.py

nohup flask run --host=0.0.0.0 --port="${FLASK_HTTP_PORT}" > /dev/null 2>&1 &

echo "-- Flask HTTP port: ${FLASK_HTTP_PORT}"
echo "-- started"

sleep 1

# ssh daemon
/usr/sbin/sshd -D
