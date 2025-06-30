# Environment Setup

Follow these steps to prepare your shell for the assistant project:

1. Create `~/bootstrap_assistant.sh`:

   ```bash
   #!/usr/bin/env bash
   export ASSISTANT_PROJECT_ROOT="/mnt/c/Users/david/jules-workspace"
   cd "$ASSISTANT_PROJECT_ROOT" || exit 1
   ```

2. Make the script executable:

   ```bash
   chmod +x ~/bootstrap_assistant.sh
   ```

3. Add the script to your shell startup if it's not already present:

   ```bash
   echo 'source ~/bootstrap_assistant.sh' >> ~/.bashrc
   ```

   The line can be added manually or via your preferred editor. Ensure it only
   appears once in `~/.bashrc`.

4. Restart your shell or run `source ~/.bashrc` to apply the changes.
