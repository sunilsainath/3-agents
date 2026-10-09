# MyTrakin API Contracts

## 1. Purpose

This document establishes API design conventions and conceptual resource contracts. The backend agent must inspect existing routes and produce exact endpoint paths, request schemas, response schemas, and OpenAPI documentation that fit the current repository. Do not assume every path below already exists.

## 2. API principles

- Use the existing backend framework and conventions.
- Use `/api/v1` versioning if the project already uses or approves versioned REST routes.
- Authenticate every protected request.
- Authorize every action server-side.
- Derive actor identity from the validated session/token, not from request body fields.
- Validate all request bodies and query parameters.
- Use consistent error formats and HTTP status codes.
- Apply server-side pagination, filtering, and sorting.
- Never return secrets or unnecessary sensitive fields.
- Use idempotency for invoice generation, payment initiation, and retryable external operations.
- Document endpoints in OpenAPI where supported.

## 3. Suggested resource groups

- Identity/profile: `/users`, `/profiles`
- Companies: `/companies`, `/companies/{companyId}/members`, `/companies/{companyId}/roles`
- Social: `/connections`, `/posts`, `/conversations`, `/notifications`
- MSA: `/msas`, `/msa-requests`
- Projects: `/projects`, `/projects/{projectId}/roles`
- SOW: `/sows`, `/sows/{sowId}/decisions`
- Contracts: `/contracts`, `/contracts/{contractId}/versions`, `/contracts/{contractId}/decisions`
- Work: `/timesheets`, `/work-entries`, `/leave-requests`
- Invoices: `/invoices`, `/invoices/{invoiceId}/decisions`
- Payments: `/payment-accounts`, `/transactions`, `/reconciliations`, `/payment-requests`
- AI: `/ai/jobs`, `/ai/analyses`, `/ai/search`

These are candidate resource names, not permission to create duplicate routes. Reuse the existing API patterns.

## 4. List endpoint conventions

List endpoints should support only approved filters relevant to the resource:
- `page`/`page_size` or cursor pagination.
- `sort_by` and `sort_order` from an allowlist.
- Search and status/date filters.
- Explicit company/project context where required.

Do not allow arbitrary SQL field names or raw sort expressions from clients. Enforce a maximum page size.

Example response shape (adapt to existing conventions):

```json
{
  "data": [],
  "pagination": {
    "page": 1,
    "page_size": 25,
    "total": 0
  }
}
```

## 5. Error format

Use a consistent machine-readable error code and safe human-readable message. Example:

```json
{
  "error": {
    "code": "ROLE_CAPACITY_EXCEEDED",
    "message": "The requested allocation exceeds the available role capacity.",
    "request_id": "correlation-id"
  }
}
```

Do not expose stack traces, SQL details, provider tokens, internal secrets, or sensitive data in client errors.

Suggested codes include:
- `AUTHENTICATION_REQUIRED`
- `PERMISSION_DENIED`
- `RESOURCE_NOT_FOUND`
- `INVALID_STATE_TRANSITION`
- `ROLE_CAPACITY_EXCEEDED`
- `DUPLICATE_INVOICE`
- `MSA_REQUIRED`
- `VALIDATION_ERROR`
- `IDEMPOTENCY_CONFLICT`
- `EXTERNAL_PROVIDER_UNAVAILABLE`

## 6. Project contracts

Project create/update contracts should represent:
- Individual or company project category.
- Project type.
- Name and description.
- Dates, estimated time, budget, and currency.
- Explicit project owner and access model.

The backend must derive/validate company ownership from the authenticated actor's permissions.

Project-role endpoints should support create/update and show required, allocated, and available capacity. Availability is advisory until the allocation transaction succeeds.

## 7. SOW contracts

SOW create/update payloads should include:
- Project reference.
- Parties and SOW type.
- Dates and commercial terms.
- Role allocations, quantities, rates, currency, billing basis and frequency.
- Documents/version references where applicable.

Decisions should be explicit commands (accept/reject) rather than arbitrary status updates. Reject commands must capture a reason or notes as required by business policy.

## 8. Contract contracts

Contract operations should support:
- Create from valid SOW allocation.
- Send/invite.
- Accept/decline.
- Amend/version.
- Renew where supported.
- Terminate/close with appropriate validation.
- View terms, line items, parties, approvals, documents, and audit history.

Clients must not directly set protected statuses such as `ACTIVE`, `ACCEPTED`, `PAID`, or `APPROVED` through generic update payloads.

## 9. Timesheet contracts

Support creating/editing eligible work entries, submitting a timesheet, reviewer decisions, and correction/resubmission.

The backend must validate:
- Actor is permitted to submit or review.
- Contract is valid for the date.
- Role matches the contract assignment.
- Hours and break values are valid.
- Period is not locked.
- Approval step is the current required step.

AI import must return a reviewable draft/extraction, not auto-approved work.

## 10. Invoice contracts

Invoice generation should be a server-side operation using approved billing sources and contract rules. It should:
- Be idempotent.
- Return the invoice ID and current state.
- Avoid duplicate billing for the same source/period.
- Record line-item provenance.
- Enforce MSA submission rules.
- Preserve financial history.

Invoice decisions should use explicit operations for submit, approve, reject, dispute, cancel, and record/allocate payment.

Never accept a client-supplied invoice total as authoritative.

## 11. Payment and webhook contracts

- Provider webhooks must be authenticated/verified according to provider requirements.
- Deduplicate events and make processing idempotent.
- Acknowledge provider events promptly and process expensive work asynchronously where appropriate.
- Store only required normalized transaction data.
- Never expose provider access tokens to clients.
- Distinguish payment initiation, processor confirmation, bank transaction detection, and reconciliation.
- Do not mark an invoice paid based only on a same-amount transaction.

## 12. AI API contracts

AI endpoints must:
- Enforce access to the underlying source entities.
- Record task status and provenance.
- Return source references/page/section citations where possible.
- Handle model/provider timeouts and failures.
- Avoid leaking one tenant's data into another tenant's results.
- Keep analysis separate from execution of business actions.
- Require explicit user confirmation for consequential changes.

## 13. API change policy

Any breaking field, endpoint, enum, or error-contract change must be discussed with the frontend agent and recorded in the decision log before merge. Update API documentation and tests in the same pull request.

## Unified workspace and ownership API rules (authoritative)
Expose one application workspace; do not require a workspace-mode switch in API clients. Company actions are initiated through Business after selecting an authorized company. API requests may include a company identifier as a requested context, but the backend must verify current membership and operation-level permissions on every request. Never trust client-provided `owner_user_id`, `company_id`, roles, or context tokens as authorization.

Create/list endpoints must explicitly support the resource's ownership model: personal-owned records are scoped to the authenticated user; company-owned records are scoped to an authorized company. For resources supporting both, require an unambiguous owner choice and reject requests that supply both or neither. List/search/export endpoints must apply the same ownership checks as detail endpoints. Keep company context visible in response metadata where useful, but avoid leaking records in cross-company aggregate results. Use consistent 403/404 behavior according to the application's resource-disclosure policy.

