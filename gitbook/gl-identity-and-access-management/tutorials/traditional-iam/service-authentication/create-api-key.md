---
icon: key
---

# Create Api Key

Generate an API key for service authentication.

{% hint style="info" %}
**When to use**: When you need programmatic access for backend services, CI/CD pipelines, or automation scripts.
{% endhint %}

<details>

<summary>Prerequisites</summary>

* Completed [Quickstart](../quickstart/quickstart-postgresql.md)
* A running PostgreSQL instance with GL IAM configured

</details>

## 5-Line Core

```python
from gl_iam.providers.postgresql import PostgreSQLProvider, PostgreSQLConfig

config = PostgreSQLConfig(database_url="postgresql+asyncpg://...")
provider = PostgreSQLProvider(config)
api_key, plain_key = await provider.create_api_key(
    name="my-service",
    organization_id="default",
    scopes=["api:read", "api:write"],
)
# Store plain_key securely - only shown once!
```

## Key Tiers

| Tier           | Use Case         | Requirements        |
| -------------- | ---------------- | ------------------- |
| `PLATFORM`     | System bootstrap | No org, no user     |
| `ORGANIZATION` | Service keys     | Requires org        |
| `PERSONAL`     | User automation  | Requires org + user |

## Step-by-Step

{% stepper %}
{% step %}
#### Setup Provider

```python
from gl_iam.providers.postgresql import (
    PostgreSQLProvider,
    PostgreSQLConfig,
)

config = PostgreSQLConfig(
    database_url="postgresql+asyncpg://postgres:postgres@localhost:5432/gliam"
)
provider = PostgreSQLProvider(config)
# PostgreSQLProvider implements all 6 protocols including ApiKeyProvider
```
{% endstep %}

{% step %}
#### Create Organization Key

```python
from gl_iam.core.types.api_key import ApiKeyTier

api_key, plain_key = await provider.create_api_key(
    name="backend-service",
    tier=ApiKeyTier.ORGANIZATION,
    organization_id="default",
    scopes=["api:read", "api:write"],
)
```
{% endstep %}

{% step %}
#### Store the Plain Key

```python
# IMPORTANT: plain_key is only returned once!
print(f"Key ID: {api_key.id}")
print(f"Key Preview: {api_key.key_preview}")
print(f"Plain Key: {plain_key}")  # Store this securely!
```
{% endstep %}

{% step %}
#### Optional: Set Expiration

```python
from datetime import datetime, timedelta, timezone

api_key, plain_key = await provider.create_api_key(
    name="temp-key",
    organization_id="default",
    scopes=["api:read"],
    expires_at=datetime.now(timezone.utc) + timedelta(days=30),
)
```
{% endstep %}

{% step %}
#### Expected Output

```
Key ID: 550e8400-e29b-41d4-a716-446655440000
Key Preview: sk_live_8
Plain Key: sk_live_8x7y6z5w4v3u2t1s...
```
{% endstep %}
{% endstepper %}

{% hint style="success" %}
You can create API keys!
{% endhint %}

## Complete Example

Create `create_api_key.py`:

```python
"""GL IAM Create API Key Example."""

import asyncio

from gl_iam.core.types.api_key import ApiKeyTier
from gl_iam.providers.postgresql import (
    PostgreSQLProvider,
    PostgreSQLConfig,
)

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/gliam"


async def main():
    # Step 1: Setup provider (implements all 6 protocols)
    config = PostgreSQLConfig(database_url=DATABASE_URL)
    provider = PostgreSQLProvider(config)

    # Step 2: Create organization-level API key
    api_key, plain_key = await provider.create_api_key(
        name="backend-service",
        tier=ApiKeyTier.ORGANIZATION,
        organization_id="default",
        scopes=["api:read", "api:write"],
    )

    print(f"Created API Key!")
    print(f"  ID: {api_key.id}")
    print(f"  Name: {api_key.name}")
    print(f"  Tier: {api_key.tier.value}")
    print(f"  Scopes: {api_key.scopes}")
    print(f"  Preview: {api_key.key_preview}")
    print(f"  Plain Key: {plain_key}")
    print("\n  Store the plain key securely - it won't be shown again!")

    await provider.close()


if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
uv run create_api_key.py
```

Expected output:

```
Created API Key!
  ID: 550e8400-e29b-41d4-a716-446655440000
  Name: backend-service
  Tier: organization
  Scopes: ['api:read', 'api:write']
  Preview: sk_live_8
  Plain Key: sk_live_8x7y6z5w4v3u2t1s...

  Store the plain key securely - it won't be shown again!
```

## Using with IAMGateway

For service-only authentication, use `for_service_auth`:

```python
from gl_iam import IAMGateway
from gl_iam.providers.postgresql import (
    PostgreSQLProvider,
    PostgreSQLConfig,
)

config = PostgreSQLConfig(database_url=DATABASE_URL)
provider = PostgreSQLProvider(config)

# Minimal gateway for service authentication only
gateway = IAMGateway.for_service_auth(provider)

# API key operations via gateway
api_key, plain_key = await gateway.api_key_provider.create_api_key(
    name="my-service",
    organization_id="default",
    scopes=["api:read"],
)
identity = await gateway.api_key_provider.validate_api_key(plain_key)
```

If you also need user authentication, use `from_fullstack_provider` instead:

```python
gateway = IAMGateway.from_fullstack_provider(provider)
```

## Common Pitfalls

| Pitfall               | Solution                            |
| --------------------- | ----------------------------------- |
| Not storing plain key | Store immediately - only shown once |
| Too broad scopes      | Use minimum required scopes         |
| No expiration         | Set expiration for security         |

---

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Fservice-authentication%2Fcreate-api-key).
{% endhint %}
