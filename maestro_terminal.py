#!/mnt/c/Users/david/projects-master/venv/bin/python
"""
Maestro Terminal - A simple text interface for Codex orchestration
Allows copy/paste and normal terminal interaction
"""

import subprocess
import os
import sys
import requests
import json
from datetime import datetime

class MaestroTerminal:
    def __init__(self):
        # Load API key
        os.environ['OPENAI_API_KEY'] = self._load_api_key()
        self.queue_api = "http://127.0.0.1:5006"
        
    def _load_api_key(self):
        """Load API key from .env file"""
        try:
            with open('.env', 'r') as f:
                for line in f:
                    if line.startswith('OPENAI_API_KEY='):
                        return line.strip().split('=')[1]
        except:
            print("❌ Could not load API key from .env")
            sys.exit(1)
    
    def send_to_codex(self, prompt):
        """Send prompt to Codex and get response"""
        cmd = ['codex', 'exec', '--skip-git-repo-check', prompt]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            return f"Error: {e}"
    
    def send_task_to_agent(self, agent, task, project="General"):
        """Send task to agent via Queue API"""
        try:
            response = requests.post(
                f"{self.queue_api}/add_task",
                json={
                    "assigned_to": agent,
                    "task": task,
                    "project": project
                }
            )
            if response.status_code == 200:
                return f"✅ Task sent to {agent}"
            else:
                return f"❌ Failed to send task"
        except Exception as e:
            return f"❌ Queue API error: {e}"
    
    def check_queue_status(self):
        """Check Queue API status"""
        try:
            response = requests.get(f"{self.queue_api}/status")
            if response.status_code == 200:
                data = response.json()
                return f"""
Queue Status:
- Pending: {data['pending_tasks']}
- In Progress: {data['in_progress']}
- Completed: {data['completed']}
"""
            else:
                return "❌ Could not get queue status"
        except:
            return "❌ Queue API not accessible"
    
    def run_interactive(self):
        """Run interactive terminal"""
        print("🎭 MAESTRO TERMINAL")
        print("==================")
        print("A text-based interface for Codex orchestration")
        print("")
        print("Commands:")
        print("  task <agent> <description> - Send task to agent (UC/DC/AC)")
        print("  status                     - Check queue status")
        print("  codex <prompt>            - Send prompt to Codex")
        print("  help                      - Show this help")
        print("  exit                      - Exit terminal")
        print("")
        print("Agents:")
        print("  UC - Lead Developer (implementation)")
        print("  DC - Code Optimizer (refactoring, testing)")
        print("  AC - General Developer (features)")
        print("")
        
        while True:
            try:
                command = input("\nmaestro> ").strip()
                
                if command == "exit":
                    print("Goodbye!")
                    break
                
                elif command == "help":
                    print("Commands: task, status, codex, help, exit")
                
                elif command == "status":
                    print(self.check_queue_status())
                
                elif command.startswith("task "):
                    parts = command.split(" ", 2)
                    if len(parts) >= 3:
                        agent = parts[1].upper()
                        task = parts[2]
                        result = self.send_task_to_agent(agent, task)
                        print(result)
                    else:
                        print("Usage: task <agent> <description>")
                
                elif command.startswith("codex "):
                    prompt = command[6:]
                    print("🤔 Asking Codex...")
                    response = self.send_to_codex(prompt)
                    print(response)
                
                else:
                    print("Unknown command. Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit")
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    terminal = MaestroTerminal()
    terminal.run_interactive()