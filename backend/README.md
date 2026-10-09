# MyTrakin Backend API (Agent 2)

FastAPI + Supabase Postgres + Supabase Auth. Phase 0 scaffold: health, auth guard,
error/pagination envelopes, OpenAPI. No business workflows yet.

## Quickstart

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e ".[test]"
copy ..\.env.example .env   # or set env vars directly; never commit .env
uvicorn app.main:app --reload --port 8000
```

- Health: `GET http://localhost:8000/api/v1/health`
- OpenAPI: `http://localhost:8000/api/v1/openapi.json`, docs at `/api/v1/docs`
- Protected example: `GET /api/v1/me` with `Authorization: Bearer <supabase-jwt>`

## Env (placeholders only — real secrets live in secret manager)

See repo-root `.env.example`. Backend needs `SUPABASE_URL` and either
`SUPABASE_JWT_SECRET` (HS256 dev) or JWKS path (production TODO).

## Rules

- Actor identity comes from the validated token, never from request bodies.
- `company_id` in a request is requested scope only; membership/role/resource
  checks run server-side on every operation (currently deny-by-default stub
  until the DB agent lands membership lookups — see `app/core/tenant.py`).
- Errors use `{"error": {"code", "message", "request_id"}}`.
- Lists use `{"data", "pagination": {"page", "page_size", "total"}}`.
