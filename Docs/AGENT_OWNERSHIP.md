# Agent Ownership and Git Workflow

## 1. Agents

### Agent 1 — Frontend
Branch: `feature/frontend-ui`

Owns:
- Pages, components, styles, navigation, client-side validation and UI states.
- Frontend API client and typed UI integration within agreed contracts.
- Frontend unit/component tests and UI documentation.

Must not independently:
- Change database schema or migrations.
- Implement privileged business rules only in the frontend.
- Redefine shared API contracts.

### Agent 2 — Backend
Branch: `feature/backend-logic`

Owns:
- API routes/controllers, services, business rules, server-side validation.
- Integrations, background-job orchestration, audit events and backend tests.
- API/OpenAPI implementation within agreed contracts.

Must not independently:
- Edit migration history or redefine shared schema.
- Bypass RLS or replace the permission model.
- Expose provider secrets to the client.

### Agent 3 — Database
Branch: `feature/database-performance`

Owns:
- Schema, new migrations, SQL functions/triggers where approved.
- RLS policies, constraints, indexes, database tests, query-plan review.
- Schema documentation and migration notes.

Must not independently:
- Make destructive production changes.
- Create duplicate domain entities without schema review.
- Rewrite applied migration history.

## 2. Shared ownership

The following require cross-agent review:
- Shared types and enums.
- Entity names and relationship changes.
- API request/response fields.
- Authentication and authorization assumptions.
- Status transitions.
- Invoice/payment semantics.
- Shared environment and build configuration.
- Any breaking migration or API change.

The integration owner maintains authoritative shared documents and decides conflicts.

## 3. Branching

Suggested branches:
- `main`: approved stable release.
- `develop` or a designated integration branch: reviewed integration.
- One feature branch per agent.

Use pull requests. Do not allow agents to independently merge their own changes to `main`.

## 4. Pull request checklist

Every pull request must include:
- Summary and scope.
- Files changed.
- Business rules implemented.
- API/schema changes.
- Migration order and compatibility notes.
- Tests run and exact results.
- Security/RLS implications.
- Dependencies on other agents.
- Known limitations and rollback/recovery notes.

## 5. Shared database policy

Branches do not isolate a shared database. Use isolated local/dev databases where possible. Only the integration owner or approved release process should apply integrated migrations to a shared environment. Never run destructive migrations against production autonomously.

## 6. Conflict resolution

When a conflict appears:
1. Stop changes to the contested contract/file.
2. Explain the conflict and its impact.
3. Propose a compatible solution.
4. Obtain integration-owner approval.
5. Update the relevant shared documentation.
6. Implement and test the approved change.

## 7. Completion report

At each milestone, each agent reports:
- Completed work.
- Files changed.
- Tests and results.
- Schema/API changes.
- Dependencies/blockers.
- Known risks.
- Next steps.

## Shared product contract: unified workspace
All agents must implement the same model: one unified workspace and app shell, Feed home, no Individual/Company workspace switch. The frontend owns the Business company-selection experience and visible context indicators; the backend owns authorization and business-rule enforcement; the database agent owns explicit ownership constraints, foreign keys, indexes and RLS. Company actions start from Business after selecting an authorized company, but company selection must never substitute for backend checks. Before merging, agents must agree on field names and API contract for owner context.

