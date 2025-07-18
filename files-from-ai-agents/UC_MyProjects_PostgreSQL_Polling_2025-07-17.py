#!/usr/bin/env python3
"""
MyProjects PostgreSQL Polling System
Polls Render PostgreSQL database for new tasks and delegates to appropriate AI agents
"""

import os
import psycopg2
import json
import time
import subprocess
from datetime import datetime
from urllib.parse import urlparse

class MyProjectsPoller:
    def __init__(self):
        # Get database URL from environment
        self.database_url = os.getenv('DATABASE_URL')
        if not self.database_url:
            raise Exception("DATABASE_URL environment variable not set")
        
        # Parse connection details
        url = urlparse(self.database_url)
        self.db_config = {
            'host': url.hostname,
            'port': url.port,
            'user': url.username,
            'password': url.password,
            'database': url.path[1:],
            'sslmode': 'require'
        }
        
    def connect(self):
        """Connect to PostgreSQL database"""
        return psycopg2.connect(**self.db_config)
    
    def get_pending_tasks(self):
        """Fetch all pending tasks from database"""
        conn = self.connect()
        cur = conn.cursor()
        
        query = """
        SELECT id, task, assigned_to, metadata
        FROM tasks
        WHERE status = 'pending'
        ORDER BY created ASC
        """
        
        cur.execute(query)
        tasks = []
        
        for row in cur.fetchall():
            task_id, task_text, assigned_to, metadata = row
            
            # Parse priority from metadata if available
            priority = 'medium'
            if metadata:
                priority = metadata.get('priority', 'medium')
            
            tasks.append({
                'id': task_id,
                'task': task_text,
                'assigned_to': assigned_to,
                'priority': priority,
                'metadata': metadata or {}
            })
        
        cur.close()
        conn.close()
        
        return tasks
    
    def delegate_task(self, task):
        """Delegate task to appropriate AI agent"""
        task_id = task['id']
        task_text = task['task']
        assigned_to = task['assigned_to'] or self.determine_agent(task_text)
        
        print(f"Delegating task {task_id} to {assigned_to}: {task_text}")
        
        # Use maestro_task_sender.py to create task
        cmd = [
            'python',
            '/mnt/c/Users/david/projects-master/maestro_task_sender.py',
            'general_task',
            assigned_to,
            task_text
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"Task {task_id} successfully delegated")
                self.mark_task_in_progress(task_id, assigned_to)
            else:
                print(f"Failed to delegate task {task_id}: {result.stderr}")
        except Exception as e:
            print(f"Error delegating task {task_id}: {e}")
    
    def determine_agent(self, task_text):
        """Determine which agent should handle the task based on content"""
        task_lower = task_text.lower()
        
        # Frontend/UI tasks -> Ubuntu Claude
        if any(word in task_lower for word in ['ui', 'frontend', 'react', 'dashboard', 'design']):
            return 'UC'
        
        # Backend/API tasks -> Debian Claude  
        elif any(word in task_lower for word in ['backend', 'api', 'database', 'server']):
            return 'DC'
        
        # DevOps/Deployment tasks -> Alpine Claude
        elif any(word in task_lower for word in ['deploy', 'devops', 'docker', 'ci/cd']):
            return 'AC'
        
        # Default to UC for general tasks
        else:
            return 'UC'
    
    def mark_task_in_progress(self, task_id, assigned_to):
        """Update task status to in_progress"""
        conn = self.connect()
        cur = conn.cursor()
        
        query = """
        UPDATE tasks 
        SET status = 'in_progress', 
            assigned_to = %s,
            metadata = jsonb_set(
                COALESCE(metadata, '{}'), 
                '{started_at}', 
                to_jsonb(%s)
            )
        WHERE id = %s
        """
        
        cur.execute(query, (assigned_to, datetime.now().isoformat(), task_id))
        conn.commit()
        
        cur.close()
        conn.close()
    
    def poll_continuously(self, interval=60):
        """Poll for new tasks every interval seconds"""
        print(f"Starting MyProjects polling (checking every {interval} seconds)")
        
        while True:
            try:
                tasks = self.get_pending_tasks()
                
                if tasks:
                    print(f"Found {len(tasks)} pending tasks")
                    
                    # Group by priority
                    high_priority = [t for t in tasks if t.get('priority') == 'high']
                    medium_priority = [t for t in tasks if t.get('priority') == 'medium']
                    low_priority = [t for t in tasks if t.get('priority') == 'low']
                    
                    # Process in priority order
                    for task in high_priority + medium_priority + low_priority:
                        self.delegate_task(task)
                else:
                    print("No pending tasks found")
                
            except Exception as e:
                print(f"Error polling tasks: {e}")
            
            time.sleep(interval)

def main():
    """Main entry point"""
    # Check if we have database access
    if not os.getenv('DATABASE_URL'):
        print("ERROR: DATABASE_URL not set")
        print("Please set: export DATABASE_URL='postgresql://user:pass@host:5432/dbname'")
        return
    
    poller = MyProjectsPoller()
    
    # Test connection
    try:
        conn = poller.connect()
        conn.close()
        print("Successfully connected to PostgreSQL database")
    except Exception as e:
        print(f"Failed to connect to database: {e}")
        return
    
    # Start polling
    poller.poll_continuously(interval=60)

if __name__ == "__main__":
    main()