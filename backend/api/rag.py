from pathlib import Path

from fastapi import APIRouter

from backend.config.settings import get_settings
from backend.rag.index import RAGIndex

router = APIRouter(prefix="/api/rag", tags=["rag"])


def get_index() -> RAGIndex:
    return RAGIndex(get_settings().rag_database_path)


@router.post("/index")
def index_documents() -> dict[str, int]:
    documents_dir = Path("data/documents")
    documents_dir.mkdir(parents=True, exist_ok=True)
    paths = [path for path in documents_dir.iterdir() if path.suffix.lower() in {".txt", ".md"}]
    return {"documents": len(paths), "chunks": get_index().index_documents(paths)}


@router.get("/search")
def search_documents(q: str, top_k: int = 5) -> dict[str, object]:
    if not q.strip():
        raise ValueError("Query cannot be empty")
    if not 1 <= top_k <= 10:
        raise ValueError("top_k must be between 1 and 10")
    results = get_index().retrieve(q, top_k=top_k)
    return {"query": q, "results": [{"source": s, "text": t, "score": score} for s, t, score in results]}
