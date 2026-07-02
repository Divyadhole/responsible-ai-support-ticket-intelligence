# Responsible AI Support-Ticket Intelligence

[![Live Dashboard](https://img.shields.io/badge/OPEN_LIVE_DASHBOARD-20A761?style=for-the-badge&logo=github&logoColor=white)](https://divyadhole.github.io/responsible-ai-support-ticket-intelligence/)

**[Explore the interactive responsible-AI dashboard →](https://divyadhole.github.io/responsible-ai-support-ticket-intelligence/)**

An end-to-end customer-operations case study that asks:

> **How can support tickets be automated without hiding uncertainty, unequal performance, or high-risk failures?**

This project builds an interpretable ticket-routing system with confidence-based automation, mandatory human review, multilingual subgroup monitoring, operational metrics, and a clear deployment decision.

## Executive result

The platform evaluates 8,000 reproducible support tickets across five queues, three languages, and three contact channels. It reports both model quality and automation coverage because accuracy alone can conceal who receives service and who is deferred to manual review.

```bash
python3 run_pipeline.py
open docs/index.html
```

No external packages, API keys, or paid model services are required.

## Responsible-AI controls

- **Interpretability:** every prediction exposes the terms that triggered routing
- **Selective automation:** only sufficiently confident, unambiguous tickets are auto-routed
- **Human oversight:** uncertain, unsupported, and ambiguous cases enter a review queue
- **High-risk hard stop:** fraud, legal, safety, discrimination, and emergency language can never be automated
- **Fairness monitoring:** accuracy and automation coverage are compared across English, Spanish, and Hindi tickets
- **Operational monitoring:** daily accuracy, automation, cost, and latency are tracked
- **Deployment gates:** selective accuracy, language gap, and high-risk escapes determine the recommendation

## Architecture

```text
Synthetic multilingual tickets
             │
             ▼
Interpretable routing + confidence policy
             │
       ┌─────┴─────┐
       ▼           ▼
  Auto-route    Human review
       └─────┬─────┘
             ▼
SQLite monitoring warehouse
             │
             ├── quality and coverage
             ├── subgroup fairness
             ├── confusion matrix
             ├── review workload
             └── cost and latency
             ▼
Interactive governance dashboard
```

## Metrics that matter

| Dimension | Metrics |
|---|---|
| Quality | Overall accuracy, selective accuracy, queue recall |
| Fairness | Language accuracy gap, automation-rate gap |
| Safety | High-risk automation escapes |
| Operations | Review workload, latency, estimated cost |
| Governance | Confidence, review reason, deployment gate |

## Project structure

```text
├── docs/index.html              # GitHub Pages dashboard
├── reports/                     # Dashboard and evaluation result
├── data/processed/              # Recruiter-friendly output tables
├── sql/metrics.sql              # Monitoring models
├── src/
│   ├── triage.py                # Interpretable routing policy
│   ├── generate_data.py         # Reproducible ticket generator
│   ├── build_database.py        # SQLite warehouse
│   ├── evaluate.py              # Governance and fairness gates
│   └── report.py                # Interactive dashboard
├── tests/
└── run_pipeline.py
```

## Run and verify

```bash
make run
make test
```

## Honest limitations

- The data is synthetic and cannot represent every real support dialect or customer context.
- Keyword evidence is intentionally interpretable but misses paraphrases, negation, and novel intent.
- Language is used for monitoring and confidence calibration, never as a routing label.
- Equal aggregate accuracy does not prove individual fairness or equal service quality.
- Production deployment requires reviewed real-world labels, privacy controls, drift alerts, override logging, and incident response.

## Interview walkthrough

1. Begin with the dashboard deployment decision.
2. Explain why automation coverage must accompany accuracy.
3. Demonstrate a clear ticket, an ambiguous ticket, and a high-risk ticket.
4. Compare language accuracy and automation gaps.
5. Close with the human-review policy and production limitations.
