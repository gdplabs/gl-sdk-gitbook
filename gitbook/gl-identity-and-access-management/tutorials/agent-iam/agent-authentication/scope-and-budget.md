---
icon: sliders
---

# Scope & Budget

Control what agents can do with scope narrowing, resource constraints, and action budgets.

{% hint style="info" %}
**When to use**: When you need fine-grained control over what an agent can access and how much it can do within a delegation.
{% endhint %}

<details>

<summary>Prerequisites</summary>

* Completed [Delegate to Agent](delegate-to-agent.md)
* Understanding of [Delegation Chain](delegation-chain.md)

</details>

## 5-Line Core

```python
from gl_iam import DelegationScope

scope = DelegationScope(
    scopes=["docs:read"],
    resource_constraints={"department": "engineering", "project_ids": ["proj-1", "proj-2"]},
    max_actions=50,
    expires_in_seconds=1800,
)
```

## The Attenuation Invariant

Every sub-delegation must be **equal to or narrower than** its parent. This is enforced automatically:

```
child.scopes       ⊆  parent.scopes
child.expiry       ≤  parent.expiry
child.max_actions  ≤  parent.max_actions
```

Attempting to widen any of these results in a `SCOPE_ESCALATION_DENIED` error.

<figure><img src="../../../../.gitbook/assets/Mermaid Chart - Create complex, visual diagrams with text.-2026-03-03-050728.png" alt=""><figcaption></figcaption></figure>

## DelegationScope Fields

| Field                  | Type             | Default      | Description                                     |
| ---------------------- | ---------------- | ------------ | ----------------------------------------------- |
| `scopes`               | `list[str]`      | _(required)_ | Permission strings the agent is granted         |
| `resource_constraints` | `dict[str, Any]` | `{}`         | Key-value constraints on accessible resources   |
| `max_actions`          | `int \| None`    | `None`       | Maximum number of actions the agent can perform |
| `expires_in_seconds`   | `int`            | `3600`       | How long the delegation token is valid          |

## Step-by-Step

{% stepper %}
{% step %}
**Scope Attenuation**

Scopes narrow at each hop in the delegation chain:

```python
from gl_iam import DelegationScope

# User delegates broad scopes to orchestrator
orch_scope = DelegationScope(
    scopes=["docs:read", "docs:write", "docs:delete"],
    max_actions=100,
    expires_in_seconds=3600,
)

# Orchestrator narrows scopes for worker — this succeeds
worker_scope = DelegationScope(
    scopes=["docs:read"],  # Subset of parent
    max_actions=10,
    expires_in_seconds=600,
)

# Attempting to escalate — this FAILS
bad_scope = DelegationScope(
    scopes=["docs:read", "admin:manage"],  # "admin:manage" not in parent!
    max_actions=10,
    expires_in_seconds=600,
)
# Result: Err(SCOPE_ESCALATION_DENIED)
```
{% endstep %}

{% step %}
**Action Budgets**

Action budgets limit how much work an agent can do. Each sub-delegation's budget must be less than or equal to the parent's:

```python
# Parent: 100 actions
parent_scope = DelegationScope(scopes=["docs:read"], max_actions=100, expires_in_seconds=3600)

# Child: 10 actions — OK (10 ≤ 100)
child_scope = DelegationScope(scopes=["docs:read"], max_actions=10, expires_in_seconds=600)

# Child: 200 actions — FAILS (200 > 100)
bad_scope = DelegationScope(scopes=["docs:read"], max_actions=200, expires_in_seconds=600)
# Result: Err(SCOPE_ESCALATION_DENIED)
```

{% hint style="warning" %}
**Budgets are declarative, not tracked.** GL IAM records the budget in the token but does not count actions. Your application must enforce action counting.
{% endhint %}
{% endstep %}

{% step %}
**Resource Constraints**

Resource constraints restrict which resources an agent can access:

```python
scope = DelegationScope(
    scopes=["docs:read"],
    resource_constraints={
        "department": "engineering",
        "project_ids": ["proj-1", "proj-2"],
        "classification": "internal",
    },
    max_actions=50,
    expires_in_seconds=1800,
)
```

After validation, the receiving service can enforce these constraints:

```python
delegation = (await gateway.validate_delegation_token(token=agent_token)).unwrap()

constraints = delegation.scope.resource_constraints
allowed_projects = constraints.get("project_ids", [])

if requested_project not in allowed_projects:
    raise PermissionError(f"Agent restricted to projects: {allowed_projects}")
```

