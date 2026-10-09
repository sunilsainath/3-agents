# MyTrakin Agent Documentation Pack

This pack provides shared working specifications for three coding agents collaborating in one GitHub repository.

## Files

- `ARCHITECTURE.md` — system boundaries and technical principles.
- `DATA_MODEL.md` — conceptual entities and relationships.
- `API_CONTRACTS.md` — API conventions and initial resource contracts.
- `BUSINESS_RULES.md` — workflow rules from project creation through payment.
- `PERMISSIONS.md` — company isolation, RBAC, RLS, and sensitive-data rules.
- `IMPLEMENTATION_PLAN.md` — phased delivery and acceptance gates.
- `AGENT_OWNERSHIP.md` — branch strategy, file ownership, and coordination.
- `SECURITY.md` — security requirements and threat-focused checks.
- `TESTING_STRATEGY.md` — testing layers and end-to-end scenarios.
- `UI_DESIGN_SYSTEM.md` — UI direction, navigation, and UX standards.
- `INTEGRATIONS_AI_PAYMENTS.md` — AI, Plaid, bank reconciliation, and payment processor boundaries.
- `DECISIONS_AND_OPEN_QUESTIONS.md` — decisions that must be verified and unresolved questions.

## Important: these are baseline specifications

The agents must inspect the actual repository before implementing. These documents express the current intended product direction, not proof that the repository already uses any specific framework or has implemented these features.

If the existing repository conflicts with a recommendation here, do not silently rewrite working architecture. Document the conflict, propose a resolution, and get approval from the integration owner.

## Required workflow

1. All agents inspect the repository and report current architecture.
2. An integration owner confirms or updates these documents.
3. The database agent proposes the schema/migration plan.
4. The backend agent confirms API and business-rule feasibility.
5. The frontend agent maps screens to the agreed API contracts.
6. Agents implement on separate branches and open pull requests.
7. Merge only after integration, security, and end-to-end tests pass.

Do not put secrets, real W-9/TIN values, bank credentials, production data, or live API tokens in these files.

## Product rule: one unified workspace (authoritative)
MyTrakin has one workspace per signed-in user. Do not create separate Individual and Company workspaces, separate application shells, or a mandatory workspace switch. The Feed is the home page and all modules remain navigable. Users can create eligible personal records in the unified workspace. For company actions, the user enters **Business**, selects a company they are authorized to access, and starts company-related actions from that company's profile/context. This selection may be carried into relevant modules with a visible company indicator, but it never bypasses server authorization. Personal records and company-owned records remain distinct in the data model.

