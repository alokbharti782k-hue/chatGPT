from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["status"])


@router.get("/status")
def status() -> dict[str, str]:
    return {"service": "ALICE AI", "status": "ready"}
