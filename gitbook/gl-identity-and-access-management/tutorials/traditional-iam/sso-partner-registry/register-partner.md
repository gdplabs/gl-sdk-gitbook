---
icon: user-plus
---

# Register Partner

Register an external SSO partner and generate consumer credentials for HMAC-SHA256 signature validation.

{% hint style="info" %}
**When to use**: When onboarding a new external identity provider that needs to push authenticated user sessions into your application via IdP-Initiated SSO.
{% endhint %}

<details>

<summary>Prerequisites</summary>

* Completed [Quickstart](../quickstart/quickstart-postgresql.md)
* A running PostgreSQL instance with GL IAM configured
* An encryption key for consumer secret storage — generate with: `python -c "import secrets, base64; print(base64.urlsafe_b64encode(secrets.token_bytes(32)).decode())"`

</details>

## Before You Register

{% hint style="warning" %}
Registering a partner means **your application trusts that partner to assert user identities**. A compromised partner secret allows the attacker to create sessions for any user within the allowed email domains.
{% endhint %}

**Trust assessment checklist:**
- [ ] The partner is a known, trusted organization (e.g., internal team, contractual partner)
- [ ] You have a secure channel to share the consumer secret (not email/Slack)
- [ ] You will configure `allowed_email_domains` to scope identity assertions
- [ ] You will configure `allowed_source_ips` to restrict server-to-server access
- [ ] You have a secret rotation schedule agreed with the partner
- [ ] You have incident response procedures if the partner secret is compromised

## 5-Line Core

```python
from gl_iam.providers.postgresql import PostgreSQLPartnerRegistryProvider, PostgreSQLConfig
from gl_iam.core.crypto_config import CryptoConfig, EncryptionAlgorithm
from gl_iam.core.types.sso import SSOPartnerCreate

config = PostgreSQLConfig(database_url="postgresql+asyncpg://...", secret_key="your-secret-key-min-32-chars", crypto_config=CryptoConfig(encryption_keys={1: "<YOUR_KEY>"}, encryption_algorithm=EncryptionAlgorithm.AES_256_GCM))
provider = PostgreSQLPartnerRegistryProvider(config)
result = await provider.register_partner(SSOPartnerCreate(partner_name="Acme Corp", org_id="default"))
# Store result.unwrap().consumer_secret securely - only shown once!
```

## Step-by-Step

{% stepper %}
{% step %}
#### Setup Provider

```python
from gl_iam.providers.postgresql import (
    PostgreSQLPartnerRegistryProvider,
    PostgreSQLConfig,
)
from gl_iam.core.crypto_config import CryptoConfig, EncryptionAlgorithm

config = PostgreSQLConfig(
    database_url="postgresql+asyncpg://postgres:postgres@localhost:5432/gliam",
    secret_key="your-secret-key-min-32-characters-long",  # Required for JWT signing
    crypto_config=CryptoConfig(
        encryption_keys={1: "<YOUR_ENCRYPTION_KEY>"},  # Required for HMAC signature validation
        encryption_algorithm=EncryptionAlgorithm.AES_256_GCM,
    ),
)
provider = PostgreSQLPartnerRegistryProvider(config)
# PostgreSQLPartnerRegistryProvider implements PartnerRegistryProvider protocol
```
{% endstep %}

{% step %}
#### Check Health

```python
healthy = await provider.health_check()
print(f"Provider healthy: {healthy}")
```
{% endstep %}

{% step %}
#### Build Partner Registration

```python
from gl_iam.core.types.sso import SSOPartnerCreate, SSOMode, SSOUserProvisioning

partner_create = SSOPartnerCreate(
    partner_name="Acme Corp",
    org_id="default",
    allowed_origins=["https://acme.example.com"],
    sso_mode=SSOMode.IDP_INITIATED,
    user_provisioning=SSOUserProvisioning.JIT,
    metadata={"contact": "admin@acme.example.com"},
    # Optional security restrictions (all default to None = no restriction)
    allowed_email_domains=["acme.com", "acme.co.id"],  # Only these email domains can SSO
    allowed_source_ips=["10.0.0.0/8"],                  # IP allowlist (enforced by your HTTP layer)
    max_users=500,                                       # User cap (enforced by your provisioning layer)
    allowed_roles=["viewer", "editor"],                  # Restrict assignable roles
)
```

{% hint style="info" %}
**Security fields are opt-in.** All four fields default to `None`, meaning no restriction. Set them to enforce security policies per partner. GL-IAM stores the configuration; your application enforces `allowed_source_ips`, `max_users`, and `allowed_roles` at the HTTP/provisioning layer. Only `allowed_email_domains` is enforced by GL-IAM during signature validation (when the `email` parameter is provided).
{% endhint %}
{% endstep %}

{% step %}
#### Register the Partner

```python
result = await provider.register_partner(partner_create)

if result.is_ok:
    registration = result.unwrap()
    print(f"Partner ID: {registration.partner.id}")
    print(f"Consumer Key: {registration.consumer_key}")
    print(f"Consumer Secret: {registration.consumer_secret}")  # Store securely!
else:
    print(f"Error: {result.error.code} - {result.error.message}")
```
{% endstep %}

