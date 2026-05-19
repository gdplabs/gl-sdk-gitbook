---
icon: users
---

# Traditional IAM

Tutorials for securing human users and services with GL IAM — the foundational building blocks of identity and access management.

{% hint style="info" %}
New to GL IAM? Start with [Introduction to GL IAM](../../introduction-to-gl-iam.md) to understand the core concepts, or check the [Terminology](../../terminology.md) page for quick definitions.
{% endhint %}

## What is Traditional IAM?

Traditional IAM covers the classic identity patterns that most applications need from day one:

- **Who is this person?** — Authenticate human users with passwords, OAuth, or SAML
- **Is this service trusted?** — Authenticate backend services with API keys
- **What can they do?** — Authorize actions with roles and permissions
- **Are tokens tamper-proof?** — Bind tokens to specific clients with DPoP
- **Can partners send users to us?** — Federate identity with SSO partners

These patterns handle **human users** and **machine-to-machine** communication. For AI agents acting on behalf of users, see [Agent IAM](../agent-iam/).

## At a Glance

| Capability | What It Does | Start Here |
| --- | --- | --- |
| **Quickstart** | Get up and running with your chosen provider | [Quickstart](quickstart/) |
| **User Authentication** | Login, sessions, token refresh, logout | [User Authentication](user-authentication/) |
| **Service Authentication** | API key create, validate, revoke | [Service Authentication](service-authentication/) |
| **Authorization** | Standard roles and fine-grained permissions | [Authorization](authorization/) |
| **DPoP** | Proof-of-possession token binding | [DPoP](dpop/) |
| **SSO Partner Registry** | IdP-initiated SSO with external partners | [SSO Partner Registry](sso-partner-registry/) |

## Recommended Learning Path

{% stepper %}
{% step %}
#### Start with a Quickstart

Pick your provider — [PostgreSQL](quickstart/quickstart-postgresql.md), [Stack Auth](quickstart/quickstart-stack-auth.md), or [Keycloak](quickstart/quickstart-keycloak.md) — and get a working setup in minutes.
{% endstep %}

{% step %}
#### Authenticate Users

Learn the full [session lifecycle](user-authentication/): login, validate, refresh, and logout.
{% endstep %}

{% step %}
#### Add Authorization

Control access with [Standard Roles](authorization/standard-roles.md) and [Permissions](authorization/permissions.md).
{% endstep %}

{% step %}
#### Secure Your Services

Set up [API key authentication](service-authentication/) for backend-to-backend communication.
{% endstep %}

{% step %}
#### Go Further

Harden tokens with [DPoP](dpop/) or federate identity with [SSO Partner Registry](sso-partner-registry/).
{% endstep %}
{% endstepper %}

---

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Ftraditional-iam).
{% endhint %}
