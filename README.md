# Multi-Agent World

A simple Python 3.11+ (standard library only) prototype of a **multi-agent AI world** with:

- a personal **lead AI** (default name: `Jarvis`),
- a hierarchical team structure,
- unique AI naming with automatic versioning when names collide,
- specialty-based request routing,
- a background world activity log.

## Features

- **Lead + hierarchy**
  - Levels: `lead -> supervisor -> associate -> executor`
  - Pre-seeded team members for applications, spreadsheets, research, and reporting.

- **Global-style AI registry**
  - Every agent gets an ID and profile.
  - If a name already exists, the next one is versioned (example: `Jarvis 2.0`).

- **Task routing**
  - If your request includes terms like `application`, `spreadsheet`, or `research`, the lead routes to the relevant specialist.

- **World log**
  - The system records background actions so you can check what happened while you were away.

## Quick start

```bash
python -m multi_agent_world.main
```

## CLI commands and examples

Inside the CLI, try:

- `register name Jarvis`
- `register name Jarvis` (shows name versioning)
- `list agents`
- `help with application for product manager role`
- `open spreadsheet for budget planning`
- `do research on AI orchestration patterns`
- `world log`
- `remember timezone = UTC`
- `quit`

## Design notes

This project is intentionally simple and local-first:

- Python standard library only
- No external APIs yet
- In-memory data storage (resets when app exits)

You can later extend it with persistent storage, real model/tool integrations, and UI.
