# MyTrakin Business Rules

## 1. Core principle

Project, SOW, contract, timesheet, invoice, and payment are separate entities. Each has its own lifecycle, permissions, history, and source of truth.

## 2. Company and project access

- Users may belong to multiple companies.
- A user's role is scoped to a specific company.
- Company membership alone does not imply access to every company project, contract, invoice, or document.
- Individual projects are owned by an individual under the agreed product rules.
- Creating/managing company projects requires the relevant company permission.
- Company lists and memberships must not be exposed to other users without authorization.

## 3. Projects and project roles

Project fields include category (individual/company), type (service/lending/blue collar), name, description, start date, estimated end date, estimated time, estimated budget, currency, owner, and status.

Project statuses may include:
- `DRAFT`
- `ACTIVE`
- `ON_HOLD`
- `COMPLETED`
- `CANCELLED`
- `CLOSED`

Only valid transitions may be performed.

A project role has a required quantity. SOW allocations and downstream assignments must not exceed capacity. Capacity checks must be server-side and concurrency-safe.

Display required, allocated, and available quantities, with a clear definition of which allocation states count against capacity.

## 4. SOW

An SOW is the commercial allocation/agreement layer between a project and a party. A project can have multiple SOWs. SOWs may be company-to-company or company-to-individual if allowed by the final legal/business model.

SOW terms may include:
- Parties
- Project
- Role/quantity allocations
- Rate and currency
- Billing basis and frequency
- Start/end dates
- Payment and invoice terms
- Special conditions
- Supporting/signed documents
- Version history

Potential statuses:
- `DRAFT`
- `SENT`
- `PENDING_ACCEPTANCE`
- `ACTIVE`
- `REJECTED`
- `EXPIRED`
- `TERMINATED`
- `CLOSED`

Acceptance/rejection must be explicit and audited. Rejection captures the actor, timestamp, and reason/notes. Rejected SOWs remain in history.

## 5. Contracts

Contracts represent actual binding engagements/assignments and should normally originate from valid SOW allocations. Any exceptional standalone contract type must be explicitly approved and modeled.

Contract types include company-to-company and company-to-individual. Multi-hop relationships are supported: Company A → Company B → Company D → individual. Each commercial link has its own contract, terms, approvals, and invoice relationship.

Potential statuses:
- `DRAFT`
- `SENT`
- `PENDING_ACCEPTANCE`
- `ACCEPTED`
- `ACTIVE`
- `DECLINED`
- `EXPIRED`
- `TERMINATED`
- `CLOSED`

The backend enforces valid transitions. Recipients can accept or decline contracts. Declines capture reason/notes. Accepted terms must be versioned; amendments do not silently overwrite prior accepted terms.

Contract details may include parties, project, SOW, role, resource, dates, rate, currency, billing basis/frequency, payment terms, timesheet rules, approval chain, line items, documents, and special terms.

## 6. Contract line items and billing

Line items may be primary charges, additional charges, commissions, vendors, expenses, or other approved categories.

Supported billing bases may include:
- `TIMESHEET`
- `FIXED`
- `RECURRING`
- `USAGE`
- `MILESTONE`

Supported frequencies may include weekly, biweekly, monthly, quarterly, and custom schedules.

Not every line item requires timesheets. Billing behavior must be determined by its configured basis and contract terms.

All calculations are performed server-side using precise monetary representations and explicit currency/rounding rules.

## 7. Timesheets and work

Work is tied to a valid contract and role. Contract terms determine rates, billable rules, and approval configuration.

Timesheet states may include:
- `DRAFT`
- `SUBMITTED`
- `UNDER_REVIEW`
- `APPROVED`
- `LOCKED`
- `REJECTED` or a resubmission state as established by the implementation.

Approval chains can be multi-stage. Example: worker → downstream company manager → upstream company manager.

Each stage records reviewer, decision, timestamp, and notes. Rejected work returns for correction and resubmission. Preserve revisions and audit history. Approved/locked work cannot be silently altered.

