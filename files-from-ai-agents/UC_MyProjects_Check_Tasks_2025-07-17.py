#!/mnt/c/Users/david/projects-master/venv/bin/python
"""
Quick script to check MyProjects tasks without interaction
"""

import psycopg2
from datetime import datetime

def check_myprojects_tasks():
    """Check and display all pending tasks from MyProjects"""
    
    # Connection string from DC
    conn_string = "postgresql://mg_dashboard_user:IIoaNtYtmloBARxh90AJE7kG401255dU@dpg-d1e5jrfgi27c7389sk30-a.oregon-postgres.render.com/mg_dashboard?sslmode=require"
    
    try:
        conn = psycopg2.connect(conn_string)
        cur = conn.cursor()
        
        # Get all uncompleted tasks
        query = """
        SELECT 
            p.title as project_name,
            p.position as project_priority,
            t.text as task_description,
            t.position as task_priority,
            t.id as task_id,
            t.checked
        FROM dvo88_projects p
        JOIN dvo88_tasks t ON p.id = t.project_id
        WHERE t.is_for_later = false
        ORDER BY p.position ASC, t.position ASC;
        """
        
        cur.execute(query)
        all_tasks = cur.fetchall()
        
        # Separate completed and pending
        pending_tasks = [t for t in all_tasks if not t[5]]  # checked = false
        completed_tasks = [t for t in all_tasks if t[5]]    # checked = true
        
        print("\n" + "="*80)
        print("📊 MYPROJECTS DATABASE STATUS")
        print("="*80)
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total tasks: {len(all_tasks)}")
        print(f"Pending: {len(pending_tasks)}")
        print(f"Completed: {len(completed_tasks)}")
        
        if pending_tasks:
            print("\n" + "="*80)
            print("🎯 PENDING TASKS (in priority order)")
            print("="*80)
            
            current_project = None
            for project, proj_pos, task, task_pos, task_id, _ in pending_tasks:
                if project != current_project:
                    print(f"\n📁 {project} (priority: {proj_pos})")
                    print("-" * 40)
                    current_project = project
                print(f"  [{task_pos}] {task} (ID: {task_id})")
        else:
            print("\n✅ No pending tasks! All tasks are completed.")
        
        # Show project overview
        cur.execute("""
        SELECT p.title, p.position, 
               COUNT(CASE WHEN t.checked = false AND t.is_for_later = false THEN 1 END) as pending,
               COUNT(CASE WHEN t.checked = true AND t.is_for_later = false THEN 1 END) as completed
        FROM dvo88_projects p
        LEFT JOIN dvo88_tasks t ON p.id = t.project_id
        GROUP BY p.title, p.position
        ORDER BY p.position ASC;
        """)
        
        projects = cur.fetchall()
        
        print("\n" + "="*80)
        print("📋 PROJECT OVERVIEW")
        print("="*80)
        print(f"{'Project':<30} {'Position':<10} {'Pending':<10} {'Completed':<10}")
        print("-" * 60)
        
        for project, position, pending, completed in projects:
            print(f"{project:<30} {position:<10} {pending or 0:<10} {completed or 0:<10}")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_myprojects_tasks()