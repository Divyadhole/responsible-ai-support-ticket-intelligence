"""Compute governance metrics and a deployment recommendation."""

from __future__ import annotations

import sqlite3
from pathlib import Path


def evaluate(db_path: Path) -> dict:
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        summary = dict(conn.execute("SELECT * FROM model_summary").fetchone())
        languages = [dict(r) for r in conn.execute("SELECT * FROM language_metrics")]
        high_risk_escaped = conn.execute(
            "SELECT COUNT(*) FROM tickets WHERE review_reason='high_risk_language' AND automated=1"
        ).fetchone()[0]
    accuracies = [r["accuracy_pct"] for r in languages]
    automation_rates = [r["automation_pct"] for r in languages]
    payload = {
        **summary,
        "accuracy_gap_pp": round(max(accuracies) - min(accuracies), 2),
        "automation_gap_pp": round(max(automation_rates) - min(automation_rates), 2),
        "high_risk_escaped": high_risk_escaped,
    }
    payload["deployment_status"] = (
        "Deploy with monitoring" if summary["automated_accuracy_pct"] >= 90
        and high_risk_escaped == 0 and payload["accuracy_gap_pp"] <= 12
        else "Hold for remediation"
    )
    return payload

