#!/bin/bash

# Start HASH Honeypot
echo "Starting HASH Honeypot..."
gnome-terminal -- bash -c "npx hash-honeypot run myhoneypot2 -l file -f ./logs/attacks.log; exec bash"

# Start Python Monitoring Script
echo "Starting Python Monitoring Script..."
gnome-terminal -- bash -c "python myhoneypot2/monitor_hash_log.py; exec bash"

# Start Go Server
echo "Starting Go Server..."
gnome-terminal -- bash -c "go run --tags json1 apiserver/cmd/api/main.go; exec bash"

# Start FastAPI Server
echo "Starting FastAPI Server..."
gnome-terminal -- bash -c "cd fastapiserver && python -m uvicorn main:app --reload; exec bash"
