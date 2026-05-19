---
icon: bolt-lightning
---

# Quickstart: Stack Auth

Integrate GL IAM with Stack Auth for modern, managed authentication.

{% hint style="info" %}
**What you'll build**: A FastAPI app with authenticated and role-protected endpoints using GL IAM + Stack Auth.
{% endhint %}

<details>

<summary>Prerequisites</summary>

* Python 3.11+
* Access to the **GDP Labs' Gen AI SDK repository** (request via [form](https://docs.google.com/forms/d/e/1FAIpQLScJxB-Xe9YjnohIzW6nic-_AeSJob6Il6spl1s85wc76tQkzQ/viewform) or ticket@gdplabs.id)
* **gcloud CLI:** [Install](https://cloud.google.com/sdk/docs/install), then run `gcloud auth login`
* [uv](https://docs.astral.sh/uv/) — Install with: `curl -LsSf https://astral.sh/uv/install.sh | sh`
* A Stack Auth project with API keys ([Cloud](https://app.stack-auth.com/) or [self-hosted](https://docs.stack-auth.com))

</details>

## Setup Stack Auth

{% tabs %}
{% tab title="Stack Auth Cloud" %}
1. Go to [Stack Auth Dashboard](https://app.stack-auth.com/) and create a new project
2. Note your **Project ID**, **Publishable Client Key**, and **Secret Server Key**
3. Go to **Team Settings** → turn on **"Create a personal team for each user on sign-up"**
{% endtab %}

{% tab title="Self-Hosted" %}
```bash
git clone https://github.com/stack-auth/stack-auth.git && cd stack-auth
pnpm install && pnpm build:packages && pnpm codegen
pnpm restart-deps && pnpm dev
```

Dashboard: `http://localhost:8100` · API: `http://localhost:8102`

The `internal` project has team auto-creation pre-enabled. Use these credentials:

```
Project ID: internal
Publishable Client Key: this-publishable-client-key-is-for-local-development-only
Secret Server Key: this-secret-server-key-is-for-local-development-only
```
{% endtab %}
{% endtabs %}

## Step-by-Step

{% stepper %}
{% step %}
#### Install GL IAM

```bash
uv init --bare
uv add --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" "gl-iam[fastapi,stackauth]"
uv add python-dotenv uvicorn
```
{% endstep %}

{% step %}
#### Create `.env`

{% tabs %}
{% tab title="Stack Auth Cloud" %}
```bash
STACKAUTH_BASE_URL=https://api.stack-auth.com
STACKAUTH_PROJECT_ID=your-project-id
STACKAUTH_PUBLISHABLE_CLIENT_KEY=pck_your_key
STACKAUTH_SECRET_SERVER_KEY=ssk_your_key
```
{% endtab %}
{% tab title="Self-Hosted" %}
```bash
STACKAUTH_BASE_URL=http://localhost:8102
STACKAUTH_PROJECT_ID=internal
STACKAUTH_PUBLISHABLE_CLIENT_KEY=this-publishable-client-key-is-for-local-development-only
STACKAUTH_SECRET_SERVER_KEY=this-secret-server-key-is-for-local-development-only
```
{% endtab %}
{% endtabs %}
{% endstep %}

{% step %}
#### Create `main.py`

This is the complete application — provider setup, authentication, and role-based access in one file:

```python
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import Depends, FastAPI

from gl_iam import IAMGateway, User
from gl_iam.fastapi import get_current_user, require_org_member, set_iam_gateway
from gl_iam.providers.stackauth import StackAuthConfig, StackAuthProvider

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    config = StackAuthConfig(
        base_url=os.getenv("STACKAUTH_BASE_URL"),
        project_id=os.getenv("STACKAUTH_PROJECT_ID"),
        publishable_client_key=os.getenv("STACKAUTH_PUBLISHABLE_CLIENT_KEY"),
        secret_server_key=os.getenv("STACKAUTH_SECRET_SERVER_KEY"),
    )
    provider = StackAuthProvider(config)
    gateway = IAMGateway.from_fullstack_provider(provider)
    set_iam_gateway(gateway, default_organization_id=os.getenv("STACKAUTH_PROJECT_ID"))
    yield
    await provider.close()


app = FastAPI(lifespan=lifespan)


@app.get("/me")
async def get_me(user: User = Depends(get_current_user)):
    return {"email": user.email, "roles": user.roles}


@app.get("/member-area")
async def member_area(
    user: User = Depends(get_current_user),
    _: None = Depends(require_org_member()),
):
    return {"message": f"Welcome {user.email}!", "access_level": "member"}
```

**What's happening:**

1. `StackAuthProvider` connects GL IAM to your Stack Auth project
2. `IAMGateway.from_fullstack_provider()` creates a unified auth gateway
3. `get_current_user` validates the Stack Auth token and returns a `User`
4. `require_org_member()` enforces that the user has the `ORG_MEMBER` role (or higher)
{% endstep %}

{% step %}
#### Run

```bash
uv run uvicorn main:app --reload
```
{% endstep %}

{% step %}
#### Test

**Sign up a user:**

{% tabs %}
{% tab title="Stack Auth Cloud" %}
```bash
curl -s -X POST https://api.stack-auth.com/api/v1/auth/password/sign-up \
  -H "Content-Type: application/json" \
  -H "x-stack-access-type: client" \
  -H "x-stack-project-id: $STACKAUTH_PROJECT_ID" \
  -H "x-stack-publishable-client-key: $STACKAUTH_PUBLISHABLE_CLIENT_KEY" \
  -d '{"email": "test@example.com", "password": "SecurePass123", "verification_callback_url": "http://localhost:3000/verify"}'
```
{% endtab %}
{% tab title="Self-Hosted" %}
```bash
curl -s -X POST http://localhost:8102/api/v1/auth/password/sign-up \
  -H "Content-Type: application/json" \
  -H "x-stack-access-type: client" \
  -H "x-stack-project-id: $STACKAUTH_PROJECT_ID" \
  -H "x-stack-publishable-client-key: $STACKAUTH_PUBLISHABLE_CLIENT_KEY" \
  -d '{"email": "test@example.com", "password": "SecurePass123", "verification_callback_url": "http://localhost:3000/verify"}'
```
{% endtab %}
{% endtabs %}

**Copy the `access_token` from the response, then test your GL IAM endpoints:**

```bash
TOKEN="<paste access_token here>"

curl http://localhost:8000/me -H "Authorization: Bearer $TOKEN"
# {"email":"test@example.com","roles":["admin"]}

curl http://localhost:8000/member-area -H "Authorization: Bearer $TOKEN"
# {"message":"Welcome test@example.com!","access_level":"member"}
```

{% hint style="warning" %}
**Token expired?** Access tokens are short-lived. Sign in again to get a fresh one:

{% tabs %}
{% tab title="Stack Auth Cloud" %}
```bash
curl -s -X POST https://api.stack-auth.com/api/v1/auth/password/sign-in \
  -H "Content-Type: application/json" \
  -H "x-stack-access-type: client" \
  -H "x-stack-project-id: $STACKAUTH_PROJECT_ID" \
  -H "x-stack-publishable-client-key: $STACKAUTH_PUBLISHABLE_CLIENT_KEY" \
  -d '{"email": "test@example.com", "password": "SecurePass123"}'
```
{% endtab %}
{% tab title="Self-Hosted" %}
```bash
curl -s -X POST http://localhost:8102/api/v1/auth/password/sign-in \
  -H "Content-Type: application/json" \
  -H "x-stack-access-type: client" \
  -H "x-stack-project-id: $STACKAUTH_PROJECT_ID" \
  -H "x-stack-publishable-client-key: $STACKAUTH_PUBLISHABLE_CLIENT_KEY" \
  -d '{"email": "test@example.com", "password": "SecurePass123"}'
```
{% endtab %}
{% endtabs %}
{% endhint %}
{% endstep %}
{% endstepper %}

{% hint style="success" %}
**Done!** You've authenticated a user and enforced role-based access with GL IAM + Stack Auth.
{% endhint %}

## How Roles Work

GL IAM maps Stack Auth **team permissions** to standard roles:

| Stack Auth | GL IAM | Passes |
| ---------- | ------ | ------ |
| `team_admin` | `ORG_ADMIN` | `require_org_member()`, `require_org_admin()` |
| `team_member` | `ORG_MEMBER` | `require_org_member()` |

When "Create personal team on sign-up" is enabled, each user gets a personal team with `team_admin` on sign-up — so roles work automatically.

<details>

<summary>Troubleshooting: <code>/me</code> returns empty roles</summary>

If `/me` returns `"roles": []` and `/member-area` returns 500, your user has no team. This happens when "Create personal team on sign-up" is not enabled in your Stack Auth project.

**Fix — Option A:** Enable it in the Stack Auth dashboard → **Team Settings**.

**Fix — Option B:** Load your `.env` values and create a team manually:

```bash
# Load your .env values into the shell
export $(grep -v '^#' .env | xargs)

USER_ID="<user_id from sign-up response>"

# Create team with user as creator (auto-grants team_admin)
TEAM_ID=$(curl -s -X POST $STACKAUTH_BASE_URL/api/v1/teams \
  -H "Content-Type: application/json" \
  -H "x-stack-access-type: server" \
  -H "x-stack-project-id: $STACKAUTH_PROJECT_ID" \
  -H "x-stack-secret-server-key: $STACKAUTH_SECRET_SERVER_KEY" \
  -d "{\"display_name\": \"Default Team\", \"creator_user_id\": \"$USER_ID\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

# Set user's active team
curl -s -X PATCH "$STACKAUTH_BASE_URL/api/v1/users/$USER_ID" \
  -H "Content-Type: application/json" \
  -H "x-stack-access-type: server" \
  -H "x-stack-project-id: $STACKAUTH_PROJECT_ID" \
  -H "x-stack-secret-server-key: $STACKAUTH_SECRET_SERVER_KEY" \
  -d "{\"selected_team_id\": \"$TEAM_ID\"}"
```

Then sign in again to get a fresh token.

</details>

<details>

<summary>Getting tokens from React/Next.js</summary>

```typescript
import { useUser } from "@stackframe/stack";

function MyComponent() {
  const user = useUser();

  async function callAPI() {
    const token = await user.getAuthJson();
    const res = await fetch("http://localhost:8000/me", {
      headers: { Authorization: `Bearer ${token.accessToken}` },
    });
    return res.json();
  }
}
```

</details>

---

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Fquickstart%2Fquickstart-stack-auth).
{% endhint %}
