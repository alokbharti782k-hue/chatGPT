from backend.rag.index import RAGIndex


class RAGContextTool:
    """Retrieve grounded local-document context without allowing arbitrary execution."""

    def __init__(self, index: RAGIndex) -> None:
        self.index = index

    def retrieve(self, query: str, top_k: int = 5) -> list[dict[str, object]]:
        if not query.strip():
            raise ValueError("Query cannot be empty")
        if not 1 <= top_k <= 10:
            raise ValueError("top_k must be between 1 and 10")
        return [
            {"source": source, "text": text, "score": score}
            for source, text, score in self.index.retrieve(query, top_k=top_k)
        ]
