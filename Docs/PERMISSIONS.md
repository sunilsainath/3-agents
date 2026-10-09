# MyTrakin Permissions and Tenant Isolation

## 1. Security model

Use layered authorization:
1. Authentication establishes identity.
2. Application RBAC and resource-level authorization decide whether an action is permitted.
3. PostgreSQL RLS restricts database access as an independent protection layer.
4. Private storage policies and short-lived signed URLs protect files.
5. Audit logging records consequential actions.

Hiding a button or route in the UI is not authorization.

## 2. Company-scoped roles

A user can belong to multiple companies and have different roles in each company. Resolve permissions using the active company context and verified membership. Never apply a role assignment from Company A to authorize actions in Company B.

The company creator is intended to become the initial Super Admin, subject to the existing onboarding rules. Only authorized company administrators can manage company roles and permissions.

## 3. Example granular permissions

### Company
- `company.read`
- `company.update`
- `company.members.read`
- `company.members.manage`
- `company.roles.read`
- `company.roles.manage`
- `company.documents.read`
- `company.documents.upload`
- `company.documents.delete`

### Projects
- `projects.read`
- `projects.create`
- `projects.update`
- `projects.close`
- `projects.manage_roles`
- `projects.manage_access`

### SOW
- `sow.read`
- `sow.create`
- `sow.update`
- `sow.send`
- `sow.accept`
- `sow.reject`
- `sow.close`

### Contracts
- `contracts.read`
- `contracts.create`
- `contracts.update_draft`
- `contracts.send`
- `contracts.accept`
- `contracts.reject`
- `contracts.amend`
- `contracts.renew`
- `contracts.terminate`
- `contracts.close`

### WORK
- `timesheets.read_own`
- `timesheets.read_team`
- `timesheets.create`
- `timesheets.submit`
- `timesheets.review`
- `timesheets.approve`
- `timesheets.reject`
- `leave.read_own`
- `leave.manage_team`

### Invoices and payments
- `invoices.read`
- `invoices.create`
- `invoices.submit`
- `invoices.approve`
- `invoices.reject`
- `invoices.dispute`
- `invoices.cancel`
- `payments.read`
- `payments.initiate`
- `payments.allocate`
- `payments.reconcile`
- `bank_accounts.manage`

### AI
- `ai.use`
- `ai.analyze_documents`
- `ai.view_financial_insights`
- `ai.execute_approved_action` only if such an action system is explicitly implemented.

Permission names are a starting vocabulary. The implementation should consolidate with existing permissions and avoid duplicates.

## 4. Resource-level access

Permissions must be combined with resource relationships. A user with `contracts.read` does not automatically have access to every contract across every company.

For cross-company records, grant access only to the fields/actions required for that party's relationship. Avoid leaking upstream/downstream commercial terms that a party is not entitled to see.

## 5. RLS requirements

- Enable RLS on all tables that expose user- or company-owned sensitive data through client-accessible database APIs.
- Write policies for select/insert/update/delete according to the intended role and resource relationship.
- Ensure insert/update policies prevent changing tenant/owner references to escape scope.
- Review security-definer functions, function search paths, grants, and service-role usage.
- Test with multiple users, multiple companies, multiple roles, and unauthorized direct-ID access.
- Do not use broad policies such as “any authenticated user can read all rows” for private records.
- Do not disable RLS to make application code work.
- Do not assume server-side service-role credentials enforce user-specific access automatically; explicitly authorize operations before privileged queries.

## 6. Sensitive data

Treat tax identifiers, W-9 files, bank identifiers, provider tokens, financial documents, and authentication tokens as sensitive.

- Mask tax identifiers in UI by default.
- Do not put sensitive values in URLs, analytics, exception messages, or ordinary logs.
- Keep provider secrets server-side.
- Use encryption and managed secrets appropriate to the environment.
- Restrict access to sensitive document fields and files.
- Use private storage and short-lived signed URLs.
- Audit access to particularly sensitive records.
- Store only the minimum bank/provider data required.
- Apply documented retention and deletion policies.

## 7. File authorization

A user must be authorized to access the underlying company/project/SOW/contract/invoice before receiving a signed download URL. Signed URLs must expire and must not be treated as permanent public access. Avoid publicly readable buckets for confidential documents.

## 8. Segregation of duties

Where configured, prevent users from approving their own financial or operational actions. Keep creator, submitter, reviewer, approver, and payer identities distinct in audit records.

## 9. Required negative tests

- User in Company A cannot access Company B private project by changing an ID.
- Company member without project access cannot read that project.
- User cannot read another party's private contract terms.
- User cannot update a record's company/owner reference to gain access.
- Unauthorized user cannot access private W-9/MSA/contract/invoice documents.
- User cannot approve a timesheet or invoice without the required permission and workflow step.
- AI search and analysis cannot return unauthorized tenant data.
- Client cannot mark an invoice paid by changing a request payload.
