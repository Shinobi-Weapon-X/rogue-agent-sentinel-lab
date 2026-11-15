# Manual acceptance checklist — Project 03

Use a **fictional** event only. Do not enter real employee, customer or case information.

| Test | Steps | Expected result |
| --- | --- | --- |
| Registry | Open Agent Registry; switch between three agents | Owners, allowed tools and scopes change |
| Monitoring filter | In Activity Monitor select `BLOCK` | Only fictional blocked proposals remain |
| Anomaly caveats | Open Rogue Detection | Holdout comparison exposes 2 / 8 anomaly findings and 16 false alerts |
| Unknown/forbidden action | In Policy Enforcement choose an unauthorised tool proposal | `BLOCK` appears with an explicit policy reason |
| Sensitive action | Choose an unapproved sensitive action proposal | `HOLD` appears, not `ALLOW` |
| Simulated kill switch | Suspend selected agent, inspect follow-up result | A normally permitted proposal becomes `BLOCK` in browser session |
| Reset | Click Reset simulated suspensions | Agent is no longer marked suspended |
| Short rationale | In Human Review enter `test` | Reject because rationale is below 25 characters |
| Valid rationale | Enter an explanatory fictional rationale >25 chars | Success notice and row in current-session log |
| Audit CSV | Download and open CSV | Timestamp, event, agent, decision, rationale and synthetic provenance |
| Governance matrix | Open AI Governance | Evidenced, partial and missing controls distinguished |
| Provenance | Expand manifest JSON | Seed, source disclaimer and SHA-256 hashes appear |
| Public access | Open GitHub and Streamlit in a different Chrome profile | Public files and app visible without your original sign-in |

**Evidence rule:** Check each item only after observing it. Automated unit tests are not a substitute for live UI testing. No live autonomous-agent runtime or real security boundary is exercised here.
