from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, UploadFile

router = APIRouter(prefix="/api/files", tags=["files"])
DOCUMENTS_DIR = Path("data/documents")
MAX_UPLOAD_BYTES = 10 * 1024 * 1024
ALLOWED_EXTENSIONS = {".txt", ".md"}


@router.post("/upload")
async def upload_file(file: UploadFile) -> dict[str, str]:
    if not file.filename:
        raise ValueError("A filename is required")

    original_name = Path(file.filename).name
    extension = Path(original_name).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError("Only .txt and .md documents are supported")

    data = await file.read(MAX_UPLOAD_BYTES + 1)
    if len(data) > MAX_UPLOAD_BYTES:
        raise ValueError("File exceeds the 10 MB upload limit")

    DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
    stored_name = f"{uuid4().hex}{extension}"
    destination = DOCUMENTS_DIR / stored_name
    destination.write_bytes(data)
    return {"filename": original_name, "stored_as": stored_name, "status": "stored"}
