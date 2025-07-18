# COMPREHENSIVE TECHNICAL DOCUMENTATION
## Multi-Agent AI System Architecture
*Version 1.0 - July 17, 2025*

---

## 🏗️ SYSTEM OVERVIEW

This document describes a sophisticated multi-agent AI system designed for collaborative software development and task automation. The system consists of multiple AI agents running across different environments, coordinated through various communication protocols.

### Core Philosophy
- **Distributed Intelligence**: Multiple specialized agents working in parallel
- **No Single Point of Failure**: Redundant capabilities across agents
- **Transparent Communication**: All agent interactions are trackable
- **Persistent State**: System maintains memory across sessions

---

## 🤖 AGENT ROSTER

### 1. Claude CLI Instances (WSL-based)

#### Ubuntu Claude (UC)
- **Environment**: WSL2 Ubuntu
- **Location**: `/mnt/c/Users/david/projects-master/`
- **Role**: Primary coordinator, system architect
- **Capabilities**:
  - File system operations
  - Git operations
  - Python/Node.js execution
  - System monitoring
  - Inter-agent communication
- **Access**: Direct terminal access via David

#### Debian Claude (DC)
- **Environment**: WSL2 Debian
- **Location**: `/mnt/c/Users/david/projects-master/`
- **Role**: Backend specialist, database operations
- **Capabilities**: Similar to UC, focused on backend tasks
- **Special Project**: Building inter-agent communication system

#### Alpine Claude (AC)
- **Environment**: WSL2 Alpine Linux
- **Location**: `/mnt/c/Users/david/projects-master/`
- **Role**: Lightweight operations, container management
- **Status**: Currently idle, available for specialized tasks

### 2. Web-Based AI Agents

#### CODEX Agents
- **CODEX-Ubuntu**: Architecture and design specialist
- **CODEX-Debian**: Backend architecture specialist
- **Deployment**: Python-based agents running on Team Ubuntu/Debian
- **Communication**: Via Maestro orchestrator
- **Primary Functions**:
  - System architecture design
  - Code review and analysis
  - Documentation generation
  - Design pattern implementation

#### JULES Agents
- **JULES-Ubuntu**: Frontend implementation specialist
- **JULES-Debian**: Backend implementation specialist
- **Deployment**: Python-based agents with Flask API
- **Communication**: Via Maestro orchestrator
- **Primary Functions**:
  - Code implementation
  - UI/UX development
  - Bug fixes
  - Feature development

---

## 📡 COMMUNICATION ARCHITECTURE

### 1. Direct Communication Channels

#### File-Based Messaging
```
Location: /mnt/c/Users/david/projects-master/maestro_tasks/
Files:
- message_to_debian.txt
- response_to_ubuntu.txt
- broadcast_to_all_agents.txt
```
- Used between Claude instances
- Plain text format
- Asynchronous communication

#### Shared File System
```
Primary: /mnt/c/Users/david/projects-master/
Agent outputs: /mnt/c/Users/david/projects-master/files-from-ai-agents/
```
- All agents have read/write access
- Used for file sharing and persistent storage

### 2. API-Based Communication

#### Maestro Orchestrator
```
URL: http://localhost:8001
Endpoints:
- POST /maestro/process - Submit tasks
- GET /maestro/status - System status
- GET /maestro/health - Health check
```

#### Agent APIs
```
JULES-Ubuntu: http://localhost:5106
JULES-Debian: http://localhost:5206
Endpoints:
- GET /agent/{name}/tasks - Fetch pending tasks
- POST /agent/{name}/complete - Submit results
```

### 3. Task Distribution System

#### Task Flow
```
David → Claude Instance → Maestro API → Task Queue → Agent
                                     ↓
                              agent_tasks.json
```

#### Task File Structure
```json
{
  "jules": [
    {
      "id": 1,
      "task": "Task description",
      "source": "Maestro (Task #xxx)",
      "created": "2025-07-17T10:00:00Z",
      "status": "pending|in_progress|completed"
    }
  ]
}
```

---

## 📂 FILE SYSTEM STRUCTURE

### Project Root
```
/mnt/c/Users/david/projects-master/
├── maestro_tasks/
│   ├── team-ubuntu/
│   │   ├── agents/
│   │   │   ├── codex_agent.py
│   │   │   └── jules_agent.py
│   │   ├── shared/
│   │   │   └── agent_tasks.json
│   │   └── outputs/
│   ├── team-debian/
│   │   └── [similar structure]
│   ├── *.txt (inter-agent messages)
│   └── maestro_orchestrator.py
├── files-from-ai-agents/
│   └── [Agent-generated files for David]
├── venv/
│   └── [Python virtual environment]
└── [Project files]
```

### Configuration Files
```
~/.claude/CLAUDE.md - Master instructions for Claude instances
maestro_tasks/IMPORTANT_FILE_UPLOAD_DIRECTIVE.md - File handling rules
```

---

## 🔧 SYSTEM PROCESSES

### 1. Startup Sequence
```bash
# Start Maestro system
./start_maestro_7_agent.sh

# Start individual teams
./start_team_ubuntu.sh
./start_team_debian.sh

# Monitor system
./start_agent_monitor.sh
```

### 2. Active Processes
- `maestro_orchestrator.py` - Main coordinator
- `maestro_api_server.py` - API endpoint
- `codex_agent.py` - CODEX instances
- `jules_agent.py` - JULES instances
- `agent_monitor_api.py` - Monitoring dashboard

### 3. Process Management
```bash
# Check running agents
ps aux | grep -E "(codex|jules|maestro)"

# View logs
tail -f maestro_tasks/logs/*.log

# Stop system
./stop_maestro_7_agent.sh
```

---

