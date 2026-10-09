# MyTrakin Integrations: AI, Plaid, and Payments

## 1. Integration principle

Use isolated service/adaptor layers for external providers. Domain logic must not depend on provider-specific payloads throughout the application. Keep secrets server-side and normalize provider data before using it in core workflows.

Inspect existing integrations before adding new providers.

## 2. AI capabilities

Useful contextual features include:
- W-9 and document field extraction with human review.
- SOW and contract summarization.
- Contract clause/risk detection with source section/page references.
- Comparison of contract versions or counterparty terms.
- Important date/deadline extraction.
- Project staffing, timeline, and budget risk insights.
- Invoice anomaly detection.
- Timesheet document extraction into a reviewable draft.
- Permission-aware natural-language search and questions.
- Drafting assistance for SOW/contract descriptions and communications.

AI outputs must include uncertainty and source evidence where possible. Treat AI findings as suggestions, not authoritative legal, tax, financial, or identity verification.

## 3. AI action limits

AI must not automatically:
- Approve timesheets or invoices.
- Accept, amend, or terminate contracts.
- Change company roles or permissions.
- Mark invoices paid.
- Bypass MSA rules.
- Publish extracted timesheets without user confirmation.
- Retrieve information the current user cannot otherwise access.

High-impact actions require explicit user confirmation and normal backend authorization.

## 4. Document extraction

Recommended workflow:
1. User uploads a file.
2. Backend validates file type, size, and authorization.
3. Store the original privately.
4. Scan for malware where available.
5. Extract text/OCR asynchronously.
6. Parse candidate fields and source locations.
7. Validate data and calculate confidence.
8. Present a review screen.
9. User confirms or edits.
10. Save official structured data with provenance and audit history.

Never allow document contents to instruct the AI to bypass permissions or execute tools.

## 5. Plaid boundary

Plaid may support:
- Bank account connection.
- Account/routing details where the product and region support them.
- Identity/account-holder matching where supported.
- Transaction synchronization and webhooks.

Plaid connectivity or Auth alone is not the same as a money-moving payment processor. If MyTrakin must initiate ACH or other payments, choose and integrate a supported processor/payment service for the relevant countries and transaction types.

Do not assume availability of any specific Plaid product or payment rail in every region. Verify provider support, compliance, account eligibility, and current API requirements before implementation.

## 6. Payment state distinctions

Keep these concepts separate:
- Payment request created.
- Payment initiated.
- Processor reports processing.
- Processor confirms completion/failure.
- Bank transaction detected.
- Transaction matched to invoice.
- Reconciliation confirmed.

Do not mark an invoice paid from an unverified client action or a same-amount bank transaction alone.

## 7. Reconciliation

Candidate matching factors:
- Currency and amount.
- Transaction date and invoice due/issue date.
- Counterparty and account.
- Payment reference/invoice number.
- Existing allocation state.
- Company/contract relationship.

Use confidence levels only as an aid. Define when auto-matching is permitted, and require human review for ambiguous cases. Preserve match decisions and reversals in an audit trail.

## 8. Webhooks and jobs

- Verify provider webhook signatures according to current provider documentation.
- Store/deduplicate provider event IDs.
- Make processing idempotent.
- Return successful webhook acknowledgments promptly after durable receipt where appropriate.
- Perform expensive sync, OCR, AI, and reconciliation work asynchronously.
- Retry transient errors with bounded backoff and dead-letter/error visibility.
- Never log provider secrets or raw sensitive payloads unnecessarily.

## 9. Provider configuration

Use environment variables/managed secrets with placeholder examples only. Document sandbox versus production setup, webhook URLs, required permissions, and provider-specific failure handling. Do not hard-code credentials or claim an integration is live without testing with approved sandbox credentials.
