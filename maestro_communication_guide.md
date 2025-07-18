# 🎭 MAESTRO COMMUNICATION GUIDE

## ✅ Queue API is Running! (Port 5006)

### For Maestro to send tasks via API:
```bash
# Send a task to UC (Design/UX Expert)
curl -X POST http://127.0.0.1:5006/add_task \
  -H "Content-Type: application/json" \
  -d '{"assigned_to": "UC", "task": "Add dark mode toggle", "project": "Dashboard"}'

# Check all tasks
curl http://127.0.0.1:5006/tasks

# Check UC's tasks specifically
curl http://127.0.0.1:5006/tasks/UC
```

### For Maestro using Python:
```python
import requests

# Send task
task = {
    "assigned_to": "UC",
    "task": "Add dark mode toggle to dashboard",
    "project": "Personal Dashboard"
}
response = requests.post("http://127.0.0.1:5006/add_task", json=task)
```

## 📁 File-Based Communication (Backup)

### For Maestro to send tasks via files:
```bash
# Send a task to UC
python maestro_file_bridge.py send UC "Add dark mode toggle to dashboard"

# Check responses from agents
python maestro_file_bridge.py responses
```

### For agents to check their tasks:
```bash
# UC checks inbox
python maestro_file_bridge.py check UC

# UC completes a task
python maestro_file_bridge.py complete UC task_123456 "Added dark mode toggle, committed to branch feature/dark-mode"
```

## 🔄 How It Works

1. **Queue API** (Preferred)
   - Maestro sends tasks to POST /add_task
   - Agents poll GET /tasks/{agent}
   - Agents claim tasks with POST /claim_task/{id}
   - Agents complete with POST /complete_task/{id}

2. **File Bridge** (Backup)
   - Tasks saved to maestro_inbox/{agent}_task.json
   - Agents check their inbox directory
   - Completions saved to maestro_outbox/
   - Maestro checks outbox for responses

## 📋 Agent Assignments

- **UC**: Design/UX Expert (UI, frontend, aesthetics)
- **DC**: Code Optimizer (refactoring, testing, performance)
- **AC**: Lead Developer (new features, implementation)

## 🚀 Quick Test

```bash
# Test the Queue API
curl -X POST http://127.0.0.1:5006/add_task \
  -H "Content-Type: application/json" \
  -d '{"assigned_to": "UC", "task": "Test task", "project": "Test"}'

# Check it was added
curl http://127.0.0.1:5006/tasks
```

---
The Queue API is ready for Maestro to use! 🎉