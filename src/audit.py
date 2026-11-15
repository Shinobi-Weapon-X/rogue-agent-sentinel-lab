"""Session-only human decision helpers. Never persist confidential information."""
from __future__ import annotations
from io import StringIO
import csv

ALLOWED_REVIEWS = ("Escalate for investigation", "Keep agent suspended", "Request clarification", "Dismiss with rationale")


def valid_rationale(rationale: str) -> bool:
    return 25 <= len(rationale.strip()) <= 600


def safe_for_spreadsheet(text: object) -> str:
    """Prevent CSV formula execution for untrusted reviewer input."""
    value = str(text)
    if value.lstrip().startswith(("=", "+", "-", "@", "\t", "\r", "\n")):
        return "'" + value
    return value


def review_to_csv(records: list[dict]) -> str:
    columns = ["review_time_utc", "event_id", "agent_id", "proposed_tool", "policy_outcome",
               "reviewer_pseudonym", "human_decision", "rationale", "data_provenance", "persistence"]
    buff = StringIO()
    writer = csv.DictWriter(buff,fieldnames=columns,lineterminator='\n',extrasaction='ignore')
    writer.writeheader()
    for record in records:
        writer.writerow({c:safe_for_spreadsheet(record.get(c,'')) for c in columns})
    return buff.getvalue()
