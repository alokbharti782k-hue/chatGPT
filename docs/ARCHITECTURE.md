# ALICE AI Architecture

ALICE is organized as a layered assistant platform:

1. **API** — FastAPI endpoints validate requests and expose chat/file operations.
2. **Orchestrator** — coordinates validation, routing, memory, and the selected model provider.
3. **AI providers** — LLM, embeddings, and vision are isolated behind interfaces.
4. **Memory** — SQLite stores conversation history; long-term memory remains provider-neutral.
5. **RAG** — documents are loaded, chunked, indexed/retrieved, and can later be upgraded to embeddings/vector search.
6. **Tools** — calculator, local file search, web-search boundary, and IoT boundary are separated from the model.
7. **Safety** — permissions default to deny external/IoT actions and side effects require explicit policy handling.
8. **Agent layer** — planning/execution is bounded and designed for controlled tool use.
9. **Services** — speech and notifications are provider-neutral extension points.

## Safety principle

The language model is not a safety controller. For the Miner Safety System and other physical systems, sensor thresholds, alarms, shutdowns, and actuation must remain deterministic and independently validated. ALICE can explain or assist with those systems, but it must not be the sole authority for a safety-critical decision.
