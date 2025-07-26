#!/usr/bin/env bash
# install_ai_clis_global.sh
# ---------------------------------------------------------------------------
# Installs *globally* (system-wide) on Ubuntu:
#   • Codex-CLI  –>  /usr/local/bin/codex
#   • Claude-CLI –>  /usr/local/bin/claude         (Anthropic)
#
# Designed for a fresh or existing server where Python 3.x is already present.
# Run with:   sudo bash install_ai_clis_global.sh
# ---------------------------------------------------------------------------

set -euo pipefail

echo "==> Updating package index & installing prerequisites..."
apt-get update -y
apt-get install -y curl python3 python3-pip

# ---------------------------------------------------------------------------
# 1. Install / upgrade Codex-CLI (OpenAI) globally
# ---------------------------------------------------------------------------
echo "==> Installing Codex-CLI..."
curl -fsSL https://raw.githubusercontent.com/openai/codex-cli/main/install.sh \
  | bash -s -- --prefix /usr/local

# confirm
if ! command -v codex >/dev/null; then
  echo "❌ Codex installation failed (codex not in PATH)." >&2
  exit 1
fi
echo "✅ Codex-CLI installed at: $(command -v codex)"

# ---------------------------------------------------------------------------
# 2. Install Claude-CLI (Anthropic) globally
#    NOTE: Adjust the package name/version if Anthropic updates it.
# ---------------------------------------------------------------------------
echo "==> Installing Claude-CLI (Anthropic)..."
python3 -m pip install --upgrade --no-cache-dir anthropic-cli

# create a convenience symlink `claude`  -> `anthropic` binary if needed
if command -v anthropic >/dev/null && ! command -v claude >/dev/null; then
  ln -s "$(command -v anthropic)" /usr/local/bin/claude
fi

# confirm
if ! command -v claude >/dev/null; then
  echo "❌ Claude installation failed (claude not in PATH)." >&2
  exit 1
fi
echo "✅ Claude-CLI installed at: $(command -v claude)"

# ---------------------------------------------------------------------------
# 3. Post-install verification
# ---------------------------------------------------------------------------
echo "==> Verifying versions..."
codex --version   || echo "Codex version check failed."
claude --version  || echo "Claude version check failed."

# ---------------------------------------------------------------------------
# 4. Reminder to authenticate
# ---------------------------------------------------------------------------
cat <<'EOM'

🎉  Both CLIs are installed system-wide.

Next steps (run as your normal user, NOT root):

    # Log in to Codex-CLI (GitHub OAuth + OpenAI key)
    codex login

    # Log in to Claude-CLI (Anthropic key)
    claude auth login

Once logged in, Codex can shell-out to Claude from any directory:

    codex repl .
    > ! claude run --prompt "Hello from Codex!"

EOM
