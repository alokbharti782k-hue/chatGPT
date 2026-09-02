# ALICE AI

ALICE AI is a modular FastAPI-based AI assistant engineered for reliability, security, extensibility, memory, RAG, bounded tools/agents, observability, and secure streaming.

## Current capabilities

- FastAPI application with browser frontend
- Persistent conversation memory with SQLite
- Deterministic lexical RAG with evaluation coverage
- Defensive cyber-security controls: validation, threat detection, containment, audit logging, authentication, rate limiting, and security headers
- Allowlisted bounded tool runtime with IoT actions disabled by default
- Aggregate observability metrics without request content or credentials
- Standard `POST /api/chat` response flow
- Secure `POST /api/chat/stream` SSE streaming flow
- Native OpenAI Responses API streaming behind a provider abstraction
- Production container baseline using Python 3.12 and a non-root runtime user

## Run locally

```bash
python -m venv .venv
# Windows PowerShell
.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

Health check: `GET /health`

Application status: `GET /api/status`

Chat endpoint: `POST /api/chat`

Streaming endpoint: `POST /api/chat/stream`

Example request:

```json
{"message":"Hello ALICE"}
```

## Configuration

Copy `.env.example` to `.env` for local development and configure `OPENAI_API_KEY` to enable live model responses. In deployed environments, store `OPENAI_API_KEY` and `API_KEY` in the platform's secret manager rather than committing them.

## Deployment

See `docs/DEPLOYMENT.md` for the production container, environment requirements, health checks, persistence considerations, and launch gate.

## Security boundary

ALICE is designed as a defensive assistant. It does not provide arbitrary shell execution, autonomous offensive cyber actions, or unrestricted physical IoT actuation. Safety-critical mining controls should remain deterministic and independent of LLM output.
