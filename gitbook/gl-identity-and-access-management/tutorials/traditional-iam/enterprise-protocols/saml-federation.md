---
description: Enable SAML 2.0 SSO with external Identity Providers through Keycloak
icon: handshake
---

# SAML Federation

{% hint style="info" %}
**What you'll build**: A FastAPI application where users from a SAML 2.0 Identity Provider (e.g., Azure AD, Okta, ADFS) can single sign-on via Keycloak, with GL IAM handling authorization.
{% endhint %}

{% hint style="info" %}
**How it works**: Keycloak acts as a **SAML Service Provider (SP)** that trusts your corporate **SAML Identity Provider (IdP)**. Users authenticate at the IdP, Keycloak receives the SAML assertion, and issues an OIDC token that GL IAM validates.
{% endhint %}

<details>

<summary>Prerequisites</summary>

This example requires completion of all setup steps listed on the [Prerequisites](../../../prerequisites.md) page. To summarize:

* Python 3.11+
* Docker and Docker Compose
* Access to the **GDP Labs' Gen AI SDK repository** (request via [form](https://docs.google.com/forms/d/e/1FAIpQLScJxB-Xe9YjnohIzW6nic-_AeSJob6Il6spl1s85wc76tQkzQ/viewform) or ticket@gdplabs.id)
* **gcloud CLI:** [Install](https://cloud.google.com/sdk/docs/install), then run `gcloud auth login`
* [uv](https://docs.astral.sh/uv/) — Install with: `curl -LsSf https://astral.sh/uv/install.sh | sh`

</details>

## Architecture

<figure><img src="../../../../.gitbook/assets/GL IAM - SAML Federation.png" alt=""><figcaption></figcaption></figure>

1. User clicks "Login with SSO" → redirected to corporate IdP
2. IdP authenticates user → sends SAML assertion to Keycloak
3. Keycloak maps SAML attributes to OIDC claims → issues token
4. GL IAM validates the OIDC token — your app code is unchanged

## Setup Keycloak

Create `docker-compose.yml`:

```yaml
services:
  keycloak-db:
    image: postgres:16-alpine
    container_name: saml-keycloak-sp-db
    environment:
      POSTGRES_DB: keycloak
      POSTGRES_USER: keycloak
      POSTGRES_PASSWORD: keycloak
    volumes:
      - keycloak_sp_db_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U keycloak -d keycloak"]
      interval: 5s
      timeout: 5s
      retries: 10

  keycloak-sp:
    image: quay.io/keycloak/keycloak:26.0
    container_name: saml-keycloak-sp
    command: start-dev
    environment:
      KC_DB: postgres
      KC_DB_URL: jdbc:postgresql://keycloak-db:5432/keycloak
      KC_DB_USERNAME: keycloak
      KC_DB_PASSWORD: keycloak
      KEYCLOAK_ADMIN: admin
      KEYCLOAK_ADMIN_PASSWORD: admin
      KC_HOSTNAME: localhost
      KC_HTTP_ENABLED: "true"
    ports:
      - "8080:8080"
    depends_on:
      keycloak-db:
        condition: service_healthy

volumes:
  keycloak_sp_db_data:
```

Start services:

```bash
docker-compose up -d
```

Wait for Keycloak to be ready (30–60 seconds). Verify:

```bash
curl -s http://localhost:8080/realms/master | jq .realm
# Expected: "master"
```

Admin console: [http://localhost:8080/admin](http://localhost:8080/admin) (credentials: `admin` / `admin`)

## Create Realm and Client

In the Keycloak Admin Console:

1. Create a new realm: **gl-iam-saml-demo**
2. Go to **Clients** → **Create client**:

| Setting               | Value            |
| --------------------- | ---------------- |
| Client ID             | `glchat-backend` |
| Client authentication | ON               |
| Direct access grants  | Enabled          |

3. In the **Credentials** tab, set Client Secret to `glchat-backend-secret`
4. In **Settings** → Valid redirect URIs, add: `http://localhost:8000/*`
5. Go to **Realm settings** → **Roles** → Create roles: `admin` and `member`
6. In **Realm settings** → **Default roles**, add `member` so all federated users get the member role

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
uv init --bare
uv add --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" "gl-iam[fastapi,keycloak]"
uv add python-dotenv uvicorn pyjwt
```
{% endtab %}

{% tab title="Windows PowerShell" %}
```powershell
uv init --bare
$token = (gcloud auth print-access-token)
uv add --extra-index-url "https://oauth2accesstoken:$token@glsdk.gdplabs.id/gen-ai-internal/simple/" "gl-iam[fastapi,keycloak]"
uv add python-dotenv uvicorn pyjwt
```
{% endtab %}
{% endtabs %}

## 5-Line Core

The GL IAM code is exactly the same as a standard Keycloak setup — no SAML-specific code needed:

```python
config = KeycloakConfig(server_url="http://localhost:8080", realm="gl-iam-saml-demo",
                        client_id="glchat-backend", client_secret="glchat-backend-secret")
provider = KeycloakProvider(config=config)
gateway = IAMGateway.from_fullstack_provider(provider)
set_iam_gateway(gateway, default_organization_id="gl-iam-saml-demo")
# SAML users authenticate through Keycloak — no code changes needed
```

## Step-by-Step

{% stepper %}
{% step %}
**1. Add SAML Identity Provider in Keycloak**

In the Keycloak Admin Console (http://localhost:8080/admin):

1. Select realm **gl-iam-saml-demo**
2. Go to **Identity Providers** → **Add provider** → **SAML v2.0**
3. Configure the basic settings:

| Setting                    | Value                                                    |
| -------------------------- | -------------------------------------------------------- |
| Alias                      | `corporate-idp` (your choice)                            |
| Display Name               | `Corporate SSO`                                          |
| Single Sign-On Service URL | Your IdP's SSO URL                                       |
| NameID Policy Format       | `urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress` |
| Principal Type             | Attribute \[Name]                                        |
| Principal Attribute        | `email`                                                  |

4.  Download Keycloak's **SP metadata** from:

    ```
    http://localhost:8080/realms/gl-iam-saml-demo/protocol/saml/descriptor
    ```
5. Import this metadata into your corporate IdP (Azure AD, Okta, ADFS, etc.)
{% endstep %}

{% step %}
**2. Map SAML Attributes**

In Keycloak, go to **Identity Providers** → your SAML provider → **Mappers** → **Add mapper**:

| SAML Attribute | Keycloak Mapper Type | Target      |
| -------------- | -------------------- | ----------- |
| `email`        | Attribute Importer   | `email`     |
| `firstName`    | Attribute Importer   | `firstName` |
| `lastName`     | Attribute Importer   | `lastName`  |

**For role mapping**, add a **Hardcoded Role** mapper to assign the `member` role to all SAML users, or use **SAML Attribute to Role** for more granular mapping.
{% endstep %}

{% step %}
**3. Configure Environment**

Create `.env` file:

```bash
KEYCLOAK_SERVER_URL=http://localhost:8080
KEYCLOAK_REALM=gl-iam-saml-demo
KEYCLOAK_CLIENT_ID=glchat-backend
KEYCLOAK_CLIENT_SECRET=glchat-backend-secret
```
{% endstep %}

{% step %}
**4. Write Your Application**

Create `main.py` — your FastAPI app is identical to any Keycloak example, no SAML-specific code:

```python
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import Depends, FastAPI

from gl_iam import IAMGateway, User
from gl_iam.fastapi import get_current_user, require_org_admin, require_org_member, set_iam_gateway
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

    is_healthy = await provider.health_check()
    if is_healthy:
        print("Connected to Keycloak (SAML IdP configured)")
    yield

app = FastAPI(title="GL-IAM SAML via Keycloak", lifespan=lifespan)

@app.get("/me")
async def get_me(user: User = Depends(get_current_user)):
    """Works for both SAML-federated and local Keycloak users."""
    return {"id": user.id, "email": user.email, "roles": user.roles}

@app.get("/member-area")
async def member_area(
    user: User = Depends(get_current_user),
    _: None = Depends(require_org_member()),
):
    return {"message": f"Welcome {user.email}!", "auth_method": "SAML or local"}

@app.get("/admin-area")
async def admin_area(
    user: User = Depends(get_current_user),
    _: None = Depends(require_org_admin()),
):
    return {"message": f"Admin access for {user.email}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Run the application:

```bash
uv run main.py
```
{% endstep %}

{% step %}
**5. Test the SAML Flow**

SAML requires a **browser-based flow** (not Resource Owner Password Grant):

1.  Open your browser and navigate to the Keycloak login page:

    ```
    http://localhost:8080/realms/gl-iam-saml-demo/protocol/openid-connect/auth?client_id=glchat-backend&response_type=code&redirect_uri=http://localhost:8000/callback&scope=openid
    ```
2. Click the **"Corporate SSO"** button (your SAML IdP)
3. Authenticate at your corporate IdP
4. Keycloak receives the SAML assertion and redirects back with a token

Then test the protected endpoints:

```bash
# Use the token from the browser flow
curl http://localhost:8000/me -H "Authorization: Bearer $TOKEN"
curl http://localhost:8000/member-area -H "Authorization: Bearer $TOKEN"
```
{% endstep %}
{% endstepper %}

## Common SAML IdP Configurations

| IdP                  | SSO URL Pattern                                      | Metadata URL                                                                                   |
| -------------------- | ---------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| **Azure AD**         | `https://login.microsoftonline.com/{tenant}/saml2`   | `https://login.microsoftonline.com/{tenant}/federationmetadata/2007-06/federationmetadata.xml` |
| **Okta**             | `https://{domain}.okta.com/app/{app}/sso/saml`       | Available in Okta admin → App → Sign On → SAML Metadata                                        |
| **ADFS**             | `https://{server}/adfs/ls/`                          | `https://{server}/FederationMetadata/2007-06/FederationMetadata.xml`                           |
| **Google Workspace** | `https://accounts.google.com/o/saml2/idp?idpid={id}` | Google Admin → Apps → SAML Apps → Download Metadata                                            |

## Common Pitfalls

| Problem                   | Why                                 | Solution                                                                     |
| ------------------------- | ----------------------------------- | ---------------------------------------------------------------------------- |
| SAML assertion rejected   | Clock skew between IdP and Keycloak | Ensure NTP sync on both servers; Keycloak has a "Allowed clock skew" setting |
| Email missing from token  | SAML attribute not mapped           | Add an Attribute Importer mapper for `email` in Keycloak's IdP settings      |
| User gets no roles        | No role mapping configured          | Add a Hardcoded Role mapper or SAML Attribute to Role mapper                 |
| Redirect loop             | Incorrect redirect URIs             | Verify `redirect_uri` in Keycloak client matches your app's callback URL     |
| `organization_id` missing | No org claim in SAML assertion      | Add a Hardcoded Claim mapper in Keycloak: `organization_id` = your org ID    |

## Production Notes

{% hint style="warning" %}
**Security considerations for production SAML integration:**

* Always use **HTTPS** for both Keycloak and your application
* Enable **assertion signing** and **assertion encryption** in Keycloak
* Verify the **IdP certificate** is valid and rotated before expiry
* Configure **Force Authentication** if re-authentication is required for sensitive operations
* Set appropriate **token lifespans** — SAML assertions may have different validity than OIDC tokens
* Enable **backchannel logout** for proper session termination across systems
{% endhint %}

## Cookbook Example

For a complete, runnable example with Docker Compose (two Keycloak instances simulating IdP + SP), see the cookbook:

[SAML + Keycloak Cookbook Example](https://github.com/gdplabs/gl-iam-cookbook/tree/main/traditional-iam/saml-keycloak)

***

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url\&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Fenterprise-protocols%2Fsaml-federation).
{% endhint %}
