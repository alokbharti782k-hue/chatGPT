# ALICE AI Observability

ALICE exposes dependency-free operational metrics through `GET /api/metrics` once the observability router is registered by the application.

Tracked values are deliberately aggregate-only:

- total requests
- total server errors
- security-block counter
- aggregate latency in milliseconds
- average latency in milliseconds

Request bodies, prompts, credentials, tokens, and other sensitive content are not recorded by this metrics layer.

## Production boundary

The collector is in-process and therefore suitable as a lightweight baseline, not a distributed metrics backend. A production deployment can later export these aggregates to a metrics system without changing the application contract.
