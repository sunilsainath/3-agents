# MyTrakin Conceptual Data Model

## 1. Purpose

This is a conceptual baseline, not a migration script. The database agent must inspect existing tables and migrations, map current entities, and propose an implementation-specific schema before adding or changing tables.

Use internal UUID/UUIDv7 identifiers where compatible with the current database. Public IDs are separate immutable display identifiers.

## 2. Identifier conventions

| Entity | Public ID example |
|---|---|
| User | `UXXXXXXXX` |
| Company | `COXXXXXXXX` |
| Project | `PXXXXXXXX` |
| Project role | `RXXXXXXXX` |
| SOW | `SXXXXXXXX` |
| Contract | `CXXXXXXXX` |
| Invoice | `IXXXXXXXX` |

IDs must be generated server-side and protected by unique constraints. Do not use sequential IDs as public identifiers. Exact format and length must be finalized with the existing implementation.

## 3. Conceptual entities

### Identity and organization
- `users/profiles`: authenticated identity and public profile fields.
- `companies`: organization profile and verification status.
- `company_memberships`: user-to-company membership and membership status.
- `company_roles`: company-specific roles.
- `role_permissions`: granular permissions assigned to a company role.
- `user_role_assignments`: company membership to company-specific role assignments.
- `profile_visibility_settings`: visibility by profile section/field where supported.

A person can belong to multiple companies and have different roles in each.

### Social
- `connections`: requester, recipient, status, timestamps.
- `posts`: author user or company, content, visibility, timestamps.
- `messages/conversations`: participants, message content, read state, attachment references.
- `notifications`: recipient, type, related entity, read state.
- Additional comments/reactions may be modeled if required by existing product scope.

### Business and documents
- `company_documents`: company, document type, private storage reference, version, uploader, status.
- `msas`: parties, status, effective dates, expiration, current version.
- `msa_versions`: document reference, version number, signer/review metadata.
- `msa_requests`: requesting party, recipient party, decision and notes.
- `audit_events`: actor, tenant context, action, entity type/id, timestamp, request/correlation ID, safe state metadata.

Do not store raw files as database blobs unless there is a documented reason. Store private object-storage references and metadata.

### Projects and roles
- `projects`: owner type (individual/company), owner reference, name, description, category/type, dates, budget, currency, status.
- `project_members/access_grants`: explicit project-level access where needed.
- `project_roles`: project, role name, required quantity, role attributes, status.
- `role_allocations`: project role, SOW, party, quantity and allocation status.

Role capacity must be enforced transactionally. Define whether reserved, active, cancelled, and completed allocations consume capacity.

### SOW
- `sows`: project, parties, SOW type, dates, commercial terms, status, current version.
- `sow_versions`: immutable snapshots or version records for sent/accepted commercial content.
- `sow_role_allocations`: SOW, project role, quantity, rate, currency, billing basis and frequency.
- `sow_documents`: versioned private document references.

An SOW is a commercial agreement/allocation layer. It is not an invoice.

### Contracts
- `contracts`: public ID, originating SOW, project, parties, contract type, role, assigned resource, dates, status, terms, currency.
- `contract_versions`: immutable accepted/sent snapshots and amendments.
- `contract_line_items`: description, recipient, amount/rate, currency, billing basis, frequency, dates, tax metadata if supported.
- `contract_approval_steps`: configured reviewer, sequence, state, timestamps and notes.
- `contract_relationships`: optional explicit parent/child or upstream/downstream links for multi-hop contracting, with carefully defined access.

An accepted contract's terms must not be silently overwritten.

### WORK
- `work_entries`: user, contract, project role, date, start/end/break or duration, description, source, status.
- `timesheets`: user, contract, period, submission status, revision/version.
- `timesheet_approval_steps`: sequence, approver, decision, comments, timestamps.
- `leave_requests`: user, relevant company/contract policy, dates, type, status and approval data.
- `timesheet_imports`: uploaded file reference, extraction status, confidence/review metadata, confirmed result reference.

A confirmed work entry must reference a valid contract and role. AI extraction must not directly approve or publish unreviewed timesheets.

### Invoices and payments
- `invoices`: public ID, issuer, recipient, direction/context, contract, SOW/project references where applicable, billing period, issue/due dates, currency, status.
- `invoice_line_items`: source contract line item or approved work references, description, quantity, unit rate, subtotal, tax and total.
- `invoice_adjustments`: credit/debit adjustments and references, if supported.
- `payments`: invoice allocation, amount, currency, method/provider, status, timestamps and reference.
- `payment_accounts`: company/user owner, provider identifiers, institution, masked account data, connection/verification state.
- `bank_transactions`: normalized provider transaction ID, account, amount, currency, date, description/counterparty fields, sync state.
- `payment_matches`: transaction/invoice relationship, match type/confidence, reviewer, timestamps and audit references.
- `idempotency_records/provider_events`: deduplication of requests and webhook events.

A bank transaction may need to match one or more payment allocations, depending on supported business rules. Define allocation and partial-payment rules explicitly before implementation.

### AI
- `ai_jobs`: task type, requesting user/tenant, status, model/provider metadata, safe error state.
- `document_extractions`: document reference, extracted fields, confidence, review state and source/page references.
- `ai_findings`: entity reference, finding type, severity, evidence/source reference, model metadata, reviewed state.
- `ai_feedback`: user feedback on AI outputs, where product requirements justify it.

Avoid storing unnecessary prompts containing sensitive data. Apply retention, redaction, and access control to AI records.

## 4. Relationship rules

- A project can have many project roles.
- A project can have many SOWs.
- A SOW belongs to a project and has explicit parties.
- A SOW can allocate quantities against one or more project roles.
- Contracts are created from valid SOW allocations under the agreed business rules.
- An individual engagement should have a traceable contract record even when commercial setup begins with a company-to-individual SOW.
- A contract can have multiple line items and approval steps.
- Work entries/timesheets reference the relevant contract and role.
- An invoice references its billing sources and must be traceable to the relevant contract/SOW/project.
- Payments reduce outstanding invoice balances through explicit allocations.
- Bank transactions and invoice matches are separate from invoice records.
- Every cross-company access path must be explicitly authorized.

## 5. Data constraints to evaluate

- Unique public IDs.
- Foreign keys for all critical relationships.
- Positive role capacity and allocation quantities.
- No total allocations beyond role capacity, enforced with transaction-safe logic.
- Valid date ranges.
- Valid currency codes.
- Unique invoice generation key for a contract/period/source combination where appropriate.
- Provider transaction and webhook idempotency.
- Unique approval step sequence per workflow instance.
- Appropriate uniqueness for company memberships and role assignments.
- Immutable or versioned accepted legal/commercial documents.

## 6. Financial data

Use PostgreSQL `numeric/decimal` types or an established money representation. Do not use binary floating point for money. Define rounding rules, currency precision, tax treatment, and currency conversion policy before implementation. Never assume every currency has two decimal places.

## 7. Migration rules

- Inspect the current schema first.
- Add new migrations; do not rewrite already-applied migration history.
- Use expand-and-contract for breaking changes.
- Backfill existing data before enforcing new non-null constraints where needed.
- Test migration ordering and RLS.
- Never run destructive migrations against production autonomously.
