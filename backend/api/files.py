from pathlib import Path

from fastapi import APIRouter, UploadFile

router = APIRouter(prefix="/api/files", tags=["files"])
DOCUMENTS_DIR = Path("data/documents")
MAX_UPLOAD_BYTES = 10 * 1024 * 1024


@router.post("/upload")
async def upload_file(file: UploadFile) -> dict[str, str]:
    if not file.filename:
        raise ValueError("A filename is required")
    safe_name = Path(file.filename).name
    destination = DOCUMENTS_DIR / safe_name
    data = await file.read(MAX_UPLOAD_BYTES + 1)
    if len(data) > MAX_UPLOAD_BYTES:
        raise ValueError("File exceeds the 10 MB upload limit")
    DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(data)
    return {"filename": safe_name, "status": "stored"}
