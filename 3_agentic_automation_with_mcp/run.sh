#!/bin/bash
# server.sh - Start MCP server (background) + client application

pip3 install -r requirements.txt 

echo "Starting MCP server..."
python3 theme_server.py &

# Give the server a moment to start up
sleep 2

echo "Starting client application..."
streamlit run theme_chatbot.py
