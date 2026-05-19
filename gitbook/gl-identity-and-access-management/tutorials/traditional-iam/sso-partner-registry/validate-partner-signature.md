---
icon: shield-check
---

# Validate Partner Signature

Verify HMAC-SHA256 signatures from SSO partners to authenticate incoming IdP-Initiated SSO requests.

{% hint style="info" %}
**When to use**: On every SSO endpoint that receives partner-signed requests. This validates the partner's identity and ensures the payload hasn't been tampered with.
{% endhint %}

<details>

<summary>Prerequisites</summary>

* Completed [Register Partner](register-partner.md)
* Have a registered partner's consumer key and secret

</details>

## 5-Line Core

```python
result = await provider.validate_partner_signature(
    consumer_key="ck_live_a1b2c3d4...",
    signature=request_signature,
    payload=request_body,
    timestamp=request_timestamp,
    email="alice@acme.com",  # Optional: validates against partner's allowed_email_domains
)
partner = result.unwrap()  # SSOPartner on success
```

## Signature Format

Partners compute signatures using:

```
HMAC-SHA256(consumer_secret, timestamp|consumer_key|payload)
```

| Component          | Description                                |
| ------------------ | ------------------------------------------ |
| `consumer_secret`  | The partner's secret (from registration)   |
| `timestamp`        | ISO 8601 timestamp (e.g., `2026-03-12T10:00:00Z`) |
| `consumer_key`     | The partner's public consumer key          |
| `payload`          | The request body being signed              |
| `\|` (pipe)        | Separator between components               |

## Step-by-Step

{% stepper %}
{% step %}
#### Extract Signature Components from Request

```python
# Typically from HTTP headers
consumer_key = request.headers.get("X-Consumer-Key")
signature = request.headers.get("X-Signature")
timestamp = request.headers.get("X-Timestamp")
payload = await request.body()
```
{% endstep %}

{% step %}
#### Validate the Signature

```python
result = await provider.validate_partner_signature(
    consumer_key=consumer_key,
    signature=signature,
    payload=payload.decode(),
    timestamp=timestamp,
    tolerance_seconds=300,  # 5-minute window (default)
    email=user_email,       # Optional: enforce allowed_email_domains
)
```
{% endstep %}

{% step %}
#### Handle the Result

```python
if result.is_ok:
    partner = result.unwrap()
    print(f"Valid signature from: {partner.partner_name}")
    print(f"SSO Mode: {partner.sso_mode.value}")
    print(f"User Provisioning: {partner.user_provisioning.value}")
else:
    print(f"Error: {result.error.code}")
    # Possible error codes:
    #   PARTNER_NOT_FOUND - consumer_key not recognized
    #   PARTNER_INACTIVE - partner has been deactivated
    #   INVALID_PARTNER_SIGNATURE - HMAC mismatch
    #   SIGNATURE_EXPIRED - timestamp outside tolerance
    #   EMAIL_DOMAIN_NOT_ALLOWED - email domain not in partner's allowed list
```
{% endstep %}

{% step %}
#### Expected Output

```
Valid signature from: Acme Corp
SSO Mode: idp_initiated
User Provisioning: jit
```
{% endstep %}
{% endstepper %}

{% hint style="success" %}
You can validate partner signatures!
{% endhint %}

## Generating a Signature (Partner Side)

Partners compute the HMAC-SHA256 signature like this:

```python
import hashlib
import hmac
from datetime import datetime, timezone

consumer_key = "ck_live_a1b2c3d4..."
consumer_secret = "cs_live_x9y8z7w6..."
payload = '{"email": "alice@example.com", "name": "Alice"}'
timestamp = datetime.now(timezone.utc).isoformat()

# Build the signing string
signing_string = f"{timestamp}|{consumer_key}|{payload}"

# Compute HMAC-SHA256
signature = hmac.new(
    consumer_secret.encode(),
    signing_string.encode(),
    hashlib.sha256,
).hexdigest()

# Send with request headers:
#   X-Consumer-Key: ck_live_a1b2c3d4...
#   X-Signature: <computed signature>
#   X-Timestamp: 2026-03-12T10:00:00+00:00
```

## Looking Up a Partner

Use `get_partner_by_consumer_key` when you need partner details without signature validation:

```python
result = await provider.get_partner_by_consumer_key("ck_live_a1b2c3d4...")

if result.is_ok:
    partner = result.unwrap()
    print(f"Partner: {partner.partner_name}")
    print(f"Active: {partner.is_active}")
    print(f"Origins: {partner.allowed_origins}")
else:
    print(f"Error: {result.error.code}")  # PARTNER_NOT_FOUND
```

## Complete Example

Create `validate_partner_signature.py`:

