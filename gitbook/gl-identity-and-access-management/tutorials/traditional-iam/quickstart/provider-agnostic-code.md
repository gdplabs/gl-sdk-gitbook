---
icon: shuffle
---

# Provider Agnostic Code

GL IAM implements the **SIMI pattern** (Single Interface, Multiple Implementations) - your application code stays the same regardless of which identity provider you use.

{% hint style="success" %}
**Write once, deploy anywhere**: Switch from PostgreSQL to Keycloak or Stack Auth by changing only your configuration. Your endpoints, dependencies, and business logic remain unchanged.
{% endhint %}

## The Problem with Provider-Specific Code

Traditional authentication code is tightly coupled to a specific provider:

```python
# Provider-specific code - hard to migrate

# With Provider A
from provider_a import verify_token_a
user = verify_token_a(request.headers["Authorization"])
if user.permissions.get("admin"):
    ...

# With Provider B (different API)
from provider_b import decode_jwt
claims = decode_jwt(request.headers["Authorization"])
if "admin" in claims["roles"]:
    ...
```

Migrating between providers requires rewriting authentication logic throughout your application.

## The GL IAM Solution

GL IAM provides a unified interface that abstracts provider-specific details:

```mermaid
graph TB
    subgraph "Your Application"
        A[FastAPI Endpoints]
        B[get_current_user]
        C[require_org_admin]
    end

    subgraph "GL IAM Gateway"
        D[IAMGateway]
    end

    subgraph "Providers"
        E[PostgreSQLProvider]
        F[StackAuthProvider]
        G[KeycloakProvider]
    end

    A --> B
    A --> C
    B --> D
    C --> D
    D --> E
    D --> F
    D --> G
```

## Same Endpoints, Different Providers

Your endpoint code is identical across all providers:

{% tabs %}
{% tab title="Endpoint Code (All Providers)" %}
```python
from fastapi import Depends, FastAPI
from gl_iam import User
from gl_iam.fastapi import (
    get_current_user,
    require_org_admin,
    require_org_member,
)

app = FastAPI()


@app.get("/health")
async def health():
    """Public endpoint - no authentication required."""
    return {"status": "healthy"}


@app.get("/me")
async def get_me(user: User = Depends(get_current_user)):
    """
    Get current user profile.

    Works with any provider - returns the same User object.
    """
    return {
        "id": user.id,
        "email": user.email,
        "display_name": user.display_name,
        "roles": user.roles,
    }


@app.get("/member-area")
async def member_area(
    user: User = Depends(get_current_user),
    _: None = Depends(require_org_member()),
):
    """Requires ORG_MEMBER, ORG_ADMIN, or PLATFORM_ADMIN."""
    return {"message": f"Welcome {user.email}!", "access_level": "member"}


@app.get("/admin-area")
async def admin_area(
    user: User = Depends(get_current_user),
    _: None = Depends(require_org_admin()),
):
    """Requires ORG_ADMIN or PLATFORM_ADMIN."""
    return {"message": f"Welcome Admin {user.email}!", "access_level": "admin"}
```
{% endtab %}

{% tab title="PostgreSQL Config" %}
```python
from contextlib import asynccontextmanager
from gl_iam import IAMGateway
from gl_iam.fastapi import set_iam_gateway
from gl_iam.providers.postgresql import (
    PostgreSQLProvider,
    PostgreSQLConfig,
)


@asynccontextmanager
async def lifespan(app):
    config = PostgreSQLConfig(
        database_url="postgresql+asyncpg://user:pass@localhost:5432/mydb"
    )
    provider = PostgreSQLProvider(config)
    gateway = IAMGateway.from_fullstack_provider(provider)

    set_iam_gateway(gateway, default_organization_id="default")

    yield

    await provider.close()
```
{% endtab %}

{% tab title="Stack Auth Config" %}
```python
from contextlib import asynccontextmanager
from gl_iam import IAMGateway
from gl_iam.fastapi import set_iam_gateway
from gl_iam.providers.stackauth import StackAuthProvider, StackAuthConfig


@asynccontextmanager
async def lifespan(app):
    config = StackAuthConfig(
        base_url="https://api.stack-auth.com",
        project_id="your-project-id",
        publishable_client_key="pck_...",
        secret_server_key="ssk_...",
    )
    provider = StackAuthProvider(config)
    gateway = IAMGateway.from_fullstack_provider(provider)

    set_iam_gateway(gateway, default_organization_id="your-project-id")

    yield

    await provider.close()
```
{% endtab %}

