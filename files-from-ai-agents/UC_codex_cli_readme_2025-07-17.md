# Codex CLI README Summary

## Overview
Codex CLI is an open-source AI coding agent that runs in the terminal, designed to help developers generate, modify, and understand code through natural language interactions.

## Core Capabilities
- Runs locally on your computer
- Supports interactive and non-interactive modes
- Can generate code, refactor, write tests, and explain complex concepts
- Supports multiple AI model providers
- Runs commands in a secure, sandboxed environment

## Installation Options
```bash
# Brew
brew install codex

# npm
npm i -g @openai/codex

# Direct binary download from GitHub Releases
```

## Key Technical Details
- Supports OpenAI API and other compatible model providers
- Configurable security model with approval policies
- Platform-specific sandboxing (macOS, Linux)
- Supports Zero Data Retention (ZDR) configurations
- Logging via `RUST_LOG` environment variable

## Unique Features
- Multimodal input support
- **Model Context Protocol (MCP) server compatibility** ← This is KEY for our integration!
- Configurable via `~/.codex/config.toml`
- Supports different sandbox and approval modes

## System Requirements
- macOS 12+, Ubuntu 20.04+/Debian 10+, Windows via WSL2
- 4-8 GB RAM recommended
- Git 2.23+ recommended

## License
Apache-2.0 license

---
*This could be a game-changer for our multi-agent system!*