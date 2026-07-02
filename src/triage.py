"""Interpretable support-ticket routing with human-review safeguards."""

from __future__ import annotations

from dataclasses import asdict, dataclass

QUEUES = ("billing", "account_access", "technical", "delivery", "cancellation")
KEYWORDS = {
    "billing": ("charge", "charged", "refund", "invoice", "payment", "double", "card"),
    "account_access": ("login", "password", "locked", "verify", "account", "sign in"),
    "technical": ("error", "crash", "bug", "loading", "broken", "app", "screen"),
    "delivery": ("delivery", "shipment", "package", "tracking", "arrive", "late", "courier"),
    "cancellation": ("cancel", "subscription", "renewal", "stop", "terminate", "membership"),
}
HIGH_RISK = ("fraud", "stolen", "legal", "discrimination", "unsafe", "emergency", "suicide")


@dataclass(frozen=True)
class TriageDecision:
    predicted_queue: str
    confidence: float
    automated: bool
    review_reason: str
    matched_terms: tuple[str, ...]


def classify(text: str, language: str = "English", threshold: float = 0.72) -> TriageDecision:
    """Route a ticket while exposing evidence and sending uncertain cases to people."""
    lowered = text.lower()
    matches = {queue: tuple(term for term in terms if term in lowered) for queue, terms in KEYWORDS.items()}
    scores = {queue: len(terms) for queue, terms in matches.items()}
    predicted = max(QUEUES, key=lambda queue: (scores[queue], -QUEUES.index(queue)))
    ordered = sorted(scores.values(), reverse=True)
    lead, runner_up = ordered[0], ordered[1]
    confidence = 0.42 + 0.16 * lead + 0.09 * max(lead - runner_up, 0)
    if language != "English":
        confidence -= 0.09
    confidence = max(0.30, min(confidence, 0.97))
    risk_terms = tuple(term for term in HIGH_RISK if term in lowered)
    if risk_terms:
        reason = "high_risk_language"
    elif lead == 0:
        reason = "no_supported_signal"
    elif lead == runner_up:
        reason = "ambiguous_intent"
    elif confidence < threshold:
        reason = "low_confidence"
    else:
        reason = "auto_routed"
    automated = reason == "auto_routed"
    return TriageDecision(predicted, round(confidence, 3), automated, reason, matches[predicted])


def classify_as_dict(text: str, language: str = "English", threshold: float = 0.72) -> dict:
    return asdict(classify(text, language, threshold))

