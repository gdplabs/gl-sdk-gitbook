---
icon: books
---

# Terminology

A quick reference for the key terms and concepts used throughout the GL IAM documentation.

{% hint style="info" %}
New to GL IAM? Start with [Introduction to GL IAM](introduction-to-gl-iam.md) for a high-level overview before diving into the details.
{% endhint %}

***

## General Concepts

| Term | Definition |
| --- | --- |
| **IAM** | Identity and Access Management — the discipline of controlling who users are (authentication) and what they can do (authorization). |
| **IAMGateway** | The central orchestrator for all GL IAM operations. You write application code against this single interface, then swap providers through configuration. |
| **Provider** | A backend implementation that powers the IAMGateway. GL IAM ships with three: **Stack Auth**, **Keycloak**, and **PostgreSQL**. |
| **Organization** | An isolated tenant unit (company, team, or workspace). Every GL IAM operation is scoped to an organization. |
| **Multi-Tenancy** | The ability to serve multiple organizations from a single deployment, with strict data isolation between them. |

***

## Authentication

| Term | Definition |
| --- | --- |
| **Authentication** | Verifying *who* a principal is — "prove you are who you claim to be." |
| **Principal** | Any entity that can authenticate: a **User**, a **Service** (via API key), or an **Agent** (via delegation token). |
| **Access Token** | A short-lived token (15–60 min) used for API calls. |
| **Refresh Token** | A long-lived token (7–30 days) used to obtain a new access token without re-authenticating. |
| **Session** | The lifecycle from login to logout, managed through access and refresh tokens. |

***

## Traditional IAM

These terms apply to human users and service-to-service communication — the "classic" IAM patterns.

| Term | Definition |
| --- | --- |
| **User Authentication** | Login, session management, and logout for human end-users via password, OAuth, or SAML. |
| **Service Authentication** | API key-based authentication for backend services, CI/CD pipelines, and automation scripts. |
| **API Key** | A secret token issued to a service for machine-to-machine communication. Follows a create-validate-revoke lifecycle. |
| **DPoP** | Demonstrating Proof-of-Possession ([RFC 9449](https://datatracker.ietf.org/doc/html/rfc9449)) — a mechanism that cryptographically binds an access token to a specific client, preventing stolen tokens from being reused. |
| **SSO** | Single Sign-On — allowing users to authenticate once and access multiple applications. |
| **IdP-Initiated SSO** | An SSO flow where the identity provider (partner) pushes authenticated user sessions into your application. |
| **SSO Partner** | An external identity provider registered in the SSO Partner Registry for federated authentication. |
| **Consumer Key/Secret** | A credential pair issued to an SSO partner for HMAC-SHA256 signature validation. |

***

## Agent IAM

These terms apply to AI agents acting on behalf of users — the newer, agent-specific IAM patterns.

| Term | Definition |
| --- | --- |
| **Agent** | An AI agent registered as a first-class principal in GL IAM. Agents authenticate through delegation, not passwords or API keys. |
| **AgentType** | Classification of an agent's role: `ORCHESTRATOR`, `WORKER`, `TOOL`, or `AUTONOMOUS`. |
| **Delegation** | The act of a human (or another agent) explicitly granting limited authority to an agent to act on their behalf. |
| **Delegation Token** | A JWT that encodes the delegation chain, scope, and task context — the agent's proof of authority. |
| **Delegation Chain** | An ordered sequence of principals from the root (user) to the leaf (current agent). Each hop can only narrow permissions. |
| **Scope Attenuation** | The principle that each delegation in a chain can only *narrow* scopes, never widen them. An agent cannot grant more authority than it has. |
| **DelegationScope** | Defines what an agent can do — scopes, resource constraints, action budget, and expiry. |
| **TaskContext** | Metadata explaining *why* a delegation exists — task ID, purpose, and data sensitivity level. |
| **Action Budget** | A numeric limit on how many actions an agent can perform within a single delegation. |
| **Kill Switch** | The ability to immediately suspend or permanently revoke an agent, blocking all future delegations. |

***

## Authorization

| Term | Definition |
| --- | --- |
| **Authorization** | Controlling *what* an authenticated principal can do — "are you allowed to perform this action?" |
| **Role** | A named level of access. GL IAM defines three standard roles that work across all providers. |
| **Standard Roles** | `PLATFORM_ADMIN` (manage all orgs), `ORG_ADMIN` (manage users within an org), `ORG_MEMBER` (basic access). Higher roles inherit lower role permissions. |
| **Permission** | A fine-grained access control string (e.g., `docs:delete`) that can be checked independently of roles. |

***

## Cross-Cutting Concepts

| Term | Definition |
| --- | --- |
| **Audit Trail** | Structured event logging for all security-relevant IAM operations. The gateway automatically emits events; you attach handlers to route them. |
| **AuditEvent** | A structured record of an IAM operation — includes event type, severity, user ID, IP address, and trace context. |
| **AuditHandler** | A destination for audit events: console (JSON logs), database (PostgreSQL), OpenTelemetry, or your own custom handler. |
| **Result Pattern** | A Rust-inspired return pattern used across all IAMGateway methods. Check `result.is_ok` for success or `result.error` for failure — no exceptions to catch. |
| **ErrorCode** | A typed enum of error categories (e.g., `AUTHENTICATION_FAILED`, `USER_NOT_FOUND`) for precise error handling via pattern matching. |

***

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fterminology).
{% endhint %}
