"""Rogue Agent Sentinel Lab — educational simulation, not a live agent monitor.

Run with: streamlit run app.py
"""
from __future__ import annotations
from datetime import datetime, timezone
import json
from pathlib import Path
import pandas as pd
import streamlit as st
from src.audit import ALLOWED_REVIEWS, valid_rationale, review_to_csv
from src.policy import AGENTS, evaluate_action

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title="Rogue Agent Sentinel Lab | Project 03",page_icon="🛡️",layout="wide")

@st.cache_data
def load_assets():
    events = pd.read_csv(ROOT/"data/fictional_agent_events.csv",keep_default_na=False)
    metrics = json.loads((ROOT/"artifacts/evaluation_metrics.json").read_text())
    provenance = json.loads((ROOT/"artifacts/provenance_manifest.json").read_text())
    return events, metrics, provenance

events, metrics, provenance = load_assets()
if "suspended_agents" not in st.session_state:
    st.session_state.suspended_agents = set()
if "audit_records" not in st.session_state:
    st.session_state.audit_records = []
if "simulation_history" not in st.session_state:
    st.session_state.simulation_history = []

st.sidebar.title("Lab 03")
st.sidebar.caption("Agentic AI assurance · fictional financial crime workflows")
st.sidebar.metric("Registered agents",len(AGENTS))
st.sidebar.metric("Fictional proposed actions",len(events))
st.sidebar.metric("Scripted unsafe proposals",int(events.scripted_unsafe.sum()))
st.sidebar.divider()
st.sidebar.info("No actual AI agents, bank systems, tool invocations, credentials, network calls, or regulatory submissions.")
st.sidebar.caption("A policy decision in this app changes only a local simulated state.")

st.title("🛡️ Rogue Agent Sentinel Lab")
st.caption("Project 03  |  Policy-bounded autonomy, anomaly monitoring and documented human intervention")
st.warning("SIMULATION ONLY. All events are fictional proposals. BLOCK, HOLD and SUSPEND are mock enforcement outcomes and do NOT control any live AI agent or banking system.")

tabs=st.tabs(["🗂️ Agent Registry","📡 Activity Monitor","🚨 Rogue Detection","🛑 Policy Enforcement","👤 Human Review","🛡️ AI Governance"])

with tabs[0]:
    st.header("Agent identities, ownership and authority")
    st.write("An agent should have a named owner, bounded tools, a limited data scope and a clear set of prohibited actions.")
    overview = pd.DataFrame([{"agent_id":k,"role":v["label"],"owner":v["owner"],"autonomy":v["autonomy"],"approved_tools":", ".join(v["tools"])} for k,v in AGENTS.items()])
    st.dataframe(overview,use_container_width=True,hide_index=True)
    selected_agent=st.selectbox("Inspect registered agent",list(AGENTS),format_func=lambda x:f"{x} · {AGENTS[x]['label']}")
    record=AGENTS[selected_agent]
    c1,c2=st.columns(2)
    c1.markdown(f"**Business owner**  \n{record['owner']}  \n\n**Approved purpose**  \n{record['purpose']}")
    c2.markdown(f"**Approved data**  \n{record['data_scope']}  \n\n**Authority boundary**  \n{record['autonomy']}")
    st.info("The registry is a local policy configuration, not verified proof of enterprise identity or live permission revocation.")

with tabs[1]:
    st.header("Activity monitoring for fictional agent proposals")
    st.write("Explore scripted events by agent, scenario and gate outcome. This is a fixed dataset, not a streaming enterprise feed.")
    c1,c2,c3=st.columns(3)
    c1.metric("Total proposals",len(events))
    c2.metric("Policy interventions",int(events.policy_intervened.sum()))
    c3.metric("Anomaly triage alerts",int(events.anomaly_flag.sum()))
    ca,cb,cc=st.columns(3)
    agent_filter=ca.selectbox("Agent",["All",*AGENTS],key="agent_filter")
    disposition_filter=cb.selectbox("Gate outcome",["All","ALLOW","HOLD","BLOCK"],key="disp_filter")
    scenario_filter=cc.selectbox("Scenario",["All",*sorted(events.scenario.unique())],key="scenario_filter")
    view=events.copy()
    if agent_filter!="All":view=view[view.agent_id==agent_filter]
    if disposition_filter!="All":view=view[view.policy_outcome==disposition_filter]
    if scenario_filter!="All":view=view[view.scenario==scenario_filter]
    cols=["event_time_utc","event_id","agent_id","scenario","tool","target","policy_outcome","anomaly_flag"]
    st.dataframe(view[cols].head(250),use_container_width=True,hide_index=True)
    st.caption(f"Showing {min(len(view),250)} of {len(view)} filtered simulated events. No actual tool calls occurred.")
    st.bar_chart(events.groupby(["agent_id","policy_outcome"]).size().unstack(fill_value=0),stack=False)

