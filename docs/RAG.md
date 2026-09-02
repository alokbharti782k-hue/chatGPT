# ALICE RAG

ALICE currently uses a persistent, dependency-free lexical retrieval layer for `.txt` and `.md` documents.

## Retrieval behavior

- Text is normalized into alphanumeric tokens.
- Retrieval scores query-term coverage and frequency.
- Exact query-phrase matches receive a small ranking bonus.
- Results are returned in descending relevance order.
- Empty queries return no results.

## Safety boundary

Uploaded files remain data, not executable content. The upload guard accepts only UTF-8 text and rejects null-byte/binary content before indexing.

## Upgrade path

The RAG interface is intentionally isolated so a future embedding/vector backend can be introduced without changing the API contract. Until that backend is configured and evaluated, the deterministic lexical index remains the default.
