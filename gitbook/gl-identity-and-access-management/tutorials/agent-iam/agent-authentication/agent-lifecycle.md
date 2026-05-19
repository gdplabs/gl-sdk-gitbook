---
icon: shield-halved
---

# Agent Lifecycle

Manage the agent lifecycle — suspend agents temporarily, revoke them permanently, and understand the kill switch behavior.

{% hint style="info" %}
**When to use**: When you need to disable an agent that is misbehaving, compromised, or no longer needed.
{% endhint %}

<details>

<summary>Prerequisites</summary>

* Completed [Register Agent](register-agent.md)
* Completed [Delegate to Agent](delegate-to-agent.md)

</details>

## 5-Line Core

```python
# Suspend (reversible)
await gateway.suspend_agent("agent:doc-reviewer", organization_id="default")

# Revoke (permanent kill switch)
await gateway.revoke_agent("agent:doc-reviewer", organization_id="default")
```

## Agent Status

| Status        | Can Delegate? | Can Reactivate?      | Existing Tokens Valid? |
| ------------- | ------------- | -------------------- | ---------------------- |
| **ACTIVE**    | Yes           | N/A                  | Yes                    |
| **SUSPENDED** | No            | Yes (provider-level) | Yes (until expiry)     |
| **REVOKED**   | No            | No (permanent)       | Yes (until expiry)     |

<figure><img src="../../../../.gitbook/assets/Mermaid Chart - Create complex, visual diagrams with text.-2026-03-03-050901.png" alt=""><figcaption></figcaption></figure>

{% hint style="warning" %}
**Stateless design**: Existing delegation tokens remain valid until they expire, even after suspension or revocation. Token validation only checks the JWT signature and expiry, not the agent's current status.
{% endhint %}

## Step-by-Step

{% stepper %}
{% step %}
**Suspend an Agent**

Suspension is **reversible** — use it when an agent needs temporary restriction:

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

result = await gateway.suspend_agent("agent:doc-reviewer", organization_id="default")
if result.is_ok:
    print("Agent suspended successfully")
```
{% endstep %}

{% step %}
**Attempt Delegation to Suspended Agent**

Delegating to a suspended agent fails immediately:

```python
from gl_iam import TaskContext, DelegationScope

result = await gateway.delegate_to_agent(
    principal_token=auth_token.access_token,
    agent_id="agent:doc-reviewer",
    task=TaskContext(id="task-002", purpose="Test delegation"),
    scope=DelegationScope(scopes=["docs:read"], expires_in_seconds=1800),
)

if not result.is_ok:
    print(f"Error: {result.error.code}")     # AGENT_SUSPENDED
    print(f"Message: {result.error.message}")
```

```
Error: AGENT_SUSPENDED
Message: Agent 'agent:doc-reviewer' is suspended and cannot receive delegations
```
{% endstep %}

{% step %}
**Reactivate an Agent**

Reactivation is done at the **provider level**, not through the gateway:

```python
# Direct provider call to reactivate
await provider.reactivate_agent("agent:doc-reviewer", organization_id="default")
print("Agent reactivated — can receive delegations again")
```

{% hint style="info" %}
Reactivation is intentionally not on the `IAMGateway` to require explicit provider-level access. This prevents accidental reactivation through the standard API.
{% endhint %}
{% endstep %}

{% step %}
**Revoke an Agent (Permanent)**

Revocation is the **kill switch** — permanent and irreversible:

```python
result = await gateway.revoke_agent("agent:doc-reviewer", organization_id="default")
if result.is_ok:
    print("Agent permanently revoked")
```

After revocation:

* No new delegations can be created
* The agent cannot be reactivated
* The `revoked_at` timestamp is recorded
{% endstep %}

{% step %}
**List Agents**

List agents in an organization, optionally including revoked ones:

```python
# Active agents only (default)
agents = await gateway.list_agents(organization_id="default")
print(f"Active agents: {len(agents)}")

# Include revoked agents
all_agents = await gateway.list_agents(organization_id="default", include_revoked=True)
print(f"All agents (including revoked): {len(all_agents)}")

# Filter by type
orchestrators = await gateway.list_agents(
    organization_id="default",
    agent_type=AgentType.ORCHESTRATOR,
)
print(f"Orchestrators: {len(orchestrators)}")

# Filter by owner
alice_agents = await gateway.list_agents(owner_user_id="user:alice")
for agent in alice_agents:
    print(f"  {agent.id}: {agent.status}")
