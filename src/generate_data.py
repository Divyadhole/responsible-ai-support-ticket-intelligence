"""Generate a reproducible multilingual customer-support dataset."""

from __future__ import annotations

import csv
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .triage import HIGH_RISK, KEYWORDS, QUEUES, classify

START = datetime(2026, 3, 1, tzinfo=timezone.utc)
LANGUAGES = ("English", "Spanish", "Hindi")
CHANNELS = ("chat", "email", "web")
TEMPLATES = {
    "billing": ("I was charged twice and need a refund", "My invoice has the wrong payment amount", "The charge on my card is incorrect"),
    "account_access": ("My account is locked and I cannot login", "Password reset does not let me sign in", "Please help verify my account"),
    "technical": ("The app keeps loading and then shows an error", "The screen is broken after the update", "I found a bug that makes the app crash"),
    "delivery": ("My package is late and tracking has not changed", "When will the delivery arrive", "The courier marked my shipment delivered"),
    "cancellation": ("Please cancel my subscription before renewal", "I want to stop my membership", "How do I terminate the subscription"),
}


def _write(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader(); writer.writerows(rows)


def generate(output: Path, n: int = 8_000, seed: int = 19) -> dict:
    rng = random.Random(seed)
    rows = []
    for i in range(1, n + 1):
        true_queue = rng.choices(QUEUES, weights=(27, 19, 24, 18, 12), k=1)[0]
        language = rng.choices(LANGUAGES, weights=(72, 16, 12), k=1)[0]
        channel = rng.choices(CHANNELS, weights=(45, 32, 23), k=1)[0]
        tier = rng.choices(("standard", "premium"), weights=(78, 22), k=1)[0]
        text = rng.choice(TEMPLATES[true_queue])
        # Realistic ambiguity and code-switching reduce lexical coverage.
        if rng.random() < (0.16 if language == "English" else 0.34):
            other = rng.choice([q for q in QUEUES if q != true_queue])
            text += " Also " + rng.choice(TEMPLATES[other]).lower()
        if rng.random() < (0.04 if language == "English" else 0.13):
            for term in KEYWORDS[true_queue]:
                text = text.replace(term, "issue")
        if rng.random() < 0.035:
            text += " This may be " + rng.choice(HIGH_RISK) + "."
        decision = classify(text, language)
        correct = int(decision.predicted_queue == true_queue)
        base_latency = rng.randint(48, 135)
        latency_ms = base_latency + len(text) // 3 + (rng.randint(20, 55) if not decision.automated else 0)
        cost = 0.0022 + len(text) * 0.000006 + (0.042 if not decision.automated else 0)
        created = START + timedelta(minutes=rng.randint(0, 59 * 24 * 60))
        rows.append({
            "ticket_id": f"T{i:06d}", "created_at": created.isoformat(), "language": language,
            "channel": channel, "customer_tier": tier, "ticket_text": text,
            "true_queue": true_queue, "predicted_queue": decision.predicted_queue,
            "confidence": decision.confidence, "automated": int(decision.automated),
            "review_reason": decision.review_reason, "correct": correct,
            "latency_ms": latency_ms, "estimated_cost_usd": round(cost, 4),
        })
    _write(output / "tickets.csv", rows)
    return {"tickets": len(rows), "automated": sum(r["automated"] for r in rows)}

