"""Build the dataset, analytics warehouse, governance result, and dashboard."""

from __future__ import annotations

import csv, json, sqlite3
from pathlib import Path
from src.build_database import build
from src.evaluate import evaluate
from src.generate_data import generate
from src.report import create_report

ROOT = Path(__file__).resolve().parent


def main() -> None:
    counts = generate(ROOT / "data/raw")
    db = ROOT / "data/support_ai.db"
    build(ROOT / "data/raw/tickets.csv", db, ROOT / "sql")
    result = evaluate(db)
    create_report(db, result, ROOT / "reports/responsible_ai_dashboard.html")
    create_report(db, result, ROOT / "docs/index.html")
    (ROOT / "reports/evaluation.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    with sqlite3.connect(db) as conn:
        for view in ("model_summary", "language_metrics", "queue_metrics", "review_queue", "daily_monitoring"):
            cursor = conn.execute(f"SELECT * FROM {view}")
            path = ROOT / "data/processed" / f"{view}.csv"; path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("w", newline="", encoding="utf-8") as handle:
                writer=csv.writer(handle); writer.writerow([c[0] for c in cursor.description]); writer.writerows(cursor.fetchall())
    print("Generated:", counts); print("Status:", result["deployment_status"])
    print(f"Automated accuracy: {result['automated_accuracy_pct']:.1f}% | Coverage: {result['automation_pct']:.1f}%")
    print("Dashboard:", ROOT / "docs/index.html")


if __name__ == "__main__": main()
