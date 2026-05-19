---
icon: square-user
---

Understand how resources are isolated by account today and what to expect from
upcoming RBAC enhancements.

> **Success**
>
> **When to use this guide:** You manage multiple tenants or environments and need to enforce isolation while planning for future RBAC.
>
> **Who benefits:** Platform administrators, PMs handling customer onboarding, and compliance teams auditing access.

## Current Behavior

_When to use:_ Review how isolation works today before making architectural decisions.

| Topic         | Details                                                                            |
| ------------- | ---------------------------------------------------------------------------------- |
| Account scope | Every agent, tool, MCP, and schedule is associated with a single account ID.       |
| API keys      | A regular API key only sees and manages resources for its account.                 |
| Master key    | Platform operators can list or modify any account using the master key.            |
| Soft delete   | Deleting a resource keeps it within the originating account.                       |
| Auditing      | Run history endpoints respect account scope; master key can audit across accounts. |

## Working Across Accounts

_When to use:_ Share resources safely or perform admin tasks between tenants.

- **Standard usage**: one API key per tenant environment (development, staging,
  production) keeps resources separated automatically.
- **Promoting configurations**: export from one account and import into another
  using the [Configuration management guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/configuration-management).
- **Operations access**: master key holders can create, list, or revoke accounts
  and keys via internal integrations. REST documentation is reference-only:
  [REST API reference](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/rest-api).

### Common isolation issues

| Symptom                                       | Likely cause                                             | Fix                                                                                       |
| --------------------------------------------- | -------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Resources appear across accounts unexpectedly | API key uses master scope.                               | Issue account-scoped keys and rotate credentials that should not have master permissions. |
| CLI refuses cross-account updates             | Selected account differs from resource owner.            | Switch API keys or use dedicated service accounts per tenant.                             |
| Audit trail incomplete                        | Manual updates performed via master key without logging. | Run exports before/after changes and store them centrally.                                |

## Preparing for RBAC

_When to use:_ Plan migrations or communicate timelines to stakeholders.

Future releases introduce roles (Creator, Runner, Viewer) and delegated API keys
with scoped permissions. Plan ahead by:

1. Tracking which teams need read vs. write access.
1. Storing owner metadata on agents/tools (`metadata` fields) to ease migration.
1. Auditing automation scripts to ensure they use least-privilege keys once
   available.

## Operational Tips

_When to use:_ Keep daily account management predictable and auditable.

- Rotate account keys regularly and revoke unused keys promptly.
- Keep a secure record of master key usage; restrict it to platform operators.
- When troubleshooting cross-account issues, verify that the API key matches the
  expected tenant before escalating.

## Related Documentation

- [Security & privacy](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/security-and-privacy) — key hygiene and PII controls.
- [Configuration management](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/configuration-management) — promote resources
  between accounts safely.
- [REST API reference](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/rest-api) — account endpoints and master-key
  operations.
