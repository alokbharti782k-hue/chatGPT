from fastapi import FastAPI

app = FastAPI(title="ALICE AI", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "ALICE AI"}
