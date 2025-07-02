## Context Health & Refresh Protocol

### Health Self-Monitoring  
Report degradation when noticing:
- Slower command execution or processing delays
- Difficulty tracking file changes across repositories
- Forgetting project structure or recent modifications
- Making errors that suggest context confusion

### Health Status Reporting
Include in terminal output when performance degrades:

### Refresh Routine
Before context refresh:
1. **Complete current command sequence** - finish active operations
2. **Commit all changes** - ensure clean git status
3. **Document branch state** - note any uncommitted work
4. **Export environment info** - current directory, active processes

## Task Execution Protocol

When learn_mode is active, follow normal procedures to ask user (David) for permission before proceeding with tasks. When not in learn_mode, assume permission is granted and proceed directly with task completion unless instructions are unclear or user intervention is required.