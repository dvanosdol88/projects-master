#!/mnt/c/Users/david/projects-master/venv/bin/python
"""
Codex CLI Orchestrator - Final Implementation
Central AI coordinator as defined in Technical Roadmap
"""

import os
import subprocess
import psycopg2
import time
from datetime import datetime
from typing import Dict, List
from dotenv import load_dotenv

# Load specialist router
import sys
sys.path.append('/mnt/c/Users/david/projects-master/files-from-ai-agents')
from codex_specialist_router import SpecialistRouter

load_dotenv()

class CodexMaestro:
    def __init__(self):
        # Verify Codex CLI
        if not os.getenv('OPENAI_API_KEY'):
            raise Exception("OPENAI_API_KEY not set!")
            
        # Database for MyProjects
        self.db_conn = "postgresql://mg_dashboard_user:IIoaNtYtmloBARxh90AJE7kG401255dU@dpg-d1e5jrfgi27c7389sk30-a.oregon-postgres.render.com/mg_dashboard?sslmode=require"
        
        # Queue API endpoint (if needed)
        self.queue_api = "http://127.0.0.1:5006"
        
        # Specialist router
        self.router = SpecialistRouter()
        
        # Working directory
        self.work_dir = "/mnt/c/Users/david/projects-master"
        
        print("🎭 Codex Maestro Initialized")
        print("=" * 60)
        print(self.router.get_specialist_summary())
    
    def fetch_tasks(self) -> List[Dict]:
        """Fetch pending tasks from MyProjects PostgreSQL"""
        try:
            conn = psycopg2.connect(self.db_conn)
            cur = conn.cursor()
            
            query = """
            SELECT t.id, p.title, t.text
            FROM dvo88_projects p
            JOIN dvo88_tasks t ON p.id = t.project_id
            WHERE t.checked = false AND t.is_for_later = false
            ORDER BY p.position ASC, t.position ASC
            LIMIT 5;
            """
            
            cur.execute(query)
            tasks = []
            for task_id, project, task_text in cur.fetchall():
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
    
    def delegate_to_specialist(self, agent: str, task: Dict):
        """Delegate task to specialist Claude instance"""
        
        task_desc = f"[{task['project']}] {task['task']}"
        
        print(f"\n📨 Delegating to {agent}")
        print(f"   Task: {task_desc}")
        
        # Use existing maestro_task_sender
        cmd = [
            self.work_dir + '/venv/bin/python',
            self.work_dir + '/maestro_task_sender.py',
            'general_task',
            agent,
            task_desc
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"   ✅ Successfully delegated")
                self.mark_task_assigned(task['id'], agent)
            else:
                print(f"   ❌ Failed: {result.stderr}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    def mark_task_assigned(self, task_id: int, agent: str):
        """Update task metadata to show assignment"""
        try:
            conn = psycopg2.connect(self.db_conn)
            cur = conn.cursor()
            
            # Update metadata with assignment info
            query = """
            UPDATE dvo88_tasks 
            SET metadata = jsonb_set(
                COALESCE(metadata, '{}'), 
                '{assigned_to}', 
                %s
            )
            WHERE id = %s;
            """
            
            cur.execute(query, (f'"{agent}"', task_id))
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(f"Failed to update task metadata: {e}")
    
    def orchestrate_cycle(self):
        """Run one orchestration cycle"""
        print(f"\n{'='*60}")
        print(f"🎼 CODEX MAESTRO ORCHESTRATION CYCLE")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        
        # Fetch tasks
        tasks = self.fetch_tasks()
        
        if not tasks:
            print("✨ No pending tasks")
            return
            
        print(f"\n📋 Found {len(tasks)} pending tasks:")
        
        # Route each task
        for i, task in enumerate(tasks, 1):
            print(f"\n{i}. {task['task'][:60]}...")
            
            # Use router to determine specialist
            routing = self.router.analyze_task(task['task'], task['project'])
            
            print(f"   → {routing['specialist']}")
            print(f"   Reasoning: {routing['reasoning']}")
            
            # Delegate to specialist
            self.delegate_to_specialist(routing['recommended_agent'], task)
            
            # Small delay between delegations
            time.sleep(2)
    
    def run_continuous(self, interval: int = 300):
        """Run orchestrator continuously (default 5 minutes)"""
        print(f"\n🚀 Starting Codex Maestro")
        print(f"   Polling interval: {interval} seconds")
        print(f"   Press Ctrl+C to stop")
        
        try:
            while True:
                self.orchestrate_cycle()
                print(f"\n💤 Next check in {interval} seconds...")
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n\n🛑 Codex Maestro shutting down")
    
    def run_once(self):
        """Run a single orchestration cycle"""
        self.orchestrate_cycle()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Codex CLI Orchestrator')
    parser.add_argument('--once', action='store_true', help='Run once and exit')
    parser.add_argument('--interval', type=int, default=300, help='Polling interval in seconds')
    
    args = parser.parse_args()
    
    maestro = CodexMaestro()
    
    if args.once:
        maestro.run_once()
    else:
        maestro.run_continuous(args.interval)