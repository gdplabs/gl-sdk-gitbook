---
icon: ban-bug
---

# Result Pattern

Handle GL IAM errors using the unified Result pattern.

{% hint style="info" %}
**When to use**: GL IAM Gateway operations return a `Result` - learn to handle success and errors consistently.
{% endhint %}

## Architecture Note

GL IAM uses a **hybrid error handling approach**:

| Layer                       | Pattern        | Rationale                                        |
| --------------------------- | -------------- | ------------------------------------------------ |
| **IAMGateway** (public API) | Result Pattern | Type-safe, explicit error handling for consumers |
| **Providers** (internal)    | Exceptions     | Simpler implementation, idiomatic Python         |

The Gateway wraps provider exceptions into Results, giving you the best of both worlds: clean Result-based APIs for your code, while providers use natural Python exception handling internally.

<details>

<summary>Prerequisites</summary>

* Completed [Login](traditional-iam/user-authentication/login.md)
* Basic understanding of error handling

</details>

## 5-Line Core

```python
result = await gateway.authenticate(credentials, organization_id="default")
if result.is_ok:
    user, token = result.unwrap()
else:
    print(f"Error: {result.error.code}")
```

## Result States

| State        | Check                 | Access                              |
| ------------ | --------------------- | ----------------------------------- |
| Success      | `result.is_ok`        | `result.value` or `result.unwrap()` |
| Error        | `result.is_err`       | `result.error`                      |
| MFA Required | `result.requires_mfa` | `result.mfa_challenge_id`           |

## Step-by-Step

{% stepper %}
{% step %}
**Check Success**

```python
result = await gateway.authenticate(credentials, organization_id="default")

if result.is_ok:
    user, token = result.unwrap()
    print(f"Welcome, {user.email}!")
```
{% endstep %}

{% step %}
**Handle Errors**

```python
if result.is_err:
    error = result.error
    print(f"Code: {error.code}")
    print(f"Message: {error.message}")
```
{% endstep %}

{% step %}
**Pattern Match Errors**

```python
from gl_iam.core.types.result import ErrorCode

if result.is_err:
    match result.error.code:
        case ErrorCode.AUTHENTICATION_FAILED:
            print("Invalid credentials")
        case ErrorCode.ACCOUNT_LOCKED:
            print("Account locked")
        case _:
            print(f"Error: {result.error.message}")
```
{% endstep %}

{% step %}
**Handle MFA**

```python
if result.requires_mfa:
    challenge_id = result.mfa_challenge_id
    print(f"MFA required: {challenge_id}")
```
{% endstep %}

{% step %}
**Expected Output**

```
Welcome, alice@example.com!
```

Or on error:

```
Code: ErrorCode.AUTHENTICATION_FAILED
Message: Invalid credentials
```
{% endstep %}
{% endstepper %}

{% hint style="success" %}
You can handle Results!
{% endhint %}

## Complete Example

Create `result_pattern.py`:

```python
"""GL IAM Result Pattern Example."""

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

    # Success case
    print("--- Success Case ---")
    result = await gateway.authenticate(
        credentials=PasswordCredentials(email="alice@example.com", password="SecurePass123"),
        organization_id="default",
    )

    if result.is_ok:
        user, token = result.unwrap()
        print(f"✓ Logged in as: {user.email}")

    # Error case
    print("\n--- Error Case ---")
    result = await gateway.authenticate(
        credentials=PasswordCredentials(email="alice@example.com", password="wrong"),
        organization_id="default",
    )

    if result.is_err:
        match result.error.code:
            case ErrorCode.AUTHENTICATION_FAILED:
                print("✗ Invalid credentials")
            case ErrorCode.ACCOUNT_LOCKED:
                print("✗ Account locked")
            case _:
                print(f"✗ Error: {result.error.message}")

    # Using unwrap_or for defaults
    print("\n--- Default Value ---")
    result = await gateway.get_user("nonexistent", organization_id="default")
    user = result.unwrap_or(None)
    print(f"User: {user}")  # None

    await provider.close()


if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
uv run result_pattern.py
```

Expected output:

```
--- Success Case ---
✓ Logged in as: alice@example.com

--- Error Case ---
✗ Invalid credentials

--- Default Value ---
User: None
```

## Error Codes Reference

| Category | Codes                                                            |
| -------- | ---------------------------------------------------------------- |
| Auth     | `AUTHENTICATION_FAILED`, `INVALID_CREDENTIALS`, `ACCOUNT_LOCKED` |
| Token    | `INVALID_TOKEN`, `SESSION_EXPIRED`, `SESSION_NOT_FOUND`          |
| User     | `USER_NOT_FOUND`, `USER_ALREADY_EXISTS`                          |
| Config   | `NO_AUTH_PROVIDER`, `NO_USER_STORE`, `NO_SESSION_PROVIDER`       |

## FastAPI Integration

```python
from fastapi import HTTPException
from gl_iam.core.types.result import ErrorCode

def error_to_status(code: ErrorCode) -> int:
    return {
        ErrorCode.AUTHENTICATION_FAILED: 401,
        ErrorCode.INVALID_TOKEN: 401,
        ErrorCode.PERMISSION_DENIED: 403,
        ErrorCode.USER_NOT_FOUND: 404,
        ErrorCode.USER_ALREADY_EXISTS: 409,
    }.get(code, 400)

@app.post("/login")
async def login(email: str, password: str):
    result = await gateway.authenticate(
        credentials=PasswordCredentials(email=email, password=password),
        organization_id="default",
    )

    if result.is_ok:
        user, token = result.unwrap()
        return {"token": token.access_token}

    raise HTTPException(
        status_code=error_to_status(result.error.code),
        detail=result.error.message,
    )
```

## Common Pitfalls

| Pitfall                             | Solution                              |
| ----------------------------------- | ------------------------------------- |
| Calling `unwrap()` without checking | Always check `is_ok` first            |
| Ignoring MFA state                  | Check `requires_mfa` for auth results |
| Generic error handling              | Pattern match on error codes          |

---

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Fresult-pattern).
{% endhint %}
