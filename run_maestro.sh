#!/bin/bash
# Run Maestro (Codex CLI) in non-interactive mode

# Load API key
export OPENAI_API_KEY=$(grep OPENAI_API_KEY .env | cut -d '=' -f2)

# Run Codex in exec mode with our orchestration logic
codex exec --skip-git-repo-check "
I am Maestro, the central orchestrator. I need to:
1. Check MyProjects database for pending tasks
2. Route tasks to specialist agents (UC for UI, DC for optimization, AC for implementation)
3. Use the codex_maestro.py script to coordinate

First, let me check for pending tasks:
\`\`\`bash
python files-from-ai-agents/UC_MyProjects_Check_Tasks_2025-07-17.py
\`\`\`
"