---
icon: ban
---

# Revoke Api Key

Invalidate an API key when it's compromised or no longer needed.

{% hint style="info" %}
**When to use**: When a key is compromised, a service is decommissioned, or for regular key rotation.
{% endhint %}

<details>

<summary>Prerequisites</summary>

* Completed [Create API Key](create-api-key.md)
* Have an API key ID to revoke

</details>

## 5-Line Core

```python
success = await api_key_provider.revoke_api_key(
    key_id=api_key.id,
    organization_id="default",
)
# Key is now invalid
```

## When to Revoke

| Scenario               | Action                     |
| ---------------------- | -------------------------- |
| Key compromised        | Revoke immediately         |
| Service decommissioned | Revoke before removal      |
| Employee leaves        | Revoke personal keys       |
| Regular rotation       | Revoke after new key works |

## Step-by-Step

{% stepper %}
{% step %}
#### Get Key ID

```python
# From the ApiKey object
key_id = api_key.id

# Or list keys to find the right one
keys = await api_key_provider.list_api_keys(
    organization_id="default"
)
for key in keys:
    print(f"{key.id}: {key.name}")
```
{% endstep %}

{% step %}
#### Revoke the Key

```python
success = await api_key_provider.revoke_api_key(
    key_id=key_id,
    organization_id="default",
)
```
{% endstep %}

{% step %}
#### Verify Revocation

```python
if success:
    print("Key revoked successfully")

    # Verify key no longer works
    identity = await api_key_provider.validate_api_key(plain_key)
    print(f"Key valid: {identity is not None}")  # False
```
{% endstep %}

{% step %}
#### Expected Output

```
Key revoked successfully
Key valid: False
```
{% endstep %}
{% endstepper %}

{% hint style="success" %}
You can revoke API keys!
{% endhint %}

## Complete Example

Create `revoke_api_key.py`:

```python
"""GL IAM Revoke API Key Example."""

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

    # Create a key to revoke
    api_key, plain_key = await provider.create_api_key(
        name="key-to-revoke",
        organization_id="default",
        scopes=["api:read"],
    )
    print(f"Created key: {api_key.id}")

    # Verify it works before revocation
    identity = await provider.validate_api_key(plain_key)
    print(f"Before revoke - valid: {identity is not None}")

    # Revoke the key
    success = await provider.revoke_api_key(
        key_id=api_key.id,
        organization_id="default",
    )

    if success:
        print("Key revoked successfully!")
    else:
        print("Failed to revoke key")

    # Verify it no longer works
    identity = await provider.validate_api_key(plain_key)
    print(f"After revoke - valid: {identity is not None}")

    await provider.close()


if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
uv run revoke_api_key.py
```

Expected output:

```
Created key: 550e8400-e29b-41d4-a716-446655440000
Before revoke - valid: True
Key revoked successfully!
After revoke - valid: False
```

## Rotating vs. Revoking

For scheduled rotation or replacing a key without downtime, use `rotate_api_key` — it preserves the key ID, tier, and scopes, and supports a grace period during which both the old and new secrets validate.

See [Rotate API Key](rotate-api-key.md) for the full tutorial, including the zero-downtime `grace_period_seconds` workflow.

Use **revoke** (this page) when you want the key gone — compromised credentials, decommissioned services, or offboarding.

## Common Pitfalls

| Pitfall                          | Solution                        |
| -------------------------------- | ------------------------------- |
| Revoking before new key deployed | Create and deploy new key first |
| Not notifying stakeholders       | Coordinate with key users       |
| Losing key ID                    | Track key IDs in secure storage |

---

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Fservice-authentication%2Frevoke-api-key).
{% endhint %}
