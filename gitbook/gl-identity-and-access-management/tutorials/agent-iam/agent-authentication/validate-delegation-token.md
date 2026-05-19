---
icon: badge-check
---

# Validate Delegation Token

Validate delegation tokens in receiving services using a minimal, lightweight gateway.

{% hint style="info" %}
**When to use**: When a service receives a request from an agent and needs to verify the delegation token before processing it.
{% endhint %}

<details>

<summary>Prerequisites</summary>

* Completed [Delegate to Agent](delegate-to-agent.md)
* `gl-iam[postgresql]` installed

</details>

## 5-Line Core

```python
from gl_iam import IAMGateway
from gl_iam.providers.postgresql import PostgreSQLAgentProvider, PostgreSQLConfig

provider = PostgreSQLAgentProvider(PostgreSQLConfig(database_url="postgresql+asyncpg://user:pass@localhost/mydb", secret_key="your-secret-key-min-32-chars-long!", default_org_id="default"))
gateway = IAMGateway.for_agent_auth(agent_provider=provider, secret_key="your-secret-key-min-32-chars-long!")
result = await gateway.validate_delegation_token(token="eyJhbGciOi...")
delegation = result.unwrap()  # DelegationToken with chain, scope, task
```

{% hint style="warning" %}
**Stateless validation**: `validate_delegation_token` only checks the JWT signature and expiry. It does **not** check whether the agent has been suspended or revoked. For real-time status checks, query the agent provider directly.
{% endhint %}

## Cross-Service Validation Architecture

Delegation tokens are stateless JWTs — the receiving service only needs the shared `secret_key` to validate, with no network call back to the issuing service.

<figure><img src="../../../../.gitbook/assets/Mermaid Chart - Create complex, visual diagrams with text.-2026-03-03-045513.png" alt=""><figcaption></figcaption></figure>

## Step-by-Step

{% stepper %}
{% step %}
**Setup Receiving Service Gateway**

Use `IAMGateway.for_agent_auth()` — a minimal gateway that only needs an agent provider and the shared `secret_key`. This enables cross-service token validation without requiring access to the full user database:

```python
from gl_iam import IAMGateway
from gl_iam.providers.postgresql import PostgreSQLAgentProvider, PostgreSQLConfig

config = PostgreSQLConfig(
    database_url="postgresql+asyncpg://user:pass@localhost/mydb",
    secret_key="your-secret-key-min-32-chars-long!",
    default_org_id="default",
)
provider = PostgreSQLAgentProvider(config)
gateway = IAMGateway.for_agent_auth(agent_provider=provider, secret_key="your-secret-key-min-32-chars-long!")
```

{% hint style="info" %}
The `secret_key` must match the key used by the service that created the delegation token. This is how cross-service validation works — shared secret, no network call.
{% endhint %}
{% endstep %}

{% step %}
**Validate Token**

```python
result = await gateway.validate_delegation_token(token=delegation_token_string)

if result.is_ok:
    delegation = result.unwrap()
    print("Token is valid!")
else:
    print(f"Validation failed: {result.error.message}")
```
{% endstep %}

{% step %}
**Inspect the Delegation**

After validation, inspect the chain, scope, and task:

```python
delegation = result.unwrap()

# Who initiated this delegation chain?
print(f"Root principal: {delegation.chain.root_principal.principal_id}")
print(f"Root type: {delegation.chain.root_principal.principal_type}")

# What scopes were granted?
print(f"Scopes: {delegation.scope.scopes}")
print(f"Budget: {delegation.scope.max_actions}")
print(f"Constraints: {delegation.scope.resource_constraints}")

# What task is this for?
print(f"Task ID: {delegation.task.id}")
print(f"Task purpose: {delegation.task.purpose}")

# Full chain
print(f"Chain depth: {delegation.chain.depth}")
for i, link in enumerate(delegation.chain.links):
    print(f"  [{i}] {link.principal_type}: {link.principal_id}")
```

```
Root principal: user:alice
Root type: PrincipalType.USER
Scopes: ['docs:read']
Budget: 50
Constraints: {'department': 'finance'}
Task ID: task-001
Task purpose: Review Q1 financial documents
Chain depth: 2
  [0] PrincipalType.USER: user:alice
  [1] PrincipalType.AGENT: agent:doc-reviewer
```
{% endstep %}

{% step %}
**Enforce Authorization**

Validation confirms the token is authentic — your service must still enforce authorization:

```python
# Example: check if the agent has the required scope
required_scope = "docs:read"
if required_scope not in delegation.scope.scopes:
    raise PermissionError(f"Agent lacks required scope: {required_scope}")

# Example: check resource constraints
if "department" in delegation.scope.resource_constraints:
    allowed_dept = delegation.scope.resource_constraints["department"]
    if requested_department != allowed_dept:
        raise PermissionError(f"Agent restricted to department: {allowed_dept}")

# Proceed with the request
print("Authorization passed, processing request...")
```
{% endstep %}
{% endstepper %}

{% hint style="success" %}
You've validated a delegation token and enforced authorization! Your service can now safely process agent requests.
{% endhint %}

## Complete Example

Create `validate_delegation_token.py`:

```python
"""Validate a delegation token in a receiving service."""

import asyncio

from gl_iam import IAMGateway
from gl_iam.providers.postgresql import PostgreSQLAgentProvider, PostgreSQLConfig


async def main():
    # Simulating a receiving service that gets a delegation token
    delegation_token = "eyJhbGciOi..."  # Token received from the agent

    config = PostgreSQLConfig(
        database_url="postgresql+asyncpg://user:pass@localhost/mydb",
        secret_key="your-secret-key-min-32-chars-long!",
        default_org_id="default",
    )
    provider = PostgreSQLAgentProvider(config)
    gateway = IAMGateway.for_agent_auth(agent_provider=provider, secret_key="your-secret-key-min-32-chars-long!")

    result = await gateway.validate_delegation_token(token=delegation_token)

    if result.is_ok:
        delegation = result.unwrap()
        print(f"Valid! Root: {delegation.chain.root_principal.principal_id}")
        print(f"Scopes: {delegation.scope.scopes}")
        print(f"Task: {delegation.task.purpose}")
        print(f"Chain depth: {delegation.chain.depth}")
    else:
        print(f"Invalid: {result.error.message}")


if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
uv run validate_delegation_token.py
```

Expected output:

```
Valid! Root: user:alice
Scopes: ['docs:read']
Task: Review Q1 financial documents
Chain depth: 2
```

## Common Pitfalls

| Pitfall                              | Solution                                                                                               |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------ |
| Different `secret_key`               | The validating service must use the same `secret_key` as the issuing service                           |
| Token expired                        | Check `delegation.expires_at` — tokens have a finite lifetime set by `expires_in_seconds`              |
| Token tampered                       | JWT signature verification will fail — the `Result` will contain the error                             |
| Not checking scopes after validation | Validation only proves authenticity. You must still check `delegation.scope.scopes` for authorization. |
| Assuming suspension is checked       | Stateless validation does not check agent status. Query the provider for real-time checks.             |

## Next Steps

* [Delegation Chain](delegation-chain.md) — Understand multi-hop chains in validated tokens
* [Scope & Budget](scope-and-budget.md) — Learn how to enforce scope and budget constraints

***

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url\&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Fagent-authentication%2Fvalidate-delegation-token).
{% endhint %}
