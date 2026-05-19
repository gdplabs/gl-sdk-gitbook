---
description: Federate users from LDAP/Active Directory through Keycloak
icon: address-book
---

# LDAP Authentication

{% hint style="info" %}
**What you'll build**: A FastAPI application where users from your corporate LDAP/Active Directory can authenticate via Keycloak, with GL IAM handling authorization and role-based access control.
{% endhint %}

{% hint style="info" %}
**How it works**: Keycloak's **User Federation** feature connects to your LDAP directory, imports/syncs users, and issues OIDC tokens. GL IAM validates these tokens — your application code is identical to any other Keycloak setup.
{% endhint %}

<details>

<summary>Prerequisites</summary>

This example requires completion of all setup steps listed on the [Prerequisites](../../../prerequisites.md) page. To summarize:

* Python 3.11+
* Docker and Docker Compose
* Access to the **GDP Labs' Gen AI SDK repository** (request via [form](https://docs.google.com/forms/d/e/1FAIpQLScJxB-Xe9YjnohIzW6nic-_AeSJob6Il6spl1s85wc76tQkzQ/viewform) or ticket@gdplabs.id)
* **gcloud CLI:** [Install](https://cloud.google.com/sdk/docs/install), then run `gcloud auth login`
* [uv](https://docs.astral.sh/uv/) — Install with: `curl -LsSf https://astral.sh/uv/install.sh | sh`

No external LDAP server needed — we'll run OpenLDAP locally with Docker.

</details>

## Architecture

<figure><img src="../../../../.gitbook/assets/GL IAM - LDAP Authentication.png" alt=""><figcaption></figcaption></figure>

1. **OpenLDAP** stores corporate users (e.g., `uid=jdoe,ou=People,dc=example,dc=org`)
2. **Keycloak** connects to OpenLDAP via User Federation, syncs users on login
3. **Your FastAPI app** validates Keycloak-issued tokens via `KeycloakProvider`

## Setup Keycloak + OpenLDAP

Create `docker-compose.yml`:

```yaml
services:
  openldap:
    image: osixia/openldap:1.5.0
    container_name: ldap-keycloak-openldap
    environment:
      LDAP_ORGANISATION: "Example Corp"
      LDAP_DOMAIN: "example.org"
      LDAP_ADMIN_PASSWORD: "adminpassword"
    ports:
      - "389:389"

  keycloak-db:
    image: postgres:16-alpine
    container_name: ldap-keycloak-db
    environment:
      POSTGRES_DB: keycloak
      POSTGRES_USER: keycloak
      POSTGRES_PASSWORD: keycloak
    volumes:
      - keycloak_db_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U keycloak -d keycloak"]
      interval: 5s
      timeout: 5s
      retries: 10

  keycloak:
    image: quay.io/keycloak/keycloak:26.0
    container_name: ldap-keycloak
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
      openldap:
        condition: service_started

volumes:
  keycloak_db_data:
```

Start services:

```bash
docker-compose up -d
```

Wait for Keycloak to be ready (30–60 seconds on first start). Verify:

```bash
curl -s http://localhost:8080/realms/master | jq .realm
# Expected: "master"
```

Admin console: [http://localhost:8080/admin](http://localhost:8080/admin) (credentials: `admin` / `admin`)

## Create Realm and Client

In the Keycloak Admin Console:

1. Create a new realm: **gl-iam-ldap-demo**
2. Go to **Clients** → **Create client**:

| Setting               | Value            |
| --------------------- | ---------------- |
| Client ID             | `glchat-backend` |
| Client authentication | ON               |
| Direct access grants  | Enabled          |

3. In the **Credentials** tab, set Client Secret to `glchat-backend-secret`
4. Go to **Realm settings** → **Roles** → Create roles: `admin` and `member`

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

The GL IAM code is exactly the same as a standard Keycloak setup — no LDAP-specific code needed:

```python
config = KeycloakConfig(server_url="http://localhost:8080", realm="gl-iam-ldap-demo",
                        client_id="glchat-backend", client_secret="glchat-backend-secret")
provider = KeycloakProvider(config=config)
gateway = IAMGateway.from_fullstack_provider(provider)
set_iam_gateway(gateway, default_organization_id="gl-iam-ldap-demo")
# LDAP users authenticate through Keycloak — no code changes needed
```

## Step-by-Step

{% stepper %}
{% step %}
**1. Configure LDAP in Keycloak**

The key step is configuring **User Federation** in Keycloak's admin console. This connects Keycloak to your LDAP directory.

**Using Keycloak Admin Console** (http://localhost:8080/admin):

1. Select realm **gl-iam-ldap-demo**
2. Go to **User federation** → **Add LDAP provider**
3. Configure the connection:

| Setting                 | Value (OpenLDAP example)            |
| ----------------------- | ----------------------------------- |
| Vendor                  | Other                               |
| Connection URL          | `ldap://ldap-keycloak-openldap:389` |
| Bind DN                 | `cn=admin,dc=example,dc=org`        |
| Bind Credential         | `adminpassword`                     |
| Users DN                | `ou=People,dc=example,dc=org`       |
| Username LDAP attribute | `uid`                               |
| UUID LDAP attribute     | `entryUUID`                         |
| User Object Classes     | `inetOrgPerson`                     |
| Search Scope            | Subtree                             |

4. Click **Test connection** and **Test authentication**
5. Set **Sync Settings** → Import users: ON
6. Click **Save**, then **Synchronize all users**
7. Go to **Users** and assign the `member` role to synced users
{% endstep %}

{% step %}
**2. Configure Environment**

Create `.env` file:

```bash
KEYCLOAK_SERVER_URL=http://localhost:8080
KEYCLOAK_REALM=gl-iam-ldap-demo
KEYCLOAK_CLIENT_ID=glchat-backend
KEYCLOAK_CLIENT_SECRET=glchat-backend-secret
```
{% endstep %}

{% step %}
**3. Write Your Application**

Create `main.py` — your FastAPI app is identical to any Keycloak example, no LDAP-specific code:

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
        print("Connected to Keycloak (LDAP federation active)")
    yield

app = FastAPI(title="GL-IAM LDAP via Keycloak", lifespan=lifespan)

@app.get("/me")
async def get_me(user: User = Depends(get_current_user)):
    """Works for both LDAP-federated and local Keycloak users."""
    return {"id": user.id, "email": user.email, "roles": user.roles}

@app.get("/member-area")
async def member_area(
    user: User = Depends(get_current_user),
    _: None = Depends(require_org_member()),
):
    return {"message": f"Welcome {user.email}!", "source": "LDAP or local"}

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
**4. Test with LDAP Users**

Get a token for an LDAP-federated user via Keycloak's token endpoint:

```bash
# Authenticate an LDAP user through Keycloak
TOKEN=$(curl -s -X POST "http://localhost:8080/realms/gl-iam-ldap-demo/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=password" \
  -d "client_id=glchat-backend" \
  -d "client_secret=glchat-backend-secret" \
  -d "username=jdoe" \
  -d "password=jdoe123" | jq -r '.access_token')

# Access protected endpoint — same as any other user
curl http://localhost:8000/me -H "Authorization: Bearer $TOKEN"
```
{% endstep %}
{% endstepper %}

## Map LDAP Groups to Keycloak Roles (Optional)

To automatically map LDAP groups to GL IAM roles:

1. In the LDAP provider settings, go to **Mappers** → **Add mapper**
2. Choose **group-ldap-mapper**:

| Setting                   | Value                         |
| ------------------------- | ----------------------------- |
| LDAP Groups DN            | `ou=Groups,dc=example,dc=org` |
| Group Object Classes      | `groupOfNames`                |
| Membership LDAP Attribute | `member`                      |
| Mode                      | READ\_ONLY                    |

3. Map LDAP groups to Keycloak roles that GL IAM recognizes:
   * LDAP group `admins` → Keycloak role `admin` → GL IAM `ORG_ADMIN`
   * LDAP group `members` → Keycloak role `member` → GL IAM `ORG_MEMBER`

## Common Pitfalls

| Problem                            | Why                              | Solution                                                                                           |
| ---------------------------------- | -------------------------------- | -------------------------------------------------------------------------------------------------- |
| LDAP users can't log in            | User Federation not synced       | Click "Synchronize all users" in Keycloak admin, or enable periodic sync                           |
| Roles not mapped                   | No LDAP group mapper             | Add a group-ldap-mapper in Keycloak's LDAP provider settings                                       |
| `organization_id` missing in token | No protocol mapper for org claim | Add a Hardcoded Claim mapper in Keycloak: `organization_id` = your org ID                          |
| Connection refused to LDAP         | Docker networking                | Use Docker container name (`ldap://ldap-keycloak-openldap:389`) not `localhost` in Keycloak config |

## Production Notes

{% hint style="warning" %}
**Security considerations for production LDAP integration:**

* Use **LDAPS** (port 636) or **StartTLS** for encrypted LDAP connections
* Use a **read-only bind account** for Keycloak's LDAP connection
* Enable **periodic sync** (not just on-demand) to detect disabled/deleted accounts
* Configure **connection pooling** in Keycloak for LDAP connections
* Set appropriate **cache policies** to balance performance vs. freshness
{% endhint %}

## Cookbook Example

For a complete, runnable example with Docker Compose (Keycloak + OpenLDAP + pre-configured realm), see the cookbook:

[LDAP + Keycloak Cookbook Example](https://github.com/gdplabs/gl-iam-cookbook/tree/main/traditional-iam/ldap-keycloak)

***

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url\&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Fenterprise-protocols%2Fldap-authentication).
{% endhint %}
