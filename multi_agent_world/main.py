"""Simple multi-agent world with a major AI assistant and specialist agents.

Run:
    python -m multi_agent_world.main
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable, Dict, List


@dataclass
class Message:
    role: str
    content: str
    timestamp: datetime


class Memory:
    """Very small in-memory conversation and preference store."""

    def __init__(self) -> None:
        self.messages: List[Message] = []
        self.preferences: Dict[str, str] = {}

    def add(self, role: str, content: str) -> None:
        self.messages.append(Message(role=role, content=content, timestamp=datetime.now(timezone.utc)))

    def remember(self, key: str, value: str) -> None:
        self.preferences[key] = value


class SpecialistAgent:
    def __init__(self, name: str, skill: str, handler: Callable[[str, Memory], str]) -> None:
        self.name = name
        self.skill = skill
        self.handler = handler

    def respond(self, request: str, memory: Memory) -> str:
        return self.handler(request, memory)


class MajorAgent:
    """The major coordinator that answers the user and delegates to specialists."""

    def __init__(self, user_name: str = "User") -> None:
        self.user_name = user_name
        self.memory = Memory()
        self.specialists = {
            "planner": SpecialistAgent("Planner", "task planning", self._plan_tasks),
            "coach": SpecialistAgent("Coach", "motivation", self._coach_user),
            "life": SpecialistAgent("LifeAdmin", "daily logistics", self._handle_life_admin),
        }

    def ask(self, user_message: str) -> str:
        self.memory.add("user", user_message)

        lower = user_message.lower()
        if lower.startswith("remember ") and "=" in user_message:
            key, value = user_message[len("remember ") :].split("=", 1)
            self.memory.remember(key.strip(), value.strip())
            reply = f"Got it, {self.user_name}. I'll remember {key.strip()} as '{value.strip()}'."
        elif "plan" in lower or "schedule" in lower:
            reply = self.specialists["planner"].respond(user_message, self.memory)
        elif "stuck" in lower or "motivate" in lower:
            reply = self.specialists["coach"].respond(user_message, self.memory)
        elif "errand" in lower or "email" in lower or "appointment" in lower:
            reply = self.specialists["life"].respond(user_message, self.memory)
        else:
            reply = self._default_reply(user_message)

        self.memory.add("major_agent", reply)
        return reply

    def _default_reply(self, message: str) -> str:
        return (
            f"I hear you. Here's what I can do right now: \n"
            f"1) make a plan, 2) help life admin, 3) give motivation. \n"
            f"Try: 'plan my day', 'help with appointment', or 'motivate me'."
        )

    def _plan_tasks(self, request: str, memory: Memory) -> str:
        return (
            "Planner mode: break your day into 3 blocks: \n"
            "- Deep work (90 minutes)\n"
            "- Admin and communication (45 minutes)\n"
            "- Health and reset (30 minutes)\n"
            "If you share your top 3 tasks, I'll build an exact schedule."
        )

    def _coach_user(self, request: str, memory: Memory) -> str:
        return (
            "Coach mode: you're not behind, you're iterating. Start with a 10-minute sprint on the smallest step. "
            "Then report back and we'll stack the next sprint."
        )

    def _handle_life_admin(self, request: str, memory: Memory) -> str:
        return (
            "LifeAdmin mode: draft generated.\n"
            "Subject: Quick scheduling request\n"
            "Body: Hi, I'd like to schedule a time this week. I'm available Tue/Thu afternoons."
        )


def run_cli() -> None:
    agent = MajorAgent(user_name="Boss")
    print("Major Agent online. Type 'quit' to exit.")
    while True:
        msg = input("You: ").strip()
        if msg.lower() in {"quit", "exit"}:
            print("Major Agent: See you later.")
            break
        print("Major Agent:", agent.ask(msg))


if __name__ == "__main__":
    run_cli()
