# MyTrakin Security Requirements

## 1. Threat model priorities

Prioritize:
- Cross-company/tenant data leakage.
- Broken object-level authorization.
- Privilege escalation through company roles.
- Sensitive document exposure.
- Financial state manipulation.
- Duplicate payment/webhook processing.
- Token/secret exposure.
- Unsafe file upload and document parsing.
- Prompt injection through uploaded documents or retrieved content.
- Abuse of search, messaging, and public endpoints.

## 2. Authentication and sessions

- Use the existing approved identity provider and secure session lifecycle.
- Verify tokens/sessions server-side.
- Support refresh and revocation according to the auth provider.
- Do not create never-expiring access tokens.
- Protect password reset and email verification flows.
- Rate-limit sensitive authentication endpoints where appropriate.

## 3. Authorization

- Enforce server-side resource authorization on every protected operation.
- Combine company-scoped roles with resource-level access.
- Apply RLS as a database layer.
- Never trust client-provided company IDs, owner IDs, roles, status values, or financial totals.
- Test direct-ID access and cross-tenant attacks.

## 4. Secrets and configuration

- Keep service-role keys, database credentials, AI keys, Plaid secrets, and payment-provider secrets server-side.
- Use managed environment secrets.
- Never commit `.env` files containing secrets.
- Keep a safe `.env.example` with placeholders only.
- Scan repository history and CI output for accidental secret leakage.
- Rotate any credential found in source control.

## 5. Sensitive data and documents

- Mask tax identifiers by default.
- Restrict access to W-9, bank, contract, invoice, and identity documents.
- Use private storage, short-lived signed URLs, file size/type limits, and malware scanning where available.
- Treat uploaded files and extracted text as untrusted.
- Do not include sensitive data in URLs, logs, analytics, or AI prompts unless strictly necessary and approved.
- Define retention and deletion policies.

## 6. Financial integrity

- Calculate monetary values on the server.
- Use numeric/decimal representations and explicit rounding rules.
- Use idempotency and transaction-safe operations.
- Verify payment-provider webhooks according to current provider requirements.
- Keep invoice, payment, bank transaction, and reconciliation states distinct.
- Never accept a browser claim as proof of payment.

## 7. AI security

- Treat document contents and retrieved text as untrusted input.
- Do not allow prompt content to override system authorization or business rules.
- Enforce tenant authorization before retrieval and before returning AI results.
- Avoid cross-tenant embedding/retrieval leakage.
- Require human confirmation for consequential actions.
- Log source references and decisions without storing unnecessary sensitive prompt data.
- Handle model output as untrusted and validate it before use.

## 8. Operational security

- Use TLS for network traffic.
- Apply least privilege to application and database roles.
- Keep dependencies updated and scan for known vulnerabilities.
- Rate-limit expensive operations.
- Add monitoring for repeated authorization failures and suspicious payment activity.
- Avoid returning stack traces or internal SQL details to clients.
- Document backup and recovery procedures.

## 9. Release blockers

Do not release with:
- Critical cross-tenant access defects.
- Public access to private financial/legal documents.
- Exposed production secrets.
- Unauthenticated or unverified payment webhooks.
- Ability to mark invoices paid through untrusted client input.
- Broken RLS on sensitive tables.
- Unreviewed destructive migrations.
