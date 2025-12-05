#!/bin/bash

# Wait for Ollama to wake up
echo "Waiting for Ollama..."
until curl -s "$OLLAMA_HOST/api/tags" > /dev/null; do sleep 2; done

# If grep fails (model not found), the command after || runs
curl -s "$OLLAMA_HOST/api/tags" | grep -q "hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF" || \
  curl -X POST "$OLLAMA_HOST/api/pull" -d '{"name": "hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF"}'


# Start App
python app.py
