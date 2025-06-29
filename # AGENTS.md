# AGENTS.md

## Overview
This repo is shared by JACK (Jules + Claude Code). JACK coordinates tasks, updates files, and manages the project using the guidelines below.

---

## File Organization & Conventions

- **Root Folder:** `projects-master`
  - `docs/` → Session notes, plans, project documentation
  - `assets/` → Screenshots, images, assets
  - `cheatsheets/` → Reference sheets, conventions
  - `dashboards/` → Dashboard-related files
- Use **kebab-case** for filenames (e.g., `session-notes-2025-06-28.md`)

---

## Git Guidelines

- Commit to a branch (not directly to `main`) unless otherwise instructed
- Use clear commit messages describing work done
- Keep `main` clean and ready for merges

---

## JACK Instructions

**Claude Code:**
- Uses local terminal environment
- Saves new files in appropriate subfolders
- Commits and pushes changes as needed
- Follows Git guidelines above

**Jules:**
- Uses connected GitHub `projects-master` repo
- Clones latest version before starting
- Submits plan before applying code changes
- Saves new files using same structure
- Uses AGENTS.md as reference for naming, commit messages, and folder destinations

---

## Automations (Future)

- Build automation to sync ChatGPT session outputs into `docs/`
- Possibly auto-update `todo.md` with new priorities and reminders

## CLI
- `jack_cli.py` script for task management via Jules API. See `docs/jack_usage.md`.
