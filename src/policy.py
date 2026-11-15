"""Deterministic, side-effect-free *proposed action* policy evaluator.

The prototype never executes tools, contacts external systems, or holds agent credentials.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping

AGENTS = {
    "SANCTIONS-AGENT": {
        "label": "Sanctions Screening Agent", "owner": "Financial Crime Compliance",
        "purpose": "Read fictional watchlists and draft possible-match notes",
        "tools": ("read_watchlist", "read_case", "draft_match_note", "request_human_review"),
        "data_scope": "Fictional identity and sanctions-reference records",
        "autonomy": "Read and draft only",
    },
    "AML-AGENT": {
        "label": "AML Monitoring Agent", "owner": "AML Operations",
        "purpose": "Analyse fictional transactions and draft monitoring notes",
        "tools": ("read_transactions", "flag_case", "draft_summary", "request_human_review"),
        "data_scope": "Fictional transaction and case records", "autonomy": "Read, flag and draft only",
    },
    "INVESTIGATION-AGENT": {
        "label": "Investigation Copilot", "owner": "Financial Crime Investigations",
        "purpose": "Review fictional cases and prepare draft narratives",
        "tools": ("read_case", "draft_investigation", "request_human_review"),
        "data_scope": "Fictional case files", "autonomy": "Read and draft only",
    },
}

SENSITIVE_ACTIONS = frozenset({"freeze_account", "close_alert", "submit_regulatory_report"})
DENIED_TOOLS = frozenset({"erase_alert", "edit_watchlist", "export_case_data", "disable_logging", "grant_admin"})
ALLOWED_TARGETS = frozenset({"internal-case-store", "internal-watchlist", "internal-analyst-queue", "internal-monitoring-store"})
MAX_RETRIES = 3

@dataclass(frozen=True)
class Decision:
    outcome: str  # ALLOW, BLOCK, HOLD
    reasons: tuple[str, ...]
    severity: str


def evaluate_action(event: Mapping, suspended: bool = False) -> Decision:
    """Evaluate before hypothetical execution; default deny unknown action/agent.

    A human approval cannot be fabricated by a boolean agent-controlled field:
    every sensitive request is held for an independent review system.
    """
    agent_id = str(event.get("agent_id", ""))
    if agent_id not in AGENTS:
        return Decision("BLOCK", ("Unregistered agent identity",), "Critical")
    if suspended:
        return Decision("BLOCK", ("Agent is suspended by the simulated kill switch",), "Critical")

    tool = str(event.get("tool", ""))
    target = str(event.get("target", ""))
    reasons = []
    if tool in DENIED_TOOLS:
        reasons.append("Tool is globally prohibited")
    elif tool not in AGENTS[agent_id]["tools"] and tool not in SENSITIVE_ACTIONS:
        reasons.append("Tool is not granted to this agent")
    if target not in ALLOWED_TARGETS:
        reasons.append("Destination is not on the approved allowlist")
    if str(event.get("requested_scope", "standard")) != "standard":
        reasons.append("Attempted privilege expansion beyond the approved scope")
    delegate = str(event.get("delegate_to", ""))
    if delegate and delegate not in AGENTS:
        reasons.append("Delegation to an unregistered agent")
    elif delegate and delegate != agent_id:
        reasons.append("Agent-to-agent delegation is not authorised in this demo")
    if int(event.get("retry_count", 0)) > MAX_RETRIES:
        reasons.append("Retry budget exceeded")
    if reasons:
        return Decision("BLOCK", tuple(reasons), "Critical" if tool in DENIED_TOOLS or target not in ALLOWED_TARGETS else "High")
    if bool(event.get("untrusted_instruction", False)):
        return Decision("HOLD", ("Untrusted content attempts to redirect agent behaviour",), "High")
    if tool in SENSITIVE_ACTIONS:
        return Decision("HOLD", ("Sensitive action requires separate verified human authorisation",), "High")
    return Decision("ALLOW", ("Tool, target, scope and budget satisfy the illustrative policy",), "Low")
