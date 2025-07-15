#!/bin/bash

SESSION="kathara-lab"
# Get the list of Kathará node names
NODES=$(sudo kathara list | awk -F'│' 'NF >= 3 { gsub(/^ +| +$/, "", $3); print $3 }' | tail -n +2)

# Start a new tmux session in the background
tmux new-session -d -s "$SESSION"

first=true
for NODE in $NODES; do
    if $first; then
        # First node in the first panel
        tmux send-keys -t "$SESSION" "sudo kathara connect $NODE" C-m
        first=false
    else
        # Split vertically (use -h for horizontal)
        tmux split-window -v -t "$SESSION"
        tmux select-layout -t "$SESSION" tiled
        tmux send-keys -t "$SESSION" "sudo kathara connect $NODE" C-m
    fi
done

# Attach to the tmux session
tmux attach -t "$SESSION"
