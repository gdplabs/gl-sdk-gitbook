---
icon: link-horizontal
---

# Delegation Chain

Build delegation chains where agents sub-delegate authority to other agents, with scope narrowing at each hop.

{% hint style="info" %}
**When to use**: When an orchestrator agent needs to delegate specific sub-tasks to specialized worker agents.
{% endhint %}

<details>

<summary>Prerequisites</summary>

* Completed [Delegate to Agent](delegate-to-agent.md)
* Completed [Validate Delegation Token](validate-delegation-token.md)
* `gl-iam[postgresql]` installed

</details>

## 5-Line Core

```python
worker_scope = DelegationScope(scopes=["docs:read"], max_actions=10, expires_in_seconds=600)
result = await gateway.delegate_to_agent(
    principal_token=orchestrator_delegation_token,  # delegation JWT, not user JWT
    agent_id="agent:summarizer", task=task, scope=worker_scope,
)
worker_token = result.unwrap()
print(f"Chain depth: {worker_token.chain.depth}")  # 3 (user -> orchestrator -> worker)
```

## How Chains Work

<figure><img src="../../../../.gitbook/assets/Mermaid Chart - Create complex, visual diagrams with text.-2026-03-03-050135.png" alt=""><figcaption></figcaption></figure>

Each hop **attenuates** (narrows) the scope. The worker can never exceed the orchestrator's permissions, and the orchestrator can never exceed the user's permissions.

## Chain Properties

| Property                   | Description                                                                  |
| -------------------------- | ---------------------------------------------------------------------------- |
| `chain.depth`              | Number of principals in the chain (e.g., 3 for user → orchestrator → worker) |
| `chain.root_principal`     | First link — always the originating user or API key                          |
| `chain.leaf_principal`     | Last link — the current agent holding the token                              |
| `chain.links`              | Ordered list of `DelegationLink` objects                                     |
| `chain.effective_scopes()` | Intersection of all scopes across the chain                                  |
| `chain.task_id`            | Task ID shared across the entire chain                                       |
| `chain.max_depth`          | Maximum allowed chain depth (default: 5)                                     |

## Step-by-Step

{% stepper %}
{% step %}
**Register Orchestrator and Worker**

```python
from gl_iam import IAMGateway, AgentRegistration, AgentType
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

# Register orchestrator
orch = (await gateway.register_agent(AgentRegistration(
    name="doc-orchestrator",
    agent_type=AgentType.ORCHESTRATOR,
    owner_user_id="user:alice",
    operator_org_id="default",
    max_delegation_depth=3,
    allowed_scopes=["docs:read", "docs:summarize", "docs:translate"],
))).unwrap()

# Register worker
worker = (await gateway.register_agent(AgentRegistration(
    name="summarizer",
    agent_type=AgentType.WORKER,
    owner_user_id="user:alice",
    operator_org_id="default",
    allowed_scopes=["docs:read", "docs:summarize"],
))).unwrap()

print(f"Orchestrator: {orch.id}")
print(f"Worker: {worker.id}")
```
{% endstep %}

{% step %}
**User Delegates to Orchestrator**

```python
from gl_iam.core.types import PasswordCredentials
from gl_iam import TaskContext, DelegationScope

# Authenticate user
user, token = (await gateway.authenticate(
    credentials=PasswordCredentials(email="alice@example.com", password="secure-password"),
    organization_id="default",
)).unwrap()

# Create delegation
task = TaskContext(id="task-review-q1", purpose="Review and summarize Q1 documents")
orch_scope = DelegationScope(
    scopes=["docs:read", "docs:summarize"],
    max_actions=100,
    expires_in_seconds=3600,
)

orch_delegation = (await gateway.delegate_to_agent(
    principal_token=token.access_token,
    agent_id=orch.id,
    task=task,
    scope=orch_scope,
)).unwrap()

print(f"Orchestrator chain depth: {orch_delegation.chain.depth}")  # 2
```
{% endstep %}

{% step %}
**Orchestrator Sub-Delegates to Worker**

The orchestrator uses its **delegation token** (not a user token) to sub-delegate:

```python
worker_scope = DelegationScope(
    scopes=["docs:read"],       # Narrower than orchestrator's scopes
    max_actions=10,              # Smaller budget
    expires_in_seconds=600,      # Shorter lifetime
)

worker_delegation = (await gateway.delegate_to_agent(
    principal_token=orch_delegation.token,  # Delegation token, not user token
    agent_id=worker.id,
    task=task,                               # Same task context
    scope=worker_scope,
)).unwrap()

print(f"Worker chain depth: {worker_delegation.chain.depth}")  # 3
```
{% endstep %}

{% step %}
**Inspect the Chain**

Walk the delegation chain to see all principals:

```python
chain = worker_delegation.chain

print(f"Chain depth: {chain.depth}")
print(f"Root: {chain.root_principal.principal_id} ({chain.root_principal.principal_type})")
print(f"Leaf: {chain.leaf_principal.principal_id} ({chain.leaf_principal.principal_type})")
print(f"Effective scopes: {chain.effective_scopes()}")
print(f"Task ID: {chain.task_id}")

print("\nFull chain:")
for i, link in enumerate(chain.links):
    print(f"  [{i}] {link.principal_type}: {link.principal_id}")
    print(f"       Scopes: {link.scope.scopes}")
    print(f"       Budget: {link.scope.max_actions}")
```

