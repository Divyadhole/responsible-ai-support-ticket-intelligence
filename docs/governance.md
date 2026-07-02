# Governance Plan

## Ownership

- Product owner: defines permitted use and automation targets
- Support operations: owns review workflows and escalation outcomes
- Model-risk owner: approves thresholds and monitors subgroup performance
- Engineering: owns logging, access controls, reliability, and rollback

## Pre-deployment gates

1. Zero high-risk automation escapes
2. At least 90% selective accuracy
3. Language accuracy gap no greater than 12 percentage points
4. Human-review capacity sized for observed deferral volume
5. Privacy and security approval for ticket-text processing

## Production monitoring

- Daily: volume, accuracy samples, automation coverage, latency, failures
- Weekly: reviewer overrides, queue-specific recall, emerging intent
- Monthly: subgroup gaps, threshold review, cost, incidents
- Quarterly: full model and policy reapproval

## Incident response

Disable automation immediately for high-risk escapes, rapid subgroup degradation, sustained routing failures, or missing audit logs. Preserve evidence, notify owners, route all affected tickets to humans, and require a documented reapproval before restoration.

