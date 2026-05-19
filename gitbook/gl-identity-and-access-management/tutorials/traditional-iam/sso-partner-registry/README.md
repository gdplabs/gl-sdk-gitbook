---
description: Tutorials for SSO Partner Registry and Signature Validation
icon: handshake
---

# SSO Partner Registry

## What is SSO Partner Registry?

SSO Partner Registry enables **IdP-Initiated Single Sign-On** by managing external identity provider partners. Each partner receives a **consumer key/secret pair** for HMAC-SHA256 signature validation, allowing partners to push authenticated user sessions into your application securely.

{% hint style="warning" %}
**Security Notice**: IdP-Initiated SSO delegates identity assertion to the partner. Unlike SP-Initiated SSO (OAuth/OIDC), there is no redirect-based consent flow — the partner asserts "this user is authenticated" and your application trusts it.

**Only register partners you fully trust**, and always configure security restrictions (`allowed_email_domains`, `allowed_source_ips`, `max_users`). See the [Security Model](#security-model) section below.
{% endhint %}

{% hint style="info" %}
New to GL IAM? Start with [Introduction to GL IAM](../../../introduction-to-gl-iam.md) to understand the core concepts before diving into partner registry.
{% endhint %}

## When to Use

| Scenario                          | Use                          |
| --------------------------------- | ---------------------------- |
| External IdP pushes user sessions | **SSO Partner Registry**     |
| Human end-user login              | [User Authentication](../user-authentication/) |
| Service-to-service calls          | [Service Authentication](../service-authentication/) |
| AI agent acting on behalf of user | [Agent Authentication](../../agent-iam/agent-authentication/) |

## When NOT to Use

| Scenario | Use Instead |
| -------- | ----------- |
| Partner already has OAuth/OIDC | SP-Initiated SSO via [User Authentication](../user-authentication/) (more secure, industry-standard flow) |
| Untrusted or unknown partner | Do not integrate — IdP-Initiated SSO requires high trust |
| Public self-service sign-up | Standard [User Authentication](../user-authentication/) with email/password or OAuth |
| Single-tenant, no external partners | Overkill — use direct authentication instead |

## Security Model

IdP-Initiated SSO has a fundamentally different trust model than SP-Initiated (OAuth/OIDC):

| | SP-Initiated (OAuth) | IdP-Initiated (Partner Registry) |
| --- | --- | --- |
| **Who asserts identity** | User proves identity via redirect flow | Partner asserts identity on behalf of user |
| **Trust boundary** | User + OAuth provider | Your application trusts the partner |
| **Replay protection** | Built-in (`state` param, authorization code) | Your responsibility (one-time tokens, nonces) |
| **Secret compromise impact** | Limited (OAuth codes are single-use) | Partner can assert any email within allowed domains |

**Minimum security checklist before registering a partner:**

1. Set `allowed_email_domains` — never allow a partner to assert arbitrary email addresses
2. Set `allowed_source_ips` — restrict server-to-server calls to known partner IPs
3. Set `max_users` — cap the number of auto-provisioned accounts
4. Use one-time tokens (Redis `GETDEL`) — prevent SSO token replay
5. Implement rate limiting on SSO endpoints — prevent brute-force signature attempts
6. Use HTTPS only — never transmit signatures or tokens over plain HTTP
7. Rotate consumer secrets periodically — use `grace_period_seconds` for zero-downtime rotation

## SSO Modes

| Mode             | Value            | Description                                      |
| ---------------- | ---------------- | ------------------------------------------------ |
| **IdP-Initiated** | `IDP_INITIATED` | Identity Provider starts the SSO flow             |
| **SP-Initiated**  | `SP_INITIATED`  | Service Provider starts the SSO flow              |
| **Both**          | `BOTH`          | Both IdP-initiated and SP-initiated are supported |

## User Provisioning Strategies

| Strategy            | Value              | Description                                  |
| ------------------- | ------------------ | -------------------------------------------- |
| **JIT**             | `jit`              | Users are created automatically on first login |
| **Pre-Provisioned** | `pre_provisioned`  | Users must exist before SSO login             |
| **Disabled**        | `disabled`         | User provisioning is disabled                 |

## Security Restrictions (Opt-in)

Each partner can be configured with optional security restrictions. All default to `None` (no restriction):

| Field                    | Type             | Enforced By     | Description                                  |
| ------------------------ | ---------------- | --------------- | -------------------------------------------- |
| `allowed_email_domains`  | `list[str]`      | **GL-IAM**      | Only these email domains can SSO (case-insensitive) |
| `allowed_source_ips`     | `list[str]`      | Your app        | IP/CIDR allowlist for SSO requests           |
| `max_users`              | `int`            | Your app        | Maximum provisioned users for this partner   |
| `allowed_roles`          | `list[str]`      | Your app        | Restrict which roles can be assigned via SSO |

{% hint style="info" %}
GL-IAM enforces `allowed_email_domains` during signature validation (when the `email` parameter is provided). The other three fields are stored by GL-IAM but enforced by your application at the HTTP middleware or provisioning layer.
{% endhint %}

## Tutorials

{% stepper %}
{% step %}
#### Register Partner

[Register an SSO Partner](register-partner.md)

What You'll Learn: Register a partner, generate consumer credentials, and verify connectivity with health check.
{% endstep %}

{% step %}
#### Validate Partner Signature

[Validate Partner Signatures](validate-partner-signature.md)

What You'll Learn: Validate HMAC-SHA256 signatures from partners and look up partners by consumer key.
{% endstep %}

{% step %}
#### Rotate Consumer Secret

[Rotate Consumer Secrets](rotate-consumer-secret.md)

What You'll Learn: Rotate a partner's consumer secret with optional grace period for zero-downtime deployments.
{% endstep %}

{% step %}
#### Update Partner

[Update Partner Scope and Policy](update-partner.md)

What You'll Learn: Edit a partner's scope/policy fields (allowed origins, IP allowlist, max users, name, metadata) without re-issuing the consumer secret.
{% endstep %}

{% step %}
#### Manage Partner Lifecycle

[Deactivate, Reactivate & List Partners](manage-partner-lifecycle.md)

What You'll Learn: Manage the full partner lifecycle — deactivate, reactivate, and list partners with filters.
{% endstep %}
{% endstepper %}

---

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Fsso-partner-registry).
{% endhint %}
