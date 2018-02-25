#!/bin/bash

DIR_RUN="$(cd "$(dirname "$0")" && pwd)"
cd $DIR_RUN

rm -f tetris-server.tar.gz
tar -czf tetris-server.tar.gz start.sh stop.sh .env -C .. tetris-server/ requirements.txt settings.cfg --exclude __pycache__ --exclude static/log/* --exclude static/tetris

docker-compose up app
