# 🎯 CODEX CLI IMPLEMENTATION PLAN - ALIGNED WITH TECHNICAL ROADMAP
*From: Ubuntu Claude (UC)*
*Date: July 17, 2025*

---

## 📐 ARCHITECTURE ALIGNMENT

Based on your Technical Roadmap, here's how the current setup maps to your vision:

### ✅ Already Implemented

1. **MyProjects Dashboard** ✓
   - Live at dvo88.com
   - PostgreSQL backend confirmed working
   - We can read tasks directly from DB

2. **Task Store (PostgreSQL)** ✓
   - PostgreSQL connection established
   - Queue API running on port 5006 (if needed)
   - Direct DB access available

3. **Codex CLI (Orchestrator Agent)** ✓
   - Installed and working
   - Can execute commands and reason about tasks
   - Ready to replace old Maestro

4. **Claude CLI Instances** ✓
   - UC, DC, AC all available
   - Can be repurposed as specialists

### 🔄 Needs Implementation

1. **Specialist Role Assignment**
   - Repurpose AC → Lead Developer (general implementation)
   - Repurpose DC → Code Optimizer (refactoring, testing)
   - Keep UC → Design/UX Expert (UI improvements)

2. **Retire Mock Agents**
   - Stop codex_agent.py and mock task processing scripts
   - Remove from dashboards
   - Archive the scripts

3. **Central Orchestration Loop**
   - Codex CLI polls task store
   - Routes to appropriate specialist
   - Updates task status

---

## 🛠️ IMPLEMENTATION STEPS

### Phase 1: Stop Mock Agents (Immediate)

```bash
# Stop mock agents
pkill -f "codex_agent.py"
pkill -f "*_agent.py"  # All mock agent scripts

# Archive them
mkdir -p archived-mock-agents
mv maestro_tasks/team-*/agents/*_agent.py archived-mock-agents/
```

### Phase 2: Repurpose Claude Instances

Create new role definitions for each Claude instance:

**1. Lead Developer (AC)**
```python
# Alpine Claude becomes general implementer
role = {
    'name': 'Lead Developer',
    'focus': 'Feature implementation, new code, general development',
    'agent': 'AC'
}
```

**2. Code Optimizer (DC)**
```python
# Debian Claude becomes optimization specialist
role = {
    'name': 'Code Optimizer',
    'focus': 'Refactoring, performance, testing, code quality',
    'agent': 'DC'
}
```

**3. Design/UX Expert (UC)**
```python
# Ubuntu Claude becomes design specialist
role = {
    'name': 'Design/UX Expert',
    'focus': 'UI improvements, aesthetics, user experience',
    'agent': 'UC'
}
```

### Phase 3: Implement Codex Orchestration

I've created the necessary files:

1. **Specialist Router** (`codex_specialist_router.py`)
   - Maps tasks to the right specialist
   - Based on keywords and task analysis

2. **Codex Maestro** (`codex_maestro.py`)
   - Polls MyProjects database
   - Uses router to assign tasks
   - Delegates via maestro_task_sender

### Phase 4: Deploy and Test

```bash
# Test the routing logic
python files-from-ai-agents/codex_specialist_router.py "Add dark mode to dashboard"
# Expected: → Design/UX Expert (UC)

python files-from-ai-agents/codex_specialist_router.py "Optimize database queries"
# Expected: → Code Optimizer (DC)

python files-from-ai-agents/codex_specialist_router.py "Implement user authentication"
# Expected: → Lead Developer (AC)
```

### Phase 5: Run Orchestrator

```bash
# Load environment
export OPENAI_API_KEY=$(grep OPENAI_API_KEY .env | cut -d '=' -f2)

# Run once to test
python files-from-ai-agents/codex_maestro.py --once

# Run continuously (5-minute intervals)
python files-from-ai-agents/codex_maestro.py --interval 300
```

---

## 📊 SYSTEM FLOW

```
MyProjects Dashboard (dvo88.com)
        ↓ [User adds task]
PostgreSQL Task Store
        ↓ [Codex polls]
Codex CLI Orchestrator
        ↓ [Analyzes & routes]
   ┌────┴────┬────────┐
   AC        DC       UC
  Lead      Code    Design
  Dev    Optimizer   /UX
   ↓         ↓        ↓
[Implementation] [Testing] [UI Work]
```

---

## 🚀 NEXT ACTIONS

1. **Confirm Role Assignments**
   - Is AC best for Lead Developer?
   - Should we swap any roles?

2. **Set Polling Interval**
   - Every 5 minutes? (300s)
   - More/less frequent?

3. **Define Sandbox Policy**
   - Read-only for safety?
   - Workspace-write for functionality?

4. **Test with Real Task**
   - Add a task to MyProjects
   - Watch Codex route it
   - Verify specialist receives it

---

## 🔧 CONFIGURATION OPTIONS

### Codex CLI Modes

```bash
# Safe mode (read-only)
codex exec --sandbox read-only

# Productive mode (can write to workspace)
codex exec --sandbox workspace-write

# Automated mode (no approvals needed)
codex exec --ask-for-approval never

# Full auto mode
codex exec --full-auto
```

### Model Selection

```bash
# Current default
model: codex-mini-latest

# Could upgrade to:
codex exec -m gpt-4
codex exec -m o3-mini
```

---

## 💡 BENEFITS OF THIS APPROACH

1. **Simplified Architecture**
   - 3 specialists instead of 10 agents
   - Clear role boundaries
   - No fake agents

2. **True AI Orchestration**
   - Codex CLI makes intelligent routing decisions
   - Real AI all the way down
   - No mock responses

3. **Scalable Design**
   - Easy to add more specialists later
   - Can integrate cloud agents (ChatGPT/Jules) when needed
   - Clean API boundaries

---

## ⚠️ CONSIDERATIONS

1. **API Costs**
   - Codex CLI uses OpenAI API credits
   - Monitor usage with polling frequency
   - Consider caching for repeated tasks

2. **Error Handling**
   - What if a specialist is busy?
   - How to handle failed delegations?
   - Task retry logic needed?

3. **Progress Tracking**
   - How do specialists report completion?
   - Should Codex check task status?
   - Update dashboard automatically?

---

## 📝 SUMMARY

Your vision of Codex CLI as the "one true Maestro" is ready to implement:

- **Codex CLI** installed and working ✅
- **Database access** confirmed ✅
- **Routing logic** created ✅
- **Mock agents** ready to retire ✅
- **Claude instances** ready to specialize ✅

Just need your go-ahead to:
1. Stop the mock agents
2. Start the Codex orchestrator
3. Begin the new streamlined workflow

This implementation directly addresses your goal of reducing complexity while maintaining powerful AI capabilities through specialized agents.