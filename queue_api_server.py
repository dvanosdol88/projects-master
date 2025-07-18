#!/mnt/c/Users/david/projects-master/venv/bin/python
"""
Queue API Server - For Maestro to communicate with specialist agents
Runs on port 5006
"""

from flask import Flask, jsonify, request
import json
import os
from datetime import datetime
from threading import Lock

app = Flask(__name__)

# Task queue storage
QUEUE_FILE = '/mnt/c/Users/david/projects-master/queue_tasks.json'
queue_lock = Lock()

def load_queue():
    """Load tasks from file"""
    if os.path.exists(QUEUE_FILE):
        with open(QUEUE_FILE, 'r') as f:
            return json.load(f)
    return {'tasks': [], 'completed': []}

def save_queue(data):
    """Save tasks to file"""
    with open(QUEUE_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Get all pending tasks"""
    with queue_lock:
        data = load_queue()
        return jsonify(data['tasks'])

@app.route('/tasks/<agent>', methods=['GET'])
def get_agent_tasks(agent):
    """Get tasks for specific agent (UC, DC, AC)"""
    with queue_lock:
        data = load_queue()
        agent_tasks = [t for t in data['tasks'] if t.get('assigned_to') == agent]
        return jsonify(agent_tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    """Add a new task to the queue"""
    with queue_lock:
        data = load_queue()
        task = request.json
        task['id'] = f"task_{int(datetime.now().timestamp())}"
        task['created'] = datetime.now().isoformat()
        task['status'] = 'pending'
        data['tasks'].append(task)
        save_queue(data)
        return jsonify({'success': True, 'task_id': task['id']})

@app.route('/claim_task/<task_id>', methods=['POST'])
def claim_task(task_id):
    """Agent claims a task"""
    with queue_lock:
        data = load_queue()
        for task in data['tasks']:
            if task['id'] == task_id:
                task['status'] = 'in_progress'
                task['claimed_at'] = datetime.now().isoformat()
                save_queue(data)
                return jsonify({'success': True})
        return jsonify({'success': False, 'error': 'Task not found'}), 404

@app.route('/complete_task/<task_id>', methods=['POST'])
def complete_task(task_id):
    """Mark task as completed"""
    with queue_lock:
        data = load_queue()
        for i, task in enumerate(data['tasks']):
            if task['id'] == task_id:
                task['status'] = 'completed'
                task['completed_at'] = datetime.now().isoformat()
                # Move to completed list
                data['completed'].append(task)
                data['tasks'].pop(i)
                save_queue(data)
                return jsonify({'success': True})
        return jsonify({'success': False, 'error': 'Task not found'}), 404

@app.route('/status', methods=['GET'])
def status():
    """API status"""
    with queue_lock:
        data = load_queue()
        return jsonify({
            'status': 'running',
            'pending_tasks': len([t for t in data['tasks'] if t['status'] == 'pending']),
            'in_progress': len([t for t in data['tasks'] if t['status'] == 'in_progress']),
            'completed': len(data['completed'])
        })

if __name__ == '__main__':
    print("🚀 Queue API Server starting on port 5006")
    print("   Endpoints:")
    print("   GET  /tasks - Get all tasks")
    print("   GET  /tasks/<agent> - Get tasks for specific agent")
    print("   POST /add_task - Add new task")
    print("   POST /claim_task/<id> - Claim a task")
    print("   POST /complete_task/<id> - Mark task complete")
    print("   GET  /status - API status")
    app.run(host='127.0.0.1', port=5006, debug=False)