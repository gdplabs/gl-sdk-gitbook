---
icon: list-check
---

# Manage Partner Lifecycle

Manage the full partner lifecycle — deactivate partners temporarily, reactivate them, and list partners with filters.

{% hint style="info" %}
**When to use**: When you need to disable a partner that is misbehaving, no longer needed, or needs temporary restriction.
{% endhint %}

<details>

<summary>Prerequisites</summary>

* Completed [Register Partner](register-partner.md)
* Have a partner ID to manage

</details>

## 5-Line Core

```python
# Deactivate (reversible)
await provider.deactivate_partner(partner_id)

# Reactivate
await provider.reactivate_partner(partner_id)
```

## Partner States

| State        | Can Sign? | Can Reactivate? | Signatures Valid? |
| ------------ | --------- | --------------- | ----------------- |
| **Active**   | Yes       | N/A             | Yes               |
| **Inactive** | No        | Yes             | No                |

## Step-by-Step

{% stepper %}
{% step %}
**Deactivate a Partner**

Deactivation is **reversible** — use it when a partner needs temporary restriction:

```python
result = await provider.deactivate_partner(partner_id)
if result.is_ok:
    print("Partner deactivated successfully")
else:
    print(f"Error: {result.error.code} - {result.error.message}")
```
{% endstep %}

{% step %}
**Verify Signature Rejection**

Signatures from deactivated partners are rejected immediately:

```python
result = await provider.validate_partner_signature(
    consumer_key=consumer_key,
    signature=signature,
    payload=payload,
    timestamp=timestamp,
)

if not result.is_ok:
    print(f"Error: {result.error.code}")  # PARTNER_INACTIVE
```

```
Error: partner_inactive
```
{% endstep %}

{% step %}
**Reactivate a Partner**

```python
result = await provider.reactivate_partner(partner_id)
if result.is_ok:
    print("Partner reactivated — can sign requests again")
```
{% endstep %}

{% step %}
**List Partners**

List partners with optional filtering:

```python
# All active partners
result = await provider.list_partners(is_active=True)
if result.is_ok:
    partners = result.unwrap()
    print(f"Active partners: {len(partners)}")
    for p in partners:
        print(f"  {p.id}: {p.partner_name} (active: {p.is_active})")

# Filter by organization
result = await provider.list_partners(
    organization_id="default",
    is_active=None,  # All statuses
)
if result.is_ok:
    partners = result.unwrap()
    print(f"\nAll partners in 'default': {len(partners)}")

# All partners (no filters)
result = await provider.list_partners()
```
{% endstep %}

{% step %}
**Expected Output**

```
Partner deactivated successfully
Error: partner_inactive
Partner reactivated — can sign requests again
Active partners: 3
  partner-001: Acme Corp (active: True)
  partner-002: Beta Inc (active: True)
  partner-003: Gamma Ltd (active: True)

All partners in 'default': 4
```
{% endstep %}
{% endstepper %}

{% hint style="success" %}
You've learned how to manage the full partner lifecycle — deactivate, reactivate, and list partners!
{% endhint %}

## Error Codes Reference

| Error Code                  | Description                                |
| --------------------------- | ------------------------------------------ |
| `partner_not_found`         | Consumer key or partner ID not recognized  |
| `partner_inactive`          | Partner has been deactivated               |
| `invalid_partner_signature` | HMAC-SHA256 signature mismatch             |
| `partner_already_exists`    | Partner with same name already registered  |
| `no_partner_registry`       | Provider does not support partner registry |
| `signature_expired`         | Timestamp outside tolerance window         |
| `email_domain_not_allowed`  | Email domain not in partner's allowed list |
| `max_users_exceeded`        | Partner has reached maximum user cap       |

## Complete Example

Create `manage_partner_lifecycle.py`:

```python
"""GL IAM Manage Partner Lifecycle Example."""

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

    # Register a partner
    reg_result = await provider.register_partner(
        SSOPartnerCreate(partner_name="Lifecycle Demo", org_id="default")
    )
    registration = reg_result.unwrap()
    partner_id = registration.partner.id
    consumer_key = registration.consumer_key
    consumer_secret = registration.consumer_secret
    print(f"1. Registered: {registration.partner.partner_name}")

    # Helper to compute and validate signature
    async def try_signature() -> bool:
        payload = '{"test": true}'
        timestamp = datetime.now(timezone.utc).isoformat()
        signing_string = f"{timestamp}|{consumer_key}|{payload}"
        signature = hmac.new(
            consumer_secret.encode(), signing_string.encode(), hashlib.sha256,
        ).hexdigest()
        result = await provider.validate_partner_signature(
            consumer_key=consumer_key, signature=signature,
            payload=payload, timestamp=timestamp,
        )
        return result.is_ok

    # Verify active partner can sign
    print(f"2. Signature valid (active): {await try_signature()}")

    # Deactivate
    deactivate_result = await provider.deactivate_partner(partner_id)
    print(f"3. Deactivated: {deactivate_result.is_ok}")

    # Verify deactivated partner is rejected
    print(f"4. Signature valid (inactive): {await try_signature()}")

    # Reactivate
    reactivate_result = await provider.reactivate_partner(partner_id)
    print(f"5. Reactivated: {reactivate_result.is_ok}")

    # Verify reactivated partner can sign again
    print(f"6. Signature valid (reactivated): {await try_signature()}")

    # List all partners
    list_result = await provider.list_partners(organization_id="default")
    if list_result.is_ok:
        partners = list_result.unwrap()
        print(f"\n7. Partners in 'default': {len(partners)}")
        for p in partners:
            print(f"   {p.id}: {p.partner_name} (active: {p.is_active})")

    # List only active partners
    active_result = await provider.list_partners(is_active=True)
    if active_result.is_ok:
        print(f"\n8. Active partners: {len(active_result.unwrap())}")

    await provider.close()


if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
uv run manage_partner_lifecycle.py
```

Expected output:

```
1. Registered: Lifecycle Demo
2. Signature valid (active): True
3. Deactivated: True
4. Signature valid (inactive): False
5. Reactivated: True
6. Signature valid (reactivated): True

7. Partners in 'default': 1
   550e8400-...: Lifecycle Demo (active: True)

8. Active partners: 1
```

## Common Pitfalls

| Pitfall                        | Solution                                                      |
| ------------------------------ | ------------------------------------------------------------- |
| Deactivating without notifying | Coordinate with partner before deactivation                   |
| Not checking error codes       | Always check `result.error.code` for specific failure reasons |
| Missing organization filter    | Pass `organization_id` to scope `list_partners` results       |
| Confusing deactivate vs revoke | Unlike agents, deactivation is always reversible              |
| Confusing deactivate vs update | Use [Update Partner](update-partner.md) to edit scope/policy fields (origins, max_users, etc.) — don't deactivate-then-re-register, which forces secret rotation unnecessarily |

## Next Steps

* [Register Partner](register-partner.md) — Register new partners
* [Validate Partner Signature](validate-partner-signature.md) — Validate incoming SSO requests
* [Rotate Consumer Secret](rotate-consumer-secret.md) — Rotate secrets for security
* [Update Partner](update-partner.md) — Edit scope/policy fields without rotating the secret
* [Result Pattern](../../result-pattern.md) — Handle errors from lifecycle operations

***

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url\&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Fsso-partner-registry%2Fmanage-partner-lifecycle).
{% endhint %}
