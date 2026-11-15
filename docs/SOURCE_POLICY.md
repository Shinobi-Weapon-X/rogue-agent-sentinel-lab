# Synthetic-data and public-source policy

All agent IDs, event times, scenario records, tool-call requests and labels are generated fictionally. No prompt or content is sent to an external LLM. No real bank/customer data or production log is used or bundled.

The app does not fetch external websites and never accesses real OWASP, IMDA, MAS or NIST data at runtime. Reference links are educational context. `scripts/build_assets.py` uses a fixed random seed and writes a provenance manifest with SHA-256 hashes.

**No reliance on real-world defensive efficacy:** label design intentionally reflects tool-policy categories. Synthetic outcomes do not measure containment of an actual rogue agent.
