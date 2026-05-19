---
description: Integrating DPoP to our resource server.
icon: server
---

# Protect Your API

{% hint style="info" %}
**What you'll build:** A FastAPI resource server that validates **DPoP-bound Keycloak access tokens**, rejecting requests that cannot prove possession of the client’s private key.
{% endhint %}

<details>

<summary><strong>Prerequisites</strong></summary>

This example requires completion of all setup steps listed on the [Prerequisites](https://gdplabs.gitbook.io/sdk/gl-iam/prerequisites) page. To summarize:

* [Keycloak Quickstart](../quickstart/quickstart-keycloak.md) — We use keycloak as an auth provider in this tutorial
* Python 3.11+
* Docker and Docker Compose
* Access to the **GDP Labs' Gen AI SDK repository** (request via [form](https://docs.google.com/forms/d/e/1FAIpQLScJxB-Xe9YjnohIzW6nic-_AeSJob6Il6spl1s85wc76tQkzQ/viewform) or ticket@gdplabs.id)
* **gcloud CLI:** [Install](https://cloud.google.com/sdk/docs/install), then run `gcloud auth login`
* [uv](https://docs.astral.sh/uv/) — Install with: `curl -LsSf https://astral.sh/uv/install.sh | sh`

</details>

## Setup Keycloak

Create `docker-compose.yml` :

```yaml
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

Create `realm-export.json` :

```json
{
  "realm": "dpop-demo",
  "enabled": true,
  "clients": [
    {
      "clientId": "dpop-client",
      "enabled": true,
      "clientAuthenticatorType": "client-secret",
      "secret": "dpop-secret",
      "directAccessGrantsEnabled": true,
      "standardFlowEnabled": true,
      "publicClient": false,
      "attributes": {
        "dpop.bound.access.tokens": "true"
      }
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

Start keycloak:

```shellscript
docker compose up -d
```

## 5-Line Core

Essential code to integrate DPoP using Keycloak provider.

```python
from gl_iam import DPoPConfig, IAMGateway
from gl_iam.providers.keycloak.dpop import KeycloakDPoPProvider

dpop_config = DPoPConfig(enabled=True)
dpop_provider = KeycloakDPoPProvider(keycloak_config, dpop_config)
gateway = IAMGateway.from_fullstack_provider(
    provider=keycloak_provider,
    dpop_provider=dpop_provider,
)
```

## Step-by-Step <a href="#step-by-step" id="step-by-step"></a>

{% stepper %}
{% step %}
#### Configure Environment

Create `.env` file:

```dotenv
KEYCLOAK_SERVER_URL=http://localhost:8080
KEYCLOAK_REALM=dpop-demo
KEYCLOAK_CLIENT_ID=dpop-client
KEYCLOAK_CLIENT_SECRET=dpop-secret
```
{% endstep %}

{% step %}
#### Setup Provider

```python
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from gl_iam import DPoPConfig, IAMGateway
from gl_iam.providers.keycloak import (
    KeycloakConfig,
    KeycloakProvider,
)
from gl_iam.providers.keycloak.dpop import KeycloakDPoPProvider

load_dotenv()

@asynccontextmanager
async def lifespan(_: FastAPI):
    keycloak_config = KeycloakConfig(
        server_url=os.getenv("KEYCLOAK_SERVER_URL"),
        realm=os.getenv("KEYCLOAK_REALM"),
        client_id=os.getenv("KEYCLOAK_CLIENT_ID"),
        client_secret=os.getenv("KEYCLOAK_CLIENT_SECRET"),
    )

    keycloak_provider = KeycloakProvider(config=keycloak_config)

    dpop_config = DPoPConfig(enabled=True, required=False, nonce_enabled=False)
    dpop_provider = KeycloakDPoPProvider(
        keycloak_config=keycloak_config, dpop_config=dpop_config
    )
    gateway = IAMGateway.from_fullstack_provider(
        provider=keycloak_provider, dpop_provider=dpop_provider
    )
    set_iam_gateway(gateway, default_organization_id=realm)
    app.state.iam_gateway = gateway
    app.state.default_organization_id = realm
    yield

app = FastAPI(title="DPoP Keycloak Demo", lifespan=lifespan)
```
{% endstep %}

{% step %}
#### Protect Endpoints

```python
from fastapi import Depends
from gl_iam import User
from gl_iam.fastapi import get_current_user_with_dpop
from pydantic import BaseModel

class UserResponse(BaseModel):
    id: str
    email: str
    display_name: str | None
    roles: list[str]

@app.get("/api/protected", response_model=UserResponse)
async def get_protected(user: User = Depends(get_current_user_with_dpop)):
    return UserResponse(
        id=user.id,
        email=user.email,
        display_name=user.display_name,
        roles=user.roles,
    )
```
{% endstep %}

{% step %}
#### Run The Server

```shellscript
uv run uvicorn main:app --reload
```
{% endstep %}

{% step %}
#### Test The API

Before you can access the protected resource, refer to Generate Proof page to understand how [DPoP proof generation](generate-proof.md) works.

```shellscript
# Generate your DPoP key pair
uv run generate_key.py

# Get DPoP-bound token
DPOP_PROOF=$(uv run create_proof.py POST "http://localhost:8080/realms/dpop-demo/protocol/openid-connect/token")
TOKEN=$(curl -s -X POST "http://localhost:8080/realms/dpop-demo/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "DPoP: $DPOP_PROOF" \
  -d "client_id=dpop-client" \
  -d "client_secret=dpop-secret" \
  -d "grant_type=password" \
  -d "username=user@example.com" \
  -d "password=user123" | jq -r '.access_token')

# Access protected endpoint (recreate proof if it's already consumed to avoid DPoP replay error)
RESOURCE_PROOF=$(uv run create_proof.py GET "http://localhost:8000/api/protected" "$TOKEN")
curl http://localhost:8000/api/protected \
  -H "Authorization: DPoP $TOKEN" \
  -H "DPoP: $RESOURCE_PROOF"
```
{% endstep %}
{% endstepper %}

{% hint style="success" %}
Congratulations! You've integrated DPoP to your server using Keycloak provider.
{% endhint %}

## Complete Example

Create `main.py`:

```python
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from pydantic import BaseModel
from gl_iam import DPoPConfig, IAMGateway, User
from gl_iam.fastapi import (
    get_current_user_with_dpop,
    set_iam_gateway,
)
from gl_iam.providers.keycloak import (
    KeycloakConfig,
    KeycloakProvider,
)
from gl_iam.providers.keycloak.dpop import KeycloakDPoPProvider


load_dotenv()

server_url = os.getenv("KEYCLOAK_SERVER_URL")
realm = os.getenv("KEYCLOAK_REALM")
client_id = os.getenv("KEYCLOAK_CLIENT_ID")
client_secret = os.getenv("KEYCLOAK_CLIENT_SECRET")

@asynccontextmanager
async def lifespan(_: FastAPI):
    """Initialize GL-IAM gateway with Keycloak and DPoP support."""
    keycloak_config = KeycloakConfig(
        server_url=server_url,
        realm=realm,
        client_id=client_id,
        client_secret=client_secret,
    )

    keycloak_provider = KeycloakProvider(config=keycloak_config)

    dpop_config = DPoPConfig(enabled=True, required=False, nonce_enabled=False)
    dpop_provider = KeycloakDPoPProvider(
        keycloak_config=keycloak_config, dpop_config=dpop_config
    )
    gateway = IAMGateway.from_fullstack_provider(
        provider=keycloak_provider, dpop_provider=dpop_provider
    )
    set_iam_gateway(gateway, default_organization_id=realm)

    is_healthy = await keycloak_provider.health_check()
    if is_healthy:
        print(f"Connected to Keycloak at {server_url}")
        print("DPoP is enabled - tokens will be bound to client keys")
    else:
        print(f"Failed to connect to Keycloak at {server_url}")
        raise RuntimeError("Cannot start server without Keycloak connection")

    app.state.iam_gateway = gateway
    app.state.default_organization_id = realm
    yield

app = FastAPI(title="DPoP Keycloak Demo", lifespan=lifespan)

class UserResponse(BaseModel):
    id: str
    email: str
    display_name: str | None
    roles: list[str]

@app.get("/api/protected", response_model=UserResponse)
async def get_protected(user: User = Depends(get_current_user_with_dpop)):
    return UserResponse(
        id=user.id,
        email=user.email,
        display_name=user.display_name,
        roles=user.roles,
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Run it:

```shellscript
uv run main.py
```

## Error Code Table

| Error            | Meaning                      |
| ---------------- | ---------------------------- |
| 401              | Missing / invalid DPoP proof |
| 401 + DPoP-Nonce | Nonce required               |
| 403              | Token bound to different key |

## Common Pitfalls

| Pitfall                                                          | Symptom                                                | Solution                                                                          |
| ---------------------------------------------------------------- | ------------------------------------------------------ | --------------------------------------------------------------------------------- |
| Using `get_current_user` instead of `get_current_user_with_dpop` | DPoP proofs are ignored and bearer tokens are accepted | Use `get_current_user_with_dpop` for endpoints that require proof-of-possession   |
| Accepting `Authorization: Bearer` for DPoP endpoints             | Stolen tokens can still be replayed                    | Require `Authorization: DPoP <token>` for DPoP-protected routes                   |
| DPoP provider not configured in the gateway                      | All DPoP requests fail validation                      | Ensure `KeycloakDPoPProvider` is passed to `IAMGateway.from_fullstack_provider()` |
| `cnf.jkt` missing in access token                                | Token is not bound to a client key                     | Verify that DPoP was used during the token request to Keycloak                    |
| Proof signature validates but request still fails                | Key thumbprint mismatch                                | Confirm the client is using the same key pair used during token issuance          |
| Forgetting to enable DPoP in `DPoPConfig`                        | DPoP headers are ignored                               | Set `DPoPConfig(enabled=True)` explicitly                                         |
| Enabling nonce without client support                            | Clients fail after first request                       | Only enable nonce protection if clients implement retry logic                     |
| Assuming DPoP replaces authorization                             | Users can authenticate but access still fails          | DPoP protects tokens; role checks and permissions are still enforced separately   |

## Production Notes

**Security Guidelines for Production Deployments**

* **Avoid Key Generation at Runtime**
  * Do not generate keys during runtime in production.
  * Each client must maintain a **stable, persistent key pair**.
* **Key Storage**
  * **Browsers**: Use IndexedDB or WebCrypto-backed storage.
  * **Non-browser clients**: Utilize secure keystores or encrypted disk storage.
  * **Important**: Protect private keys as secrets.
* **Handling DPoP Private Keys**
  * DPoP private keys are as sensitive as access tokens. Treat them with care:
    * **Do not log them.**
    * **Do not commit them to version control.**
    * **Do not transmit them over the network.**
* **Exclusively Use HTTPS**
  * DPoP does not replace TLS. Always use HTTPS to secure headers, proofs, and tokens during transit.
* **Nonce Handling**
  * If your server requires nonce-based replay protection:
    * Detect `401` responses with `DPoP-Nonce`.
    * Regenerate the proof including the nonce.
    * Retry the request as necessary.
* **Key Pair Segregation**
  * Never share keys across users or devices.
  * Each user-agent instance should have its **own key pair** to maintain DPoP security guarantees.

***

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url\&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Fdpop%2Fprotect-your-api).
{% endhint %}
