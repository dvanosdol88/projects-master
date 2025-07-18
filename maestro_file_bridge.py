#!/mnt/c/Users/david/projects-master/venv/bin/python
"""
File-based communication bridge for Maestro
Allows Maestro to send tasks without the Queue API
"""

import json
import os
from datetime import datetime

class MaestroFileBridge:
    def __init__(self):
        self.inbox_dir = "/mnt/c/Users/david/projects-master/maestro_inbox"
        self.outbox_dir = "/mnt/c/Users/david/projects-master/maestro_outbox"
        
        # Create directories
        os.makedirs(self.inbox_dir, exist_ok=True)
        os.makedirs(self.outbox_dir, exist_ok=True)
    
    def send_task(self, agent, task_description, project=None):
        """Maestro sends a task to an agent"""
        task = {
            'id': f"task_{int(datetime.now().timestamp())}",
            'assigned_to': agent,
            'task': task_description,
            'project': project,
            'created': datetime.now().isoformat(),
            'status': 'pending'
        }
        
        # Save to agent's inbox
        filename = f"{self.inbox_dir}/{agent}_{task['id']}.json"
        with open(filename, 'w') as f:
            json.dump(task, f, indent=2)
        
        print(f"✅ Task sent to {agent}: {filename}")
        return task['id']
    
    def check_responses(self):
        """Check for responses from agents"""
        responses = []
        for filename in os.listdir(self.outbox_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.outbox_dir, filename)
                with open(filepath, 'r') as f:
                    response = json.load(f)
                responses.append(response)
                # Archive processed response
                os.rename(filepath, filepath + '.processed')
        return responses
    
    def agent_check_tasks(self, agent):
        """Agent checks for their tasks"""
        tasks = []
        for filename in os.listdir(self.inbox_dir):
            if filename.startswith(f"{agent}_") and filename.endswith('.json'):
                filepath = os.path.join(self.inbox_dir, filename)
                with open(filepath, 'r') as f:
                    task = json.load(f)
                tasks.append(task)
        return tasks
    
    def agent_complete_task(self, agent, task_id, result):
        """Agent reports task completion"""
        response = {
            'task_id': task_id,
            'agent': agent,
            'status': 'completed',
            'result': result,
            'completed': datetime.now().isoformat()
        }
        
        # Save to outbox
        filename = f"{self.outbox_dir}/{agent}_{task_id}_complete.json"
        with open(filename, 'w') as f:
            json.dump(response, f, indent=2)
        
        # Remove from inbox
        inbox_file = f"{self.inbox_dir}/{agent}_{task_id}.json"
        if os.path.exists(inbox_file):
            os.remove(inbox_file)
        
        print(f"✅ Task {task_id} completed by {agent}")

# CLI interface
if __name__ == "__main__":
    import sys
    bridge = MaestroFileBridge()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Send task: python maestro_file_bridge.py send <agent> <task>")
        print("  Check inbox: python maestro_file_bridge.py check <agent>")
        print("  Complete: python maestro_file_bridge.py complete <agent> <task_id> <result>")
        print("  Responses: python maestro_file_bridge.py responses")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "send" and len(sys.argv) >= 4:
        agent = sys.argv[2]
        task = " ".join(sys.argv[3:])
        task_id = bridge.send_task(agent, task)
        print(f"Task ID: {task_id}")
    
    elif cmd == "check" and len(sys.argv) >= 3:
        agent = sys.argv[2]
        tasks = bridge.agent_check_tasks(agent)
        print(f"\n📥 Tasks for {agent}:")
        for task in tasks:
            print(f"- [{task['id']}] {task['task']}")
    
    elif cmd == "complete" and len(sys.argv) >= 5:
        agent = sys.argv[2]
        task_id = sys.argv[3]
        result = " ".join(sys.argv[4:])
        bridge.agent_complete_task(agent, task_id, result)
    
    elif cmd == "responses":
        responses = bridge.check_responses()
        print(f"\n📤 Responses:")
        for resp in responses:
            print(f"- {resp['agent']} completed {resp['task_id']}: {resp['result']}")