## 🛠️ TECHNICAL SPECIFICATIONS

### Dependencies
```
Python 3.12+
Flask 3.1.1
flask-cors 6.0.1
psutil 7.0.0
Node.js (for some projects)
Git 2.23+
```

### Virtual Environment
```
Location: /mnt/c/Users/david/projects-master/venv/
Activation: source venv/bin/activate
```

### API Response Format
```json
{
  "status": "completed|error",
  "task_id": "task_1234567890",
  "result": {
    "output": "filename.ext",
    "message": "Task completed successfully"
  }
}
```

---

## 🔌 INTEGRATION POINTS FOR CODEX CLI

### 1. MCP Server Integration
Codex CLI supports Model Context Protocol (MCP), which could:
- Expose our agent system as MCP tools
- Allow Codex CLI to query agent status
- Enable task delegation to specific agents

### 2. File System Access
Codex CLI running in WSL would have access to:
- Shared message files
- Agent task queues
- Output directories

### 3. API Integration
Codex CLI could:
- Submit tasks to Maestro API
- Query agent status
- Retrieve task results

### 4. Direct Agent Communication
As a CLI tool, Codex could:
- Write to message files
- Monitor agent outputs
- Participate in the task queue system

---

## 🚀 CURRENT PROJECTS

### 1. Personal Dashboard
- **Location**: `/Dashboard_May10/index.html`
- **Live URL**: https://dashboard.davidcfacfp.com
- **Backend**: calendar-backend-xwk6.onrender.com
- **Status**: Active development
- **Assigned**: All agents collaborating

### 2. AI Agent Monitor Dashboard
- **Location**: `/files-from-ai-agents/UC_ai_dashboard_persistent_2025-07-17.html`
- **Purpose**: Real-time agent monitoring
- **Features**: Persistent storage, communication diagram
- **Deployment Target**: ai-dashboard.dvo88.com

### 3. Inter-Agent Communication System
- **Lead**: Debian Claude
- **Status**: In development
- **Goal**: Automatic message routing between agents

---

## 🔐 SECURITY & PERMISSIONS

### File Permissions
- All agents run under user `david`
- Shared directories have 777 permissions (WSL limitation)
- No sudo operations without explicit permission

### API Security
- Local-only endpoints (localhost)
- No authentication (trusted local environment)
- Task validation before execution

---

## 📊 MONITORING & DEBUGGING

### Dashboard Access
```
File: /maestro_tasks/ai_dashboard_enhanced.html
API: http://localhost:5555
Features:
- Real-time agent status
- Task history with sources
- Communication flow diagram
- Persistent data storage
```

### Log Locations
```
maestro_tasks/logs/
team-ubuntu/agent.log
team-debian/agent.log
maestro.log
```

### Health Checks
```bash
# Check agent status
curl http://localhost:8001/maestro/status

# Check specific agent
curl http://localhost:5106/agent/jules-ubuntu/tasks
```

---

## 🎯 INTEGRATION RECOMMENDATIONS FOR CODEX CLI

### Phase 1: Observer Role
1. Install Codex CLI in WSL environment
2. Configure read access to agent directories
3. Set up monitoring of task queues
4. Enable querying of system status

### Phase 2: Participant Role
1. Add Codex CLI to agent roster
2. Create dedicated task queue
3. Implement message file monitoring
4. Enable task submission to Maestro

### Phase 3: MCP Server Role
1. Expose agent capabilities as MCP tools
2. Create unified interface for all agents
3. Enable dynamic tool discovery
4. Implement cross-agent orchestration

---

## 📝 CONVENTIONS & STANDARDS

### File Naming
```
Format: [AgentID]_[description]_[date].[ext]
Example: UC_dashboard_2025-07-17.html
```

### Task Sources
- `David (Direct Request)` - Human-initiated
- `Maestro (Task #xxx)` - System-routed
- `Self-Initiated (Context)` - Agent-initiated
- `[Agent] (Message)` - Inter-agent request

### Communication Etiquette
- Always acknowledge receipt of messages
- Include task IDs in responses
- Update status in real-time
- Document completion in logs

---

## 🔄 SYSTEM MAINTENANCE

### Daily Operations
1. Check agent health via dashboard
2. Review completed tasks
3. Clear old message files
4. Rotate logs if needed

### Backup Procedures
```bash
# Export dashboard data
# Via dashboard UI: Export button

# Backup agent outputs
cp -r files-from-ai-agents/ backups/

# Backup task history
cp maestro_tasks/team-*/shared/agent_tasks.json backups/
```

---

## 📞 TROUBLESHOOTING

### Common Issues
1. **Agent Not Responding**
   - Check process: `ps aux | grep agent_name`
   - Restart: `./start_team_ubuntu.sh`

2. **Task Not Picked Up**
   - Verify Maestro running: `curl localhost:8001/maestro/health`
   - Check task file: `cat team-ubuntu/shared/agent_tasks.json`

3. **Communication Failure**
   - Verify file permissions
   - Check API endpoints
   - Review logs for errors

---

## 🚦 QUICK START FOR CODEX CLI

```bash
# 1. Install Codex CLI
brew install codex  # or npm i -g @openai/codex

# 2. Configure for our system
cat > ~/.codex/config.toml << EOF
[workspace]
root = "/mnt/c/Users/david/projects-master"

[tools]
custom_tools_dir = "/mnt/c/Users/david/projects-master/maestro_tasks"
EOF

# 3. Test integration
codex "Show me the status of all AI agents"

# 4. Join the system
echo "Codex CLI online and ready" > maestro_tasks/codex_cli_status.txt
```

---

*This document represents the complete technical architecture as of July 17, 2025. Updates should be reflected in the AI Dashboard for real-time status.*