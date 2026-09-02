# ALICE Security Model

ALICE uses defense-in-depth controls around its AI and agent layers.

## Controls

- Threat detection blocks known prompt-injection, credential-exfiltration, shell/script, and path-traversal indicators.
- Tool execution is allowlisted and bounded by step/call budgets.
- Tool arguments and outputs are security-checked before they continue through the agent flow.
- External tools and IoT actions are disabled by default through the permission policy.
- Configurable Bearer API-key authentication is available for deployed environments.
- API requests are rate-limited with a dependency-free sliding-window limiter.
- Responses receive request IDs and baseline security headers.
- Security events are written to a JSONL audit log with common credential values redacted.
- Uploaded documents are restricted to UTF-8 text and reject binary/null-byte content; uploaded files are treated as data, not executable code.

## Safety boundary

ALICE is designed to detect, block, contain, log, and recover. It must not autonomously retaliate against, compromise, exploit, or attack another system. Physical safety decisions for the Miner Safety System remain deterministic and must not depend solely on an LLM.

## Limitations

The in-process rate limiter is suitable as a dependency-free baseline but should be replaced or backed by shared infrastructure for horizontally scaled deployments. Secret redaction is heuristic, not a guarantee of finding every possible secret format. The application audit log is append-only at the application layer but is not cryptographically tamper-evident.

## Operational guidance

For production, use authenticated HTTPS, a managed/shared rate limiter, a real secret manager, protected and rotated audit logs, network egress restrictions, monitoring/alerting, backups, and an external malware scanner/WAF where appropriate. These deployment controls are not claimed to be provided by the application itself.
