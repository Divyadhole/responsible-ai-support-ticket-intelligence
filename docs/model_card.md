# Model Card: Responsible AI Support-Ticket Router

## Intended use

Assist customer-support operations by recommending one of five queues and automatically routing only high-confidence, low-risk tickets. It is a decision-support system, not a replacement for support professionals.

## Out-of-scope use

- Emergency response, legal decisions, credit decisions, or fraud adjudication
- Fully autonomous handling of high-risk or unsupported requests
- Employee-performance scoring
- Inferring protected or sensitive personal traits

## Model design

The model uses an interpretable keyword-evidence layer and a conservative confidence policy. Every decision returns the proposed queue, confidence, matched terms, automation decision, and review reason.

## Human oversight

Tickets enter human review when they contain high-risk language, lack supported evidence, express multiple equally likely intents, or fall below the confidence threshold. Human reviewers make the final routing decision for these cases.

## Evaluation

- 8,000 reproducible synthetic tickets
- English, Spanish, and Hindi monitoring groups
- Five support queues and three contact channels
- Overall and selective accuracy, automation coverage, subgroup gaps, cost, and latency

The current evaluation intentionally fails the language-equity deployment gate. The recommendation is to hold broad deployment until multilingual performance is remediated.

## Limitations

Synthetic data cannot represent the full diversity of real customer language. Keyword evidence misses paraphrases, sarcasm, negation, and novel intent. Production readiness requires privacy review, real labeled data, drift monitoring, override logs, and incident-response ownership.

