---
icon: user-robot
---

# Register Agent

Register an AI agent as a principal in GL IAM so it can receive delegated authority.

{% hint style="info" %}
**When to use**: Before an agent can participate in delegation, it must be registered with an identity, type, and owner.
{% endhint %}

<details>

<summary>Prerequisites</summary>

* Completed [Quickstart: PostgreSQL](../../traditional-iam/quickstart/quickstart-postgresql.md)
* `gl-iam[postgresql]` installed

</details>

## 5-Line Core

```python
from gl_iam import IAMGateway, AgentRegistration, AgentType
from gl_iam.providers.postgresql import PostgreSQLAgentProvider, PostgreSQLConfig

provider = PostgreSQLAgentProvider(PostgreSQLConfig(database_url="postgresql+asyncpg://user:pass@localhost/mydb", secret_key="your-secret-key-min-32-chars-long!", default_org_id="default"))
gateway = IAMGateway.for_agent_auth(agent_provider=provider, secret_key="your-secret-key-min-32-chars-long!")
result = await gateway.register_agent(AgentRegistration(name="my-worker", agent_type=AgentType.WORKER, owner_user_id="user:alice", operator_org_id="default"))
agent = result.unwrap()  # AgentIdentity
```

## Agent Types

| Type             | Value                    | Use Case                                             |
| ---------------- | ------------------------ | ---------------------------------------------------- |
| **Orchestrator** | `AgentType.ORCHESTRATOR` | Coordinates other agents, manages workflows          |
| **Worker**       | `AgentType.WORKER`       | Performs specific tasks (summarize, translate, etc.) |
| **Tool**         | `AgentType.TOOL`         | Wraps an external tool or API call                   |
| **Autonomous**   | `AgentType.AUTONOMOUS`   | Long-running agent with independent decision-making  |

## Step-by-Step

{% stepper %}
{% step %}
**Setup Gateway**

Create an agent provider and a minimal gateway using `for_agent_auth`:

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
{% endstep %}

{% step %}
**Create Registration**

Define the agent's identity and capabilities:

```python
from gl_iam import AgentRegistration, AgentType

registration = AgentRegistration(
    name="doc-reviewer",
    agent_type=AgentType.WORKER,
    owner_user_id="user:alice",
    operator_org_id="default",
    max_delegation_depth=3,
    allowed_scopes=["docs:read", "docs:summarize"],
    metadata={"model": "claude-sonnet-4-6", "version": "1.0"},
)
```
{% endstep %}

{% step %}
**Register Agent**

```python
result = await gateway.register_agent(registration)
agent = result.unwrap()
```
{% endstep %}

{% step %}
**Expected Output**

```python
print(f"Agent ID: {agent.id}")           # agent:doc-reviewer
print(f"Type: {agent.agent_type}")        # AgentType.WORKER
print(f"Status: {agent.status}")          # AgentStatus.ACTIVE
print(f"Owner: {agent.owner_user_id}")    # user:alice
print(f"Scopes: {agent.allowed_scopes}")  # ['docs:read', 'docs:summarize']
```

```
Agent ID: agent:doc-reviewer
Type: worker
Status: active
Owner: user:alice
Scopes: ['docs:read', 'docs:summarize']
```
{% endstep %}
{% endstepper %}

{% hint style="success" %}
You've registered your first agent! It's now ready to receive delegated authority.
{% endhint %}

## Complete Example

Create `register_agent.py`:

```python
"""Register an AI agent in GL IAM."""

import asyncio

from gl_iam import IAMGateway, AgentRegistration, AgentType
from gl_iam.providers.postgresql import PostgreSQLAgentProvider, PostgreSQLConfig


async def main():
    config = PostgreSQLConfig(
        database_url="postgresql+asyncpg://user:pass@localhost/mydb",
        secret_key="your-secret-key-min-32-chars-long!",
        default_org_id="default",
    )
    provider = PostgreSQLAgentProvider(config)
    gateway = IAMGateway.for_agent_auth(agent_provider=provider, secret_key="your-secret-key-min-32-chars-long!")

    registration = AgentRegistration(
        name="doc-reviewer",
        agent_type=AgentType.WORKER,
        owner_user_id="user:alice",
        operator_org_id="default",
        max_delegation_depth=3,
        allowed_scopes=["docs:read", "docs:summarize"],
        metadata={"model": "claude-sonnet-4-6", "version": "1.0"},
    )

    result = await gateway.register_agent(registration)
    agent = result.unwrap()

    print(f"Agent ID: {agent.id}")
    print(f"Type: {agent.agent_type}")
    print(f"Status: {agent.status}")
    print(f"Owner: {agent.owner_user_id}")
    print(f"Scopes: {agent.allowed_scopes}")


if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
uv run register_agent.py
```

Expected output:

```
Agent ID: agent:doc-reviewer
Type: worker
Status: active
Owner: user:alice
Scopes: ['docs:read', 'docs:summarize']
```

## Common Pitfalls

| Pitfall                        | Solution                                                                       |
| ------------------------------ | ------------------------------------------------------------------------------ |
| Missing `owner_user_id`        | Every agent must have a human owner for accountability                         |
| Duplicate agent name           | Agent IDs are derived from names (`agent:<slugified-name>`). Use unique names. |
| Empty `allowed_scopes`         | An agent with no allowed scopes cannot receive any delegation                  |
| Missing `secret_key` in config | `PostgreSQLConfig` requires `secret_key` for JWT operations                    |
| Missing `default_org_id`       | Required by `PostgreSQLConfig` for auto-creating organizations                 |

## Next Steps

* [Delegate to Agent](delegate-to-agent.md) — Grant authority to your registered agent
* [Agent Lifecycle](agent-lifecycle.md) — Suspend and revoke agents

***

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url\&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Fagent-authentication%2Fregister-agent).
{% endhint %}
