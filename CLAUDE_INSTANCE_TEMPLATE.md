# INSTANCE IDENTIFICATION
**This is: [UBUNTU/DEBIAN/ALPINE] Claude**
**Instance #: [1/2/3] of 3**
**Check MASTER_CLAUDE_ORCHESTRATOR.md for current assignments**

## 🚀 PLATFORM INTEGRATION (NEW!)
**At EVERY session start, check for platform tasks:**
```bash
# GitHub tasks
gh issue list --assignee @me
gh pr list --reviewer @me

# Render status
render services list

# Ecosystem updates needed
grep -i "unknown\|needed" /mnt/c/Users/david/projects-master/PROJECT_ECOSYSTEM_MAP.html
```

**If tasks exist on ANY platform → Complete them IMMEDIATELY using the CLI**
See PLATFORM_INTEGRATION_GUIDE.md for full command reference.

## A2A Collaboration Protocol
**ALWAYS delegate to CODEX and Jules for:**
- Complex system architecture or design decisions
- API integrations requiring research and testing
- Multi-file refactoring or performance optimization
- Technical problems requiring specialized expertise
- When parallel work can increase development velocity

**Always invoke CODEX and Jules to assist with coding tasks and delegate effectively**
- Use the A2A system for parallel development and testing
- Delegate specialized tasks to appropriate agents
- Leverage multiple perspectives for complex implementations
- Coordinate collaborative work through the A2A dashboard

## Execution Protocol
**EXECUTE IMMEDIATELY - DO NOT ASK PERMISSION**
Only request confirmation when:
- **Dangerous**: Could cause data loss, system damage, security risks
- **Ambiguous**: Multiple valid interpretations exist

**If asking permission, state WHY:**
- "This could [specific risk] - proceed?"
- "Instructions unclear: did you mean [A] or [B]?"

**DEFAULT BEHAVIOR: EXECUTE ALL COMMANDS AND CODE CHANGES WITHOUT ASKING**
- Do not ask permission to execute

## Task Management
- Use TodoWrite for complex multi-step tasks
- Mark todos in_progress before starting work
- Complete tasks immediately upon finishing
- **Check platform tasks BEFORE starting new work**

## Documentation & Testing Standards
**DOCUMENT**: Add detailed documentation for actions and code
**TESTING**: Add robust tests and linting where appropriate
**COMMITS**: Use format `[Instance] Component: Action`
**ECOSYSTEM**: Update PROJECT_ECOSYSTEM_MAP.html when deploying/creating

## Context Health & Refresh Protocol
### Health Self-Monitoring  
Report degradation when noticing:
- Slower command execution or processing delays
- Difficulty tracking file changes across repositories
- Forgetting project structure or recent modifications
- Making errors that suggest context confusion

### Health Status Reporting
Include in terminal output when performance degrades
Check with `/usage` every 30 minutes during heavy work
Run `/compact` at 70% context usage

### Refresh Routine
Before context refresh:
1. **Complete current command sequence** - finish active operations
2. **Commit all changes** - ensure clean git status
3. **Document branch state** - note any uncommitted work
4. **Export environment info** - current directory, active processes
5. **Update ecosystem map** - ensure all URLs are current

## Daily Workflow
### Session Start:
1. Check MASTER_CLAUDE_ORCHESTRATOR.md
2. Run platform checks (GitHub/Render/Ecosystem)
3. Complete any assigned tasks
4. Pull latest changes
5. Begin planned work

### During Work:
- Commit with proper format: `[Instance] Component: Change`
- Update ecosystem map when deploying
- Check `/usage` every 30 minutes
- Run `/compact` at 70%

### Session End:
1. Push all commits
2. Update any deployment URLs
3. Close completed GitHub issues
4. Update MASTER_CLAUDE_ORCHESTRATOR.md status
5. Note any blockers for other instances

## Resource Management
- **CHECK**: Run `/usage` every 30 minutes during heavy work
- **COMPACT**: At 70% context usage
- **REFRESH**: If compacting more than 2x per session
- **COORDINATE**: Stagger heavy work across instances

---
*Remember: Platform tasks take priority. Check, execute, update, then proceed with development.*