Timesheet imports can accept supported document formats, extract candidate dates/hours/descriptions, map them to a contract/role, and present a review screen. Ambiguous dates or low-confidence values require confirmation. AI never writes unreviewed extraction directly into official work records and never auto-approves.

## 8. MSA policy

MSA status and document verification are separate from SOW/contract existence.

The intended rule is:
- A valid project/SOW/contract may be created without an active MSA where policy allows.
- If an invoice requires an MSA and none is active, invoice generation may occur but the invoice must remain a draft and be clearly flagged `MSA_REQUIRED`; it must not be submitted to the counterparty until the requirement is satisfied.
- Do not silently bypass MSA policy.
- If a stricter company policy blocks SOWs/contracts without an MSA, that policy must be explicit and permission-controlled.

Potential MSA states include requested, submitted, under review, active, rejected, expired, and terminated. Preserve versions and decision notes.

## 9. Invoices

Invoices can be payable or receivable from the relevant company's perspective.

- Receivable: money owed to the company.
- Payable: money the company owes another party.

Generate invoices from approved timesheets and/or eligible contract line items according to the billing basis.

Potential statuses:
- `DRAFT`
- `PENDING`
- `SUBMITTED`
- `APPROVED`
- `PARTIALLY_PAID`
- `PAID`
- `OVERDUE`
- `REJECTED`
- `DISPUTED`
- `CANCELLED`
- `REFUNDED`

The implementation must define and enforce valid transitions. Do not let generic update operations arbitrarily set invoice statuses.

Prevent duplicate invoice generation for the same billing source/period unless an explicit adjustment/revision process is used.

Invoice line items must be traceable to their source contract terms, approved work, fixed charge, usage, or milestone.

## 10. Payments and reconciliation

Support payment history, partial payments, failed payments, due dates, payment references, and outstanding balances.

Example: a 10,000 invoice with 6,000 allocated is `PARTIALLY_PAID` with 4,000 outstanding. When the remaining 4,000 is allocated, the invoice becomes `PAID`, subject to any required settlement/confirmation policy.

Distinguish:
- Payment requested
- Payment initiated
- Processor-confirmed
- Bank transaction detected
- Reconciliation pending
- Reconciled/confirmed

Plaid bank connectivity and transaction data can assist verification/reconciliation but do not, by themselves, move money. Actual movement requires a supported processor or payment service.

Transaction matches should consider amount, currency, date, account, counterparty, reference, and relationship. Amount equality alone is insufficient. Ambiguous matches require human review.

## 11. Audit and notifications

Keep an auditable record of significant changes and decisions. Notify relevant authorized parties about SOW/contract requests and decisions, expiring contracts, timesheet decisions, invoice events, and payment/reconciliation events.

Notifications must not disclose confidential data to unauthorized recipients.

## 12. AI behavior

AI may summarize, extract, compare, flag anomalies, recommend actions, and answer questions over authorized data.

AI must not independently:
- Accept or terminate a contract.
- Approve timesheets.
- Approve/submit invoices.
- Mark invoices paid without verified business logic.
- Change permissions or company ownership.
- Bypass MSA requirements.
- Expose data outside the user's access scope.

High-impact AI findings should show supporting source references and allow user review.

## Unified workspace and action initiation (authoritative)
- Every signed-in user operates in one unified workspace with Feed as home and access to all modules. Module navigation is not gated by company job title or role.
- Users may create personal records wherever the resource rules permit, without creating or selecting a company.
- To act on behalf of a company, the user opens Business, selects an authorized company, and initiates the action in that company's profile/context. Relevant downstream screens may retain the selected company context, but must show it clearly and permit an authorized switch.
- A company selection is not an authorization grant. The backend checks membership, role, resource-level access and business prerequisites for every action.
- Personal and company records are separate ownership scopes. Never silently convert an existing personal record to company-owned or vice versa. Ownership changes, where allowed, require a dedicated authorized workflow, validation, audit history and safe handling of dependent records.
- Contracts, SOWs, timesheets, invoices, payments and documents must retain consistent ownership/party relationships. A user's ability to open a module does not permit bypassing approval, contract, MSA, invoice or payment rules.

