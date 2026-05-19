---
icon: pen-to-square
---

# Update Partner

Edit an SSO partner's scope and policy fields without re-issuing the consumer secret. Use this when a partner's deployment URL changes, when you need to widen or tighten an allowlist, or when you want to relabel a partner — anything that doesn't require a new credential.

{% hint style="info" %}
**When to use**: When a partner's `allowed_origins`, `allowed_email_domains`, `allowed_source_ips`, `allowed_roles`, `max_users`, `partner_name`, `metadata`, `sso_mode`, or `user_provisioning` needs to change. The HMAC signature is computed only over `timestamp|consumer_key|payload` — scope fields are not part of signed material, so editing them does not require rotating the secret.
{% endhint %}

<details>

<summary>Prerequisites</summary>

* Completed [Register Partner](register-partner.md)
* Have a partner ID to update

</details>

## 5-Line Core

```python
from gl_iam.core.types.sso import SSOPartnerUpdate, CLEAR_PARTNER_FIELD

# Add a new origin without rotating the secret
result = await provider.update_partner(
    partner_id, SSOPartnerUpdate(allowed_origins=["https://app.example.com", "https://staging.example.com"]),
)
```

## What You Can and Cannot Edit

| Field | Editable via `update_partner`? | Use Instead |
| --- | --- | --- |
| `partner_name` | Yes | — |
| `allowed_origins` | Yes | — |
| `allowed_email_domains` | Yes | — |
| `allowed_source_ips` | Yes | — |
| `allowed_roles` | Yes | — |
| `max_users` | Yes | — |
| `metadata` | Yes | — |
| `sso_mode` | Yes | — |
| `user_provisioning` | Yes | — |
| `id` | No | Immutable |
| `consumer_key` | No | Immutable |
| `consumer_secret` | No | [Rotate Consumer Secret](rotate-consumer-secret.md) |
| `org_id` | No | Not supported (cross-tenant transfer is a separate workflow) |
| `is_active` | No | [Manage Partner Lifecycle](manage-partner-lifecycle.md) |
| `created_at`, `updated_at` | No | Server-managed |

{% hint style="warning" %}
**Why credential rotation is a separate operation**: editing scope is a low-risk admin action, while rotating the consumer secret invalidates the partner's existing signing key and requires a coordinated re-deployment on the partner's side. Keeping them separate matches the AWS IAM / Stripe / Google OAuth pattern: secret = rotate-only, scope = freely editable with audit trail.
{% endhint %}

## PATCH Semantics

`SSOPartnerUpdate` is a partial-update model — only fields you explicitly set are applied:

| Value passed | Effect |
| --- | --- |
| `None` (or field omitted) | **Leave unchanged** |
| New value (string, list, dict, enum) | **Replace** the field with the new value |
| `[]` (empty list) | **Set to empty list** — different from `CLEAR_PARTNER_FIELD` (see below) |
| `{}` (empty dict, on `metadata`) | **Set to empty dict** |
| `CLEAR_PARTNER_FIELD` (on nullable allowlists only) | **Set to NULL** — restores "no restriction" semantics |

{% hint style="info" %}
The `CLEAR_PARTNER_FIELD` sentinel is a Python singleton with **no JSON representation**. A web layer that naively forwards an HTTP body to `SSOPartnerUpdate(**payload)` cannot accidentally wipe an allowlist — Pydantic rejects the bare string `"__clear__"`. The only way to send "set to NULL" is to call the SDK directly with the singleton.
{% endhint %}

## Step-by-Step

{% stepper %}
{% step %}
#### Add an Origin Without Rotating

```python
from gl_iam.core.types.sso import SSOPartnerUpdate

result = await provider.update_partner(
    partner_id,
    SSOPartnerUpdate(
        allowed_origins=["https://app.example.com", "https://staging.example.com"],
    ),
)

if result.is_ok:
    partner = result.unwrap()
    print(f"Updated origins: {partner.allowed_origins}")
else:
    print(f"Error: {result.error.code} - {result.error.message}")
```
{% endstep %}

{% step %}
#### Update Multiple Fields Atomically

```python
result = await provider.update_partner(
    partner_id,
    SSOPartnerUpdate(
        partner_name="Acme Corp (renamed)",
        max_users=1000,
        metadata={"contact": "ops@acme.example.com", "tier": "enterprise"},
    ),
)
```
{% endstep %}

{% step %}
#### Clear a Previously-Set Allowlist

```python
from gl_iam.core.types.sso import CLEAR_PARTNER_FIELD

# Restore "no IP restriction" — different from passing []
result = await provider.update_partner(
    partner_id,
    SSOPartnerUpdate(allowed_source_ips=CLEAR_PARTNER_FIELD),
)
```

`[]` would set the column to an empty allowlist (deny all); `CLEAR_PARTNER_FIELD` sets it to NULL (no restriction).
{% endstep %}

{% step %}
#### No-Op Patch

Empty patches and patches where every field already matches the current value short-circuit — no SQL UPDATE is issued and `updated_at` is **not** bumped:

```python
result = await provider.update_partner(partner_id, SSOPartnerUpdate())
# No DB write; result is the current partner state.
```
{% endstep %}

{% step %}
#### Expected Output

```
Updated origins: ['https://app.example.com', 'https://staging.example.com']
```
{% endstep %}
{% endstepper %}

{% hint style="success" %}
You've learned how to edit SSO partner scope without re-issuing credentials!
{% endhint %}

## Validation Rules