{% hint style="info" %}
Resource constraints are **opaque to GL IAM** — the SDK stores them in the token but your application defines their meaning and enforces them.
{% endhint %}
{% endstep %}

{% step %}
**Error Handling**

Handle scope-related errors in delegation:

```python
result = await gateway.delegate_to_agent(
    principal_token=parent_token,
    agent_id="agent:worker",
    task=task,
    scope=escalated_scope,
)

if not result.is_ok:
    error = result.error
    print(f"Error: {error.code}")     # SCOPE_ESCALATION_DENIED
    print(f"Message: {error.message}")  # "Requested scope 'admin:manage' not in parent scopes"
```
{% endstep %}
{% endstepper %}

{% hint style="success" %}
You've learned how to control agent authority with scope attenuation, budgets, and resource constraints!
{% endhint %}

## Complete Example

Create `scope_and_budget.py`:

```python
"""Demonstrate scope attenuation and action budgets."""

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

    # Register agents
    orch = (await gateway.register_agent(AgentRegistration(
        name="scope-demo-orch",
        agent_type=AgentType.ORCHESTRATOR,
        owner_user_id="user:alice",
        operator_org_id="default",
        allowed_scopes=["docs:read", "docs:write", "docs:delete"],
    ))).unwrap()

    worker = (await gateway.register_agent(AgentRegistration(
        name="scope-demo-worker",
        agent_type=AgentType.WORKER,
        owner_user_id="user:alice",
        operator_org_id="default",
        allowed_scopes=["docs:read"],
    ))).unwrap()

    # User delegates to orchestrator
    user, token = (await gateway.authenticate(
        credentials=PasswordCredentials(email="alice@example.com", password="secure-password"),
        organization_id="default",
    )).unwrap()
    task = TaskContext(id="task-scope-demo", purpose="Demonstrate scope attenuation")

    orch_delegation = (await gateway.delegate_to_agent(
        principal_token=token.access_token,
        agent_id=orch.id,
        task=task,
        scope=DelegationScope(
            scopes=["docs:read", "docs:write"],
            max_actions=100,
            expires_in_seconds=3600,
        ),
    )).unwrap()
    print(f"Orchestrator scopes: {orch_delegation.scope.scopes}")
    print(f"Orchestrator budget: {orch_delegation.scope.max_actions}")

    # Orchestrator narrows scope for worker
    worker_delegation = (await gateway.delegate_to_agent(
        principal_token=orch_delegation.token,
        agent_id=worker.id,
        task=task,
        scope=DelegationScope(
            scopes=["docs:read"],
            resource_constraints={"department": "engineering"},
            max_actions=10,
            expires_in_seconds=600,
        ),
    )).unwrap()
    print(f"\nWorker scopes: {worker_delegation.scope.scopes}")
    print(f"Worker budget: {worker_delegation.scope.max_actions}")
    print(f"Worker constraints: {worker_delegation.scope.resource_constraints}")
    print(f"Effective scopes: {worker_delegation.chain.effective_scopes()}")

    # Attempt scope escalation — should fail
    bad_result = await gateway.delegate_to_agent(
        principal_token=orch_delegation.token,
        agent_id=worker.id,
        task=task,
        scope=DelegationScope(
            scopes=["docs:read", "admin:manage"],  # Escalation!
            max_actions=10,
            expires_in_seconds=600,
        ),
    )
    print(f"\nEscalation attempt: {bad_result.error.message}")


if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
uv run scope_and_budget.py
```

Expected output:

```
Orchestrator scopes: ['docs:read', 'docs:write']
Orchestrator budget: 100

Worker scopes: ['docs:read']
Worker budget: 10
Worker constraints: {'department': 'engineering'}
Effective scopes: {'docs:read'}

Escalation attempt: Requested scope 'admin:manage' not in parent scopes
```

## Common Pitfalls

| Pitfall                                     | Solution                                                                                                                 |
| ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| Budget doesn't track usage                  | GL IAM records the budget but does not count actions — your app must enforce this                                        |
| `expires_in_seconds=0`                      | A zero expiry creates an immediately-expired token. Use a positive value.                                                |
| Resource constraints not enforced by GL IAM | Constraints are stored in the token but your application must check them                                                 |
| Assuming wildcard behavior                  | `docs:*` does not automatically match `docs:read`. Scopes are exact string matches unless your app implements wildcards. |

## Next Steps

* [Agent Lifecycle](agent-lifecycle.md) — Suspend and revoke agents
* [Delegation Chain](delegation-chain.md) — See how scope attenuation works across chains

***

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url\&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Fagent-authentication%2Fscope-and-budget).
{% endhint %}
