---
icon: robot
---

# Agent IAM

Tutorials for securing AI agents with GL IAM — giving agents their own identity, scoped authority, and auditable actions.

{% hint style="info" %}
New to GL IAM? Start with [Introduction to GL IAM](../../introduction-to-gl-iam.md) to understand the core concepts, or check the [Terminology](../../terminology.md) page for quick definitions.
{% endhint %}

## What is Agent IAM?

As AI agents take on more complex tasks — browsing the web, calling APIs, managing data — they need proper identity and access controls, just like human users do.

Agent IAM extends GL IAM to treat **AI agents as first-class principals**. Instead of sharing a user's credentials or using a generic API key, each agent gets its own identity and receives *delegated* authority with clear boundaries.

{% hint style="success" %}
**The key principle**: Agents don't have standing permissions. A human (or another agent) explicitly grants limited authority through **delegation**, and that authority can only narrow — never widen — as it passes down the chain.
{% endhint %}

## How It Differs from Traditional IAM

| | Traditional IAM | Agent IAM |
| --- | --- | --- |
| **Who** | Human users, backend services | AI agents acting on behalf of users |
| **Authenticates via** | Password, OAuth, API key | Delegation token |
| **Authority model** | Assigned roles and permissions | Delegated scopes with attenuation |
| **Lifecycle** | Login/logout sessions | Register, delegate, suspend, revoke |
| **Trust boundary** | User proves identity directly | Agent's authority traces back to a human |

For human users and services, see [Traditional IAM](../traditional-iam/).

## At a Glance

| Capability | What It Does | Start Here |
| --- | --- | --- |
| **Agent Authentication** | Register agents, delegate authority, validate tokens | [Agent Authentication](agent-authentication/) |

## What You Can Do

<table data-view="cards"><thead><tr><th data-card-target data-type="content-ref">Target</th><th data-hidden>Tutorial</th></tr></thead><tbody><tr><td><a href="agent-authentication/">agent-authentication</a></td><td>Agent Authentication</td></tr></tbody></table>

---

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fagent-iam).
{% endhint %}
