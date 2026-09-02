# ALICE Roadmap

## Foundation — completed
- FastAPI API and static web UI
- Environment-based configuration
- Provider-neutral LLM, embeddings, vision, speech, and notification boundaries
- Persistent SQLite conversation memory
- Persistent local text/Markdown RAG
- Calculator and allowlisted tool registry
- Deny-by-default permission boundary for external/IoT actions
- Bounded agent planner/executor with defensive security controls
- Threat detection and containment
- Authentication, rate limiting, request IDs, security headers, audit logging, secret redaction
- Hardened UTF-8 document ingestion

## Current RAG quality track
- Deterministic token normalization for retrieval
- Query-term coverage and frequency scoring
- Exact-phrase ranking bonus
- Regression tests for ranking behavior
- Explicit boundary for future embedding/vector retrieval

## Next feature track
- Embedding-backed RAG after measurable evaluation
- Streaming responses and cancellation
- Structured tool schemas and model-driven tool calling
- Observability, latency/token metrics, health/readiness checks, and alerting
- Answer-quality and tool-safety evaluation suite
- Production database abstraction
- Real speech/vision providers
- Controlled MSS gateway integration with deterministic safety logic
- Deployment automation and performance/security testing

## Verification note
GitHub Actions workflow results are not currently verified for the latest baseline. Do not treat CI as passing until a workflow run or equivalent test execution is confirmed.
