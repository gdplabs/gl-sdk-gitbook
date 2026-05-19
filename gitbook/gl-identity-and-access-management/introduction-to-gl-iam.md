---
icon: lightbulb-on
---

# Introduction to GL Identity and Access Management

**IAM** stands for **Identity and Access Management**—handling who users are (authentication) and what they can do (authorization).

GL IAM is a Python SDK that provides a unified interface for IAM across GDP Labs products. You write application code once against the `IAMGateway`, then swap providers through configuration—no code changes required.

<figure><img src="../.gitbook/assets/GL IAM Architecture.png" alt=""><figcaption></figcaption></figure>

The GL IAM SDK includes:

* **IAMGateway** - Central orchestrator for all IAM operations
* **Providers** - Stack Auth, Keycloak, PostgreSQL implementations
* **Standard Roles** - Cross-provider role hierarchy
* **Multi-Tenancy** - Organization-scoped isolation enforced by default
* **API Key Authentication** - Service-to-service authentication
* **Third-Party Integrations** - External service credential management _(in development)_
* **Audit Trail** - Structured event logging for authentication, authorization, and identity operations

***

## Single Interface, Multiple Implementations

You write application code once against the `IAMGateway`, then swap providers through configuration — no code changes required.

| Provider       | Use Case                                                       |
| -------------- | -------------------------------------------------------------- |
| **StackAuth**  | Open-source Auth0/Clerk alternative with OAuth, passkeys, RBAC |
| **Keycloak**   | Enterprise IAM with SSO, SAML, identity federation             |
| **PostgreSQL** | Direct database user storage                                   |

***

## Standard Roles

GL IAM defines three standard roles that work consistently across all providers:

| Role             | Level   | Description                             |
| ---------------- | ------- | --------------------------------------- |
| `PLATFORM_ADMIN` | Highest | Can manage all organizations            |
| `ORG_ADMIN`      | Middle  | Can manage users within an organization |
| `ORG_MEMBER`     | Base    | Basic organization access               |

Higher roles automatically include lower role permissions. For example, checking for `ORG_MEMBER` will pass for users with `ORG_ADMIN` or `PLATFORM_ADMIN`.

<figure><img src="../.gitbook/assets/GL IAM - Roles Hierarchy.png" alt=""><figcaption></figcaption></figure>

***

## Multi-Tenancy

GL IAM enforces organization-scoped isolation by default. Every operation requires an `organization_id` parameter.

| Concept           | Description                                    |
| ----------------- | ---------------------------------------------- |
| Organization      | Isolated tenant (company, team, workspace)     |
| `organization_id` | Required parameter for all operations          |
| Data isolation    | Users, roles, permissions are per-organization |

{% hint style="info" %}
**Single-tenant apps**: Use a constant organization ID like `"default"`.
{% endhint %}

***

## Service Authentication

For service-to-service communication, GL IAM supports API key authentication as an alternative to user sessions.

| Auth Method            | Use Case                                      |
| ---------------------- | --------------------------------------------- |
| User Authentication    | Human users logging into web/mobile apps      |
| Service Authentication | Backend services, CI/CD pipelines, automation |

API keys provide direct access without the session lifecycle (login → refresh → logout) required for user authentication.

***

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url\&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fintroduction-to-gl-iam).
{% endhint %}
