# ALICE AI deployment

## Production prerequisites

Set these environment variables in the hosting platform's secret/configuration store:

- `OPENAI_API_KEY`: provider credential; never commit it.
- `OPENAI_MODEL`: deployed model identifier.
- `API_KEY`: long random Bearer token for ALICE API clients.
- `ENVIRONMENT=production`
- `DEBUG=false`
- `CORS_ORIGINS`: comma-separated production frontend origins.
- `DATABASE_PATH`: persistent writable path if conversation persistence is required.
- `RAG_DATABASE_PATH`: persistent writable path for the RAG SQLite database.

## Container

The repository includes a non-root Python 3.12 container. Build it with:

```bash
docker build -t alice-ai .
```

Run it with a secret API key supplied by the platform:

```bash
docker run --rm -p 8000:8000 \
  -e ENVIRONMENT=production \
  -e DEBUG=false \
  -e OPENAI_API_KEY="$OPENAI_API_KEY" \
  -e API_KEY="$API_KEY" \
  -e CORS_ORIGINS="https://your-frontend.example" \
  alice-ai
```

## Health checks

Use `GET /health` for the basic process health check. Use `GET /api/status` as the authenticated application status endpoint.

## Production safety

- Keep API credentials in platform-managed secrets.
- Do not expose `/api/metrics` publicly without the API authentication boundary.
- Use HTTPS at the edge.
- Use a persistent volume for SQLite if conversation/RAG state must survive restarts.
- For multiple application replicas, replace the in-process rate limiter and SQLite persistence with shared production infrastructure before horizontal scaling.
- Keep deterministic safety logic authoritative for safety-critical IoT/MSS actions; ALICE must not directly actuate physical equipment.

## Launch gate

ALICE should be considered launch-ready only after the main branch contains the final reviewed changes and the CI workflow reports a successful test run. A deployed environment should then be smoke-tested through `/health`, authenticated `/api/status`, `/api/chat`, and `/api/chat/stream`.
