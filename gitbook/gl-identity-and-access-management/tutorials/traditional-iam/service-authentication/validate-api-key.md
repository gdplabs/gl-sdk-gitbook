---
icon: badge-check
---

# Validate Api Key

Verify an incoming API key and get its identity.

{% hint style="info" %}
**When to use**: On every protected API endpoint that accepts API key authentication.
{% endhint %}

<details>

<summary>Prerequisites</summary>

* Completed [Create API Key](create-api-key.md)
* Have an API key to validate

</details>

## 5-Line Core

```python
identity = await api_key_provider.validate_api_key(api_key)
if identity:
    print(f"Valid! Scopes: {identity.scopes}")
else:
    print("Invalid key")
```

## Step-by-Step

{% stepper %}
{% step %}
**Extract API Key from Request**

```python
# Typically from X-API-Key header
api_key = request.headers.get("X-API-Key")
if not api_key:
    raise HTTPException(status_code=401, detail="Missing API key")
```
{% endstep %}

{% step %}
**Validate the Key**

```python
identity = await api_key_provider.validate_api_key(api_key)
```
{% endstep %}

{% step %}
**Check Result**

```python
if identity is None:
    raise HTTPException(status_code=401, detail="Invalid API key")

print(f"Key ID: {identity.api_key_id}")
print(f"Tier: {identity.tier}")
print(f"Scopes: {identity.scopes}")
```
{% endstep %}

{% step %}
**Check Scopes**

```python
if not identity.has_scope("api:write"):
    raise HTTPException(status_code=403, detail="Insufficient scope")

# Proceed with operation
```
{% endstep %}

{% step %}
**Expected Output**

```
Key ID: 550e8400-e29b-41d4-a716-446655440000
Tier: organization
Scopes: ['api:read', 'api:write']
```
{% endstep %}
{% endstepper %}

{% hint style="success" %}
You can validate API keys!
{% endhint %}

## Complete Example

Create `validate_api_key.py`:

```python
"""GL IAM Validate API Key Example."""

import asyncio

from gl_iam.providers.postgresql import (
    PostgreSQLProvider,
    PostgreSQLConfig,
)

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/gliam"


async def main():
    # Setup provider (implements all 6 protocols)
    config = PostgreSQLConfig(database_url=DATABASE_URL)
    provider = PostgreSQLProvider(config)

    # Create a key to validate (normally you'd have this already)
    api_key, plain_key = await provider.create_api_key(
        name="test-key",
        organization_id="default",
        scopes=["api:read", "api:write"],
    )
    print(f"Created key: {api_key.key_preview}...")

    # Validate the key
    identity = await provider.validate_api_key(plain_key)

    if identity:
        print("\n Key is valid!")
        print(f"  Key ID: {identity.api_key_id}")
        print(f"  Name: {identity.name}")
        print(f"  Tier: {identity.tier.value}")
        print(f"  Scopes: {identity.scopes}")
        print(f"  Organization: {identity.organization_id}")

        # Check specific scope
        if identity.has_scope("api:write"):
            print("\n Key has write access")
        if identity.has_scope("admin:all"):
            print(" Key has admin access")
        else:
            print(" Key does not have admin access")
    else:
        print("\n Key is invalid")

    # Try with invalid key
    print("\n--- Testing invalid key ---")
    invalid_identity = await provider.validate_api_key("invalid-key")
    if invalid_identity is None:
        print(" Invalid key rejected correctly")

    await provider.close()


if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
uv run validate_api_key.py
```

Expected output:

```
Created key: sk_live_8...

Key is valid!
  Key ID: 550e8400-e29b-41d4-a716-446655440000
  Name: test-key
  Tier: organization
  Scopes: ['api:read', 'api:write']
  Organization: default

Key has write access
Key does not have admin access

--- Testing invalid key ---
Invalid key rejected correctly
```

## FastAPI Integration

```python
from fastapi import Depends, HTTPException, Header
from gl_iam.providers.postgresql import PostgreSQLProvider

# Initialize at app startup
provider: PostgreSQLProvider = None  # Set during startup

async def get_api_key_identity(x_api_key: str = Header(...)):
    """Dependency to validate API key."""
    identity = await provider.validate_api_key(x_api_key)
    if identity is None:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return identity


def require_scope(scope: str):
    """Dependency factory to require a specific scope."""
    async def check_scope(identity = Depends(get_api_key_identity)):
        if not identity.has_scope(scope):
            raise HTTPException(status_code=403, detail=f"Missing scope: {scope}")
        return identity
    return check_scope


@app.get("/data")
async def get_data(identity = Depends(require_scope("api:read"))):
    return {"message": "You have read access"}
```

## Common Pitfalls

| Pitfall              | Solution                                   |
| -------------------- | ------------------------------------------ |
| Not checking scopes  | Always verify required scopes              |
| Exposing key details | Only log key ID, never full key            |
| Wrong status codes   | 401 for invalid key, 403 for missing scope |

---

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Fservice-authentication%2Fvalidate-api-key).
{% endhint %}