{% step %}
#### Expected Output

```
Provider healthy: True
Partner ID: 550e8400-e29b-41d4-a716-446655440000
Consumer Key: ck_live_a1b2c3d4e5f6...
Consumer Secret: cs_live_x9y8z7w6v5u4...
```
{% endstep %}
{% endstepper %}

{% hint style="success" %}
You can register SSO partners!
{% endhint %}

## Complete Example

Create `register_partner.py`:

```python
"""GL IAM Register SSO Partner Example."""

import asyncio

from gl_iam.core.crypto_config import CryptoConfig, EncryptionAlgorithm
from gl_iam.core.types.sso import SSOPartnerCreate, SSOMode, SSOUserProvisioning
from gl_iam.providers.postgresql import (
    PostgreSQLPartnerRegistryProvider,
    PostgreSQLConfig,
)

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/gliam"
SECRET_KEY = "your-secret-key-min-32-characters-long"  # For JWT signing
# Generate with: python -c "import secrets, base64; print(base64.urlsafe_b64encode(secrets.token_bytes(32)).decode())"
ENCRYPTION_KEY = "<YOUR_ENCRYPTION_KEY>"


async def main():
    # Step 1: Setup provider
    config = PostgreSQLConfig(
        database_url=DATABASE_URL,
        secret_key=SECRET_KEY,
        crypto_config=CryptoConfig(
            encryption_keys={1: ENCRYPTION_KEY},
            encryption_algorithm=EncryptionAlgorithm.AES_256_GCM,
        ),
    )
    provider = PostgreSQLPartnerRegistryProvider(config)

    # Step 2: Health check
    healthy = await provider.health_check()
    print(f"Provider healthy: {healthy}")

    # Step 3: Register partner with security restrictions
    partner_create = SSOPartnerCreate(
        partner_name="Acme Corp",
        org_id="default",
        allowed_origins=["https://acme.example.com"],
        sso_mode=SSOMode.IDP_INITIATED,
        user_provisioning=SSOUserProvisioning.JIT,
        metadata={"contact": "admin@acme.example.com"},
        # Security restrictions (all optional, default None = no restriction)
        allowed_email_domains=["acme.com"],  # Only allow @acme.com emails
        max_users=500,                        # Cap at 500 provisioned users
    )

    result = await provider.register_partner(partner_create)

    if result.is_ok:
        registration = result.unwrap()
        print(f"\nPartner registered!")
        print(f"  ID: {registration.partner.id}")
        print(f"  Name: {registration.partner.partner_name}")
        print(f"  Consumer Key: {registration.consumer_key}")
        print(f"  Consumer Secret: {registration.consumer_secret}")
        print(f"  SSO Mode: {registration.partner.sso_mode.value}")
        print(f"  User Provisioning: {registration.partner.user_provisioning.value}")
        print(f"\n  Store the consumer secret securely - it won't be shown again!")
    else:
        print(f"Error: {result.error.code} - {result.error.message}")

    await provider.close()


if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
uv run register_partner.py
```

Expected output:

```
Provider healthy: True

Partner registered!
  ID: 550e8400-e29b-41d4-a716-446655440000
  Name: Acme Corp
  Consumer Key: ck_live_a1b2c3d4e5f6...
  Consumer Secret: cs_live_x9y8z7w6v5u4...
  SSO Mode: idp_initiated
  User Provisioning: jit

  Store the consumer secret securely - it won't be shown again!
```

## Using with IAMGateway

If your `PostgreSQLProvider` has `enable_partner_registry=True`, the gateway auto-detects the partner registry:

```python
from gl_iam import IAMGateway
from gl_iam.core.crypto_config import CryptoConfig, EncryptionAlgorithm
from gl_iam.providers.postgresql import PostgreSQLProvider, PostgreSQLConfig

config = PostgreSQLConfig(
    database_url=DATABASE_URL,
    secret_key=SECRET_KEY,
    crypto_config=CryptoConfig(encryption_keys={1: ENCRYPTION_KEY}, encryption_algorithm=EncryptionAlgorithm.AES_256_GCM),
    enable_partner_registry=True,
)
provider = PostgreSQLProvider(config)

# Gateway auto-detects partner registry from fullstack provider
gateway = IAMGateway.from_fullstack_provider(provider)

# Partner operations via gateway
result = await gateway.partner_registry.register_partner(partner_create)
```

## Common Pitfalls

| Pitfall                      | Solution                                               |
| ---------------------------- | ------------------------------------------------------ |
| Not storing consumer secret  | Store immediately — only shown once                    |
| Missing `secret_key`         | Required — set a secure random key (min 32 characters) |
| Missing encryption config    | Set `crypto_config.encryption_keys` (or legacy `encryption_key`) for HMAC validation |
| Duplicate partner name       | Check `PARTNER_ALREADY_EXISTS` error code              |
| Confusing `None` vs `[]`     | `None` = no restriction (skip check); don't use `[]`  |

---

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Fsso-partner-registry%2Fregister-partner).
{% endhint %}
