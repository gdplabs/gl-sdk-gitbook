---
icon: rotate
---

# Rotate Consumer Secret

Generate a new consumer secret for a partner. Optionally keep the old secret valid for a grace period to enable zero-downtime rotation in distributed deployments.

{% hint style="info" %}
**When to use**: When a consumer secret is compromised, an employee with access leaves, or as part of regular secret rotation policy.
{% endhint %}

<details>

<summary>Prerequisites</summary>

* Completed [Register Partner](register-partner.md)
* Have a partner ID to rotate

</details>

## 5-Line Core

```python
# Immediate rotation (old secret invalidated instantly)
result = await provider.rotate_consumer_secret(partner_id=partner.id)

# Zero-downtime rotation (old secret valid for 1 hour)
result = await provider.rotate_consumer_secret(partner_id=partner.id, grace_period_seconds=3600)
# Store result.unwrap().consumer_secret securely - only shown once!
```

## When to Rotate

| Scenario                 | Action                            |
| ------------------------ | --------------------------------- |
| Secret compromised       | Rotate immediately                |
| Employee with access leaves | Rotate as part of offboarding  |
| Regular rotation policy  | Rotate on schedule (e.g., quarterly) |
| Distributed deployment   | Use `grace_period_seconds` for zero-downtime |
| Partner requests reset   | Rotate and share new secret       |

## Step-by-Step

{% stepper %}
{% step %}
#### Get Partner ID

```python
# From the registration result
partner_id = registration.partner.id

# Or look up by consumer key
lookup = await provider.get_partner_by_consumer_key("ck_live_a1b2c3d4...")
if lookup.is_ok:
    partner_id = lookup.unwrap().id
```
{% endstep %}

{% step %}
#### Rotate the Secret

```python
# Option A: Immediate rotation (old secret invalidated)
result = await provider.rotate_consumer_secret(partner_id=partner_id)

# Option B: Grace period rotation (old secret valid for 1 hour)
result = await provider.rotate_consumer_secret(
    partner_id=partner_id,
    grace_period_seconds=3600,  # 0-604800 (max 7 days)
)
```
{% endstep %}

{% step %}
#### Store the New Secret

```python
if result.is_ok:
    registration = result.unwrap()
    print(f"Consumer Key: {registration.consumer_key}")  # Unchanged
    print(f"New Secret: {registration.consumer_secret}")  # Store securely!
else:
    print(f"Error: {result.error.code} - {result.error.message}")
```
{% endstep %}

{% step %}
#### Verify Old Secret Behavior

```python
# Without grace period: old secret fails immediately
# With grace period: old secret works until grace period expires
old_result = await provider.validate_partner_signature(
    consumer_key=registration.consumer_key,
    signature=old_signature,  # Computed with old secret
    payload=payload,
    timestamp=timestamp,
)
print(f"Old secret valid: {old_result.is_ok}")
# True if within grace period, False if no grace period or expired
```
{% endstep %}

{% step %}
#### Expected Output

Without grace period:
```
Consumer Key: ck_live_a1b2c3d4e5f6...
New Secret: cs_live_new_secret_here...
Old secret valid: False
```

With `grace_period_seconds=3600`:
```
Consumer Key: ck_live_a1b2c3d4e5f6...
New Secret: cs_live_new_secret_here...
Old secret valid: True   (within 1-hour grace period)
```
{% endstep %}
{% endstepper %}

{% hint style="success" %}
You can rotate consumer secrets!
{% endhint %}

## Complete Example

Create `rotate_consumer_secret.py`:

