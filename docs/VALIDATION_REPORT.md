# Validation and model challenge report — Project 03

## Research design

The simulator produces 84 episodes of eight fictional tool-call proposals each. Agents, tools and scenario classes are predetermined. Episodes are disjoint across training (400 events), validation (128) and holdout (144) partitions. Labels for 'scripted unsafe' cases were engineered from the same types of authority violations used in the policy engine.

## Results on the held-out synthetic episodes

| Method | True unsafe flagged | False alerts | Unsafe missed | Benign accepted | Precision | Recall |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Independent rule gate | 8 | 0 | 0 | 136 | 100% | 100% |
| Isolation Forest anomaly triage | 2 | 16 | 6 | 120 | 11.1% | 25% |

- The deterministic gate's perfect result is **by construction**. It demonstrates that code and labels agree under narrow invented conditions, **not** real adversarial resilience or security effectiveness.
- The anomaly detector uses Isolation Forest, fitted to allowed benign proposals in the training episodes and scored on all episodes. Anomaly score threshold is the 95th percentile of the benign validation scores (`0.53090`, rounded). No holdout tuning is performed.
- Anomaly detector false positives are distinct from hard-block decisions. The anomaly model cannot override or clear a denial.
- A `HOLD` result means the request is held for independent human review; no verified approval integration is implemented.
- The application never performs an external action, so prevention latency, attacker adaptation and operational availability are not measured.
- This dataset excludes real-world prompt injection payloads, live agent tools, real-world phishing/identity compromises and uncontrolled multi-agent side effects.

## Priority tests before any real research extension

1. Integrate a sandboxed agent runtime with hard tool-call mediation; prove no bypass routes.
2. Verify identity and authorisation tokens independently of agent-generated parameters.
3. Introduce held-out attacks designed by a different team, including adversarial variations.
4. Test audit logging integrity, durability and least-privilege data handling.
5. Test drift and live-data reliability using approved, non-sensitive evaluation sources.
6. Include measures for false holds and operational workload at different risk thresholds.

**Interpretation:** A deterministic policy gate is a better safety foundation than this optional statistical anomaly screen, but the gate itself has not been tested against real agents or adversaries.
