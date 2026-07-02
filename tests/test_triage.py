import unittest
from src.triage import classify


class TriageTests(unittest.TestCase):
    def test_routes_clear_billing_ticket(self):
        result = classify("I was charged twice and need a refund")
        self.assertEqual(result.predicted_queue, "billing")
        self.assertTrue(result.automated)
        self.assertIn("refund", result.matched_terms)

    def test_high_risk_language_requires_human(self):
        result = classify("My card was stolen and this looks like fraud")
        self.assertFalse(result.automated)
        self.assertEqual(result.review_reason, "high_risk_language")

    def test_unsupported_ticket_requires_human(self):
        result = classify("I would like to speak with somebody")
        self.assertFalse(result.automated)
        self.assertEqual(result.review_reason, "no_supported_signal")

    def test_ambiguous_intent_requires_human(self):
        result = classify("The app error prevents my package tracking")
        self.assertFalse(result.automated)
        self.assertEqual(result.review_reason, "ambiguous_intent")


if __name__ == "__main__": unittest.main()

