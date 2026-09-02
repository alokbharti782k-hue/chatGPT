# ALICE setup

## Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Set `OPENAI_API_KEY` in `.env` before starting the model-backed assistant.

Run:

```powershell
uvicorn backend.main:app --reload
```

Open `http://127.0.0.1:8000/` for the web interface.

## API

- `GET /health` — health check
- `GET /api/status` — service status
- `POST /api/chat` — chat with optional `conversation_id`
- `POST /api/files/upload` — bounded local document upload

The repository never expects API secrets to be committed. `.env` is ignored by Git.
