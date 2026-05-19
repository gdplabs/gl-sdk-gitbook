---
description: Tutorials for Agent Authentication and Delegation
icon: robot
---

# Agent Authentication

## What is Agent IAM?

Agent IAM extends GL IAM to support **AI agents as first-class principals**. Just like users authenticate with passwords and services authenticate with API keys, agents authenticate through **delegation** — a human or another agent explicitly grants limited authority to act on their behalf.

{% hint style="info" %}
New to GL IAM? Start with [Introduction to GL IAM](../../../introduction-to-gl-iam.md) to understand the core concepts before diving into agents.
{% endhint %}

## The Three Principal Types

| Principal   | Authenticates via     | Typical Use Case                    |
| ----------- | --------------------- | ----------------------------------- |
| **User**    | Password, OAuth, SAML | Human end-users                     |
| **API Key** | Secret token          | Service-to-service                  |
| **Agent**   | Delegation token      | AI agents acting on behalf of users |

## How Agent Delegation Works

<figure><img src="../../../../.gitbook/assets/GL IAM - How Agent Delegation Works.png" alt=""><figcaption></figcaption></figure>

## Key Concepts

| Concept               | Description                                                                  |
| --------------------- | ---------------------------------------------------------------------------- |
| **AgentType**         | Classification of agent role: `ORCHESTRATOR`, `WORKER`, `TOOL`, `AUTONOMOUS` |
| **DelegationScope**   | What an agent can do — scopes, resource constraints, action budget, expiry   |
| **DelegationChain**   | Ordered list of principals from root (user) to leaf (current agent)          |
| **DelegationToken**   | JWT encoding the chain, scope, and task context                              |
| **TaskContext**       | Why the delegation exists — task ID, purpose, data sensitivity               |
| **Scope Attenuation** | Each hop in the chain can only narrow scopes, never widen them               |
| **Kill Switch**       | Suspend or permanently revoke an agent to block future delegations           |

## Tutorials

{% stepper %}
{% step %}
**Register Agent**

[Register Your First Agent](register-agent.md)

What You'll Learn: Register an agent with a type, owner, and allowed scopes.
{% endstep %}

{% step %}
**Delegate to Agent**

[Delegate Authority to an Agent](delegate-to-agent.md)

What You'll Learn: Create a delegation token granting limited authority to an agent.
{% endstep %}

{% step %}
**Validate Delegation Token**

[Validate Delegation Tokens](validate-delegation-token.md)

What You'll Learn: Validate delegation tokens in receiving services using a minimal gateway.
{% endstep %}

{% step %}
**Delegation Chain**

[Multi-Hop Delegation Chains](delegation-chain.md)

What You'll Learn: Build multi-hop delegation chains where agents sub-delegate to other agents.
{% endstep %}

{% step %}
**Scope & Budget**

[Scope Attenuation & Action Budgets](scope-and-budget.md)

What You'll Learn: Control what agents can do with scope narrowing, resource constraints, and budgets.
{% endstep %}

{% step %}
**Agent Lifecycle**

[Suspend, Revoke & Kill Switch](agent-lifecycle.md)

What You'll Learn: Manage agent lifecycle — suspend, reactivate, and permanently revoke agents.
{% endstep %}
{% endstepper %}

***

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url\&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Fagent-authentication).
{% endhint %}
