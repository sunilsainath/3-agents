# MyTrakin UI Design System

## 1. Design direction

Create a modern, trustworthy enterprise SaaS interface that feels professional and distinctive. Preferred palette direction:
- Light blue for primary actions and informational emphasis.
- Light green for positive/success states.
- Light grey/neutral surfaces for structure.
- Additional colors used sparingly and consistently.

Avoid relying on black/white alone or using purple as the dominant brand color. Do not sacrifice contrast or accessibility to achieve a color preference.

## 2. Layout

- Consistent authenticated application shell.
- Clear sidebar hierarchy and active navigation.
- Global header with search, notifications, messaging, and profile controls where applicable.
- Company context selector where the user is authorized to switch company context.
- Breadcrumbs on nested project/SOW/contract/invoice pages.
- Responsive behavior for smaller screens.

## 3. Navigation baseline

```text
WORK
  Overview
  My Contracts
  Timesheets
  Leave
  Payments

BUSINESS
  Dashboard
  Posts
  Partners
    MSA Connections
    Active MSAs
    Requests
  Roles
  Employees
  Documents

CODE
  Overview
  Projects
  SOW
  Contracts
  Invoices

PAYMENTS
  Dashboard
  Accounts
  Accounts Receivable
  Accounts Payable
  Transactions
  Reconciliation
  Payment Requests
  Scheduled / Recurring
  Settings

AI
  Assistant
  Search
  Document Analysis
  Insights
```

Inspect the existing product and preserve established navigation if already implemented. Profile, settings, and logout may live in the account menu.

## 4. Shared components

Create reusable patterns for:
- Page headers and breadcrumbs.
- Tables with server-side sorting/filtering/pagination.
- Search fields and filter panels.
- Status badges with accessible labels.
- Form fields and validation messages.
- Date/currency/amount display.
- Confirm dialogs.
- Side panels/detail drawers.
- File upload and document preview.
- Approval timelines.
- Audit/activity timelines.
- Empty/loading/error states.
- Permission-denied screens.
- Toasts and inline success/error messages.

## 5. Status presentation

Use one consistent label/color mapping for each entity lifecycle. Do not rely on color alone; include text and, where helpful, icons.

Never let a UI dropdown expose arbitrary state transitions. Render actions that the user is authorized to perform, while relying on the backend for final authorization and transition validation.

## 6. Core screens

### Project
Overview, roles/capacity, SOWs, contracts, timesheets, invoices, documents, activity, AI insights.

### SOW
Parties, project, role allocation, commercial terms, documents/version, approval/decision history.

### Contract
Overview, parties, project/SOW, role, terms, billing, timesheets, invoices, payments, documents, approvals, activity, AI insights.

### Invoice
Direction, issuer/recipient, billing period, due date, line items, subtotal/tax/total, paid amount, outstanding balance, status, source traceability, approvals, payment history, reconciliation.

### Timesheet
Calendar/list, time entry, contract/role selection, period summary, submit, approval chain, revision history.

### Payment/reconciliation
Bank account status, transaction list, matched/unmatched items, match rationale, review action, payment history, partial balances, provider connection errors.

## 7. UX requirements

Every screen needs appropriate:
- Loading/skeleton state.
- Empty state with a relevant next action.
- Error state with retry where appropriate.
- Field validation and accessible error text.
- Confirmation for destructive/consequential actions.
- Keyboard and screen-reader support.
- Mobile/tablet behavior.
- Clear disabled and permission-denied states.

Do not display fake success. A successful toast must follow a successful API response.

## 8. Data and security

- Use API data, not hard-coded production claims.
- Mock fixtures are permitted only for isolated development.
- Mask sensitive tax/bank data.
- Never put secrets in client code.
- Do not expose company membership lists or confidential commercial data without permission.
- Respect profile field visibility.
- Never treat UI visibility as authorization.

## Unified workspace and company selection UX (authoritative)
Use one app shell and one navigation system. Feed is the home page. Do not show a global Individual-vs-Company workspace mode or require users to switch workspaces. Personal actions are available in their relevant modules. For company work, the user opens Business and selects a company from a list of companies they are authorized to access; company profile actions then lead into the relevant workflows. Show a persistent, unmistakable company name/identity in company-specific screens and forms, with a clear route back to Business to change company. Before saving, confirm the target company where ambiguity could cause a costly mistake. Never suggest that selecting a company gives blanket access; render permission-denied and unavailable states correctly.

