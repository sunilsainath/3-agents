# MyTrakin Backend — Agent 2 Working Notes

Branch: `feature/backend-logic` (canonical per approval 2026-10-09).
Stack: FastAPI (Python) + Supabase Postgres + Supabase Auth. Azure hosting TBD.
API base: `/api/v1`. OpenAPI via FastAPI (`/api/v1/openapi.json`, docs at `/api/v1/docs`).

## Baseline (Phase 0, 2026-10-09)
Greenfield repo: docs only (`Docs/`, `README.md`). No backend/frontend/migrations/tests existed.
Scaffold scope (approved): health + auth-guard + error/pagination envelopes + OpenAPI only.
No business workflows implemented yet. No schema/migration edits (DB agent owns).

## Conventions (from API_CONTRACTS.md, binding for new endpoints)
- Error envelope: `{"error": {"code": "SOME_CODE", "message": "...", "request_id": "..."}}`
- List envelope: `{"data": [], "pagination": {"page": 1, "page_size": 25, "total": 0}}`
- Auth every protected route; actor from validated token, never from body.
- `company_id` in requests = requested scope only; revalidate membership + role + resource access server-side.
- Ownership: exactly one of `owner_user_id` (derived from principal) / `company_id` where resource supports both.
- No generic status sets; use explicit decision commands. No client totals. No `PAID`/`APPROVED` from client.

## DB dependencies (requested, not implemented by backend)
1. Tables + RLS for users/profiles, companies, memberships, company roles/permissions, projects/roles/allocations, SOWs/versions, contracts/versions/line items/approvals, work/timesheets/approvals, invoices/lines, payments/accounts/transactions/matches, idempotency_records, audit_events, AI tables.
2. Ownership invariant (`owner_user_id` XOR `company_id`), indexes, FKs, public-ID uniqueness.
3. Money as `numeric`, currency/rounding policy (D-010). Capacity-counting states (D-002). Invoice idempotency key (D-007). MSA gate semantics (D-005).
4. Supabase project URL + anon key (frontend) / service-role + JWT secret (backend only, via secret manager). No secrets in repo.

## Frontend dependencies
- Use `/api/v1` + envelopes above; send `Authorization: Bearer <supabase-jwt>`, optional `X-Request-ID`.
- Expect 401 `AUTHENTICATION_REQUIRED`, 403 `PERMISSION_DENIED` (deny-by-default stub denies company scopes until DB membership lookup lands), 422 `VALIDATION_ERROR`.
- Breaking field/enum/error changes require joint approval + decision-log entry.

## Unresolved (D-001 resolved to FastAPI+Supabase; D-002–D-016 open)
See `Docs/DECISIONS_AND_OPEN_QUESTIONS.md`. Backend blocked on D-002, D-003, D-004, D-005, D-006, D-007, D-010 before Phases 2–6.

## Work order
1. ✅ Scaffold (this commit): health, guards, envelopes, OpenAPI, tests.
2. Next (Phase 1, needs DB schema): real JWT verify + membership/role lookup, companies/members/roles endpoints, audit writer.
3. Then vertical slices per IMPLEMENTATION_PLAN.md Phases 2→7. No AI auto-approve, no client-proof payments, ever.
