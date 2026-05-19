---
icon: sitemap
---

# Standard Roles

Check user roles with automatic hierarchy support.

{% hint style="info" %}
**When to use**: When you need coarse access control like "is this user an admin?"
{% endhint %}

<details>

<summary>Prerequisites</summary>

* Completed [Login](../user-authentication/login.md)
* Have a user object from authentication

</details>

## 5-Line Core

```python
from gl_iam.core.roles import StandardRole

if user.has_standard_role(StandardRole.ORG_ADMIN):
    print("User has admin access")
# Also true for PLATFORM_ADMIN (hierarchy)
```

## Role Hierarchy

| Role             | Implies                 |
| ---------------- | ----------------------- |
| `PLATFORM_ADMIN` | ORG\_ADMIN, ORG\_MEMBER |
| `ORG_ADMIN`      | ORG\_MEMBER             |
| `ORG_MEMBER`     | (none)                  |

Higher roles automatically include lower role access.

## Step-by-Step

{% stepper %}
{% step %}
**Import Standard Roles**

```python
from gl_iam.core.roles import StandardRole
```
{% endstep %}

{% step %}
**Check Role with Hierarchy**

```python
# Returns True if user is ORG_ADMIN or PLATFORM_ADMIN
if user.has_standard_role(StandardRole.ORG_ADMIN):
    print("User has admin access")
```
{% endstep %}

{% step %}
**Check Exact Role**

```python
# Only returns True if user is exactly ORG_MEMBER
if user.has_standard_role(StandardRole.ORG_MEMBER, respect_hierarchy=False):
    print("User is exactly ORG_MEMBER")
```
{% endstep %}

{% step %}
**Get User's Roles**

```python
roles = user.get_standard_roles()
print(f"User roles: {[r.value for r in roles]}")
```
{% endstep %}

{% step %}
**Expected Output**

```
User has admin access
User roles: ['org_admin']
```
{% endstep %}
{% endstepper %}

{% hint style="success" %}
You can check standard roles!
{% endhint %}

## Complete Example

Create `standard_roles.py`:

```python
"""GL IAM Standard Roles Example."""

import asyncio

from gl_iam import IAMGateway
from gl_iam.core.roles import StandardRole
from gl_iam.core.types import PasswordCredentials
from gl_iam.providers.postgresql import PostgreSQLProvider, PostgreSQLConfig

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/gliam"


async def main():
    # Setup
    config = PostgreSQLConfig(database_url=DATABASE_URL)
    provider = PostgreSQLProvider(config)
    gateway = IAMGateway.from_fullstack_provider(provider)

    # Login to get user
    result = await gateway.authenticate(
        credentials=PasswordCredentials(email="alice@example.com", password="SecurePass123"),
        organization_id="default",
    )
    user, token = result.unwrap()

    print(f"User: {user.email}")
    print(f"Raw roles: {user.roles}")

    # Check with hierarchy (default)
    print("\n--- With Hierarchy ---")
    print(f"Is PLATFORM_ADMIN: {user.has_standard_role(StandardRole.PLATFORM_ADMIN)}")
    print(f"Is ORG_ADMIN: {user.has_standard_role(StandardRole.ORG_ADMIN)}")
    print(f"Is ORG_MEMBER: {user.has_standard_role(StandardRole.ORG_MEMBER)}")

    # Check exact role
    print("\n--- Exact Check ---")
    print(f"Is exactly ORG_MEMBER: {user.has_standard_role(StandardRole.ORG_MEMBER, respect_hierarchy=False)}")

    await provider.close()


if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
uv run standard_roles.py
```

Expected output:

```
User: alice@example.com
Raw roles: ['org_member']

--- With Hierarchy ---
Is PLATFORM_ADMIN: False
Is ORG_ADMIN: False
Is ORG_MEMBER: True

--- Exact Check ---
Is exactly ORG_MEMBER: True
```

## Provider Mapping

GL IAM maps provider-specific roles to standard roles:

| Provider   | Admin       | Member       |
| ---------- | ----------- | ------------ |
| PostgreSQL | `org_admin` | `org_member` |
| Stack Auth | `$admin`    | `$member`    |
| Keycloak   | `admin`     | `member`     |

## Common Pitfalls

| Pitfall                  | Solution                                                    |
| ------------------------ | ----------------------------------------------------------- |
| Forgetting hierarchy     | Default respects hierarchy - admins pass member checks      |
| Hard-coding role strings | Use `StandardRole` enum for provider independence           |
| Wrong status code        | Role check is authorization (403), not authentication (401) |

---

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Fauthorization%2Fstandard-roles).
{% endhint %}
