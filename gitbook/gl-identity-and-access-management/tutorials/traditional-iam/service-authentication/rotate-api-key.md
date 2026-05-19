---
icon: rotate
---

# Rotate Api Key

Generate a new API key value while preserving the key ID, tier, scopes, and metadata. Optionally keep the old key valid for a grace period to enable zero-downtime rotation in distributed deployments.

{% hint style="info" %}
**When to use**: When a key is compromised, as part of scheduled rotation policy, or whenever you need to replace a service credential without coordinated downtime.
{% endhint %}

<details>

<summary>Prerequisites</summary>

* Completed [Create API Key](create-api-key.md)
* Have an API key ID to rotate

</details>

## 5-Line Core

```python
# Immediate rotation (old key invalidated instantly)
api_key, new_plain_key = await provider.rotate_api_key(key_id=api_key.id, organization_id="default")

# Zero-downtime rotation (old key valid for 1 hour)
api_key, new_plain_key = await provider.rotate_api_key(
    key_id=api_key.id, organization_id="default", grace_period_seconds=3600,
)
# Store new_plain_key securely - only shown once!
```

## When to Rotate

| Scenario                       | Action                                                        |
| ------------------------------ | ------------------------------------------------------------- |
| Key compromised                | Rotate immediately (no grace period)                          |
| Scheduled rotation policy      | Rotate on schedule (e.g., quarterly)                          |
| Distributed deployment         | Use `grace_period_seconds` for zero-downtime rollout          |
| Rate-limit fallback rotation   | Rotate with grace period so in-flight requests keep working   |
| Employee with access leaves    | Rotate as part of offboarding                                 |

## How It Works

Rotation is a single atomic operation — it does **not** create a new row. The `key_id`, `tier`, `scopes`, `parent_key_id`, and `metadata` are preserved; only the secret material changes.

When `grace_period_seconds` is set, the old hash is moved to `previous_key_hash` with `previous_key_expires_at = now + grace_period_seconds`. `validate_api_key()` then accepts either the current or the previous key (constant-time verification, so timing cannot leak which one matched). Expired grace data is lazily cleaned up on the next validation.

**Bounds**: `grace_period_seconds` must be `0` to `604800` (7 days). Values outside this range raise `ValueError`.

## Step-by-Step

{% stepper %}
{% step %}
#### Get Key ID

```python
# From the ApiKey object
key_id = api_key.id

# Or list keys to find the right one
keys = await provider.list_api_keys(organization_id="default")
for key in keys:
    print(f"{key.id}: {key.name}")
```
{% endstep %}

{% step %}
#### Rotate the Key

```python
# Option A: Immediate rotation (old key invalidated)
api_key, new_plain_key = await provider.rotate_api_key(
    key_id=key_id,
    organization_id="default",
)

# Option B: Grace period rotation (old key valid for 1 hour)
api_key, new_plain_key = await provider.rotate_api_key(
    key_id=key_id,
    organization_id="default",
    grace_period_seconds=3600,  # 0-604800 (max 7 days)
)
```
{% endstep %}

{% step %}
#### Store the New Plain Key

```python
# IMPORTANT: new_plain_key is only returned once (HASHED storage mode)
print(f"Key ID: {api_key.id}")                # Unchanged
print(f"Key Preview: {api_key.key_preview}")  # New preview
print(f"New Plain Key: {new_plain_key}")      # Store securely!
```
{% endstep %}

{% step %}
#### Verify Behavior

```python
# New key always works
new_identity = await provider.validate_api_key(new_plain_key)
print(f"New key valid: {new_identity is not None}")

# Old key behavior depends on grace period:
#  - Without grace period: old key fails immediately
#  - With grace period:    old key works until previous_key_expires_at
old_identity = await provider.validate_api_key(old_plain_key)
print(f"Old key valid: {old_identity is not None}")
```
{% endstep %}

{% step %}
#### Expected Output

Without grace period:
```
New key valid: True
Old key valid: False
```

With `grace_period_seconds=3600`:
```
New key valid: True
Old key valid: True   (within 1-hour grace period)
```
{% endstep %}
{% endstepper %}

{% hint style="success" %}
You can rotate API keys!
{% endhint %}

