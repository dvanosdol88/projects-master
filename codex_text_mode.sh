#!/bin/bash
# Run Codex in text-only mode for copy/paste capability

echo "🎭 CODEX TEXT MODE - Copy/Paste Enabled"
echo "========================================"
echo ""
echo "This runs Codex in protocol mode which allows normal text I/O"
echo ""

# Load API key
export OPENAI_API_KEY=$(grep OPENAI_API_KEY .env | cut -d '=' -f2)

# Create a simple wrapper that uses protocol mode
cat << 'EOF' > /tmp/codex_session.txt
You are Maestro, the central orchestrator for the multi-agent development system.

Available agents:
- UC: Lead Developer (implementation)
- DC: Code Optimizer (refactoring, testing)
- AC: General Developer (features)

You can send tasks via the Queue API at http://127.0.0.1:5006/add_task

Current working directory: /mnt/c/Users/david/projects-master

What would you like to orchestrate?
EOF

# Run in protocol mode (allows copy/paste)
echo "Starting Codex in protocol mode..."
echo "Type your commands and press Enter. Type 'exit' to quit."
echo ""

cat /tmp/codex_session.txt | codex proto --skip-git-repo-check