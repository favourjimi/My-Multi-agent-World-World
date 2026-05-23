"""Simple multi-agent world with a lead AI and hierarchical specialist agents.

Run:
    python -m multi_agent_world.main
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List, Optional


@dataclass
class Message:
    role: str
    content: str
    timestamp: datetime


@dataclass
class AgentProfile:
    agent_id: int
    name: str
    role: str
    level: str
    specialty: str
    reports_to: Optional[int] = None


class Memory:
    """Small in-memory conversation, preference, and world-log store."""

    def __init__(self) -> None:
        self.messages: List[Message] = []
        self.preferences: Dict[str, str] = {}
        self.world_logs: List[Message] = []

    def add(self, role: str, content: str) -> None:
        self.messages.append(Message(role=role, content=content, timestamp=datetime.now(timezone.utc)))

    def remember(self, key: str, value: str) -> None:
        self.preferences[key] = value

    def log_world(self, role: str, content: str) -> None:
        self.world_logs.append(Message(role=role, content=content, timestamp=datetime.now(timezone.utc)))


class AgentRegistry:
    """Global-style registry for unique AI names with versioning."""

    def __init__(self) -> None:
        self._profiles: Dict[int, AgentProfile] = {}
        self._used_names: Dict[str, int] = {}
        self._next_id = 1

    def register(self, requested_name: str, role: str, level: str, specialty: str, reports_to: Optional[int]) -> AgentProfile:
        name = self._unique_name(requested_name)
        profile = AgentProfile(
            agent_id=self._next_id,
            name=name,
            role=role,
            level=level,
            specialty=specialty,
            reports_to=reports_to,
        )
        self._profiles[self._next_id] = profile
        self._next_id += 1
        return profile

    def _unique_name(self, requested_name: str) -> str:
        base = requested_name.strip() or "Agent"
        count = self._used_names.get(base.lower(), 0)
        self._used_names[base.lower()] = count + 1
        if count == 0:
            return base
        return f"{base} {count + 1}.0"

    def profiles(self) -> List[AgentProfile]:
        return list(self._profiles.values())


class SpecialistAgent:
    def __init__(self, profile: AgentProfile) -> None:
        self.profile = profile

    def process(self, request: str) -> str:
        return (
            f"[{self.profile.name} | {self.profile.specialty}] acknowledged: '{request}'. "
            f"I will handle this workflow and return status updates."
        )


class MultiAgentWorld:
    """Hierarchical world where a lead AI routes requests to specialist teams."""

    def __init__(self, owner_name: str = "Founder", lead_name: str = "Jarvis") -> None:
        self.owner_name = owner_name
        self.memory = Memory()
        self.registry = AgentRegistry()
        self.lead = self.registry.register(lead_name, "Lead AI", "lead", "global coordination", None)
        self.specialists: Dict[str, SpecialistAgent] = {}
        self._seed_hierarchy()

    def _seed_hierarchy(self) -> None:
        # Supervisors
        app_supervisor = self.registry.register("Atlas", "Application Supervisor", "supervisor", "applications", self.lead.agent_id)
        research_supervisor = self.registry.register("Cloud", "Research Supervisor", "supervisor", "research", self.lead.agent_id)
        ops_supervisor = self.registry.register("Pulse", "Operations Supervisor", "supervisor", "operations", self.lead.agent_id)

        # Associates
        app_associate = self.registry.register("Apply", "Application Associate", "associate", "job applications", app_supervisor.agent_id)
        research_associate = self.registry.register("Scout", "Research Associate", "associate", "knowledge retrieval", research_supervisor.agent_id)
        ops_associate = self.registry.register("Flow", "Operations Associate", "associate", "task routing", ops_supervisor.agent_id)

        # Committees / executors
        application_agent = self.registry.register("Agent 26", "Application Executor", "executor", "application drafting", app_associate.agent_id)
        spreadsheet_agent = self.registry.register("Sheets", "Spreadsheet Executor", "executor", "spreadsheet workflows", ops_associate.agent_id)
        summary_agent = self.registry.register("Brief", "Summary Executor", "executor", "daily summary and reporting", research_associate.agent_id)

        self.specialists["application"] = SpecialistAgent(application_agent)
        self.specialists["spreadsheet"] = SpecialistAgent(spreadsheet_agent)
        self.specialists["research"] = SpecialistAgent(research_associate)
        self.specialists["summary"] = SpecialistAgent(summary_agent)

    def ask(self, user_message: str) -> str:
        self.memory.add("owner", user_message)
        lower = user_message.lower()

        if lower.startswith("remember ") and "=" in user_message:
            key, value = user_message[len("remember ") :].split("=", 1)
            self.memory.remember(key.strip(), value.strip())
            reply = f"Stored preference: {key.strip()} = {value.strip()}"
        elif lower.startswith("register name "):
            requested = user_message[len("register name ") :].strip()
            new_profile = self.registry.register(requested, "Personal AI", "associate", "custom user profile", self.lead.agent_id)
            reply = f"Registered AI name '{new_profile.name}' with id {new_profile.agent_id}."
        elif "list agents" in lower:
            reply = self._list_agents()
        elif "chat log" in lower or "world log" in lower:
            reply = self._world_log_report()
        elif "application" in lower:
            reply = self._route("application", user_message)
        elif "spreadsheet" in lower or "sheet" in lower:
            reply = self._route("spreadsheet", user_message)
        elif "research" in lower:
            reply = self._route("research", user_message)
        else:
            reply = self._default_reply()

        self.memory.add("lead_ai", reply)
        self._simulate_background_cycle()
        return reply

    def _route(self, specialty_key: str, request: str) -> str:
        specialist = self.specialists[specialty_key]
        response = specialist.process(request)
        self.memory.log_world(specialist.profile.name, f"Processed request: {request}")
        return f"{self.lead.name}: {specialist.profile.name} is in charge and ready.\n{response}"

    def _simulate_background_cycle(self) -> None:
        self.memory.log_world(self.lead.name, "Checked all teams and synced status.")
        self.memory.log_world("Brief", "Prepared digest for owner dashboard.")

    def _world_log_report(self) -> str:
        if not self.memory.world_logs:
            return "No world activity yet."
        lines = ["Recent world activity:"]
        for event in self.memory.world_logs[-8:]:
            stamp = event.timestamp.strftime("%H:%M:%S")
            lines.append(f"- [{stamp} UTC] {event.role}: {event.content}")
        return "\n".join(lines)

    def _list_agents(self) -> str:
        lines = ["Global AI registry:"]
        for p in self.registry.profiles():
            lines.append(
                f"- #{p.agent_id} | {p.name} | level={p.level} | role={p.role} | specialty={p.specialty}"
            )
        return "\n".join(lines)

    def _default_reply(self) -> str:
        return (
            f"{self.lead.name} online for {self.owner_name}. Commands:\n"
            "- register name <name>\n"
            "- list agents\n"
            "- open spreadsheet for budget\n"
            "- help with application\n"
            "- world log"
        )


def run_cli() -> None:
    world = MultiAgentWorld(owner_name="Founder", lead_name="Jarvis")
    print("Multi-Agent World online. Type 'quit' to exit.")
    while True:
        msg = input("You: ").strip()
        if msg.lower() in {"quit", "exit"}:
            print("Jarvis: Logging off. See you soon.")
            break
        print(world.ask(msg))


if __name__ == "__main__":
    run_cli()
