"""Load ticket outcomes into SQLite and materialize responsible-AI metrics."""

from __future__ import annotations

import csv
import sqlite3
from pathlib import Path


def build(csv_path: Path, db_path: Path, sql_dir: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists(): db_path.unlink()
    with csv_path.open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    with sqlite3.connect(db_path) as conn:
        conn.execute("""CREATE TABLE tickets (
            ticket_id TEXT PRIMARY KEY, created_at TEXT, language TEXT, channel TEXT,
            customer_tier TEXT, ticket_text TEXT, true_queue TEXT, predicted_queue TEXT,
            confidence REAL, automated INTEGER, review_reason TEXT, correct INTEGER,
            latency_ms INTEGER, estimated_cost_usd REAL)""")
        conn.executemany("INSERT INTO tickets VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", [tuple(r.values()) for r in rows])
        conn.executescript((sql_dir / "metrics.sql").read_text())

