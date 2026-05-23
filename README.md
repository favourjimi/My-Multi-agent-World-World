# Multi-Agent World

A simple Python 3.11+ (standard library only) prototype of a **multi-agent AI world** with:

- a personal **lead AI** (default name: `ORACLE`),
- a hierarchical team structure,
- unique AI naming with automatic versioning when names collide,
- specialty-based request routing,
- a background world activity log.

- **MajorAgent**: your main assistant (the one that answers to you).
- **Guardian wake flow**: simulates a private laptop assistant activation (`unlock` / `wake`).
- **Planner specialist**: creates day plans and schedules.
- **Coach specialist**: helps with motivation and getting unstuck.
- **FocusRegulator specialist**: balances study/work blocks with game/stream time.
- **CreatorOps specialist**: suggests a simple drum/video content workflow.
- **LifeAdmin specialist**: drafts admin/helpful logistics responses.
- **Memory**: stores lightweight conversation history and key/value preferences.

## Features

- **Lead + hierarchy**
  - Levels: `lead -> supervisor -> associate -> executor`
  - Pre-seeded team members for applications, spreadsheets, research, and reporting.

- **Global-style AI registry**
  - Every agent gets an ID and profile.
  - If a name already exists, the next one is versioned (example: `ORACLE 2.0`).

- **Task routing**
  - If your request includes terms like `application`, `spreadsheet`, or `research`, the lead routes to the relevant specialist.

- **World log**
  - The system records background actions so you can check what happened while you were away.

## Requirements

- Python 3.11+
- Standard library only (no external dependencies)

## Setup (Console / Laptop)

Use these commands directly in your terminal:

```bash
# 1) Go to the project folder
cd /workspace/My-Multi-agent-World-World

# 2) Confirm Python 3.11+
python3 --version

# 3) (Recommended) Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 4) Run the app
python -m multi_agent_world.main
```

If your system maps Python 3.11+ to `python` already, you can use:

```bash
python --version
python -m multi_agent_world.main
```

## Quick start

```bash
python -m multi_agent_world.main
```

## Example commands

- `unlock`
- `set guardian Nightwing`
- `plan my day around 3 priorities`
- `I am stuck and need motivation`
- `study for 2 hours then play FIFA`
- `help me turn a drum video into a post`
- `help me with an appointment email`
- `remember wake_up_time = 6:30 AM`

## Current limits (intentional for v1)

- No real voice activation yet (text simulation only).
- No real social-media upload integration.
- No real calendar integration.

## Next upgrades i will add

1. Integrate real LLM APIs for each specialist.
2. Add wake-word + local voice interface.
3. Add local-first encrypted profile storage.
4. Add calendar/reminder connectors with permission prompts.
5. Add creator integrations (editing helpers, upload APIs).