```python
"""GL IAM Rotate Consumer Secret Example."""

import asyncio
import hashlib
import hmac
from datetime import datetime, timezone

from gl_iam.core.crypto_config import CryptoConfig, EncryptionAlgorithm
from gl_iam.core.types.sso import SSOPartnerCreate
from gl_iam.providers.postgresql import (
    PostgreSQLPartnerRegistryProvider,
    PostgreSQLConfig,
)

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/gliam"
SECRET_KEY = "your-secret-key-min-32-characters-long"  # For JWT signing
# Generate with: python -c "import secrets, base64; print(base64.urlsafe_b64encode(secrets.token_bytes(32)).decode())"
ENCRYPTION_KEY = "<YOUR_ENCRYPTION_KEY>"


def compute_signature(consumer_key: str, consumer_secret: str, payload: str) -> tuple[str, str]:
    """Compute HMAC-SHA256 signature (partner side)."""
    timestamp = datetime.now(timezone.utc).isoformat()
    signing_string = f"{timestamp}|{consumer_key}|{payload}"
    signature = hmac.new(
        consumer_secret.encode(),
        signing_string.encode(),
        hashlib.sha256,
    ).hexdigest()
    return signature, timestamp


async def main():
    # Setup
    config = PostgreSQLConfig(
        database_url=DATABASE_URL,
        secret_key=SECRET_KEY,
        crypto_config=CryptoConfig(
            encryption_keys={1: ENCRYPTION_KEY},
            encryption_algorithm=EncryptionAlgorithm.AES_256_GCM,
        ),
    )
    provider = PostgreSQLPartnerRegistryProvider(config)

    # Register partner
    reg_result = await provider.register_partner(
        SSOPartnerCreate(partner_name="Acme Corp", org_id="default")
    )
    registration = reg_result.unwrap()
    partner_id = registration.partner.id
    consumer_key = registration.consumer_key
    old_secret = registration.consumer_secret
    print(f"Registered: {registration.partner.partner_name}")
    print(f"  Consumer Key: {consumer_key}")
    print(f"  Original Secret: {old_secret[:16]}...")

    # Verify old secret works
    payload = '{"email": "alice@example.com"}'
    sig, ts = compute_signature(consumer_key, old_secret, payload)
    result = await provider.validate_partner_signature(
        consumer_key=consumer_key, signature=sig, payload=payload, timestamp=ts,
    )
    print(f"\nOld secret works: {result.is_ok}")

    # Rotate the secret with a 1-hour grace period
    rotate_result = await provider.rotate_consumer_secret(
        partner_id=partner_id,
        grace_period_seconds=3600,  # Old secret valid for 1 hour
    )
    new_registration = rotate_result.unwrap()
    new_secret = new_registration.consumer_secret
    print(f"\nRotated (with 1-hour grace period)!")
    print(f"  Consumer Key: {new_registration.consumer_key}")  # Same
    print(f"  New Secret: {new_secret[:16]}...")

    # Verify new secret works
    sig, ts = compute_signature(consumer_key, new_secret, payload)
    result = await provider.validate_partner_signature(
        consumer_key=consumer_key, signature=sig, payload=payload, timestamp=ts,
    )
    print(f"\nNew secret works: {result.is_ok}")

    # Old secret still works during grace period
    sig, ts = compute_signature(consumer_key, old_secret, payload)
    result = await provider.validate_partner_signature(
        consumer_key=consumer_key, signature=sig, payload=payload, timestamp=ts,
    )
    print(f"Old secret works (grace period): {result.is_ok}")  # True

    # For immediate invalidation, omit grace_period_seconds:
    # await provider.rotate_consumer_secret(partner_id=partner_id)

    await provider.close()


if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
uv run rotate_consumer_secret.py
```

Expected output:

```
Registered: Acme Corp
  Consumer Key: ck_live_a1b2c3d4e5f6...
  Original Secret: cs_live_x9y8z7w6...

Old secret works: True

Rotated (with 1-hour grace period)!
  Consumer Key: ck_live_a1b2c3d4e5f6...
  New Secret: cs_live_new_a1b2c3d4...

New secret works: True
Old secret works (grace period): True
```

## Common Pitfalls

| Pitfall                          | Solution                              |
| -------------------------------- | ------------------------------------- |
| Not storing new secret           | Store immediately — only shown once   |
| Rotating before partner updates  | Use `grace_period_seconds` for zero-downtime rotation |
| Losing partner ID                | Look up via `get_partner_by_consumer_key` |
| Grace period too long            | Maximum is 604800 seconds (7 days)    |
| Distributed deploy failures      | Set `grace_period_seconds=3600` (1 hour) to allow gradual rollout |

---

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Fsso-partner-registry%2Frotate-consumer-secret).
{% endhint %}
