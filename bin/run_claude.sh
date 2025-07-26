#!/usr/bin/env bash
# Simple wrapper to run the Claude CLI non-interactively
CLAUDE_CMD=${CLAUDE_CMD:-claude}

if [ -z "$1" ]; then
  echo "Usage: $0 <prompt>" >&2
  exit 1
fi

printf "%s" "$1" | "$CLAUDE_CMD"
