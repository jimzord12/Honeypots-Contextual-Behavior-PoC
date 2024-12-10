#!/bin/bash

# Create a new tmux session for the project
echo "Starting tmux session for all components..."

# Start the HASH Honeypot
tmux new-session -d -s honeypot "npx hash-honeypot run myhoneypot2 -l file -f ./logs/attacks.log" || echo "Failed to start HASH Honeypot"

# Add a pane for the Python monitoring script
tmux split-window -h "source ./venv/bin/activate && python myhoneypot2/monitor_hash_log.py || echo 'Failed to start Python Monitoring Script'" || echo "Failed to create Python monitoring pane"

# Add a pane for the Go server
tmux split-window -v "cd apiserver && go run --tags json1 cmd/api/main.go || echo 'Failed to start Go Server'" || echo "Failed to create Go server pane"

# Add a pane for the FastAPI server
tmux split-window -v "cd fastapiserver && source ../venv/bin/activate && python -m uvicorn main:app --reload || echo 'Failed to start FastAPI Server'" || echo "Failed to create FastAPI pane"

# Organize the panes in a tiled layout
tmux select-layout tiled

# Check if the session was created
tmux list-sessions || echo "tmux session creation failed"

# Attach to the session so you can view the output
tmux attach-session -t honeypot