`update_partner` rejects malformed input at write-time so misconfigurations surface immediately rather than at the next signature check.

| Field | Rule |
| --- | --- |
| `partner_name` | Must not be empty/whitespace-only. Max 255 characters (matches DB column). |
| `allowed_origins` | Each entry must be a parseable `http://` or `https://` URL. No leading/trailing whitespace. No embedded userinfo (`https://user:pass@host`) — browsers strip these so the entry would silently never match. |
| `allowed_email_domains` | Each entry must be non-empty and have no leading/trailing whitespace. |
| `allowed_source_ips` | Each entry must be a valid IP address or CIDR (parsed via `ipaddress.ip_network(strict=False)`). |
| `allowed_roles` | Each entry must be non-empty and have no leading/trailing whitespace. |
| `max_users` | Must be `>= 0` (rejected at the Pydantic layer). |
| `metadata` | Must be JSON-serializable. Serialized size capped at 64 KB. |
| All allowlists | Capped at 100 entries each, with each entry capped at 2048 characters. |

## Error Codes Reference

| Error Code | Description |
| --- | --- |
| `partner_not_found` | No partner exists with the given `partner_id` |
| `partner_already_exists` | New `partner_name` collides with another partner in the same `org_id` |
| `validation_error` | Input failed one of the validation rules above (see `error.details` for which field/value) |
| `internal_error` | Unexpected database integrity failure |

## Complete Example

Create `update_partner.py`:

```python
"""GL IAM Update SSO Partner Example."""

import asyncio

from gl_iam.core.crypto_config import CryptoConfig, EncryptionAlgorithm
from gl_iam.core.types.sso import (
    CLEAR_PARTNER_FIELD,
    SSOPartnerCreate,
    SSOPartnerUpdate,
)
from gl_iam.providers.postgresql import (
    PostgreSQLConfig,
    PostgreSQLPartnerRegistryProvider,
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
        SSOPartnerCreate(
            partner_name="Acme Corp",
            org_id="default",
            allowed_origins=["https://acme.example.com"],
            allowed_email_domains=["acme.com"],
            max_users=100,
        )
    )
    partner_id = reg_result.unwrap().partner.id
    print(f"1. Registered: id={partner_id}")

    # Add a second origin (the use case that motivated this feature)
    update_result = await provider.update_partner(
        partner_id,
        SSOPartnerUpdate(
            allowed_origins=["https://acme.example.com", "https://staging.acme.example.com"],
        ),
    )
    if update_result.is_ok:
        partner = update_result.unwrap()
        print(f"2. Origins now: {partner.allowed_origins}")

    # Bump the user cap
    await provider.update_partner(partner_id, SSOPartnerUpdate(max_users=500))
    print("3. max_users bumped to 500")

    # Clear the email-domain restriction (back to NULL = no restriction)
    await provider.update_partner(
        partner_id, SSOPartnerUpdate(allowed_email_domains=CLEAR_PARTNER_FIELD),
    )
    print("4. allowed_email_domains cleared (no restriction)")

    # Demonstrate a validation rejection
    bad_result = await provider.update_partner(
        partner_id, SSOPartnerUpdate(allowed_origins=["javascript:alert(1)"]),
    )
    print(f"5. Bad origin rejected: {bad_result.error.code}")

    # No-op patch
    noop = await provider.update_partner(partner_id, SSOPartnerUpdate())
    print(f"6. No-op patch returned current state: id={noop.unwrap().id}")

    await provider.close()


if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
uv run update_partner.py
```

Expected output:

```
1. Registered: id=550e8400-e29b-41d4-a716-446655440000
2. Origins now: ['https://acme.example.com', 'https://staging.acme.example.com']
3. max_users bumped to 500
4. allowed_email_domains cleared (no restriction)
5. Bad origin rejected: validation_error
6. No-op patch returned current state: id=550e8400-e29b-41d4-a716-446655440000
```

## Common Pitfalls

| Pitfall | Solution |
| --- | --- |
| Confusing `[]` with `CLEAR_PARTNER_FIELD` | `[]` is "configured but empty" (deny all); `CLEAR_PARTNER_FIELD` is "no restriction" (NULL) |
| Trying to edit `consumer_key` or `consumer_secret` | These are immutable — use [Rotate Consumer Secret](rotate-consumer-secret.md) to roll the secret |
| Trying to edit `is_active` | Use [Manage Partner Lifecycle](manage-partner-lifecycle.md) (`deactivate_partner` / `reactivate_partner`) |
| Trying to move a partner across organizations | Not supported via `update_partner` — `org_id` is fixed at registration |
| Sending a JSON body with `"allowed_source_ips": "__clear__"` from a web layer | Pydantic will reject the bare string. To clear from a web layer, define an explicit endpoint that translates a flag (e.g. `?clear=allowed_source_ips`) into the singleton in your backend code |
| Padding allowlist entries (`"   admin.com   "`) | Rejected at write-time — the runtime comparator does not strip, so a padded entry would silently never match |

## Next Steps

* [Register Partner](register-partner.md) — Onboard new partners
* [Validate Partner Signature](validate-partner-signature.md) — Validate incoming SSO requests
* [Rotate Consumer Secret](rotate-consumer-secret.md) — Roll the consumer secret independently of scope edits
* [Manage Partner Lifecycle](manage-partner-lifecycle.md) — Deactivate / reactivate / list partners
* [Result Pattern](../../result-pattern.md) — Handle errors from update operations

***

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url\&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Fsso-partner-registry%2Fupdate-partner).
{% endhint %}