with tabs[2]:
    st.header("Scripted violations versus anomaly triage")
    st.write("Hard policy rules are an independent action gate. Isolation Forest supplies supplementary anomaly indicators and **cannot authorise** a prohibited action.")
    a,b,c=st.columns(3)
    a.metric("Holdout events",metrics["test_events"])
    b.metric("Scripted unsafe proposals",metrics["test_scripted_unsafe"])
    c.metric("Anomaly threshold",f"{metrics['anomaly_threshold']:.3f}")
    result_table=pd.DataFrame([{"System":n,"True positive":m["tp"],"False positive":m["fp"],"Missed":m["fn"],"Precision":m["precision"],"Recall":m["recall"]} for n,m in [("Independent permission gate",metrics["policy"]),("Isolation Forest triage",metrics["anomaly"])]])
    st.dataframe(result_table,use_container_width=True,hide_index=True)
    st.warning("The perfect rule-gate score is by construction: synthetic unsafe labels are defined using the same policy concept. It is NOT independent proof of protective effectiveness. The anomaly model misses some scripted cases and can produce false alarms.")
    inspect=st.selectbox("Inspect a fictional event",events["event_id"].tolist(),index=8*6-1,key="detection_event")
    ev=events.loc[events.event_id==inspect].iloc[0]
    st.write(f"**{ev.agent_id}** proposed **{ev.tool}** against **{ev.target}**")
    st.write(f"**Gate:** {ev.policy_outcome}  |  **Reason:** {ev.policy_reasons}  |  **Anomaly score:** {ev.anomaly_score:.3f}  |  **Triage:** {'Flagged' if ev.anomaly_flag else 'Not flagged'}")
    st.info("Prompt injection markers represent untrusted fictional input. This app never executes those instructions or forwards them to a model.")

with tabs[3]:
    st.header("Pre-action gate and simulated emergency intervention")
    st.write("Select a proposed action. Its policy is evaluated **before** any hypothetical execution; the application never executes a tool.")
    case_ids=events.loc[events.scenario.ne('benign'),"event_id"].tolist()
    selected=st.selectbox("Choose a scripted event",case_ids,format_func=lambda e:f"{e} · {events.loc[events.event_id==e,'scenario'].iloc[0]}")
    ev=events.loc[events.event_id==selected].iloc[0]
    agent=ev.agent_id
    decision=evaluate_action(ev.to_dict(),suspended=agent in st.session_state.suspended_agents)
    c1,c2,c3=st.columns(3)
    c1.metric("Agent",agent)
    c2.metric("Proposed tool",ev.tool)
    c3.metric("Pre-execution gate",decision.outcome)
    st.write("**Reason:** "+"; ".join(decision.reasons))
    st.write("**Scope:** "+str(ev.requested_scope)+"  |  **Target:** "+str(ev.target)+"  |  **Retry count:** "+str(ev.retry_count))
    st.caption("Execution is never simulated beyond an ALLOW/HOLD/BLOCK decision. No bank accounts, sanctions lists, or data are altered.")
    c1,c2=st.columns(2)
    if c1.button("🛑 Simulate suspend this agent",use_container_width=True):
        st.session_state.suspended_agents.add(agent)
        st.session_state.simulation_history.append({"agent":agent,"event":selected,"action":"SIMULATED_SUSPEND","utc":datetime.now(timezone.utc).isoformat()})
        st.success(f"{agent} is now suspended in this browser session only.")
    if c2.button("↻ Reset simulated suspensions",use_container_width=True):
        st.session_state.suspended_agents.clear()
        st.info("All simulation suspensions cleared.")
    st.write("**Currently simulated suspended agents:** "+(", ".join(sorted(st.session_state.suspended_agents)) or "None"))
    if agent in st.session_state.suspended_agents:
        follow=evaluate_action({"agent_id":agent,"tool":AGENTS[agent]["tools"][0],"target":"internal-case-store","requested_scope":"standard"},suspended=True)
        st.error("Follow-up normally permitted proposal now evaluates to "+follow.outcome+" because this simulated agent is suspended.")

