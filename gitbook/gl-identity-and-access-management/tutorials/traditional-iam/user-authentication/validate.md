---
icon: badge-check
---

# Validate

Verify an access token and get the associated user.

{% hint style="info" %}
**When to use**: On every protected API request to verify the token is valid.
{% endhint %}

<details>

<summary>Prerequisites</summary>

* Completed [Login](/broken/pages/70e495103ab305fdfcba6cdc17d9a7499195c67a)
* Have an access token from authentication

</details>

## 5-Line Core

```python
result = await gateway.validate_session(
    access_token=token.access_token,
    organization_id="default",
)
user = result.unwrap()
```

## Step-by-Step

{% stepper %}
{% step %}
**Extract Token from Request**

```python
# Typically from Authorization header
authorization = request.headers.get("Authorization")
if authorization and authorization.startswith("Bearer "):
    access_token = authorization.removeprefix("Bearer ")
```
{% endstep %}

{% step %}
**Validate Token**

```python
result = await gateway.validate_session(
    access_token=access_token,
    organization_id="default",
)
```
{% endstep %}

{% step %}
**Handle Result**

```python
if result.is_ok:
    user = result.value
    print(f"Token valid! User: {user.email}")
else:
    print(f"Token invalid: {result.error.code}")
```
{% endstep %}

{% step %}
**Expected Output**

```
Token valid! User: alice@example.com
```
{% endstep %}
{% endstepper %}

{% hint style="success" %}
You can validate tokens!
{% endhint %}

## Complete Example

Create `validate.py`:

```python
"""GL IAM Token Validation Example."""

import asyncio

from gl_iam import IAMGateway
from gl_iam.core.types import PasswordCredentials
from gl_iam.core.types.result import ErrorCode
from gl_iam.providers.postgresql import PostgreSQLProvider, PostgreSQLConfig

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/gliam"


async def main():
    # Setup
    config = PostgreSQLConfig(database_url=DATABASE_URL)
    provider = PostgreSQLProvider(config)
    gateway = IAMGateway.from_fullstack_provider(provider)

    # First, login to get a token
    auth_result = await gateway.authenticate(
        credentials=PasswordCredentials(email="alice@example.com", password="SecurePass123"),
        organization_id="default",
    )
    user, token = auth_result.unwrap()
    print(f"Got token: {token.access_token[:30]}...")

    # Validate the token (simulating a subsequent request)
    result = await gateway.validate_session(
        access_token=token.access_token,
        organization_id="default",
    )

    if result.is_ok:
        user = result.value
        print(f"Token valid! User: {user.email}")
    else:
        print(f"Token invalid: {result.error.code}")

    # Try with invalid token
    bad_result = await gateway.validate_session(
        access_token="invalid-token",
        organization_id="default",
    )

    if bad_result.is_err:
        match bad_result.error.code:
            case ErrorCode.SESSION_NOT_FOUND:
                print("Invalid token: session not found")
            case ErrorCode.INVALID_TOKEN:
                print("Invalid token: malformed")
            case _:
                print(f"Invalid token: {bad_result.error.code}")

    await provider.close()


if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
uv run validate.py
```

Expected output:

```
Got token: eyJhbGciOiJIUzI1NiIsInR5cCI6...
Token valid! User: alice@example.com
Invalid token: session not found
```

## FastAPI Integration

For a ready-made dependency, use `get_current_user` from `gl_iam.fastapi`. To build your own:

```python
from fastapi import Depends, HTTPException, Header
from gl_iam.fastapi import get_iam_gateway

async def get_current_user(authorization: str = Header(...)):
    """Dependency to get current user from token."""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    gateway = get_iam_gateway()
    token = authorization.removeprefix("Bearer ")
    result = await gateway.validate_session(token, organization_id="default")

    if result.is_err:
        raise HTTPException(status_code=401, detail="Invalid token")

    return result.value


@app.get("/me")
async def get_me(user = Depends(get_current_user)):
    return {"email": user.email, "id": user.id}
```

## Common Pitfalls

| Pitfall                       | Solution                                  |
| ----------------------------- | ----------------------------------------- |
| Using query params for tokens | Use `Authorization` header instead        |
| Forgetting `organization_id`  | Always validate in correct tenant context |
| Logging full tokens           | Log only a short prefix if needed         |

## Next Steps

* [Refresh](refresh.md) - Renew expired tokens
* [User](user.md) - Work with the returned User object

---

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Fuser-authentication%2Fvalidate).
{% endhint %}
