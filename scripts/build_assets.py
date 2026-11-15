"""Rebuild synthetic telemetry, model evidence and dataset integrity manifest."""
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.synthetic import generate_events, SEED
from src.monitor import evaluate_dataset, train_detector, summary


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    data = ROOT/'data'; art=ROOT/'artifacts'; data.mkdir(exist_ok=True); art.mkdir(exist_ok=True)
    df=evaluate_dataset(generate_events())
    model, threshold, scores, splits=train_detector(df)
    df['anomaly_score']=scores
    df['anomaly_flag']=df['anomaly_score']>=threshold
    dataset=data/'fictional_agent_events.csv'; df.to_csv(dataset,index=False)
    metrics=summary(df,scores,threshold,splits)
    (art/'evaluation_metrics.json').write_text(json.dumps(metrics,indent=2)+'\n',encoding='utf8')
    metadata={"title":"Fictional agent telemetry provenance","generated_seed":SEED,
        "dataset_character":"DETERMINISTIC FICTIONAL ACTION PROPOSALS; NO AGENTS OR CONNECTED BANKING TOOLS",
        "threshold_source":"95th percentile of benign validation anomalies; no holdout tuning",
        "policy_source":"src/policy.py — independent pre-execution action gate",
        "persistent_log":"NONE; local session export only",
        "files_sha256": {"data/fictional_agent_events.csv":sha256(dataset),
                          "artifacts/evaluation_metrics.json":sha256(art/'evaluation_metrics.json')}}
    (art/'provenance_manifest.json').write_text(json.dumps(metadata,indent=2)+'\n',encoding='utf8')
    print(json.dumps(metrics,indent=2))

if __name__=='__main__': main()
