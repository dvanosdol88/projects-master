#!/mnt/c/Users/david/projects-master/venv/bin/python
"""
Codex CLI Orchestrator
The true Maestro - fetches tasks, routes them, and coordinates agents
"""

import os
import sys
import time
import json
import requests
import psycopg2
import subprocess
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.append('/mnt/c/Users/david/projects-master/files-from-ai-agents')
from codex_task_router import TaskRouter

load_dotenv()

class CodexOrchestrator:
    def __init__(self):
        # Database connection (from DC)
        self.db_conn_string = "postgresql://mg_dashboard_user:IIoaNtYtmloBARxh90AJE7kG401255dU@dpg-d1e5jrfgi27c7389sk30-a.oregon-postgres.render.com/mg_dashboard?sslmode=require"
        
        # Queue API endpoint (if needed)
        self.queue_api = "http://127.0.0.1:5006"
        
        # Task router
        self.router = TaskRouter()
        
        # Track processed tasks to avoid duplicates
        self.processed_tasks = set()
        
        # Agent status
        self.agent_status = {
            'UC': {'busy': False, 'current_task': None},
            'DC': {'busy': False, 'current_task': None},
            'AC': {'busy': False, 'current_task': None}
        }
    
    def fetch_tasks_from_db(self) -> List[Dict]:
        """Fetch pending tasks from PostgreSQL"""
        try:
            conn = psycopg2.connect(self.db_conn_string)
            cur = conn.cursor()
            
            query = """
            SELECT 
                t.id,
                p.title as project,
                t.text as task,
                p.position as project_priority,
                t.position as task_priority
            FROM dvo88_projects p
            JOIN dvo88_tasks t ON p.id = t.project_id
            WHERE t.checked = false 
                AND t.is_for_later = false
            ORDER BY p.position ASC, t.position ASC
            LIMIT 10;
            """
            
            cur.execute(query)
            tasks = []
            
            for row in cur.fetchall():
                task_id, project, task_text, proj_pri, task_pri = row
                
                # Skip if already processed
                if task_id in self.processed_tasks:
                    continue
                    
                tasks.append({
                    'id': task_id,
                    'project': project,
                    'task': task_text,
                    'priority': proj_pri * 100 + task_pri,  # Combined priority
                    'source': 'postgresql'
                })
            
            cur.close()
            conn.close()
            return tasks
            
        except Exception as e:
            print(f"DB Error: {e}")
            return []
    
    def fetch_tasks_from_api(self) -> List[Dict]:
        """Fetch tasks from Queue API as backup"""
        try:
            resp = requests.get(f"{self.queue_api}/tasks", timeout=5)
            if resp.status_code == 200:
                tasks_data = resp.json()
                tasks = []
                
                # Handle different response formats
                if isinstance(tasks_data, list):
                    for i, task in enumerate(tasks_data):
                        if isinstance(task, str):
                            tasks.append({
                                'id': f'api_{i}',
                                'task': task,
                                'source': 'queue_api'
                            })
                        elif isinstance(task, dict):
                            tasks.append({
                                'id': task.get('id', f'api_{i}'),
                                'task': task.get('task', task.get('description', '')),
                                'project': task.get('project', 'Unknown'),
                                'source': 'queue_api'
                            })
                
                return tasks
        except Exception as e:
            print(f"Queue API Error: {e}")
            return []
    
    def delegate_to_agent(self, agent: str, task: Dict) -> bool:
        """Delegate task to specific agent via maestro_task_sender"""
        
        # Check if agent is busy
        if self.agent_status[agent]['busy']:
            print(f"⏳ {agent} is busy with another task")
            return False
        
        # Format task description
        task_desc = f"[{task.get('project', 'General')}] {task['task']}"
        
        print(f"\n🚀 Delegating to {agent}:")
        print(f"   Task: {task_desc}")
        
        cmd = [
            '/mnt/c/Users/david/projects-master/venv/bin/python',
            '/mnt/c/Users/david/projects-master/maestro_task_sender.py',
            'general_task',
            agent,
            task_desc
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"   ✅ Successfully delegated")
                self.agent_status[agent]['busy'] = True
                self.agent_status[agent]['current_task'] = task['id']
                self.processed_tasks.add(task['id'])
                return True
            else:
                print(f"   ❌ Delegation failed: {result.stderr}")
                return False
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False
    
    def process_tasks(self, tasks: List[Dict]):
        """Route and delegate tasks"""
        if not tasks:
            return
        
        print(f"\n📋 Processing {len(tasks)} tasks...")
        
        # Route all tasks
        routed_tasks = self.router.route_batch(tasks)
        
        # Delegate each task
        for task in routed_tasks:
            routing = task['routing']
            agent = routing['recommended_agent']
            
            print(f"\n📌 Task: {task['task'][:60]}...")
            print(f"   → {routing['agent_name']}")
            print(f"   Reasoning: {routing['reasoning']}")
            
            success = self.delegate_to_agent(agent, task)
            
            if not success:
                # Try next best agent
                sorted_agents = sorted(routing['scores'].items(), 
                                     key=lambda x: x[1], reverse=True)
                for backup_agent, score in sorted_agents[1:]:
                    if score > 0 and not self.agent_status[backup_agent]['busy']:
                        print(f"   🔄 Trying backup: {backup_agent}")
                        if self.delegate_to_agent(backup_agent, task):
                            break
    
    def check_agent_status(self):
        """Check if agents have completed their tasks"""
        # In a real implementation, we'd check with actual agents
        # For now, simulate completion after some time
        for agent, status in self.agent_status.items():
            if status['busy']:
                # Simulate task completion (in reality, check with agent)
                print(f"   ℹ️  {agent} working on task {status['current_task']}")
                # Reset after assumed completion (would check real status)
                # self.agent_status[agent]['busy'] = False
                # self.agent_status[agent]['current_task'] = None
    
    def run_cycle(self):
        """Run one orchestration cycle"""
        print(f"\n{'='*60}")
        print(f"🤖 CODEX ORCHESTRATOR CYCLE")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        
        # Check agent status
        self.check_agent_status()
        
        # Fetch tasks from primary source (DB)
        tasks = self.fetch_tasks_from_db()
        
        # Fallback to Queue API if needed
        if not tasks:
            print("No tasks in DB, checking Queue API...")
            tasks = self.fetch_tasks_from_api()
        
        if tasks:
            self.process_tasks(tasks)
        else:
            print("✨ No pending tasks found")
        
        # Show summary
        print(f"\n📊 Agent Status:")
        for agent, status in self.agent_status.items():
            status_icon = "🔴" if status['busy'] else "🟢"
            print(f"   {status_icon} {agent}: {'Busy' if status['busy'] else 'Available'}")
    
    def run_continuous(self, interval: int = 60):
        """Run orchestrator continuously"""
        print(f"🚀 Starting Codex Orchestrator")
        print(f"   Polling interval: {interval} seconds")
        print(f"   Press Ctrl+C to stop")
        
        try:
            while True:
                self.run_cycle()
                print(f"\n💤 Sleeping for {interval} seconds...")
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n\n👋 Codex Orchestrator shutting down")
    
    def run_once(self):
        """Run a single cycle"""
        self.run_cycle()


# CLI Interface
if __name__ == "__main__":
    orchestrator = CodexOrchestrator()
    
    if len(sys.argv) > 1 and sys.argv[1] == "once":
        # Run once mode
        orchestrator.run_once()
    else:
        # Continuous mode
        interval = int(sys.argv[1]) if len(sys.argv) > 1 else 60
        orchestrator.run_continuous(interval)