---
icon: bolt-lightning
---

# Quickstart: PostgreSQL

A self-contained GL IAM quickstart using PostgreSQL - no external auth services required.

{% hint style="info" %}
**When to use PostgreSQL**: Choose the PostgreSQL provider when you want full control over user data, the fastest local setup, or don't need external identity provider features like SSO or social login.
{% endhint %}

{% hint style="info" %}
**When to use this page**: Use this Quickstart when you want the fastest "it works on my machine" proof. You can run GL IAM with PostgreSQL locally (no external IdP needed) and do the full lifecycle: register → login → validate.
{% endhint %}

{% hint style="info" %}
**What you'll build**: A minimal local setup that runs PostgreSQL using Docker, installs GL IAM, and runs a Python script that creates a user with password and authenticates them.
{% endhint %}

<details>

<summary>Prerequisites</summary>

This example requires completion of all setup steps listed on the [Prerequisites](../../../prerequisites.md) page. To summarize:

* Python 3.11+
* Docker (for PostgreSQL)
* Access to the **GDP Labs' Gen AI SDK repository** (request via [form](https://docs.google.com/forms/d/e/1FAIpQLScJxB-Xe9YjnohIzW6nic-_AeSJob6Il6spl1s85wc76tQkzQ/viewform) or ticket@gdplabs.id)
* **gcloud CLI:** [Install](https://cloud.google.com/sdk/docs/install), then run `gcloud auth login`
* [uv](https://docs.astral.sh/uv/) — Install with: `curl -LsSf https://astral.sh/uv/install.sh | sh`

</details>

## Setup PostgreSQL

Start PostgreSQL with Docker:

```bash
docker run -d --name gliam-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=gliam \
  -p 5432:5432 \
  postgres:16
```

## Installation

Install GL IAM from the internal Google Artifact Registry (latest version).

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
uv init --bare
uv add --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" "gl-iam[postgresql]"
```
{% endtab %}

{% tab title="Windows PowerShell" %}
```powershell
uv init --bare
$token = (gcloud auth print-access-token)
uv add --extra-index-url "https://oauth2accesstoken:$token@glsdk.gdplabs.id/gen-ai-internal/simple/" "gl-iam[postgresql]"
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
uv init --bare
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO uv add --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/" "gl-iam[postgresql]"
```
{% endtab %}
{% endtabs %}

## Quick Start

{% stepper %}
{% step %}
**Setup Provider**

```python
from gl_iam import IAMGateway
from gl_iam.core.types import PasswordCredentials, UserCreateInput
from gl_iam.core.types.result import ErrorCode
from gl_iam.providers.postgresql import PostgreSQLProvider, PostgreSQLConfig

config = PostgreSQLConfig(database_url="postgresql+asyncpg://postgres:postgres@localhost:5432/gliam")
provider = PostgreSQLProvider(config)
gateway = IAMGateway.from_fullstack_provider(provider)
```
{% endstep %}

{% step %}
**Create User with Password**

```python
result = await gateway.create_user_with_password(
    user_data=UserCreateInput(email="alice@example.com", display_name="Alice"),
    password="SecurePass123",
    organization_id="default",
)

if result.is_ok:
    user = result.value
    print(f"Created user: {user.email}")
elif result.error.code == ErrorCode.USER_ALREADY_EXISTS:
    print("User already exists")
```
{% endstep %}

{% step %}
**Authenticate User**

```python
result = await gateway.authenticate(
    credentials=PasswordCredentials(email="alice@example.com", password="SecurePass123"),
    organization_id="default",
)

if result.is_ok:
    user, token = result.unwrap()
    print(f"Hello, {user.display_name or user.email}!")
```
{% endstep %}

{% step %}
**Expected Output**

```
Created user: alice@example.com
Hello, Alice!
```
{% endstep %}
{% endstepper %}

{% hint style="success" %}
Congratulations! You've verified GL IAM is working with PostgreSQL.
{% endhint %}

## Complete Example

This example includes user registration with password and authentication - the full auth lifecycle.

Create `quickstart.py`:

```python
"""GL IAM Quickstart with PostgreSQL Provider."""

import asyncio

from gl_iam import IAMGateway
from gl_iam.core.types import PasswordCredentials, UserCreateInput
from gl_iam.core.types.result import ErrorCode
from gl_iam.providers.postgresql import PostgreSQLProvider, PostgreSQLConfig

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/gliam"


async def main():
    # Step 1: Setup GL IAM
    config = PostgreSQLConfig(database_url=DATABASE_URL)
    provider = PostgreSQLProvider(config)
    gateway = IAMGateway.from_fullstack_provider(provider)

    # Step 2: Create user with password (registration)
    result = await gateway.create_user_with_password(
        user_data=UserCreateInput(
            email="alice@example.com",
            display_name="Alice",
        ),
        password="SecurePass123",
        organization_id="default",
    )

    if result.is_ok:
        user = result.value
        print(f"Created user: {user.email}")
    elif result.error.code == ErrorCode.USER_ALREADY_EXISTS:
        print("User alice@example.com already exists, skipping creation")
    else:
        print(f"Error creating user: {result.error.message}")

    # Step 3: Authenticate (login)
    result = await gateway.authenticate(
        credentials=PasswordCredentials(email="alice@example.com", password="SecurePass123"),
        organization_id="default",
    )

    # Step 4: Check result and print success message
    if result.is_ok:
        user, token = result.unwrap()
        print(f"Hello, {user.display_name or user.email}!")
        print(f"User ID: {user.id}")
        print(f"Token: {token.access_token[:50]}...")
    else:
        print(f"Authentication failed: {result.error.message}")

    await provider.close()


if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
uv run quickstart.py
```

Expected output (first run):

```
Created user: alice@example.com
Hello, Alice!
User ID: 550e8400-e29b-41d4-a716-446655440000
Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWI...
```

Expected output (subsequent runs):

```
User alice@example.com already exists, skipping creation
Hello, Alice!
User ID: 550e8400-e29b-41d4-a716-446655440000
Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWI...
```

## Common Pitfalls

| Pitfall                  | Solution                                                                                     |
| ------------------------ | -------------------------------------------------------------------------------------------- |
| Port 5432 already in use | Map to another port: `-p 5433:5432` and update `DATABASE_URL`                                |
| Wrong DB URL scheme      | Keep `asyncpg` in the URL: `postgresql+asyncpg://...`                                        |
| Org/Tenant confusion     | `organization_id="default"` is a local placeholder—use your real tenant/org ID in production |

## Cleanup

Stop and remove the PostgreSQL container when done:

```bash
docker stop gliam-postgres && docker rm gliam-postgres
```

## Other Providers

GL IAM supports multiple identity providers with the same application code. Only the configuration changes:

* [Quickstart: Stack Auth](quickstart-stack-auth.md) - Modern managed authentication with UI components
* [Quickstart: Keycloak](quickstart-keycloak.md) - Enterprise identity management with SSO

***

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url\&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Fquickstart%2Fquickstart-postgresql).
{% endhint %}
