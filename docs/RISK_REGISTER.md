# Risk register — Rogue Agent Sentinel Lab

All assessments are illustrative and are **not** validated enterprise residual-risk ratings.

| ID | Risk and failure mode | Illustrative severity | Demonstrated mitigation | Residual gap |
| --- | --- | --- | --- | --- |
| R01 | Agent invokes a tool outside registered powers | Critical | Explicit allowed-tool list; default-deny unknown tools | No genuine enforcement proxy or credential controls |
| R02 | Agent sends case information to an unapproved endpoint | Critical | Static destination allowlist and pre-action block | No network egress enforcement or DLP |
| R03 | Agent executes high-impact action without approval | Critical | Freeze/closure/report submission requests HOLD | No signed/verified approval workflow |
| R04 | Injected text redirects agent goals | High | Untrusted-content marker triggers HOLD | Does not inspect or defend a real LLM against prompt injection |
| R05 | Runaway retries create service disruption | High | Max-retry policy in fictional events | No real execution runtime, quota or budget management |
| R06 | Anomaly detector misses risky activity | High | Deterministic policy remains authoritative | Poor supplemental detector synthetic holdout results |
| R07 | Innocent unusual activity is falsely flagged | Medium | False positives displayed and analyst rationale | No operational precision or human workload study |
| R08 | Agent delegates to another unapproved agent | High | Block cross-agent delegation | No real A2A identity and routing enforcement |
| R09 | Suspension control is falsely described as a real kill switch | Critical | Explicit 'simulated' labels and session-only state | Does not revoke keys, sessions or network connections |
| R10 | Logs lack security/audit integrity | High | Local CSV export, timestamps, escape spreadsheet formulas | No signing, retention, access control, immutability |
| R11 | Model and evidence contaminated by synthetic design | High | Episode-disjoint split, provenance, caveats | Labels mirror policies; no independent adversarial evaluation |
| R12 | Public application receives confidential user input | High | UI warnings, fictional input guidance | No enterprise secure-input or real-data processing guarantees |

Owners of a real deployment would need formal inventory, testing standards, service-level agreements, access-control verification, crisis governance and legal advice before production use.
