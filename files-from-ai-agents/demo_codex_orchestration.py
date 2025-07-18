#!/mnt/c/Users/david/projects-master/venv/bin/python
"""
Demo: How Codex CLI orchestrates tasks
"""

import subprocess
import os
from dotenv import load_dotenv

load_dotenv()

# Example tasks that would come from MyProjects
demo_tasks = [
    {"project": "Personal Dashboard", "task": "Add dark mode toggle to settings page"},
    {"project": "Operations Center", "task": "Optimize database queries for faster loading"},
    {"project": "MyProjects", "task": "Deploy latest version to Render"}
]

print("🎭 DEMO: Codex CLI Task Orchestration")
print("="*60)
print("\nSample tasks from MyProjects:")
for i, task in enumerate(demo_tasks, 1):
    print(f"{i}. [{task['project']}] {task['task']}")

print("\n🤖 Asking Codex to analyze and route these tasks...")

# Create prompt for Codex
task_list = "\n".join([f"- [{t['project']}] {t['task']}" for t in demo_tasks])

prompt = f"""You are the AI orchestrator for a multi-agent development system. 
Analyze these tasks and determine which specialist agent should handle each:

Available Agents:
- UC (Ubuntu Claude): Frontend specialist - UI/UX, React, dashboards, design
- DC (Debian Claude): Optimization specialist - backend, testing, performance, APIs  
- AC (Alpine Claude): DevOps specialist - deployment, Docker, CI/CD, infrastructure

Tasks to route:
{task_list}

For each task, explain your reasoning and assign it to the most appropriate agent.
Format: Task N -> AGENT (reasoning)"""

# Call Codex
cmd = [
    'codex', 'exec',
    '--skip-git-repo-check',
    prompt
]

env = os.environ.copy()
env['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

print("\n" + "-"*60)
result = subprocess.run(cmd, env=env)
print("-"*60)

print("\n✅ This demonstrates how Codex CLI would:")
print("   1. Analyze incoming tasks from MyProjects")
print("   2. Use AI reasoning to route to the right specialist")
print("   3. Delegate tasks via maestro_task_sender.py")
print("\n🚀 Ready to replace the old Maestro system!")