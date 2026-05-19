---
description: SAML 2.0 and LDAP/Active Directory via Keycloak
icon: building-columns
---

# Enterprise Protocols

GL IAM supports enterprise authentication protocols — **SAML 2.0** and **LDAP/Active Directory** — through Keycloak's native protocol handling.

{% hint style="warning" %}
**Architecture note**: SAML and LDAP are not implemented directly in the GL IAM SDK. Instead, Keycloak handles these protocols natively, and the SDK communicates with Keycloak via OIDC. This is a deliberate design decision — SAML and LDAP are complex enterprise protocols best handled by a purpose-built identity platform.
{% endhint %}

## How It Works

<figure><img src="../../../../.gitbook/assets/GL IAM - Enterprise Protocol.png" alt=""><figcaption></figcaption></figure>

1. **Keycloak** handles the SAML assertion exchange or LDAP bind/search
2. **Keycloak** issues an OIDC token with claims mapped from SAML attributes or LDAP fields
3. **GL IAM SDK** validates the OIDC token via `KeycloakProvider` — your application code stays the same

## Provider Comparison

| Protocol                    | PostgreSQL | Stack Auth | Keycloak             |
| --------------------------- | ---------- | ---------- | -------------------- |
| **Password (built-in)**     | Yes        | Yes        | Yes                  |
| **OIDC / OAuth 2.0**        | No         | Yes        | Yes                  |
| **SAML 2.0**                | No         | No         | **Yes (native)**     |
| **LDAP / Active Directory** | No         | No         | **Yes (federation)** |
| **Social Login**            | No         | Yes        | Yes                  |

## When to Use

| If you need...                                                | See                                           |
| ------------------------------------------------------------- | --------------------------------------------- |
| LDAP/AD user federation (sync users from corporate directory) | [LDAP Authentication](ldap-authentication.md) |
| SAML 2.0 SSO with an external Identity Provider               | [SAML Federation](saml-federation.md)         |
| Both SAML and LDAP in the same deployment                     | Start with LDAP, then add SAML IdP            |

## Your Application Code Doesn't Change

This is the key benefit of the SIMI pattern. Whether users authenticate via password, SAML, or LDAP, your endpoint code is identical:

```python
from fastapi import Depends
from gl_iam import User
from gl_iam.fastapi import get_current_user, require_org_member

@app.get("/protected")
async def protected(
    user: User = Depends(get_current_user),
    _: None = Depends(require_org_member()),
):
    # This works for password, SAML, and LDAP users
    return {"email": user.email, "roles": user.roles}
```

Keycloak handles protocol translation. GL IAM handles authorization. Your app handles business logic.

## Tutorials

{% stepper %}
{% step %}
**LDAP Authentication**

[LDAP Authentication](ldap-authentication.md)

What You'll Learn: Federate users from LDAP/Active Directory through Keycloak.
{% endstep %}

{% step %}
**SAML Federation**

[SAML Federation](saml-federation.md)

What You'll Learn: Enable SAML 2.0 SSO with external Identity Providers through Keycloak.
{% endstep %}
{% endstepper %}

***

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url\&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Fenterprise-protocols).
{% endhint %}
