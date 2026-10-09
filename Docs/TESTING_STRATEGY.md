# MyTrakin Testing Strategy

## 1. Test layers

- Static checks: lint, type checks, formatting, dependency/security scans where configured.
- Unit tests: business calculations, state transitions, validation, permission helpers.
- Database tests: migrations, constraints, RLS, transactions, idempotency.
- API integration tests: authentication, authorization, request/response contracts.
- Frontend tests: rendering, form behavior, loading/error/empty states.
- End-to-end tests: complete user workflows.
- Performance tests: representative query/data volumes and concurrency.
- Security tests: tenant isolation, direct-ID access, role escalation, document access.

## 2. Test environments

Use isolated test databases and synthetic data. Never run test suites that can alter production data. Do not use live financial credentials or real bank account details in automated tests.

## 3. Required security matrix

Test at least:
- User A in Company A cannot access Company B private data.
- Company member without project permission cannot access that project.
- A user with different roles in two companies gets only the active company's permissions.
- User cannot change a request's company ID to access another tenant.
- Private documents cannot be downloaded without resource authorization.
- AI retrieval/search cannot return unauthorized content.
- Client cannot forge approval, acceptance, payment, or owner fields.
- RLS remains effective for direct database API access where applicable.

## 4. Required business tests

### Projects and allocation
- Create individual project.
- Create company project with proper permission.
- Create project roles.
- Allocate within capacity.
- Reject over-capacity allocation.
- Concurrent requests cannot oversubscribe capacity.

### SOW and contracts
- Create and send SOW.
- Accept and reject SOW.
- Preserve rejection notes.
- Create contract from valid allocation.
- Accept/decline contract.
- Prevent invalid state transitions.
- Amend accepted contract without destroying prior version.
- Terminate contract with reason and effective date.

### Timesheets
- Create work entry for valid contract and role.
- Reject work for invalid/expired contract as specified by policy.
- Submit and approve through configured steps.
- Reject and resubmit while preserving revisions.
- Prevent unauthorized approval.
- Prevent silent changes to locked records.
- Require user review of imported timesheet extraction.

### Invoices and payments
- Generate invoice from approved billing sources.
- Verify line-item provenance and totals.
- Prevent duplicate invoice generation.
- Keep invoice in draft when MSA is required but absent.
- Record partial payment and calculate outstanding amount.
- Allocate remaining payment and update status correctly.
- Deduplicate provider webhook events.
- Require review of ambiguous bank transaction matches.
- Prevent forged `PAID` status.

## 5. Core end-to-end test

1. User signs in.
2. Authorized user creates a company project.
3. User creates a project role with a defined capacity.
4. User creates and sends an SOW.
5. Counterparty accepts the SOW.
6. Contract is created from a valid allocation.
7. Authorized counterparty accepts the contract.
8. Worker submits timesheet entries tied to that contract and role.
9. Configured reviewers approve the timesheet.
10. Backend generates an invoice from eligible billing sources.
11. Invoice follows the required MSA and approval policy.
12. Invoice is submitted to the counterparty.
13. Payment is recorded or verified using the supported payment workflow.
14. Transaction is reconciled where applicable.
15. Invoice outstanding balance and status are verified.
16. Audit events and permissions are verified at every step.

## 6. Multi-hop test

Test Company A → Company B → Company D → individual.

Verify each link has its own authorized SOW/contract/terms/approval and invoice relationships. Confirm that no party can see another party's confidential terms without explicit authorization.

## 7. Performance tests

Use representative synthetic data. Measure:
- Query plans and latency for project, contract, timesheet, invoice, and transaction lists.
- Pagination under realistic row counts.
- RLS query performance.
- Concurrent role allocation.
- Invoice generation throughput and lock contention.
- Webhook deduplication and background processing.
- Resource use and error rates.

Do not claim a scale target is met without measured evidence.

## 8. Test reporting

For each release candidate, report:
- Test command.
- Environment.
- Pass/fail result.
- Failed cases and severity.
- Known coverage gaps.
- Performance measurements where applicable.
- Security issues and remediation status.

## Required unified workspace / ownership tests
- New user lands on Feed and sees all module navigation without role-based module gating.
- User can create a supported personal record without creating or selecting a company.
- User can open Business, select a company they belong to, and start a company-owned workflow.
- Company context is clearly displayed downstream and changing it cannot leak prior-company data.
- User cannot read/write/export/download/search/AI-retrieve another user's personal data or an unauthorized company's data by changing IDs or request payloads.
- Membership in Company A never authorizes Company B; membership removal blocks company access but preserves the user's personal records.
- API, RLS and background-job tests enforce the same ownership rules; UI-only tests are insufficient.
- Resource creation rejects ambiguous ownership (both personal and company owner set, or neither set where one is required).