## Complete Example

Create `rotate_api_key.py`:

```python
"""GL IAM Rotate API Key Example."""

import asyncio

from gl_iam.providers.postgresql import (
    PostgreSQLProvider,
    PostgreSQLConfig,
)

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/gliam"


async def main():
    # Setup provider (implements all 6 protocols)
    config = PostgreSQLConfig(
        database_url=DATABASE_URL,
        secret_key="your-secret-key-min-32-characters-long",
        default_org_id="default",
        # Disable third-party provider so no encryption key is required.
        # Omit this line (and set `encryption_key=...`) if you use third-party integrations.
        enable_third_party_provider=False,
    )
    provider = PostgreSQLProvider(config)

    # Create a key to rotate
    api_key, old_plain_key = await provider.create_api_key(
        name="backend-service",
        organization_id="default",
        scopes=["api:read", "api:write"],
    )
    print(f"Created key: {api_key.id}")
    print(f"  Original preview: {api_key.key_preview}")

    # Verify the original key works
    identity = await provider.validate_api_key(old_plain_key)
    print(f"  Original key valid: {identity is not None}")

    # Rotate with a 1-hour grace period
    rotated_key, new_plain_key = await provider.rotate_api_key(
        key_id=api_key.id,
        organization_id="default",
        grace_period_seconds=3600,  # Old key valid for 1 hour
    )
    print(f"\nRotated (with 1-hour grace period)!")
    print(f"  Key ID: {rotated_key.id}")           # Unchanged
    print(f"  New preview: {rotated_key.key_preview}")

    # New key works
    new_identity = await provider.validate_api_key(new_plain_key)
    print(f"\nNew key valid: {new_identity is not None}")

    # Old key still works during the grace period
    old_identity = await provider.validate_api_key(old_plain_key)
    print(f"Old key valid (grace period): {old_identity is not None}")  # True

    # For immediate invalidation, omit grace_period_seconds:
    # rotated_key, new_plain_key = await provider.rotate_api_key(
    #     key_id=api_key.id, organization_id="default",
    # )

    await provider.close()


if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
uv run rotate_api_key.py
```

Expected output:

```
Created key: 550e8400-e29b-41d4-a716-446655440000
  Original preview: gliam_Yu
  Original key valid: True

Rotated (with 1-hour grace period)!
  Key ID: 550e8400-e29b-41d4-a716-446655440000
  New preview: gliam_CW

New key valid: True
Old key valid (grace period): True
```

Note: the key ID is preserved across rotation. The preview changes because it is derived from the new plain key.

## Rotation vs. Create-then-Revoke

| Approach                           | Key ID  | Rollout Safety    | Consumer Impact                    |
| ---------------------------------- | ------- | ----------------- | ---------------------------------- |
| `rotate_api_key(grace_period_seconds=N)` | Preserved | Zero-downtime | Dual-key window; swap on schedule  |
| `rotate_api_key()` (no grace)      | Preserved | Immediate cutover | Any in-flight request with old key fails |
| `create_api_key` + `revoke_api_key` | New      | Manual coordination | New ID breaks consumers keyed by ID |

Prefer `rotate_api_key` unless you specifically need a new key ID (e.g., you are splitting one service into two).

## Common Pitfalls

| Pitfall                               | Solution                                                                |
| ------------------------------------- | ----------------------------------------------------------------------- |
| Not storing the new plain key         | Store `new_plain_key` immediately — only returned once (HASHED mode)    |
| Rotating before consumers roll over   | Use `grace_period_seconds` sized to your deploy/rollout window          |
| Grace period too long                 | Maximum is `604800` seconds (7 days); values above raise `ValueError`   |
| Rotating a revoked key                | `rotate_api_key` raises `ValueError`; revoked keys cannot be rotated    |
| Compromise response with grace period | Use `revoke_api_key` — calling `rotate_api_key()` without a grace period does **not** shorten a previously-set grace window, so the original key can still validate until the earlier grace expires |
| Needing to retrieve the new secret later | Create with `storage_mode=ENCRYPTED`; use `retrieve_api_key_secret` afterwards |

---

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Fservice-authentication%2Frotate-api-key).
{% endhint %}