```python
"""GL IAM Validate Partner Signature Example."""

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
    # Setup provider
    config = PostgreSQLConfig(
        database_url=DATABASE_URL,
        secret_key=SECRET_KEY,
        crypto_config=CryptoConfig(
            encryption_keys={1: ENCRYPTION_KEY},
            encryption_algorithm=EncryptionAlgorithm.AES_256_GCM,
        ),
    )
    provider = PostgreSQLPartnerRegistryProvider(config)

    # Register a partner with email domain restriction (normally done once during onboarding)
    reg_result = await provider.register_partner(
        SSOPartnerCreate(
            partner_name="Acme Corp",
            org_id="default",
            allowed_email_domains=["acme.com"],  # Only @acme.com emails allowed
        )
    )
    registration = reg_result.unwrap()
    consumer_key = registration.consumer_key
    consumer_secret = registration.consumer_secret
    print(f"Registered partner: {registration.partner.partner_name}")

    # --- Partner side: compute signature ---
    payload = '{"email": "alice@example.com", "name": "Alice"}'
    timestamp = datetime.now(timezone.utc).isoformat()
    signing_string = f"{timestamp}|{consumer_key}|{payload}"
    signature = hmac.new(
        consumer_secret.encode(),
        signing_string.encode(),
        hashlib.sha256,
    ).hexdigest()
    print(f"\nPartner computed signature: {signature[:16]}...")

    # --- Your side: validate signature with email domain check ---
    result = await provider.validate_partner_signature(
        consumer_key=consumer_key,
        signature=signature,
        payload=payload,
        timestamp=timestamp,
        email="alice@acme.com",  # Checked against allowed_email_domains
    )

    if result.is_ok:
        partner = result.unwrap()
        print(f"\nSignature valid!")
        print(f"  Partner: {partner.partner_name}")
        print(f"  SSO Mode: {partner.sso_mode.value}")
        print(f"  User Provisioning: {partner.user_provisioning.value}")
        print(f"  Allowed Email Domains: {partner.allowed_email_domains}")
    else:
        print(f"\nSignature invalid: {result.error.code} - {result.error.message}")

    # --- Test disallowed email domain ---
    print("\n--- Testing disallowed email domain ---")
    bad_email_result = await provider.validate_partner_signature(
        consumer_key=consumer_key,
        signature=signature,
        payload=payload,
        timestamp=timestamp,
        email="alice@evil.com",  # Not in allowed_email_domains
    )
    if not bad_email_result.is_ok:
        print(f"Rejected correctly: {bad_email_result.error.code}")

    # --- Test invalid signature ---
    print("\n--- Testing invalid signature ---")
    bad_result = await provider.validate_partner_signature(
        consumer_key=consumer_key,
        signature="invalid-signature",
        payload=payload,
        timestamp=timestamp,
    )
    if not bad_result.is_ok:
        print(f"Rejected correctly: {bad_result.error.code}")

    # --- Look up partner by consumer key ---
    print("\n--- Looking up partner ---")
    lookup_result = await provider.get_partner_by_consumer_key(consumer_key)
    if lookup_result.is_ok:
        partner = lookup_result.unwrap()
        print(f"Found: {partner.partner_name} (active: {partner.is_active})")

    await provider.close()


if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
uv run validate_partner_signature.py
```

Expected output:

```
Registered partner: Acme Corp

Partner computed signature: a1b2c3d4e5f6g7h8...

Signature valid!
  Partner: Acme Corp
  SSO Mode: idp_initiated
  User Provisioning: jit
  Allowed Email Domains: ['acme.com']

--- Testing disallowed email domain ---
Rejected correctly: email_domain_not_allowed

--- Testing invalid signature ---
Rejected correctly: invalid_partner_signature

--- Looking up partner ---
Found: Acme Corp (active: True)
```

## FastAPI Integration

```python
from fastapi import Depends, HTTPException, Header, Request
from gl_iam.providers.postgresql import PostgreSQLPartnerRegistryProvider

# Initialize at app startup
provider: PostgreSQLPartnerRegistryProvider = None  # Set during startup


async def validate_sso_request(
    request: Request,
    x_consumer_key: str = Header(...),
    x_signature: str = Header(...),
    x_timestamp: str = Header(...),
):
    """Dependency to validate SSO partner signatures."""
    body = await request.body()
    payload = body.decode()

    # Extract email from payload for domain validation (optional)
    import json
    email = json.loads(payload).get("email") if payload else None

    result = await provider.validate_partner_signature(
        consumer_key=x_consumer_key,
        signature=x_signature,
        payload=payload,
        timestamp=x_timestamp,
        email=email,  # Validates against partner's allowed_email_domains
    )
    if not result.is_ok:
        status = 403 if result.error.code.value == "email_domain_not_allowed" else 401
        raise HTTPException(status_code=status, detail=result.error.message)
    return result.unwrap()


@app.post("/sso/callback")
async def sso_callback(partner=Depends(validate_sso_request)):
    return {"message": f"Authenticated via {partner.partner_name}"}
```

## Common Pitfalls

| Pitfall                  | Solution                                              |
| ------------------------ | ----------------------------------------------------- |
| Signature always invalid | Ensure signing string format: `timestamp\|key\|payload` |
| Timestamp rejected       | Use ISO 8601 format, check `tolerance_seconds`        |
| Wrong error handling     | Check `result.error.code` for specific error codes    |
| Email domain rejected    | Check partner's `allowed_email_domains` configuration (case-insensitive) |
| Email check unexpected   | `email` param is opt-in — omit it to skip domain check |

---

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Fsso-partner-registry%2Fvalidate-partner-signature).
{% endhint %}
