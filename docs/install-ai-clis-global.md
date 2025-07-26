# Installing Codex-CLI and Claude-CLI

This repository includes a helper script to set up the Codex and Claude command line interfaces system-wide on Ubuntu. The script installs the latest versions of both tools and verifies they are available on your PATH.

## Usage

Run the installer as root:

```bash
sudo bash scripts/install_ai_clis_global.sh
```

After installation, authenticate each CLI:

```bash
# Codex (GitHub OAuth + OpenAI key)
codex login

# Claude (Anthropic key)
claude auth login
```

Once logged in, you can call Claude directly from Codex:

```bash
codex repl .
> ! claude run --prompt "Hello from Codex!"
```
