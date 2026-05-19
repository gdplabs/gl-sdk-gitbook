---
icon: share-nodes
---

# Delegate to Agent

Create a delegation token that grants limited authority from a user (or another agent) to an agent.

{% hint style="info" %}
**When to use**: When a human user wants an AI agent to act on their behalf with specific, bounded permissions.
{% endhint %}

<details>

<summary>Prerequisites</summary>

* Completed [Register Agent](register-agent.md)
* Completed [Login](../../traditional-iam/user-authentication/login.md) (user authentication)
* `gl-iam[postgresql]` installed

</details>

## Delegation Flow

<figure><img src="../../../../.gitbook/assets/Mermaid Chart - Create complex, visual diagrams with text.-2026-03-03-044549.png" alt=""><figcaption></figcaption></figure>

## 5-Line Core

```python
from gl_iam import TaskContext, DelegationScope

task = TaskContext(id="task-001", purpose="Review Q1 documents")
scope = DelegationScope(scopes=["docs:read"], max_actions=50, expires_in_seconds=1800)
result = await gateway.delegate_to_agent(principal_token=auth_token.access_token, agent_id="agent:doc-reviewer", task=task, scope=scope)
delegation = result.unwrap()  # DelegationToken
```

## Step-by-Step

{% stepper %}
{% step %}
**Setup Gateway with Full Provider**

Delegation requires both user authentication (to verify the user token) and agent support. Use a full provider with agent support:

```python
from gl_iam import IAMGateway
from gl_iam.providers.postgresql import PostgreSQLProvider, PostgreSQLAgentProvider, PostgreSQLConfig

config = PostgreSQLConfig(
    database_url="postgresql+asyncpg://user:pass@localhost/mydb",
    secret_key="your-secret-key-min-32-chars-long!",
    default_org_id="default",
)
provider = PostgreSQLProvider(config)
agent_provider = PostgreSQLAgentProvider(config)

gateway = IAMGateway(
    auth_provider=provider,
    user_store=provider,
    session_provider=provider,
    organization_provider=provider,
    agent_provider=agent_provider,
    secret_key="your-secret-key-min-32-chars-long!",
)
```
{% endstep %}

{% step %}
**Authenticate the User**

The delegating user must have a valid token:

```python
from gl_iam.core.types import PasswordCredentials

auth_result = await gateway.authenticate(
    credentials=PasswordCredentials(email="alice@example.com", password="secure-password"),
    organization_id="default",
)
user, auth_token = auth_result.unwrap()
```
{% endstep %}

{% step %}
**Create TaskContext**

Every delegation is tied to a specific task — this provides auditability:

```python
from gl_iam import TaskContext

task = TaskContext(
    id="task-001",
    purpose="Review Q1 financial documents",
    data_sensitivity="standard",
    metadata={"department": "finance", "quarter": "Q1-2026"},
)
```
{% endstep %}

{% step %}
**Define DelegationScope**

Specify exactly what the agent can do:

```python
from gl_iam import DelegationScope

scope = DelegationScope(
    scopes=["docs:read", "docs:summarize"],
    resource_constraints={"department": "finance"},
    max_actions=50,
    expires_in_seconds=1800,  # 30 minutes
)
```
{% endstep %}

{% step %}
**Create Delegation Token**

```python
result = await gateway.delegate_to_agent(
    principal_token=auth_token.access_token,
    agent_id="agent:doc-reviewer",
    task=task,
    scope=scope,
)
delegation = result.unwrap()

print(f"Token: {delegation.token[:50]}...")
print(f"Agent: {delegation.agent_id}")
print(f"Scopes: {delegation.scope.scopes}")
print(f"Budget: {delegation.scope.max_actions}")
print(f"Expires: {delegation.expires_at}")
print(f"Task: {delegation.task.purpose}")
print(f"Chain depth: {delegation.chain.depth}")
```

```
Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjaGFpbi...
Agent: agent:doc-reviewer
Scopes: ['docs:read', 'docs:summarize']
Budget: 50
Expires: 2026-03-03 15:30:00+00:00
Task: Review Q1 financial documents
Chain depth: 2
```
{% endstep %}
{% endstepper %}

{% hint style="success" %}
You've delegated authority to an agent! The agent can now use this token to act on Alice's behalf within the defined scope.
{% endhint %}

## Complete Example

Create `delegate_to_agent.py`:

```python
"""Delegate authority from a user to an agent."""

import asyncio

from gl_iam import (
    IAMGateway,
    AgentRegistration,
    AgentType,
    DelegationScope,
    TaskContext,
)
from gl_iam.core.types import PasswordCredentials
from gl_iam.providers.postgresql import PostgreSQLProvider, PostgreSQLAgentProvider, PostgreSQLConfig


async def main():
    config = PostgreSQLConfig(
        database_url="postgresql+asyncpg://user:pass@localhost/mydb",
        secret_key="your-secret-key-min-32-chars-long!",
        default_org_id="default",
    )
    provider = PostgreSQLProvider(config)
    agent_provider = PostgreSQLAgentProvider(config)

    gateway = IAMGateway(
        auth_provider=provider,
        user_store=provider,
        session_provider=provider,
        organization_provider=provider,
        agent_provider=agent_provider,
        secret_key="your-secret-key-min-32-chars-long!",
    )

    # Register an agent
    reg_result = await gateway.register_agent(AgentRegistration(
        name="doc-reviewer",
        agent_type=AgentType.WORKER,
        owner_user_id="user:alice",
        operator_org_id="default",
        allowed_scopes=["docs:read", "docs:summarize"],
    ))
    agent = reg_result.unwrap()
    print(f"Registered: {agent.id}")

    # Authenticate the user
    auth_result = await gateway.authenticate(
        credentials=PasswordCredentials(email="alice@example.com", password="secure-password"),
        organization_id="default",
    )
    user, token = auth_result.unwrap()

    # Delegate to agent
    task = TaskContext(id="task-001", purpose="Review Q1 financial documents")
    scope = DelegationScope(
        scopes=["docs:read"],
        max_actions=50,
        expires_in_seconds=1800,
    )

    result = await gateway.delegate_to_agent(
        principal_token=token.access_token,
        agent_id=agent.id,
        task=task,
        scope=scope,
    )
    delegation = result.unwrap()

    print(f"Token: {delegation.token[:50]}...")
    print(f"Scopes: {delegation.scope.scopes}")
    print(f"Budget: {delegation.scope.max_actions}")
    print(f"Chain depth: {delegation.chain.depth}")


if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
uv run delegate_to_agent.py
```

Expected output:

```
Registered: agent:doc-reviewer
Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjaGFpbi...
Scopes: ['docs:read']
Budget: 50
Chain depth: 2
```

## Common Pitfalls

| Pitfall                    | Solution                                                          |
| -------------------------- | ----------------------------------------------------------------- |
| Expired user token         | The delegating user's token must be valid. Refresh if needed.     |
| Scope escalation           | Requested scopes must be a subset of the agent's `allowed_scopes` |
| Missing `task.id`          | Every delegation requires a `TaskContext` with a unique `id`      |
| Agent suspended/revoked    | Only `ACTIVE` agents can receive delegations                      |
| No `secret_key` on gateway | The gateway needs `secret_key` to sign delegation JWTs            |

## Next Steps

* [Validate Delegation Token](validate-delegation-token.md) — Validate tokens in receiving services
* [Delegation Chain](delegation-chain.md) — Build multi-hop delegation chains
* [Scope & Budget](scope-and-budget.md) — Fine-tune scope attenuation and action budgets

***

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url\&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Fagent-authentication%2Fdelegate-to-agent).
{% endhint %}
