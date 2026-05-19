---
icon: bolt-lightning
---

# Quickstart: Keycloak

Integrate GL IAM with Keycloak for enterprise-grade identity management.

{% hint style="info" %}
**When to use Keycloak**: Choose Keycloak for enterprise environments with existing Keycloak infrastructure, advanced identity features (SSO, MFA, federation), or requirements for OIDC/SAML protocol support.
{% endhint %}

{% hint style="info" %}
**What you'll build**: A FastAPI application that authenticates users via Keycloak tokens and enforces role-based access control using GL IAM's unified interface.
{% endhint %}

<details>

<summary>Prerequisites</summary>

This example requires completion of all setup steps listed on the [Prerequisites](../../../prerequisites.md) page. To summarize:

* Python 3.11+
* Docker and Docker Compose
* Access to the **GDP Labs' Gen AI SDK repository** (request via [form](https://docs.google.com/forms/d/e/1FAIpQLScJxB-Xe9YjnohIzW6nic-_AeSJob6Il6spl1s85wc76tQkzQ/viewform) or ticket@gdplabs.id)
* **gcloud CLI:** [Install](https://cloud.google.com/sdk/docs/install), then run `gcloud auth login`
* [uv](https://docs.astral.sh/uv/) — Install with: `curl -LsSf https://astral.sh/uv/install.sh | sh`

No external Keycloak server needed — we'll run it locally with Docker.

</details>

## Setup Keycloak

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  keycloak:
    image: quay.io/keycloak/keycloak:24.0
    environment:
      KEYCLOAK_ADMIN: admin
      KEYCLOAK_ADMIN_PASSWORD: admin
    ports:
      - "8080:8080"
    command:
      - start-dev
      - --import-realm
    volumes:
      - ./realm-export.json:/opt/keycloak/data/import/realm-export.json
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health/ready"]
      interval: 10s
      timeout: 5s
      retries: 5
```

Create `realm-export.json` with pre-configured users:

```json
{
  "realm": "gl-iam-demo",
  "enabled": true,
  "clients": [
    {
      "clientId": "glchat-backend",
      "enabled": true,
      "clientAuthenticatorType": "client-secret",
      "secret": "glchat-backend-secret",
      "directAccessGrantsEnabled": true,
      "standardFlowEnabled": true,
      "publicClient": false
    }
  ],
  "roles": {
    "realm": [
      { "name": "admin" },
      { "name": "member" }
    ]
  },
  "users": [
    {
      "username": "user@example.com",
      "email": "user@example.com",
      "firstName": "user",
      "lastName": "example",
      "enabled": true,
      "emailVerified": true,
      "credentials": [{ "type": "password", "value": "user123" }],
      "realmRoles": ["member"]
    },
    {
      "username": "admin@example.com",
      "email": "admin@example.com",
      "firstName": "admin",
      "lastName": "example",
      "enabled": true,
      "emailVerified": true,
      "credentials": [{ "type": "password", "value": "admin123" }],
      "realmRoles": ["admin", "member"]
    }
  ]
}
```

Start Keycloak:

```bash
docker-compose up -d
```

Wait for Keycloak to be healthy (30-60 seconds on first start):

```bash
docker-compose logs -f keycloak
# Look for: "Keycloak ... started"
```

Admin console: [http://localhost:8080/admin](http://localhost:8080/admin) (credentials: `admin` / `admin`)

## Demo Users

The pre-configured realm includes these test users:

| Email             | Password | Roles         |
| ----------------- | -------- | ------------- |
| user@example.com  | user123  | member        |
| admin@example.com | admin123 | admin, member |

## Installation

Install GL IAM from the internal Google Artifact Registry (latest version).

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
uv init --bare
uv add --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" "gl-iam[fastapi,keycloak]"
uv add python-dotenv uvicorn
```
{% endtab %}

{% tab title="Windows PowerShell" %}
```powershell
uv init --bare
$token = (gcloud auth print-access-token)
uv add --extra-index-url "https://oauth2accesstoken:$token@glsdk.gdplabs.id/gen-ai-internal/simple/" "gl-iam[fastapi,keycloak]"
uv add python-dotenv uvicorn
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
uv init --bare
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO uv add --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/" "gl-iam[fastapi,keycloak]"
uv add python-dotenv uvicorn
```
{% endtab %}
{% endtabs %}

## 5-Line Core

The essential code to validate Keycloak tokens with GL IAM:

```python
from gl_iam import IAMGateway
from gl_iam.providers.keycloak import KeycloakProvider, KeycloakConfig

config = KeycloakConfig(server_url="http://localhost:8080", realm="gl-iam-demo", client_id="glchat-backend", client_secret="glchat-backend-secret")
provider = KeycloakProvider(config=config)
gateway = IAMGateway.from_fullstack_provider(provider)
```

## Step-by-Step

{% stepper %}
{% step %}
**Configure Environment**

Create `.env` file:

```bash
KEYCLOAK_SERVER_URL=http://localhost:8080
KEYCLOAK_REALM=gl-iam-demo
KEYCLOAK_CLIENT_ID=glchat-backend
KEYCLOAK_CLIENT_SECRET=glchat-backend-secret
```
{% endstep %}

{% step %}
**Setup Provider**

```python
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI

from gl_iam import IAMGateway
from gl_iam.fastapi import set_iam_gateway
from gl_iam.providers.keycloak import KeycloakConfig, KeycloakProvider

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    config = KeycloakConfig(
        server_url=os.getenv("KEYCLOAK_SERVER_URL"),
        realm=os.getenv("KEYCLOAK_REALM"),
        client_id=os.getenv("KEYCLOAK_CLIENT_ID"),
        client_secret=os.getenv("KEYCLOAK_CLIENT_SECRET"),
    )
    provider = KeycloakProvider(config=config)
    gateway = IAMGateway.from_fullstack_provider(provider)

    set_iam_gateway(gateway, default_organization_id=os.getenv("KEYCLOAK_REALM"))
    yield

app = FastAPI(title="GL-IAM Keycloak Demo", lifespan=lifespan)
```
{% endstep %}

{% step %}
**Add Protected Endpoints**

```python
from fastapi import Depends
from gl_iam import User
from gl_iam.fastapi import get_current_user, require_org_admin, require_org_member

@app.get("/health")
async def health():
    return {"status": "healthy", "provider": "keycloak"}

@app.get("/me")
async def get_me(user: User = Depends(get_current_user)):
    return {"id": user.id, "email": user.email, "roles": user.roles}

@app.get("/member-area")
async def member_area(
    user: User = Depends(get_current_user),
    _: None = Depends(require_org_member()),
):
    return {"message": f"Welcome {user.email}!", "access_level": "member"}

@app.get("/admin-area")
async def admin_area(
    user: User = Depends(get_current_user),
    _: None = Depends(require_org_admin()),
):
    return {"message": f"Welcome Admin {user.email}!", "access_level": "admin"}
```
{% endstep %}

{% step %}
**Run the Server**

```bash
uv run uvicorn main:app --reload
```

Output:

```
Connected to Keycloak at http://localhost:8080
INFO:     Uvicorn running on http://127.0.0.1:8000
```
{% endstep %}

{% step %}
**Test the API**

Get a token using the Resource Owner Password Grant:

```bash
# Get token for regular user
TOKEN=$(curl -s -X POST "http://localhost:8080/realms/gl-iam-demo/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=glchat-backend" \
  -d "client_secret=glchat-backend-secret" \
  -d "grant_type=password" \
  -d "username=user@example.com" \
  -d "password=user123" | jq -r '.access_token')

# Health check
curl http://localhost:8000/health

# Get user profile
curl http://localhost:8000/me -H "Authorization: Bearer $TOKEN"

# Access member area (should succeed)
curl http://localhost:8000/member-area -H "Authorization: Bearer $TOKEN"

# Access admin area (will fail for regular user)
curl http://localhost:8000/admin-area -H "Authorization: Bearer $TOKEN"
```
{% endstep %}

{% step %}
**Test Admin Access**

```bash
# Get token for admin user
ADMIN_TOKEN=$(curl -s -X POST "http://localhost:8080/realms/gl-iam-demo/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=glchat-backend" \
  -d "client_secret=glchat-backend-secret" \
  -d "grant_type=password" \
  -d "username=admin@example.com" \
  -d "password=admin123" | jq -r '.access_token')

# Access admin area (should succeed)
curl http://localhost:8000/admin-area -H "Authorization: Bearer $ADMIN_TOKEN"
```
{% endstep %}
{% endstepper %}

{% hint style="success" %}
Congratulations! You've integrated GL IAM with Keycloak.
{% endhint %}

## Complete Example

Create `main.py`:

```python
"""Secure FastAPI application with GL-IAM Keycloak authentication."""

import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from pydantic import BaseModel

from gl_iam import IAMGateway, User
from gl_iam.fastapi import (
    get_current_user,
    require_org_admin,
    require_org_member,
    set_iam_gateway,
)
from gl_iam.providers.keycloak import KeycloakConfig, KeycloakProvider

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize GL-IAM with Keycloak provider."""
    config = KeycloakConfig(
        server_url=os.getenv("KEYCLOAK_SERVER_URL"),
        realm=os.getenv("KEYCLOAK_REALM"),
        client_id=os.getenv("KEYCLOAK_CLIENT_ID"),
        client_secret=os.getenv("KEYCLOAK_CLIENT_SECRET"),
    )
    provider = KeycloakProvider(config=config)
    gateway = IAMGateway.from_fullstack_provider(provider)

    set_iam_gateway(gateway, default_organization_id=os.getenv("KEYCLOAK_REALM"))

    # Verify connection
    is_healthy = await provider.health_check()
    if is_healthy:
        print(f"Connected to Keycloak at {os.getenv('KEYCLOAK_SERVER_URL')}")

    yield


app = FastAPI(title="GL-IAM Keycloak Demo", lifespan=lifespan)


class UserResponse(BaseModel):
    """Response model for user data."""
    id: str
    email: str
    display_name: str | None
    roles: list[str]


@app.get("/health")
async def health():
    """Public health check endpoint."""
    return {"status": "healthy", "provider": "keycloak"}


@app.get("/me", response_model=UserResponse)
async def get_me(user: User = Depends(get_current_user)):
    """Get current user profile. Requires authentication."""
    return UserResponse(
        id=user.id,
        email=user.email,
        display_name=user.display_name,
        roles=user.roles,
    )


@app.get("/member-area")
async def member_area(
    user: User = Depends(get_current_user),
    _: None = Depends(require_org_member()),
):
    """Member area. Requires ORG_MEMBER, ORG_ADMIN, or PLATFORM_ADMIN."""
    return {"message": f"Welcome {user.email}!", "access_level": "member"}


@app.get("/admin-area")
async def admin_area(
    user: User = Depends(get_current_user),
    _: None = Depends(require_org_admin()),
):
    """Admin area. Requires ORG_ADMIN or PLATFORM_ADMIN."""
    return {"message": f"Welcome Admin {user.email}!", "access_level": "admin"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Run it:

```bash
uv run main.py
```

## Keycloak Role Mapping

Keycloak realm roles map to GL IAM standard roles:

| Keycloak Role | GL IAM Standard Role | Access Level     |
| ------------- | -------------------- | ---------------- |
| `admin`       | `ORG_ADMIN`          | Admin endpoints  |
| `member`      | `ORG_MEMBER`         | Member endpoints |

## Common Pitfalls

| Pitfall                                | Solution                                                                |
| -------------------------------------- | ----------------------------------------------------------------------- |
| Keycloak not starting                  | Wait 30-60 seconds on first start; check `docker-compose logs keycloak` |
| Token validation fails                 | Ensure `client_secret` matches the Keycloak client configuration        |
| User has no roles                      | Assign realm roles to the user in Keycloak admin console                |
| Port 8080 in use                       | Change the port mapping in `docker-compose.yml`                         |
| Resource Owner Password Grant disabled | Enable "Direct Access Grants" on the Keycloak client                    |

## Cleanup

Stop and remove the Keycloak container:

```bash
docker-compose down -v
```

## Production Notes

{% hint style="warning" %}
The Resource Owner Password Grant used in this quickstart is for testing only. In production, use the Authorization Code Flow with PKCE for better security.
{% endhint %}

For production deployments:

* Use HTTPS for the Keycloak server URL
* Configure proper SSL/TLS certificates
* Set up realm roles and client scopes according to your security requirements
* Consider using Keycloak's built-in user federation for LDAP/Active Directory integration

***

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url\&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Fquickstart%2Fquickstart-keycloak).
{% endhint %}
