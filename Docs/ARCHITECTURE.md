# MyTrakin Architecture

## 1. Product scope

MyTrakin is intended to be a multi-tenant SaaS platform combining:
- Professional profiles, feed, connections, and messaging.
- Company administration, membership, roles, and documents.
- Business relationships and Master Service Agreements (MSAs).
- Project, role, Statement of Work (SOW), and contract management.
- Work tracking, timesheets, leave, and approvals.
- Invoice generation, accounts receivable/payable, payments, and reconciliation.
- Contextual AI for document understanding, search, analysis, and recommendations.

This is a target architecture. First inspect the current repository and preserve working implementations.

## 2. Preferred technology direction

Use existing project choices when sound and already established. If the repository is greenfield or has no contrary decision, the current preferred direction is:
- Frontend: Next.js + TypeScript.
- UI: Tailwind CSS and an established reusable component library such as shadcn/ui.
- Backend: FastAPI/Python for domain APIs if compatible with the current repository.
- Data: Supabase PostgreSQL.
- Authentication: Supabase Auth or the repository's existing secure auth system.
- Authorization: application-level RBAC plus PostgreSQL RLS.
- Files: private object storage, preferably existing Supabase Storage if already configured.
- Background work: a durable queue/worker system appropriate to the current hosting setup.
- Cache: introduce Redis only where measurements or workflow needs justify it.
- Hosting: existing Azure setup unless an approved architecture decision changes it.
- API specification: OpenAPI where supported.
- Monitoring: structured logs, error reporting, metrics, and tracing appropriate to the deployment.

Do not add a technology just because it appears in this document. Confirm operational fit, cost, support, and current repository conventions.

## 3. Logical architecture

```text
Browser / Mobile Client
        |
        v
Frontend / Presentation
        |
        v
Authenticated API Layer
        |
        +--> Identity and Authorization
        +--> Business Domain Services
        +--> Document Service
        +--> AI Service
        +--> Payment Service
        +--> Notification Service
        |
        +--> PostgreSQL / Supabase
        +--> Private Object Storage
        +--> Background Job Queue / Workers
        +--> External Providers (Plaid, payment processor, email, AI)
```

Keep business rules out of presentation components. The backend is responsible for validating actions and calculating financial values. The database enforces integrity and tenant isolation as an additional security layer.

## 4. Domain boundaries

- Identity: users, profiles, sessions, company memberships, user preferences.
- Social: connections, posts, comments/reactions if supported, messages, notifications.
- Business: companies, company-specific roles/permissions, employees/members, documents, MSAs.
- CODE: projects, project roles, SOWs, role allocations, contracts, contract versions, contract line items, invoices.
- WORK: work entries, timesheets, approval stages, leave requests, contract-specific work/payment views.
- PAYMENTS: bank connections, transactions, payment records, invoice matching, reconciliation, payment requests.
- AI: document extraction, summaries, risk findings, semantic search, recommendations, model/provider orchestration.
- Platform: audit events, background jobs, idempotency, feature flags, system settings.

Avoid duplicating the same business entity across modules. Module screens may present joined views, but the underlying entity must have one authoritative record.

## 5. Core business chain

```text
User / Company
      |
      v
Project
  + Project Roles and Capacity
      |
      v
SOW + Role Allocation
      |
      v
Contract + Commercial Terms
      |
      +--> Work / Timesheets / Approvals
      |
      +--> Contract Line Items
                  |
                  v
             Invoice
                  |
                  v
       Payment / Bank Reconciliation
```

Project, SOW, contract, invoice, and payment are distinct entities with separate lifecycles and permissions.

## 6. Multi-tenancy

Company-specific data must be scoped by explicit relationships and authorization. Membership alone does not grant access to every project or contract owned by that company. Some records involve multiple parties; access must be granted to each party only for the data and actions required by the relationship.

Never trust a client-provided company ID as proof of access.

## 7. Reliability and performance

- Use bounded, server-side pagination and filtering.
- Avoid N+1 queries and unbounded data retrieval.
- Use database transactions for allocation, invoice generation, and financial state changes.
- Use idempotency for retryable operations and external-provider webhooks.
- Add indexes based on query patterns and query-plan evidence.
- Move long-running OCR, AI extraction, and transaction synchronization into background jobs.
- Use caching only where invalidation and authorization are understood.
- Do not claim a one-million-user capacity without load testing, query measurements, and infrastructure sizing.

## 8. Architecture change policy

Any change to shared architecture, API conventions, data relationships, authentication, or authorization must be documented in `DECISIONS_AND_OPEN_QUESTIONS.md` and approved by the integration owner before incompatible implementation begins.

## Unified workspace and ownership context (authoritative)
The application shell is unified: one login, one Feed home page, one persistent navigation, and no separate Individual-vs-Company workspace mode. The user can open WORK, BUSINESS, CODE, PAYMENTS, and AI regardless of job title or company role; access to records and execution of business operations are still permission- and rule-controlled. Company-specific actions must be initiated by opening Business and selecting an authorized company. Pass a selected company context to subsequent screens only as a convenience hint; the server must re-resolve membership and permissions for every request. The same module can contain personal records and records belonging to a company, but ownership must be explicit and never inferred from whichever page happens to be open.

Use a clear ownership abstraction, preferably relational `owner_user_id` for individual-owned resources and `company_id` for company-owned resources, with constraints preventing ambiguous ownership. If a shared ownership abstraction is adopted, enforce exactly one valid owner type and matching owner reference. Do not use a client-provided owner/company identifier as proof of authorization.

