import os
import time
from datetime import datetime

CLAUDE_TO_JULES = os.path.join('shared', 'claude-to-jules-message.md')
JULES_TO_CC = os.path.join('shared', 'jules-to-cc.md')


def read_message():
    """Return trimmed message from Claude or an empty string."""
    if not os.path.exists(CLAUDE_TO_JULES):
        return ''
    with open(CLAUDE_TO_JULES, 'r', encoding='utf-8') as f:
        return f.read().strip()


def clear_message_file():
    open(CLAUDE_TO_JULES, 'w').close()


def append_reply(message: str):
    timestamp = datetime.utcnow().isoformat()
    with open(JULES_TO_CC, 'a', encoding='utf-8') as f:
        f.write(f"{timestamp} - {message}\n")


def main():
    last_processed = ''
    while True:
        msg = read_message()
        if msg and msg != last_processed:
            append_reply(f"Received: {msg}")
            clear_message_file()
            last_processed = msg
        time.sleep(2)


if __name__ == '__main__':
    main()