{% tab title="Keycloak Config" %}
```python
from contextlib import asynccontextmanager
from gl_iam import IAMGateway
from gl_iam.fastapi import set_iam_gateway
from gl_iam.providers.keycloak import KeycloakProvider, KeycloakConfig


@asynccontextmanager
async def lifespan(app):
    config = KeycloakConfig(
        server_url="http://localhost:8080",
        realm="my-realm",
        client_id="my-client",
        client_secret="my-secret",
    )
    provider = KeycloakProvider(config)
    gateway = IAMGateway.from_fullstack_provider(provider)

    set_iam_gateway(gateway, default_organization_id="my-realm")

    yield
```
{% endtab %}
{% endtabs %}

## Unified User Object

Regardless of which provider you use, `get_current_user` returns the same `User` object:

```python
class User:
    id: str                    # Unique user identifier
    email: str                 # User's email address
    display_name: str | None   # Optional display name
    roles: list[str]           # List of role names (e.g., ["admin", "member"])
```

## Standard Role Mapping

GL IAM maps provider-specific roles to standard roles:

| Provider   | Provider Role | GL IAM Standard Role |
| ---------- | ------------- | -------------------- |
| PostgreSQL | `admin`       | `ORG_ADMIN`          |
| PostgreSQL | `member`      | `ORG_MEMBER`         |
| Stack Auth | `team_admin`  | `ORG_ADMIN`          |
| Stack Auth | `team_member` | `ORG_MEMBER`         |
| Keycloak   | `admin`       | `ORG_ADMIN`          |
| Keycloak   | `member`      | `ORG_MEMBER`         |

The authorization dependencies (`require_org_admin()`, `require_org_member()`) work identically across providers because they check against these standard roles.

## Benefits of Provider-Agnostic Code

| Benefit                   | Description                                          |
| ------------------------- | ---------------------------------------------------- |
| **Migration flexibility** | Switch providers without rewriting application code  |
| **Testing simplicity**    | Use PostgreSQL locally, production IdP in deployment |
| **Reduced lock-in**       | Your code doesn't depend on a specific vendor's API  |
| **Consistent patterns**   | Same authorization patterns across all projects      |
| **Faster development**    | Learn once, apply everywhere                         |

## Environment-Based Provider Selection

A common pattern is selecting the provider based on environment:

```python
import os
from gl_iam import IAMGateway
from gl_iam.fastapi import set_iam_gateway


def create_provider():
    provider_type = os.getenv("PROVIDER_TYPE", "postgresql")

    if provider_type == "postgresql":
        from gl_iam.providers.postgresql import (
            PostgreSQLProvider,
            PostgreSQLConfig,
        )
        config = PostgreSQLConfig(
            database_url=os.getenv("DATABASE_URL")
        )
        return PostgreSQLProvider(config)

    elif provider_type == "stackauth":
        from gl_iam.providers.stackauth import (
            StackAuthProvider,
            StackAuthConfig,
        )
        config = StackAuthConfig(
            base_url=os.getenv("STACKAUTH_BASE_URL"),
            project_id=os.getenv("STACKAUTH_PROJECT_ID"),
            publishable_client_key=os.getenv("STACKAUTH_PUBLISHABLE_CLIENT_KEY"),
            secret_server_key=os.getenv("STACKAUTH_SECRET_SERVER_KEY"),
        )
        return StackAuthProvider(config)

    elif provider_type == "keycloak":
        from gl_iam.providers.keycloak import (
            KeycloakProvider,
            KeycloakConfig,
        )
        config = KeycloakConfig(
            server_url=os.getenv("KEYCLOAK_SERVER_URL"),
            realm=os.getenv("KEYCLOAK_REALM"),
            client_id=os.getenv("KEYCLOAK_CLIENT_ID"),
            client_secret=os.getenv("KEYCLOAK_CLIENT_SECRET"),
        )
        return KeycloakProvider(config)


@asynccontextmanager
async def lifespan(app):
    provider = create_provider()
    gateway = IAMGateway.from_fullstack_provider(provider)
    set_iam_gateway(gateway)
    yield
    await provider.close()
```

---

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Fquickstart%2Fprovider-agnostic-code).
{% endhint %}
