#!/bin/bash

source .env

echo "SHUTDOWN: tetris-server"
curl -XPOST http://localhost:${X_SERVER_PORT}/shutdown
echo
