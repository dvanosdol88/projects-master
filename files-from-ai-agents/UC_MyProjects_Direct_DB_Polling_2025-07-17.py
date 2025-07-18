#!/mnt/c/Users/david/projects-master/venv/bin/python
"""
MyProjects Direct Database Polling System
Polls Render PostgreSQL database for prioritized tasks and delegates to AI agents
Uses DC's provided connection details and priority schema
"""

import psycopg2
import time
import subprocess
from datetime import datetime

class MyProjectsDatabasePoller:
    def __init__(self):
        # Direct connection string from DC
        self.connection_string = "postgresql://mg_dashboard_user:IIoaNtYtmloBARxh90AJE7kG401255dU@dpg-d1e5jrfgi27c7389sk30-a.oregon-postgres.render.com/mg_dashboard?sslmode=require"
        
    def connect(self):
        """Connect to PostgreSQL database"""
        return psycopg2.connect(self.connection_string)
    
    def get_prioritized_tasks(self, limit=10):
        """Fetch uncompleted tasks in priority order"""
        conn = self.connect()
        cur = conn.cursor()
        
        # Query from DC's guide - gets tasks in priority order
        query = """
        SELECT 
            p.title as project_name,
            p.position as project_priority,
            t.text as task_description,
            t.position as task_priority,
            t.id as task_id,
            p.color as project_color
        FROM dvo88_projects p
        JOIN dvo88_tasks t ON p.id = t.project_id
        WHERE t.checked = false 
            AND t.is_for_later = false
        ORDER BY p.position ASC, t.position ASC
        LIMIT %s;
        """
        
        cur.execute(query, (limit,))
        tasks = []
        
        for row in cur.fetchall():
            project_name, project_priority, task_text, task_priority, task_id, project_color = row
            
            tasks.append({
                'task_id': task_id,
                'project': project_name,
                'project_priority': project_priority,
                'task': task_text,
                'task_priority': task_priority,
                'color': project_color
            })
        
        cur.close()
        conn.close()
        
        return tasks
    
    def get_top_priority_task(self):
        """Get the single highest priority uncompleted task"""
        conn = self.connect()
        cur = conn.cursor()
        
        query = """
        SELECT 
            p.title as project_name,
            t.text as task_description,
            t.id as task_id
        FROM dvo88_projects p
        JOIN dvo88_tasks t ON p.id = t.project_id
        WHERE t.checked = false 
            AND t.is_for_later = false
        ORDER BY p.position ASC, t.position ASC
        LIMIT 1;
        """
        
        cur.execute(query)
        result = cur.fetchone()
        
        cur.close()
        conn.close()
        
        if result:
            project_name, task_text, task_id = result
            return {
                'task_id': task_id,
                'project': project_name,
                'task': task_text
            }
        return None
    
    def determine_agent(self, project_name, task_text):
        """Determine which agent should handle the task"""
        task_lower = task_text.lower()
        project_lower = project_name.lower()
        
        # Frontend/UI tasks -> Ubuntu Claude
        if any(word in task_lower for word in ['ui', 'frontend', 'react', 'dashboard', 'design', 'style', 'css']):
            return 'UC'
        
        # Personal Dashboard is primarily frontend
        if 'personal dashboard' in project_lower:
            return 'UC'
        
        # Backend/API tasks -> Debian Claude  
        elif any(word in task_lower for word in ['backend', 'api', 'database', 'server', 'postgresql']):
            return 'DC'
        
        # DevOps/Deployment tasks -> Alpine Claude
        elif any(word in task_lower for word in ['deploy', 'devops', 'docker', 'ci/cd', 'render']):
            return 'AC'
        
        # Default to UC for general tasks
        else:
            return 'UC'
    
    def delegate_task(self, task_info):
        """Delegate task to appropriate AI agent"""
        task_id = task_info['task_id']
        task_text = task_info['task']
        project = task_info['project']
        
        # Determine which agent should handle this
        agent = self.determine_agent(project, task_text)
        
        # Format task with project context
        full_task = f"[Project: {project}] {task_text}"
        
        print(f"\n📋 Delegating Task #{task_id}")
        print(f"   Project: {project}")
        print(f"   Task: {task_text}")
        print(f"   Agent: {agent}")
        
        # Use maestro_task_sender.py to create task
        cmd = [
            '/mnt/c/Users/david/projects-master/venv/bin/python',
            '/mnt/c/Users/david/projects-master/maestro_task_sender.py',
            'general_task',
            agent,
            full_task
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"   ✅ Successfully delegated to {agent}")
                # Note: We don't mark as checked - agent will do that when complete
            else:
                print(f"   ❌ Failed to delegate: {result.stderr}")
        except Exception as e:
            print(f"   ❌ Error delegating: {e}")
    
    def mark_task_completed(self, task_id):
        """Mark a task as completed in the database"""
        conn = self.connect()
        cur = conn.cursor()
        
        query = """
        UPDATE dvo88_tasks 
        SET checked = true, updated_at = CURRENT_TIMESTAMP
        WHERE id = %s;
        """
        
        cur.execute(query, (task_id,))
        conn.commit()
        
        cur.close()
        conn.close()
        
        print(f"✅ Marked task {task_id} as completed")
    
    def display_task_summary(self):
        """Display current task priorities"""
        tasks = self.get_prioritized_tasks(limit=20)
        
        print("\n" + "="*60)
        print("📊 MYPROJECTS TASK SUMMARY")
        print("="*60)
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total pending tasks: {len(tasks)}")
        print("\nTop 5 Priority Tasks:")
        print("-"*60)
        
        for i, task in enumerate(tasks[:5]):
            print(f"{i+1}. [{task['project']}] {task['task'][:50]}...")
        
        print("="*60 + "\n")
    
    def poll_single_task(self):
        """Poll and delegate one top priority task"""
        task = self.get_top_priority_task()
        
        if task:
            self.delegate_task(task)
            return True
        else:
            print("No pending tasks found")
            return False
    
    def poll_continuously(self, interval=300, batch_size=1):
        """Poll for new tasks every interval seconds"""
        print(f"🚀 Starting MyProjects Database Polling")
        print(f"   Interval: {interval} seconds")
        print(f"   Batch size: {batch_size} task(s) per cycle")
        print(f"   Database: Direct PostgreSQL connection")
        
        while True:
            try:
                # Display summary
                self.display_task_summary()
                
                # Get and delegate tasks
                tasks = self.get_prioritized_tasks(limit=batch_size)
                
                if tasks:
                    for task in tasks:
                        self.delegate_task(task)
                        time.sleep(2)  # Small delay between delegations
                else:
                    print("No pending tasks to delegate")
                
            except Exception as e:
                print(f"❌ Error during polling: {e}")
            
            print(f"\n💤 Sleeping for {interval} seconds...")
            time.sleep(interval)

def main():
    """Main entry point"""
    poller = MyProjectsDatabasePoller()
    
    # Test connection
    try:
        conn = poller.connect()
        conn.close()
        print("✅ Successfully connected to MyProjects PostgreSQL database")
    except Exception as e:
        print(f"❌ Failed to connect to database: {e}")
        return
    
    # Show current tasks
    poller.display_task_summary()
    
    # Ask for mode
    print("\nPolling Modes:")
    print("1. Single task (delegate one task and exit)")
    print("2. Continuous polling (check every 5 minutes)")
    print("3. Test mode (show tasks only, no delegation)")
    
    mode = input("\nSelect mode (1-3): ").strip()
    
    if mode == "1":
        poller.poll_single_task()
    elif mode == "2":
        poller.poll_continuously(interval=300, batch_size=1)
    elif mode == "3":
        tasks = poller.get_prioritized_tasks(limit=10)
        print("\nTest Mode - Current Tasks:")
        for i, task in enumerate(tasks):
            print(f"{i+1}. [{task['project']}] {task['task']}")
    else:
        print("Invalid mode selected")

if __name__ == "__main__":
    main()