```
{% endstep %}
{% endstepper %}

{% hint style="success" %}
You've learned how to manage the full agent lifecycle — suspend, reactivate, revoke, and list agents!
{% endhint %}

## Kill Switch Behavior

When you suspect an agent is compromised:

1. **Suspend immediately** — blocks all new delegations
2. **Investigate** — check audit logs, review delegation chains
3. **Revoke if confirmed** — permanent kill switch

```python
# Emergency response
await gateway.suspend_agent("agent:compromised-bot", organization_id="default")

# After investigation...
await gateway.revoke_agent("agent:compromised-bot", organization_id="default")
```

{% hint style="warning" %}
**Existing tokens remain valid** until they expire. If you need immediate invalidation, use short `expires_in_seconds` values in your delegation scopes as a best practice. For truly critical scenarios, rotate the `secret_key` to invalidate all tokens (this affects all agents and users).
{% endhint %}

## Complete Example

Create `agent_lifecycle.py`:

```python
"""Manage agent lifecycle: suspend, reactivate, revoke."""

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

    # Register agent
    agent = (await gateway.register_agent(AgentRegistration(
        name="lifecycle-demo",
        agent_type=AgentType.WORKER,
        owner_user_id="user:alice",
        operator_org_id="default",
        allowed_scopes=["docs:read"],
    ))).unwrap()
    print(f"1. Registered: {agent.id} (status: {agent.status})")

    # Suspend
    await gateway.suspend_agent(agent.id, organization_id="default")
    print(f"2. Suspended: {agent.id}")

    # Try to delegate — should fail
    user, auth_token = (await gateway.authenticate(
        credentials=PasswordCredentials(email="alice@example.com", password="secure-password"),
        organization_id="default",
    )).unwrap()
    task = TaskContext(id="task-lifecycle", purpose="Lifecycle demo")
    scope = DelegationScope(scopes=["docs:read"], expires_in_seconds=1800)

    result = await gateway.delegate_to_agent(
        principal_token=auth_token.access_token, agent_id=agent.id, task=task, scope=scope,
    )
    print(f"3. Delegation while suspended: {result.error.code}")

    # Reactivate (provider-level)
    await agent_provider.reactivate_agent(agent.id, organization_id="default")
    print(f"4. Reactivated: {agent.id}")

    # Delegate again — should succeed
    result = await gateway.delegate_to_agent(
        principal_token=auth_token.access_token, agent_id=agent.id, task=task, scope=scope,
    )
    print(f"5. Delegation after reactivation: {'OK' if result.is_ok else result.error.code}")

    # Revoke (permanent)
    await gateway.revoke_agent(agent.id, organization_id="default")
    print(f"6. Revoked: {agent.id} (permanent)")

    # List agents
    agents = await gateway.list_agents(organization_id="default", include_revoked=True)
    for a in agents:
        print(f"   {a.id}: {a.status}")


if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
uv run agent_lifecycle.py
```

Expected output:

```
1. Registered: agent:lifecycle-demo (status: active)
2. Suspended: agent:lifecycle-demo
3. Delegation while suspended: AGENT_SUSPENDED
4. Reactivated: agent:lifecycle-demo
5. Delegation after reactivation: OK
6. Revoked: agent:lifecycle-demo (permanent)
   agent:lifecycle-demo: revoked
```

## Common Pitfalls

| Pitfall                         | Solution                                                                        |
| ------------------------------- | ------------------------------------------------------------------------------- |
| Revoking when suspend is enough | Revocation is permanent. Use `suspend_agent` first to investigate.              |
| Existing tokens still valid     | Tokens are stateless JWTs. Use short `expires_in_seconds` as a best practice.   |
| Reactivate is provider-only     | `reactivate_agent` is on the provider, not the gateway. This is by design.      |
| Missing `organization_id`       | Pass `organization_id` to scope operations to the correct organization.         |
| Revoking affects all chains     | All delegation chains involving the revoked agent will fail on new delegations. |

## Next Steps

* [Register Agent](register-agent.md) — Register new agents to replace revoked ones
* [Scope & Budget](scope-and-budget.md) — Use short expiry times for defense in depth
* [Result Pattern](../../result-pattern.md) — Handle errors from lifecycle operations

***

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url\&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Fagent-authentication%2Fagent-lifecycle).
{% endhint %}
