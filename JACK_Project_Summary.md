# JACK Project Summary and Framework
**Date:** 2025-06-27  
**Updated:** 2025-06-29 – project renamed from JCC to **JACK**

## Project Goals
- Establish a robust AI-to-AI framework between two agents: **Jules** (Flask API) and **Claude Code**—together called **JACK**.  
- Enable task hand-offs, shared context, and status reporting between JACK agents via HTTP.  
- Build a scalable foundation for orchestration, monitoring, and mission control.

## What We Have Done So Far
1. **Flask API (Jules)**  
   Endpoints: `POST /add_task`, `GET /tasks`, `GET /health` (public via ngrok).
2. **Conceptual framework** for AI-to-AI communication—next steps include richer message types and session management.
3. **Testing & monitoring plan** drafted; focus is to test every interaction before adding orchestration tools.

## Roles Going Forward
- **Jules** – hosts Flask API, manages task queue & health.  
- **Claude Code** – external controller for tests and orchestration.  
- **JACK (together)** – seamless, reliable, trackable AI collaboration.

## Next Steps (Priorities)
✅ **Priority #1** Document current state (this doc)  
✅ **Priority #2** Create rigorous test framework  
🔜 **After testing** Add monitoring & mission-control interface

## CLI Utility
A new script `jack_cli.py` provides a lightweight command-line interface to interact with Jules’ API.  
See **`docs/jack_usage.md`** for usage details.

---
**End of Summary**
