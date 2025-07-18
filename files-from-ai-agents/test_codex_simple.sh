#!/bin/bash
# Simple test script for Codex CLI

echo "🧪 Testing Codex CLI Installation"
echo "================================="

# Check if codex is installed
if command -v codex &> /dev/null; then
    echo "✅ Codex CLI found at: $(which codex)"
    echo "   Version: $(codex --version)"
else
    echo "❌ Codex CLI not found in PATH"
    exit 1
fi

# Check for API key
if [ -z "$OPENAI_API_KEY" ]; then
    echo ""
    echo "❌ OPENAI_API_KEY not set!"
    echo ""
    echo "To set it temporarily:"
    echo "  export OPENAI_API_KEY=sk-proj-your-key-here"
    echo ""
    echo "To set it permanently, create a .env file:"
    echo "  echo 'OPENAI_API_KEY=sk-proj-your-key-here' > .env"
    echo "  source setup_codex_env.sh"
    exit 1
else
    echo "✅ OPENAI_API_KEY is set"
fi

# Test basic functionality
echo ""
echo "🤖 Testing basic Codex functionality..."
echo ""

codex exec --skip-git-repo-check "Say 'Hello from Codex CLI!' and list 3 things you can help with"