---
icon: right-to-bracket
---

# Login

Authenticate a user and create a session.

{% hint style="info" %}
**When to use**: Implement sign-in in your application.
{% endhint %}

<details>

<summary>Prerequisites</summary>

* Completed [Quickstart](/broken/pages/a0e2da72d6d797a5bb2d5673459cd61e6f6ca829)
* A running PostgreSQL instance with GL IAM configured

</details>

## 5-Line Core

```python
result = await gateway.authenticate(
    credentials=PasswordCredentials(email="alice@example.com", password="SecurePass123"),
    organization_id="default",
)
user, token = result.unwrap()
```

## Step-by-Step

{% stepper %}
{% step %}
**Setup Gateway**

```python
from gl_iam import IAMGateway
from gl_iam.core.types import PasswordCredentials
from gl_iam.providers.postgresql import PostgreSQLProvider, PostgreSQLConfig

config = PostgreSQLConfig(
    database_url="postgresql+asyncpg://postgres:postgres@localhost:5432/gliam"
)
provider = PostgreSQLProvider(config)
gateway = IAMGateway.from_fullstack_provider(provider)
```
{% endstep %}

{% step %}
**Authenticate**

```python
result = await gateway.authenticate(
    credentials=PasswordCredentials(
        email="alice@example.com",
        password="SecurePass123"
    ),
    organization_id="default",
)
```
{% endstep %}

{% step %}
**Handle Result**

```python
if result.is_ok:
    user, token = result.unwrap()
    print(f"Welcome, {user.display_name}!")
    print(f"Access token: {token.access_token[:20]}...")
else:
    print(f"Login failed: {result.error.message}")
```
{% endstep %}

{% step %}
**Expected Output**

```
Welcome, Alice!
Access token: eyJhbGciOiJIUzI1N...
```
{% endstep %}
{% endstepper %}

{% hint style="success" %}
You've implemented user login!
{% endhint %}

## Complete Example

Create `login.py`:

```python
"""GL IAM Login Example."""

import asyncio

from gl_iam import IAMGateway
from gl_iam.core.types import PasswordCredentials
from gl_iam.providers.postgresql import PostgreSQLProvider, PostgreSQLConfig

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/gliam"


async def main():
    # Setup
    config = PostgreSQLConfig(database_url=DATABASE_URL)
    provider = PostgreSQLProvider(config)
    gateway = IAMGateway.from_fullstack_provider(provider)

    # Login
    result = await gateway.authenticate(
        credentials=PasswordCredentials(
            email="alice@example.com",
            password="SecurePass123"
        ),
        organization_id="default",
    )

    # Handle result
    if result.is_ok:
        user, token = result.unwrap()
        print(f"Welcome, {user.display_name or user.email}!")
        print(f"Access token: {token.access_token[:50]}...")
    else:
        print(f"Login failed: {result.error.code} - {result.error.message}")

    await provider.close()


if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
uv run login.py
```

## Common Pitfalls

| Pitfall                   | Solution                                               |
| ------------------------- | ------------------------------------------------------ |
| Missing `organization_id` | Always pass organization context                       |
| User enumeration          | Return same error for "not found" and "wrong password" |
| Exposing tokens           | Never log full tokens or pass in URLs                  |

## Next Steps

* [User](user.md) - Understand the User object you received
* [Validate](validate.md) - Verify tokens on protected endpoints

---

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Fuser-authentication%2Flogin).
{% endhint %}
