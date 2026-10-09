# MyTrakin Implementation Plan

## 1. Working principle

Build small, integrated vertical slices. Do not implement three disconnected layers and postpone integration until the end.

## 2. Phase 0 — Discovery and alignment

All agents:
- Inspect the repository and current deployment configuration.
- Identify existing features and incomplete workflows.
- Read this documentation pack.
- Report architecture conflicts, risks, missing requirements, and dependencies.
- Do not make breaking changes before the integration owner approves the plan.

Deliverables:
- Repository assessment.
- Confirmed architecture.
- Confirmed entity/API contracts.
- Ordered implementation plan.
- Test and environment strategy.

## 3. Phase 1 — Identity and company foundation

- Authentication and profile.
- Company creation and membership.
- Company-specific roles and permissions.
- RLS and private document storage.
- Basic application shell and company context.

Acceptance:
- Users can authenticate.
- Company membership is explicit.
- Cross-company access tests pass.
- Sensitive documents are private.

## 4. Phase 2 — Projects and role capacity

- Project creation and visibility.
- Project roles.
- Required, allocated, and available capacity.
- Transaction-safe allocation.

Acceptance:
- Individual/company authorization works.
- Concurrent allocation cannot exceed capacity.
- Project detail and role screens use real API data.

## 5. Phase 3 — SOW and MSA

- SOW create/edit/send/review/accept/reject.
- Role allocations and commercial terms.
- MSA requests, versioned documents, decisions, and status.
- Audit trail and notifications.

Acceptance:
- Parties can only see authorized SOW data.
- Rejections preserve reasons/history.
- Capacity constraints remain valid.
- MSA status is applied consistently.

## 6. Phase 4 — Contracts

- Contract creation from valid SOW allocation.
- Contract lifecycle and acceptance.
- Line items and billing rules.
- Versioning, amendments, termination, expiry.
- Multi-hop relationships and approval chains.

Acceptance:
- Accepted contract terms cannot be silently overwritten.
- Contract status transitions are enforced.
- Each contract is traceable to its originating project/SOW.
- Permissions and audit history work.

## 7. Phase 5 — WORK and timesheets

- Work entries and timesheets.
- Submission and multi-stage approval.
- Rejection and resubmission.
- Locking and revisions.
- Leave workflow.
- Reviewed document import.

Acceptance:
- Timesheets are tied to valid contracts and roles.
- Approval chain is enforced.
- Locked/approved records are not silently edited.
- AI extraction cannot auto-approve or bypass user review.

## 8. Phase 6 — Invoices and billing

- Invoice generation from approved work and eligible contract line items.
- Fixed, recurring, usage, and milestone billing where specified.
- Invoice review/submission/approval/rejection.
- Duplicate-generation prevention.
- MSA-required draft handling.
- Partial payment allocation.

Acceptance:
- Calculations are server-side and use precise monetary types.
- Source work/line items are traceable.
- Duplicate billing is prevented.
- Outstanding balances are consistent.

## 9. Phase 7 — Payments and reconciliation

- Bank account connection and verification.
- Provider transaction synchronization.
- Payment processor integration if money movement is required.
- Invoice matching and reconciliation.
- Partial/failed payments and audit trails.

Acceptance:
- Webhooks are verified and idempotent.
- Bank transaction detection is distinct from payment confirmation.
- Ambiguous matches require review.
- Tokens and credentials remain server-side.

## 10. Phase 8 — Social and AI

- Feed, connections, messaging, and notifications.
- AI summaries, extraction, risk findings, search, and recommendations.
- AI source references and feedback where appropriate.

Acceptance:
- AI uses only authorized context.
- High-impact actions require human confirmation.
- AI failures do not corrupt official records.
- Social and messaging permissions are tested.

## 11. Phase 9 — Hardening

- RLS/RBAC regression suite.
- API and UI test suites.
- End-to-end tests.
- Load and query performance tests.
- Accessibility and responsive checks.
- Error monitoring and operational documentation.
- Backup, migration, rollback/recovery, and release readiness review.

## 12. Definition of release readiness

- No known critical authorization or tenant-isolation defects.
- Migrations apply in order to an isolated environment.
- Core end-to-end flow passes.
- Financial totals and payment allocations reconcile.
- No fake data is used to claim acceptance.
- No secrets are committed.
- Pull requests are reviewed.
- Outstanding limitations are documented.

## Acceptance gates for unified workspace and ownership
Before feature rollout, implement and verify: (1) one signed-in app shell with Feed as home and persistent navigation; (2) personal record creation without a company; (3) company actions initiated from Business after selecting an authorized company; (4) visible selected-company identity in relevant downstream flows; (5) backend-enforced ownership and membership checks independent of UI; (6) no separate Individual/Company workspace mode; (7) ownership-aware migrations and indexes; and (8) automated cross-user/cross-company isolation tests. Do not mark the work complete merely because the selector or UI exists.

