#!/bin/bash

# Wait for Ollama to wake up
echo "Waiting for Ollama..."
until curl -s "$OLLAMA_HOST/api/tags" > /dev/null; do sleep 2; done

# If grep fails (model not found), the command after || runs
curl -s "$OLLAMA_HOST/api/tags" | grep -q "phi3" || \
  curl -X POST "$OLLAMA_HOST/api/pull" -d '{"name": "phi3"}'


# Start App
python app.py