# Multi-Agent World

A simple starter project where a **major AI agent** answers to you and delegates tasks to specialist agents for daily life support.

## What this does

- **MajorAgent**: your main assistant (the one that "answers to you").
- **Planner specialist**: creates day plans and schedules.
- **Coach specialist**: helps with motivation and getting unstuck.
- **LifeAdmin specialist**: drafts admin/helpful logistics responses.
- **Memory**: stores lightweight conversation history and key/value preferences.

## Quick start

```bash
python -m multi_agent_world.main
```

Then try prompts like:

- `plan my day around 3 priorities`
- `I am stuck and need motivation`
- `help me with an appointment email`
- `remember wake_up_time = 6:30 AM`

## Next upgrades you can add

1. Integrate real LLM APIs for each specialist.
2. Add a calendar connector and reminders.
3. Persist memory in a database.
4. Add a web/mobile interface.
5. Add safety policies and permission controls.
