# MyTrakin Decisions and Open Questions

## 1. Purpose

Track decisions that affect multiple agents. Do not silently guess a missing business rule or replace a repository decision with a preferred design. The integration owner updates this file and the relevant specification after a decision is made.

## 2. Initial working assumptions to verify

These are current product-direction assumptions and must be checked against the existing repository:

- Supabase/PostgreSQL is the intended database.
- Company isolation is enforced with application authorization plus RLS.
- The sidebar modules include BUSINESS, CODE, WORK, PAYMENTS, and AI.
- CODE contains Projects, SOW, Contracts, and Invoices.
- The core chain is Project → SOW → Contract → Timesheet/Line Items → Invoice → Payment.
- Public IDs are distinct from internal UUIDs.
- An accepted contract is versioned rather than silently overwritten.
- AI extraction requires user review before official records are created.
- An absent active MSA may allow invoice generation but requires a draft `MSA_REQUIRED` state before submission, subject to explicit company policy.
- Plaid is used for bank connectivity/transaction verification where supported; money movement requires a separate supported payment service if needed.

## 3. Decisions required before production

Record each decision with: ID, question, options, decision, rationale, owner, date, affected docs, migration/API impact.

### D-001: Existing stack
What frontend/backend framework and deployment architecture already exist? Preserve existing choices unless an approved change is justified.

### D-002: Project role capacity
Exactly which allocation states consume capacity: reserved, pending SOW, active SOW, active contract, terminated, completed? Avoid double-counting SOW allocations and contracts.

### D-003: SOW-to-contract cardinality
Can one SOW create many contracts? Can one contract reference multiple SOWs? Recommended baseline: many contracts per SOW; each ordinary contract references one originating SOW, unless a validated business case requires otherwise.

### D-004: Company-to-individual SOW
Is an individual SOW a commercial document that automatically creates one or more actual contract records? Define who signs and which entity is the counterparty.

### D-005: MSA enforcement
Is an active MSA required to create an SOW, activate a contract, submit an invoice, or only for certain company relationships? The current baseline permits project/SOW/contract creation where policy allows, while invoices remain draft with `MSA_REQUIRED` if an active MSA is required but missing.

### D-006: Invoice approval
Who approves invoices, and is approval required before submission, before payment, or both? Define segregation-of-duties requirements.

### D-007: Invoice uniqueness
Define the idempotency key and rules for re-invoicing, corrections, credit notes, partial periods, and amendments.

### D-008: Payment provider
Which countries, currencies, payment rails, and processors are required? Plaid product availability and payment processor capabilities must be verified before implementation.

### D-009: Tax calculation
Which tax jurisdictions and rules are in scope? Define whether tax is calculated internally or by an external tax service. Do not invent tax rules.

### D-010: Currency and rounding
Define supported currencies, decimal precision, rounding, exchange rates, and treatment of foreign-currency invoices/payments.

### D-011: Legal documents and e-signature
Is electronic signature required? If so, select the provider and define signature status, evidence, retention, and version locking.

### D-012: AI provider and data policy
Which AI providers may receive documents? Define sensitive-data redaction, region/residency, retention, opt-out, and source-citation expectations.

### D-013: Retention and deletion
Define retention for W-9s, tax identifiers, contracts, invoices, bank transactions, messages, AI outputs, and audit events.

### D-014: Messaging
Define whether messages require a connection, whether group conversations are supported, and rules for blocking/reporting/attachments.

### D-015: Ratings
Define who can rate whom, eligibility, evidence, moderation, disputes, visibility, and anti-manipulation controls before implementation.

### D-016: Performance objectives
Define measurable p50/p95/p99 latency, concurrency, data volume, uptime, and recovery objectives based on deployment and budget. Validate with load tests.

## 4. Decision log template

```text
Decision ID:
Question:
Options:
Decision:
Rationale:
Owner:
Date:
Affected documents:
Database impact:
API impact:
Migration/compatibility impact:
Tests required:
```

## 5. Change policy

When a decision changes:
1. Update this log.
2. Update the relevant architecture/data/API/business/security documents.
3. Identify required migrations and compatibility changes.
4. Notify all agents.
5. Do not merge incompatible implementations until aligned.
