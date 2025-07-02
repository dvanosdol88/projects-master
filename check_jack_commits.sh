#!/bin/bash

echo "Fetching last 5 commits by Jules:"
git log --author="Jules" -n 5 > docs/jules_recent_commits.txt

echo "Fetching last 5 commits by Claude Code:"
git log --author="Claude Code" -n 5 > docs/claude_recent_commits.txt

echo "Done. Recent commits saved to docs/jules_recent_commits.txt and docs/claude_recent_commits.txt"