# RAG Evaluation v2

ALICE now has a small deterministic evaluation fixture covering exact phrases, partial term overlap, case/punctuation normalization, and numeric sensor terms.

## Purpose

This suite measures whether representative queries retrieve a chunk containing the expected concept. It is intentionally lightweight and dependency-free.

## Gate for future retrieval upgrades

The lexical retriever remains the baseline. An embedding/vector backend should only replace or augment it after an evaluation shows measurable improvement on this fixture and a larger production-like dataset.

This evaluation is not a guarantee of factual answer quality; it is a retrieval regression gate.
