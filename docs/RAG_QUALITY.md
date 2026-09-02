# RAG Quality Milestone

The ALICE RAG layer now uses deterministic token normalization, query-term coverage, frequency scoring, and an exact-phrase bonus. Regression tests cover punctuation normalization, ranking, and empty queries. The implementation remains dependency-free and isolated so an embedding/vector backend can be added after measurable evaluation.