```
Chain depth: 3
Root: user:alice (PrincipalType.USER)
Leaf: agent:summarizer (PrincipalType.AGENT)
Effective scopes: {'docs:read'}
Task ID: task-review-q1

Full chain:
  [0] PrincipalType.USER: user:alice
       Scopes: ['docs:read', 'docs:summarize']
       Budget: 100
  [1] PrincipalType.AGENT: agent:doc-orchestrator
       Scopes: ['docs:read', 'docs:summarize']
       Budget: 100
  [2] PrincipalType.AGENT: agent:summarizer
       Scopes: ['docs:read']
       Budget: 10
```
{% endstep %}

{% step %}
**Validate on Worker Service**

A separate service receiving the worker's token can validate and inspect the full chain:

```python
# On the receiving service — only needs for_agent_auth
worker_gateway = IAMGateway.for_agent_auth(
    agent_provider=PostgreSQLAgentProvider(config),
    secret_key="your-secret-key-min-32-chars-long!",
)

result = await worker_gateway.validate_delegation_token(token=worker_delegation.token)
delegation = result.unwrap()

print(f"Root: {delegation.chain.root_principal.principal_id}")
print(f"Effective scopes: {delegation.chain.effective_scopes()}")
```
{% endstep %}
{% endstepper %}

{% hint style="success" %}
You've built a multi-hop delegation chain! The worker agent operates with the intersection of all scopes in the chain.
{% endhint %}

## Cross-Service Delegation

In production, delegation often spans multiple services. The pattern is simple: **share the `secret_key`**.

<figure><img src="../../../../.gitbook/assets/Mermaid Chart - Create complex, visual diagrams with text.-2026-03-03-050358.png" alt=""><figcaption></figcaption></figure>

Service B needs only `for_agent_auth()` — no user database, no session store, just the agent provider and the shared secret.

## Depth Limits

Chains have two depth controls:

| Control                | Set On              | Description                                                                        |
| ---------------------- | ------------------- | ---------------------------------------------------------------------------------- |
| `max_delegation_depth` | `AgentRegistration` | Per-agent limit (default: 3). The agent cannot appear in a chain deeper than this. |
| `max_depth`            | `DelegationChain`   | Per-chain limit (default: 5). The entire chain cannot exceed this depth.           |

When either limit is exceeded, delegation fails with a `DELEGATION_DEPTH_EXCEEDED` error.

## Complete Example

Create `delegation_chain.py`:

```python
"""Build a multi-hop delegation chain: User -> Orchestrator -> Worker."""

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
        name="doc-orchestrator",
        agent_type=AgentType.ORCHESTRATOR,
        owner_user_id="user:alice",
        operator_org_id="default",
        allowed_scopes=["docs:read", "docs:summarize"],
    ))).unwrap()

    worker = (await gateway.register_agent(AgentRegistration(
        name="summarizer",
        agent_type=AgentType.WORKER,
        owner_user_id="user:alice",
        operator_org_id="default",
        allowed_scopes=["docs:read", "docs:summarize"],
    ))).unwrap()

    # User authenticates and delegates to orchestrator
    user, token = (await gateway.authenticate(
        credentials=PasswordCredentials(email="alice@example.com", password="secure-password"),
        organization_id="default",
    )).unwrap()

    task = TaskContext(id="task-review-q1", purpose="Review and summarize Q1 documents")

    orch_delegation = (await gateway.delegate_to_agent(
        principal_token=token.access_token,
        agent_id=orch.id,
        task=task,
        scope=DelegationScope(scopes=["docs:read", "docs:summarize"], max_actions=100, expires_in_seconds=3600),
    )).unwrap()

    # Orchestrator sub-delegates to worker
    worker_delegation = (await gateway.delegate_to_agent(
        principal_token=orch_delegation.token,
        agent_id=worker.id,
        task=task,
        scope=DelegationScope(scopes=["docs:read"], max_actions=10, expires_in_seconds=600),
    )).unwrap()

    # Inspect chain
    chain = worker_delegation.chain
    print(f"Chain depth: {chain.depth}")
    print(f"Effective scopes: {chain.effective_scopes()}")
    for i, link in enumerate(chain.links):
        print(f"  [{i}] {link.principal_type}: {link.principal_id} (scopes: {link.scope.scopes})")


if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
uv run delegation_chain.py
```

Expected output:

```
Chain depth: 3
Effective scopes: {'docs:read'}
  [0] PrincipalType.USER: user:alice (scopes: ['docs:read', 'docs:summarize'])
  [1] PrincipalType.AGENT: agent:doc-orchestrator (scopes: ['docs:read', 'docs:summarize'])
  [2] PrincipalType.AGENT: agent:summarizer (scopes: ['docs:read'])
```

## Common Pitfalls

| Pitfall                             | Solution                                                                    |
| ----------------------------------- | --------------------------------------------------------------------------- |
| Depth exceeded                      | Increase `max_delegation_depth` on the agent or `max_depth` on the chain    |
| Task ID mismatch                    | All hops in a chain must use the same `TaskContext.id`                      |
| Scope escalation in chain           | Each sub-delegation must use a subset of the parent's scopes                |
| Using user token for sub-delegation | Orchestrator must use its **delegation token**, not the original user token |

## Next Steps

* [Scope & Budget](scope-and-budget.md) — Deep dive into scope attenuation and action budgets
* [Agent Lifecycle](agent-lifecycle.md) — Manage agent status across chains

***

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url\&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Fagent-authentication%2Fdelegation-chain).
{% endhint %}
