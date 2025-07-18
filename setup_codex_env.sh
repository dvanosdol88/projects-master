#!/bin/bash
# Setup script for Codex CLI environment variables

# Load environment variables from .env file
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
    echo "✅ Loaded environment variables from .env"
else
    echo "❌ No .env file found!"
    echo "Please create a .env file with your OPENAI_API_KEY"
    echo "Example:"
    echo "OPENAI_API_KEY=sk-proj-your-key-here"
    exit 1
fi

# Verify API key is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ OPENAI_API_KEY is not set!"
    exit 1
else
    echo "✅ OPENAI_API_KEY is configured"
fi

# Test Codex
echo ""
echo "Testing Codex CLI..."
codex exec --skip-git-repo-check "Say 'Hello from Codex!' and list your capabilities"