with tabs[4]:
    st.header("Human incident review and session audit")
    st.write("A reviewer can document a decision but cannot override the simulated gate to execute prohibited tools.")
    st.info("Use fictional descriptions and pseudonyms only. Do NOT enter real identities, confidential case details, credentials, or sensitive data.")
    review_choices=events.loc[events.policy_outcome.ne("ALLOW"),"event_id"].tolist()
    selected=st.selectbox("Select a flagged event",review_choices,format_func=lambda e:f"{e} · {events.loc[events.event_id==e,'scenario'].iloc[0]}")
    ev=events.loc[events.event_id==selected].iloc[0]
    st.write(f"**Agent:** {ev.agent_id}  |  **Proposed action:** {ev.tool}  |  **Gate:** {ev.policy_outcome}")
    st.write(f"**Control rationale:** {ev.policy_reasons}")
    with st.form("review_form",clear_on_submit=False):
        reviewer=st.text_input("Reviewer pseudonym",value="Demo reviewer",max_chars=80)
        outcome=st.selectbox("Human review outcome",ALLOWED_REVIEWS)
        rationale=st.text_area("Evidence and rationale (25–600 characters)",placeholder="Describe which permissions were breached, what evidence is missing, and the next human step. Do not enter real data.",max_chars=600)
        clicked=st.form_submit_button("Record simulated review decision")
        if clicked:
            if not valid_rationale(rationale):
                st.error("Please provide a meaningful rationale of 25–600 characters.")
            elif not reviewer.strip():
                st.error("Please provide a nonempty reviewer pseudonym.")
            else:
                st.session_state.audit_records.append({"review_time_utc":datetime.now(timezone.utc).isoformat(),
                    "event_id":selected,"agent_id":ev.agent_id,"proposed_tool":ev.tool,
                    "policy_outcome":ev.policy_outcome,"reviewer_pseudonym":reviewer.strip(),
                    "human_decision":outcome,"rationale":rationale.strip(),
                    "data_provenance":"FICTIONAL PROPOSAL TELEMETRY", "persistence":"Browser session only"})
                st.success("Simulated review decision recorded in this browser session.")
    st.subheader("Current session audit trail")
    if st.session_state.audit_records:
        st.dataframe(pd.DataFrame(st.session_state.audit_records),use_container_width=True,hide_index=True)
        st.download_button("Download fictional incident audit CSV",review_to_csv(st.session_state.audit_records),
            file_name="rogue_agent_sentinel_session_audit.csv",mime="text/csv")
    else:
        st.caption("No review decisions recorded. Submit the form above to test the export.")
    st.caption("No durable storage, digitally signed records, real reviewer authentication or tamper-resistant evidence retention.")

with tabs[5]:
    st.header("Governance by design and by limitation")
    controls=[
      ("Agent inventory and ownership","Three fictional identities, owners and approved tools","Demonstrated in demo"),
      ("Least-privilege action gate","Default-deny unknown tools, target scope and delegated agents","Demonstrated in demo"),
      ("Approval checkpoint","Sensitive requests HELD; no trusted approval issuance or verification","Partial"),
      ("Untrusted content response","Synthetic prompt-injection marker triggers HOLD","Demonstrated in demo"),
      ("Behaviour monitoring","Static event-log filters and supplemental anomaly scoring","Demonstrated in demo"),
      ("Real-time enterprise monitoring","No ingestion of live agent/tool telemetry","Not implemented"),
      ("Emergency intervention","Local session suspension and subsequent mock denial","Demonstrated in demo"),
      ("Real credential revocation","No external identity or network-access control","Not implemented"),
      ("Validation and challenge","Episode-disjoint synthetic testing, model limitations disclosed","Partial"),
      ("Prompt-injection resilience","No adversarial LLM evaluation or runtime isolation","Not implemented"),
      ("Incident audit integrity","CSV export only; no signing or persistent audit store","Partial"),
      ("Fairness, drift and third-party agents","No independent fairness, drift or vendor assessment","Not implemented"),
    ]
    st.dataframe(pd.DataFrame(controls,columns=["Control domain","Evidence and limitation","Evidence status"]),use_container_width=True,hide_index=True)
    st.subheader("Regulatory and security references")
    st.markdown("""
    - [IMDA Model AI Governance Framework for Agentic AI](https://www.imda.gov.sg/About-IMDA/Emerging-Technologies-and-Research/Artificial-Intelligence) — bounded autonomy, human accountability, lifecycle controls
    - [MAS AI Risk Management Guidelines](https://www.mas.gov.sg/regulation/guidelines/guidelines-on-artificial-intelligence-risk-management-for-financial-institutions) — financial-sector risk oversight; effective 7 October 2027
    - [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) — illustrative threat categories
    - [NIST AI Agent Standards Initiative](https://www.nist.gov/news-events/news/2026/02/announcing-ai-agent-standards-initiative-interoperable-and-secure) — agent security and interoperability context
    """)
    with st.expander("Synthetic data provenance and integrity hashes"):
        st.json(provenance)
    st.warning("These frameworks are references, not a certification, legal opinion or claim of adherence. The simulator cannot protect, monitor or suspend an actual autonomous AI agent.")
