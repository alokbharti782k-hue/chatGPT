# ALICE Security Model

ALICE uses defense-in-depth controls around its AI and agent layers.

## Controls

- Threat detection blocks known prompt-injection, credential-exfiltration, shell/script, and path-traversal indicators.
- Tool execution is allowlisted and bounded by step/call budgets.
- Tool arguments and outputs are security-checked before they continue through the agent flow.
- External tools and IoT actions are disabled by default through the permission policy.
- API requests are rate-limited with a dependency-free sliding-window limiter.
- Security events are written to a JSONL audit log with common credential values redacted.
- Uploaded documents are treated as data; they are not executable.

## Safety boundary

ALICE is designed to defend and contain. It must not autonomously retaliate against, compromise, or attack another system. Physical safety decisions for the Miner Safety System remain deterministic and must not depend solely on an LLM.

## Operational guidance

For deployment, place ALICE behind authenticated HTTPS infrastructure, rotate credentials regularly, restrict network egress, protect audit logs, and add an external malware scanner/WAF where appropriate. These deployment controls are not claimed to be provided by the application itself.
