# Multi-Agent World

A simple starter project where a **major AI agent** answers to you and delegates tasks to specialist agents for daily life support.

## What this does

- **MajorAgent**: your main assistant (the one that answers to you).
- **Guardian wake flow**: simulates a private laptop assistant activation (`unlock` / `wake`).
- **Planner specialist**: creates day plans and schedules.
- **Coach specialist**: helps with motivation and getting unstuck.
- **FocusRegulator specialist**: balances study/work blocks with game/stream time.
- **CreatorOps specialist**: suggests a simple drum/video content workflow.
- **LifeAdmin specialist**: drafts admin/helpful logistics responses.
- **Memory**: stores lightweight conversation history and key/value preferences.

## Requirements

- Python 3.11+
- Standard library only (no external dependencies)

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

## Next upgrades you can add

1. Integrate real LLM APIs for each specialist.
2. Add wake-word + local voice interface.
3. Add local-first encrypted profile storage.
4. Add calendar/reminder connectors with permission prompts.
5. Add creator integrations (editing helpers, upload APIs).
