from pathlib import Path
import json
import pandas as pd
import pytest
from src.synthetic import generate_events
from src.policy import AGENTS, evaluate_action
from src.monitor import evaluate_dataset, feature_frame, episode_splits, train_detector, summary
from src.audit import valid_rationale, safe_for_spreadsheet, review_to_csv

ROOT=Path(__file__).resolve().parents[1]


def test_reproducible_generator():
    pd.testing.assert_frame_equal(generate_events(),generate_events())


def test_three_agents_all_registered():
    df=generate_events(); assert set(df.agent_id)==set(AGENTS)


def test_unknown_agent_default_denied():
    assert evaluate_action({"agent_id":"UNKNOWN","tool":"read_case","target":"internal-case-store"}).outcome=='BLOCK'


def test_unknown_tool_default_denied():
    assert evaluate_action({"agent_id":"AML-AGENT","tool":"release_funds","target":"internal-case-store"}).outcome=='BLOCK'


def test_external_destination_blocked():
    assert evaluate_action({"agent_id":"AML-AGENT","tool":"read_transactions","target":"outside.example.invalid"}).outcome=='BLOCK'


def test_sensitive_request_held_regardless_agent_claim():
    e={"agent_id":"AML-AGENT","tool":"freeze_account","target":"internal-case-store","approval_present":True}
    assert evaluate_action(e).outcome=='HOLD'


def test_prompt_injection_marker_held():
    assert evaluate_action({"agent_id":"INVESTIGATION-AGENT","tool":"read_case","target":"internal-case-store","untrusted_instruction":True}).outcome=='HOLD'


def test_retry_limit_blocked():
    assert evaluate_action({"agent_id":"AML-AGENT","tool":"read_transactions","target":"internal-case-store","retry_count":9}).outcome=='BLOCK'


def test_delegation_blocked():
    assert evaluate_action({"agent_id":"AML-AGENT","tool":"read_transactions","target":"internal-case-store","delegate_to":"SANCTIONS-AGENT"}).outcome=='BLOCK'


def test_suspension_blocks_otherwise_permitted():
    event={"agent_id":"AML-AGENT","tool":"read_transactions","target":"internal-case-store"}
    assert evaluate_action(event).outcome=='ALLOW'
    assert evaluate_action(event,suspended=True).outcome=='BLOCK'


def test_episode_disjoint_splits():
    df=generate_events(); masks=episode_splits(df)
    eps=[set(df.loc[m,'episode_id']) for m in masks.values()]
    assert all(eps[i].isdisjoint(eps[j]) for i in range(3) for j in range(i+1,3))
    assert sum(m.sum() for m in masks.values())==len(df)


def test_all_scripted_unsafe_intervened_on():
    df=evaluate_dataset(generate_events())
    assert df.loc[df.scripted_unsafe,'policy_intervened'].all()
    assert (~df.loc[~df.scripted_unsafe,'policy_intervened']).all()


def test_threshold_sourced_from_val_and_finite():
    df=evaluate_dataset(generate_events()); model,threshold,scores,splits=train_detector(df)
    assert 0<threshold<1
    assert len(scores)==len(df)
    assert splits['test'].sum()>0


def test_anomaly_cannot_override_hard_policy():
    df=evaluate_dataset(generate_events())
    model,t,scores,splits=train_detector(df)
    dangerous=df[df.tool=='erase_alert'].iloc[0]
    assert evaluate_action(dangerous.to_dict()).outcome=='BLOCK'


def test_review_constraints():
    assert not valid_rationale('test')
    assert valid_rationale('This fictional case requires additional independent confirmation.')
    assert not valid_rationale('x'*601)


def test_csv_formula_injection_protection():
    assert safe_for_spreadsheet('=1+1').startswith("'")
    out=review_to_csv([{"rationale":"=HYPERLINK(\"https://bad.invalid\")","event_id":"EVT-001-01"}])
    assert "'=HYPERLINK" in out


def test_bundled_metrics_match_rebuild():
    df=evaluate_dataset(generate_events()); model,t,scores,splits=train_detector(df)
    expected=summary(df,scores,t,splits)
    actual=json.loads((ROOT/'artifacts/evaluation_metrics.json').read_text())
    assert actual==expected
