---
icon: bolt-lightning
---

# Quickstart

Get started with GL IAM in minutes. Choose a quickstart based on your identity provider.

{% hint style="info" %}
**Not sure which provider to use?** See [Choosing a Provider](choosing-a-provider.md) for a detailed comparison.
{% endhint %}

## Choose Your Quickstart

<table data-view="cards"><thead><tr><th data-card-target data-type="content-ref">Target</th><th data-hidden>Tutorial</th></tr></thead><tbody><tr><td><a href="quickstart-postgresql.md">quickstart-postgresql.md</a></td><td>PostgreSQL - Full control, no external services</td></tr><tr><td><a href="quickstart-stack-auth.md">quickstart-stack-auth.md</a></td><td>Stack Auth - Modern managed authentication</td></tr><tr><td><a href="quickstart-keycloak.md">quickstart-keycloak.md</a></td><td>Keycloak - Enterprise identity management</td></tr></tbody></table>

## Quick Comparison

| Provider                               | Setup Time | Best For                                      |
| -------------------------------------- | ---------- | --------------------------------------------- |
| [PostgreSQL](quickstart-postgresql.md) | \~2 min    | Prototypes, internal tools, full data control |
| [Stack Auth](quickstart-stack-auth.md) | \~5 min    | SaaS apps, managed auth, social login         |
| [Keycloak](quickstart-keycloak.md)     | \~5 min    | Enterprise SSO, SAML, user federation         |

## What You'll Learn

{% stepper %}
{% step %}
#### Setup

Install GL IAM and configure the provider.
{% endstep %}

{% step %}
#### Authentication

Validate tokens and get user info.
{% endstep %}

{% step %}
#### Authorization

Protect endpoints with role-based access.
{% endstep %}

{% step %}
#### Complete Example

A working FastAPI application.
{% endstep %}
{% endstepper %}

## Provider-Agnostic Code

All quickstarts use the same application code - only the provider configuration differs:

{% code title="app.py" %}
```python
# Same code works with any provider
from fastapi import Depends, FastAPI
from gl_iam import User
from gl_iam.fastapi import get_current_user, require_org_admin

app = FastAPI()

@app.get("/me")
async def get_me(user: User = Depends(get_current_user)):
    return {"email": user.email, "roles": user.roles}

@app.get("/admin")
async def admin_only(
    user: User = Depends(get_current_user),
    _: None = Depends(require_org_admin()),
):
    return {"message": f"Welcome, Admin {user.display_name}!"}
```
{% endcode %}

Learn more about this pattern in [Provider-Agnostic Code](provider-agnostic-code.md).

---

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Fquickstart).
{% endhint %}
