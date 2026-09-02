# ALICE AI Architecture

ALICE is organized as a layered assistant/agent platform:

1. **Interface/API** — FastAPI chat, health, status, files, and RAG endpoints.
2. **Safety & validation** — input validation, threat detection, containment, authentication, permissions, and deterministic safety boundaries.
3. **Orchestrator** — coordinates routing, memory, and model/tool work.
4. **AI providers** — LLM, embeddings, and vision are isolated behind interfaces.
5. **Memory** — SQLite stores conversation history; long-term memory remains provider-neutral.
6. **RAG** — documents are loaded, chunked, persistently indexed/retrieved, with a clean boundary for future vector search.
7. **Tools** — allowlisted tools are separated from the model and bounded by execution policy.
8. **Bounded agent** — plans, executes approved tools, observes results, stops on failure, and enforces step budgets.
9. **Security operations** — rate limiting, request IDs, audit events, secret redaction, security headers, and hardened document ingestion.
10. **Services** — speech and notifications remain provider-neutral extension points.

## Safety principle

The language model is not a safety controller. For the Miner Safety System and other physical systems, sensor thresholds, alarms, shutdowns, and actuation must remain deterministic and independently validated. ALICE can explain or assist with those systems, but it must not be the sole authority for a safety-critical decision.

## Defensive cybersecurity principle

ALICE is designed to detect, block, contain, log, and recover from threats. It must not autonomously retaliate against, compromise, exploit, or attack another system.

## Production boundary

Application-level controls do not replace a secure deployment perimeter. Production should additionally use authenticated HTTPS, managed/shared rate limiting when horizontally scaled, secret management, protected log storage and rotation, network egress controls, monitoring/alerting, backups, and external malware scanning/WAF where appropriate.
