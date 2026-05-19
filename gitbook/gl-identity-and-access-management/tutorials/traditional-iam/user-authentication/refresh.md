---
icon: rotate
---

# Refresh

Get a new access token using a refresh token.

{% hint style="info" %}
**When to use**: When the access token expires and you need a new one without re-authenticating.
{% endhint %}

<details>

<summary>Prerequisites</summary>

* Completed [Login](/broken/pages/70e495103ab305fdfcba6cdc17d9a7499195c67a)
* Have a refresh token from authentication

</details>

## 5-Line Core

```python
result = await gateway.refresh_session(
    refresh_token=token.refresh_token,
    organization_id="default",
)
new_token = result.unwrap()
```

## When to Refresh

| Situation                 | Action                   |
| ------------------------- | ------------------------ |
| Access token expired      | Call `refresh_session()` |
| API returns 401           | Call `refresh_session()` |
| Proactively before expiry | Call `refresh_session()` |
| Refresh token expired     | User must login again    |

## Step-by-Step

{% stepper %}
{% step %}
**Check Token Expiry**

```python
# AuthToken has an is_expired property
if token.is_expired:
    print("Token expired, need to refresh")
```
{% endstep %}

{% step %}
**Refresh the Token**

```python
result = await gateway.refresh_session(
    refresh_token=token.refresh_token,
    organization_id="default",
)
```
{% endstep %}

{% step %}
**Use New Token**

```python
if result.is_ok:
    new_token = result.unwrap()
    print(f"New access token: {new_token.access_token[:20]}...")
else:
    print("Refresh failed, user must login again")
```
{% endstep %}

{% step %}
**Expected Output**

```
New access token: eyJhbGciOiJIUzI1N...
```
{% endstep %}
{% endstepper %}

{% hint style="success" %}
You can refresh tokens!
{% endhint %}

## Complete Example

Create `refresh.py`:

```python
"""GL IAM Token Refresh Example."""

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

    # Login to get tokens
    auth_result = await gateway.authenticate(
        credentials=PasswordCredentials(email="alice@example.com", password="SecurePass123"),
        organization_id="default",
    )
    user, token = auth_result.unwrap()
    print(f"Original token: {token.access_token[:30]}...")

    # Refresh the token
    result = await gateway.refresh_session(
        refresh_token=token.refresh_token,
        organization_id="default",
    )

    if result.is_ok:
        new_token = result.unwrap()
        print(f"New token: {new_token.access_token[:30]}...")
        print("Token refreshed successfully!")
    else:
        print(f"Refresh failed: {result.error.message}")

    await provider.close()


if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
uv run refresh.py
```

Expected output:

```
Original token: eyJhbGciOiJIUzI1NiIsInR5cCI6...
New token: eyJhbGciOiJIUzI1NiIsInR5cCI6...
Token refreshed successfully!
```

## Common Pitfalls

| Pitfall                           | Solution                             |
| --------------------------------- | ------------------------------------ |
| Storing refresh token in frontend | Keep refresh tokens server-side only |
| Not handling refresh failure      | Redirect user to login on failure    |
| Refreshing too late               | Refresh proactively before expiry    |

## Next Steps

* [Logout](logout.md) - End the session
* [Validate](validate.md) - Verify the new token works

---

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Fuser-authentication%2Frefresh).
{% endhint %}
