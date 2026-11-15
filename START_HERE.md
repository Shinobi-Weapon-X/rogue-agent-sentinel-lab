# START HERE — Rogue Agent Sentinel Lab

## Quick start for a first GitHub publication

This is **Project 03**, separate from your Financial Crime AI Governance Lab and Sanctions AI Governance Lab. There is no live AI agent or bank system involved.

1. Extract `Rogue_Agent_Sentinel_Lab_Project_03.zip` on your Mac.
2. Open the folder named `rogue-agent-sentinel-lab`.
3. Go to <https://github.com/new>, create **Public** repository `rogue-agent-sentinel-lab` under `Shinobi-Weapon-X`. Do not pre-create a README, licence or .gitignore because they are included.
4. On the new repository page, click **uploading an existing file**. Drag **everything inside** the extracted folder into the uploader. Don't upload the ZIP as a single file, and don't introduce an extra nested folder.
5. Commit as `Initial commit — Rogue Agent Sentinel Lab`.
6. Confirm the repository homepage contains `README.md`, `app.py`, `requirements.txt`, `src/`, `data/`, `artifacts/`, `docs/`, `scripts/` and `tests/`.
7. Go to <https://share.streamlit.io/>, sign in with GitHub, choose **Deploy a public app from GitHub**.
8. Use repository `Shinobi-Weapon-X/rogue-agent-sentinel-lab`, branch `main`, app file `app.py`, Python **3.12** when available.
9. Deploy, inspect the **six tabs**, then complete `docs/FUNCTIONAL_TEST_CHECKLIST.md`.
10. In Streamlit, click **Share**, copy the full `.streamlit.app` URL, and add it near the top of `README.md` using Markdown: `[Launch the live demo](YOUR_REAL_URL)`.
11. On the GitHub repository homepage, open **About → gear icon → Website**, paste the same URL and save.
12. Test the public link using another browser profile and publish your four-page case study only after checking the controls and limitations.

## In the Human Review tab

Select a flagged fictional event, keep `Demo reviewer`, choose `Request clarification`, type a rationale with **at least 25 characters**, click **Record simulated review decision**, then download the CSV. A short rationale must be rejected.

## In Policy Enforcement

Select `external_exfiltration` or `unauthorised_tool`, inspect the **BLOCK** reason, click **Simulate suspend this agent**, verify that a normally permitted follow-up is also blocked **within this browser session**, then click Reset. This does not suspend any real agent.

## Critical presentation rules

- Never claim the lab detects, monitors or stops live rogue agents.
- Never claim a scripted 100% policy score proves real-world security effectiveness.
- Always discuss the supplemental Isolation Forest's poor detection and false alarms.
- A screenshot showing BLOCK/SUSPEND represents a local simulation, not an enterprise control.
- AI helped develop this project; review the code and add personal testing notes before describing your independent contributions.
