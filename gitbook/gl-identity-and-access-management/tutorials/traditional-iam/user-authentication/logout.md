---
icon: right-from-bracket
---

# Logout

End a user session and invalidate the token.

{% hint style="info" %}
**When to use**: When the user signs out or you need to invalidate a session for security.
{% endhint %}

<details>

<summary>Prerequisites</summary>

* Completed [Login](/broken/pages/70e495103ab305fdfcba6cdc17d9a7499195c67a)
* Have an access token to invalidate

</details>

## 5-Line Core

```python
result = await gateway.logout(
    access_token=token.access_token,
    organization_id="default",
)
# Token is now invalid
```

## Step-by-Step

{% stepper %}
{% step %}
**Call Logout**

```python
result = await gateway.logout(
    access_token=token.access_token,
    organization_id="default",
)
```
{% endstep %}

{% step %}
**Handle Result**

```python
if result.is_ok:
    print("Logged out successfully")
else:
    print(f"Logout failed: {result.error.message}")
```
{% endstep %}

{% step %}
**Token is Invalid**

```python
# After logout, the token no longer works
validate_result = await gateway.validate_session(
    access_token=token.access_token,
    organization_id="default",
)
print(f"Token valid: {validate_result.is_ok}")  # False
```
{% endstep %}

{% step %}
**Expected Output**

```
Logged out successfully
Token valid: False
```
{% endstep %}
{% endstepper %}

{% hint style="success" %}
You can log out users!
{% endhint %}

## Complete Example

Create `logout.py`:

```python
"""GL IAM Logout Example."""

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
    auth_result = await gateway.authenticate(
        credentials=PasswordCredentials(email="alice@example.com", password="SecurePass123"),
        organization_id="default",
    )
    user, token = auth_result.unwrap()
    print(f"Logged in as: {user.email}")

    # Verify token works
    validate_result = await gateway.validate_session(token.access_token, "default")
    print(f"Before logout - token valid: {validate_result.is_ok}")

    # Logout
    result = await gateway.logout(
        access_token=token.access_token,
        organization_id="default",
    )

    if result.is_ok:
        print("Logged out successfully")

    # Verify token no longer works
    validate_result = await gateway.validate_session(token.access_token, "default")
    print(f"After logout - token valid: {validate_result.is_ok}")

    await provider.close()


if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
uv run logout.py
```

Expected output:

```
Logged in as: alice@example.com
Before logout - token valid: True
Logged out successfully
After logout - token valid: False
```

## Common Pitfalls

| Pitfall                            | Solution                                          |
| ---------------------------------- | ------------------------------------------------- |
| Not clearing client token          | Clear stored token after logout                   |
| Ignoring logout errors             | Log errors but don't block user                   |
| Not logging out on security events | Logout when password changed, suspicious activity |

## Next Steps

* [Login](login.md) - User can login again
* [Result Pattern](../../result-pattern.md) - Handle errors properly

***

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url\&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Fuser-authentication%2Flogout).
{% endhint %}
