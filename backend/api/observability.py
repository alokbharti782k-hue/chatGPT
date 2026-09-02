from fastapi import APIRouter

from backend.observability.metrics import metrics

router = APIRouter(prefix="/api", tags=["observability"])


@router.get("/metrics")
def get_metrics() -> dict[str, float | int]:
    snapshot = metrics.snapshot()
    return {
        "requests_total": snapshot.requests_total,
        "errors_total": snapshot.errors_total,
        "security_blocks_total": snapshot.security_blocks_total,
        "total_latency_ms": round(snapshot.total_latency_ms, 3),
        "average_latency_ms": round(snapshot.average_latency_ms, 3),
    }
