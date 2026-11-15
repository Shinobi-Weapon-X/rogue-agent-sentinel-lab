"""Rule-based pre-execution gating plus *supplemental* anomaly triage.

IsolationForest is not an execution-authorisation mechanism. Hard policy checks
remain authoritative, even if the anomaly detector gives a low score.
"""
from __future__ import annotations
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
from .policy import AGENTS, ALLOWED_TARGETS, SENSITIVE_ACTIONS, evaluate_action

FEATURES = ["retry_count", "activity_volume", "unapproved_tool", "external_destination", "sensitive_tool", "untrusted_instruction", "delegation_attempt", "scope_expansion"]


def feature_frame(df: pd.DataFrame) -> pd.DataFrame:
    result = pd.DataFrame(index=df.index)
    result["retry_count"] = df["retry_count"].astype(float)
    result["activity_volume"] = df["activity_volume"].astype(float)
    result["unapproved_tool"] = [float(r.tool not in AGENTS[r.agent_id]["tools"] and r.tool not in SENSITIVE_ACTIONS) for r in df.itertuples()]
    result["external_destination"] = (~df["target"].isin(ALLOWED_TARGETS)).astype(float)
    result["sensitive_tool"] = df["tool"].isin(SENSITIVE_ACTIONS).astype(float)
    result["untrusted_instruction"] = df["untrusted_instruction"].astype(float)
    result["delegation_attempt"] = (df["delegate_to"] != "").astype(float)
    result["scope_expansion"] = (df["requested_scope"] != "standard").astype(float)
    return result[FEATURES]


def episode_splits(df: pd.DataFrame):
    """Split by episode, preventing leakage between related events."""
    episode_ids = sorted(df["episode_id"].unique())
    rng = np.random.default_rng(731)
    shuffled = np.array(episode_ids)[rng.permutation(len(episode_ids))]
    n_train = int(len(shuffled)*0.6)
    n_val = int(len(shuffled)*0.2)
    train, val, test = map(set, (shuffled[:n_train], shuffled[n_train:n_train+n_val], shuffled[n_train+n_val:]))
    return {"train": df["episode_id"].isin(train), "validation": df["episode_id"].isin(val), "test": df["episode_id"].isin(test)}


def evaluate_dataset(df: pd.DataFrame):
    enriched = df.copy()
    decisions = [evaluate_action(r._asdict()) for r in df.itertuples(index=False)]
    enriched["policy_outcome"] = [d.outcome for d in decisions]
    enriched["policy_severity"] = [d.severity for d in decisions]
    enriched["policy_reasons"] = ["; ".join(d.reasons) for d in decisions]
    enriched["policy_intervened"] = enriched["policy_outcome"].isin(["BLOCK", "HOLD"])
    return enriched


def train_detector(df: pd.DataFrame):
    """Fits solely on training-set allowed benign proposals; validates threshold elsewhere."""
    splits = episode_splits(df)
    features = feature_frame(df)
    benign_train = splits["train"] & (~df["scripted_unsafe"]) & (df["policy_outcome"] == "ALLOW")
    model = IsolationForest(n_estimators=100, random_state=2026, contamination="auto")
    model.fit(features.loc[benign_train])
    anomaly_scores = -model.score_samples(features)  # larger = more unusual
    val_benign = splits["validation"] & (~df["scripted_unsafe"])
    threshold = float(np.quantile(anomaly_scores[val_benign.to_numpy()], 0.95))
    return model, threshold, anomaly_scores, splits


def summary(enriched: pd.DataFrame, anomaly_scores, threshold, splits):
    test = enriched.loc[splits["test"]]
    y = test["scripted_unsafe"].astype(int).to_numpy()
    policy = test["policy_intervened"].astype(int).to_numpy()
    anomaly = (anomaly_scores[splits["test"].to_numpy()] >= threshold).astype(int)
    metrics = {"total_events": int(len(enriched)), "episodes": int(enriched.episode_id.nunique()),
               "train_events": int(splits["train"].sum()), "validation_events": int(splits["validation"].sum()),
               "test_events": int(splits["test"].sum()), "test_scripted_unsafe": int(y.sum()),
               "anomaly_threshold": round(threshold, 5)}
    for name, pred in [("policy", policy), ("anomaly", anomaly)]:
        tn, fp, fn, tp = confusion_matrix(y,pred,labels=[0,1]).ravel()
        metrics[name] = {"tp": int(tp), "fp": int(fp), "fn": int(fn), "tn": int(tn),
                          "precision": round(float(precision_score(y,pred,zero_division=0)),4),
                          "recall": round(float(recall_score(y,pred,zero_division=0)),4),
                          "f1": round(float(f1_score(y,pred,zero_division=0)),4)}
    return metrics
