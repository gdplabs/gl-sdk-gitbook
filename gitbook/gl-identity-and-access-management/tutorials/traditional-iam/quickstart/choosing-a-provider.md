---
icon: code-compare
---

# Choosing a Provider

GL IAM supports multiple identity providers through a unified interface. This guide helps you choose the right provider for your use case.

{% hint style="info" %}
**Provider-agnostic by design**: Your application code remains the same regardless of which provider you choose. Only the configuration changes. See [Provider-Agnostic Code](provider-agnostic-code.md) for details.
{% endhint %}

## Quick Decision Guide

| If you need...                            | Choose                                 |
| ----------------------------------------- | -------------------------------------- |
| Fastest setup, no external services       | [PostgreSQL](quickstart-postgresql.md) |
| Modern managed auth with user-friendly UI | [Stack Auth](quickstart-stack-auth.md) |
| Enterprise SSO, SAML, federation          | [Keycloak](quickstart-keycloak.md)     |

## Feature Comparison

| Feature                   | PostgreSQL                | Stack Auth           | Keycloak        |
| ------------------------- | ------------------------- | -------------------- | --------------- |
| **Setup complexity**      | Low                       | Low                  | Medium          |
| **External dependencies** | Database only             | Cloud or self-hosted | Self-hosted     |
| **User registration**     | Built-in                  | Built-in UI          | Admin console   |
| **Password management**   | Built-in                  | Managed              | Managed         |
| **SSO (OIDC/SAML)**       | No                        | OIDC                 | OIDC + SAML     |
| **MFA**                   | No                        | Yes                  | Yes             |
| **User federation**       | No                        | No                   | Yes             |
| **Social login**          | No                        | Yes                  | Yes             |
| **Best for**              | Prototypes, internal apps | SaaS products        | Enterprise apps |

## Provider Overview

### PostgreSQL Provider

The PostgreSQL provider gives you full control over user data storage. GL IAM handles password hashing, token generation, and session management.

**Best for:**

* Rapid prototyping and development
* Internal tools and admin dashboards
* Applications requiring full data ownership
* Scenarios where external auth services aren't desired

{% code title="example.py" %}
```python
from gl_iam.providers.postgresql import PostgreSQLProvider, PostgreSQLConfig

config = PostgreSQLConfig(
    database_url="postgresql+asyncpg://user:pass@localhost:5432/mydb"
)
provider = PostgreSQLProvider(config)
```
{% endcode %}

[Get started with PostgreSQL →](quickstart-postgresql.md)

***

### Stack Auth Provider

Stack Auth is a modern authentication platform with a developer-friendly API and pre-built UI components.

**Best for:**

* SaaS applications needing quick auth setup
* Teams wanting managed authentication
* Applications requiring modern auth features (social login, MFA)
* Projects with frontend integration needs

{% code title="example.py" %}
```python
from gl_iam.providers.stackauth import StackAuthProvider, StackAuthConfig

config = StackAuthConfig(
    base_url="https://api.stack-auth.com",
    project_id="your-project-id",
    publishable_client_key="pck_...",
    secret_server_key="ssk_...",
)
provider = StackAuthProvider(config)
```
{% endcode %}

[Get started with Stack Auth →](quickstart-stack-auth.md)

***

### Keycloak Provider

Keycloak is an enterprise-grade identity solution with comprehensive features for complex authentication scenarios.

**Best for:**

* Enterprise environments with existing Keycloak infrastructure
* Applications requiring SAML support
* Multi-application SSO requirements
* User federation with LDAP/Active Directory

{% code title="example.py" %}
```python
from gl_iam.providers.keycloak import KeycloakProvider, KeycloakConfig

config = KeycloakConfig(
    server_url="http://localhost:8080",
    realm="my-realm",
    client_id="my-client",
    client_secret="my-secret",
)
provider = KeycloakProvider(config)
```
{% endcode %}

[Get started with Keycloak →](quickstart-keycloak.md)

## The Power of Provider-Agnostic Code

Regardless of which provider you choose, your application endpoints look identical:

{% code title="main.py" %}
```python
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

This code works with PostgreSQL, Stack Auth, and Keycloak without modification. Learn more about this pattern in [Provider-Agnostic Code](provider-agnostic-code.md).

---

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Fquickstart%2Fchoosing-a-provider).
{% endhint %}
