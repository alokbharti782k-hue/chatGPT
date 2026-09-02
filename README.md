# ALICE AI

A modular AI assistant engineered for reliability, extensibility, and future integration with memory, RAG, tools, agents, voice, vision, and IoT systems.

## Current foundation

- FastAPI application
- `/health` endpoint
- Validated `/api/chat` endpoint
- Configuration via environment variables
- Deterministic request routing foundation
- LLM provider abstraction
- Initial safety-oriented system prompt
- Basic automated tests

## Run locally

```bash
python -m venv .venv
# Windows PowerShell
.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

Health check: `GET /health`

Chat endpoint: `POST /api/chat`

Example body:

```json
{"message":"Hello ALICE"}
```

The current chat engine intentionally uses a placeholder orchestrator until an LLM provider is configured.
