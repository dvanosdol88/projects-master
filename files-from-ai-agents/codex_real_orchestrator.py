#!/mnt/c/Users/david/projects-master/venv/bin/python
"""
Real Codex CLI Orchestrator
Uses the actual OpenAI Codex CLI to orchestrate tasks
"""

import os
import subprocess
import json
import time
import psycopg2
from datetime import datetime
from typing import Dict, List
from dotenv import load_dotenv

load_dotenv()

class RealCodexOrchestrator:
    def __init__(self):
        # Verify API key
        if not os.getenv('OPENAI_API_KEY'):
            raise Exception("OPENAI_API_KEY not found in environment!")
            
        # Database connection
        self.db_conn_string = "postgresql://mg_dashboard_user:IIoaNtYtmloBARxh90AJE7kG401255dU@dpg-d1e5jrfgi27c7389sk30-a.oregon-postgres.render.com/mg_dashboard?sslmode=require"
        
        # Codex working directory
        self.work_dir = "/mnt/c/Users/david/projects-master"
        
    def ask_codex_to_route(self, tasks: List[Dict]) -> Dict[str, List[Dict]]:
        """Ask Codex CLI to analyze and route tasks"""
        
        # Create a prompt for Codex
        task_list = "\n".join([f"- [{t['project']}] {t['task']}" for t in tasks])
        
        prompt = f"""You are an AI task router. Analyze these tasks and determine which agent should handle each:

Agents:
- UC (Ubuntu Claude): Frontend, UI/UX, React, dashboards, design
- DC (Debian Claude): Backend, optimization, testing, APIs
- AC (Alpine Claude): DevOps, deployment, Docker, CI/CD

Tasks to route:
{task_list}

Output a JSON object mapping each task to an agent like:
{{"task1": "UC", "task2": "DC"}}"""

        # Call Codex
        cmd = [
            'codex', 'exec',
            '--skip-git-repo-check',
            '-C', self.work_dir,
            prompt
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, 
                                  env={**os.environ, 'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY')})
            
            if result.returncode == 0:
                # Parse Codex response
                output = result.stdout
                # Extract JSON from output (Codex might include explanation)
                import re
                json_match = re.search(r'\{[^}]+\}', output)
                if json_match:
                    routing = json.loads(json_match.group())
                    return routing
            else:
                print(f"Codex error: {result.stderr}")
                
        except Exception as e:
            print(f"Error calling Codex: {e}")
            
        return {}
    
    def delegate_task_via_codex(self, agent: str, task: Dict):
        """Use Codex to create and delegate task"""
        
        task_desc = f"[{task['project']}] {task['task']}"
        
        prompt = f"""Execute this Python code to delegate a task:

```python
import subprocess
cmd = ['/mnt/c/Users/david/projects-master/venv/bin/python', 
       '/mnt/c/Users/david/projects-master/maestro_task_sender.py',
       'general_task', '{agent}', '{task_desc}']
result = subprocess.run(cmd, capture_output=True, text=True)
print(f"Delegated to {agent}: {{result.returncode == 0}}")
```"""

        cmd = [
            'codex', 'exec',
            '--skip-git-repo-check',
            '--sandbox', 'workspace-write',
            '-C', self.work_dir,
            prompt
        ]
        
        try:
            subprocess.run(cmd, env={**os.environ, 'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY')})
        except Exception as e:
            print(f"Error delegating via Codex: {e}")
    
    def fetch_tasks_from_db(self) -> List[Dict]:
        """Fetch pending tasks from PostgreSQL"""
        try:
            conn = psycopg2.connect(self.db_conn_string)
            cur = conn.cursor()
            
            query = """
            SELECT 
                t.id,
                p.title as project,
                t.text as task
            FROM dvo88_projects p
            JOIN dvo88_tasks t ON p.id = t.project_id
            WHERE t.checked = false 
                AND t.is_for_later = false
            ORDER BY p.position ASC, t.position ASC
            LIMIT 5;
            """
            
            cur.execute(query)
            tasks = []
            
            for row in cur.fetchall():
                task_id, project, task_text = row
                tasks.append({
                    'id': task_id,
                    'project': project,
                    'task': task_text
                })
            
            cur.close()
            conn.close()
            return tasks
            
        except Exception as e:
            print(f"DB Error: {e}")
            return []
    
    def run_orchestration_cycle(self):
        """Run one complete orchestration cycle with Codex"""
        print(f"\n{'='*60}")
        print(f"🤖 REAL CODEX ORCHESTRATOR")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        
        # Fetch tasks
        tasks = self.fetch_tasks_from_db()
        
        if not tasks:
            print("No pending tasks found")
            return
            
        print(f"Found {len(tasks)} pending tasks")
        
        # Ask Codex to route them
        print("\n🧠 Asking Codex CLI to analyze and route tasks...")
        routing = self.ask_codex_to_route(tasks)
        
        if routing:
            print("\n📋 Codex routing decisions:")
            for i, task in enumerate(tasks):
                agent = routing.get(f"task{i+1}", "UC")  # Default to UC
                print(f"  - {task['task'][:50]}... → {agent}")
                
                # Delegate via Codex
                self.delegate_task_via_codex(agent, task)
        else:
            print("Failed to get routing from Codex")


if __name__ == "__main__":
    # Check for API key
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ OPENAI_API_KEY not set!")
        print("Please run: export OPENAI_API_KEY=sk-proj-your-key-here")
        exit(1)
    
    orchestrator = RealCodexOrchestrator()
    orchestrator.run_orchestration_cycle()