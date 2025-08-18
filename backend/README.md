## DocuTalk API (FastAPI)

Run locally:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --factory
```

Environment:

Copy `.env.example` to `.env` and fill in keys.

