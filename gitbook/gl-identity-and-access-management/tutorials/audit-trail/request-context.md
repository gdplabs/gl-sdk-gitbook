---
icon: globe
---

# Request Context

Attach IP address and user agent to every audit event automatically.

{% hint style="info" %}
**When to use**: When running behind a web framework (FastAPI, Django) and you want `ip_address` / `user_agent` on every audit event without passing them manually.
{% endhint %}

<details>

<summary>Prerequisites</summary>

* Completed [Console Logging](console-logging.md)
* A web framework (FastAPI or Django) application

</details>

## 5-Line Core

```python
from gl_iam import set_audit_context, clear_audit_context

set_audit_context(ip_address="192.168.1.1", user_agent="Mozilla/5.0")
result = await gateway.authenticate(credentials, organization_id="default")
# AuditEvent now has ip_address and user_agent populated automatically
clear_audit_context()
```

## How It Works

GL IAM uses Python's `contextvars` to store request-scoped metadata. You call `set_audit_context()` once in middleware, and all audit events emitted during that request inherit `ip_address` and `user_agent` automatically.

```
Request arrives
    │
    ▼
Middleware: set_audit_context(ip, ua)
    │
    ▼
Your endpoint code → gateway.authenticate(...)
    │                        │
    │                  AuditEvent created
    │                  ip_address ← from context
    │                  user_agent ← from context
    │
    ▼
Middleware finally: clear_audit_context()
```

Events with explicitly set `ip_address` or `user_agent` are **not** overwritten by the context.

## Step-by-Step

{% stepper %}
{% step %}
#### FastAPI Middleware

```python
from gl_iam import set_audit_context, clear_audit_context

@app.middleware("http")
async def audit_context_middleware(request, call_next):
    set_audit_context(
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent"),
    )
    try:
        return await call_next(request)
    finally:
        clear_audit_context()
```
{% endstep %}

{% step %}
#### Django Middleware

```python
from gl_iam import set_audit_context, clear_audit_context


class AuditContextMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        set_audit_context(
            ip_address=self._get_client_ip(request),
            user_agent=request.META.get("HTTP_USER_AGENT"),
        )
        try:
            return self.get_response(request)
        finally:
            clear_audit_context()

    @staticmethod
    def _get_client_ip(request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")
```

Add to `settings.py`:

```python
MIDDLEWARE = [
    "myapp.middleware.AuditContextMiddleware",
    # ... other middleware
]
```
{% endstep %}

{% step %}
#### Verify Enrichment

With the middleware in place, trigger a login and observe the audit output:

```python
@app.post("/login")
async def login(username: str, password: str):
    result = await gateway.authenticate(
        credentials=Credentials(username=username, password=password),
        organization_id="default",
    )
    return {"status": "ok" if result.is_ok else "error"}
```
{% endstep %}

{% step %}
#### Expected Output

```
INFO:gl_iam.audit:audit_event: login_success
  audit_event_type=login_success
  audit_severity=info
  audit_user_id=usr_abc123
  audit_ip_address=192.168.1.42
  audit_user_agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)
```

The `ip_address` and `user_agent` fields are now populated automatically.
{% endstep %}
{% endstepper %}

{% hint style="success" %}
Every audit event now carries request metadata without any changes to your auth logic.
{% endhint %}

## Complete Example

Create `fastapi_audit.py`:

```python
"""GL IAM FastAPI with Audit Context Example."""

import asyncio
import logging

from fastapi import FastAPI
from gl_iam import IAMGateway, ConsoleAuditHandler, set_audit_context, clear_audit_context
from gl_iam.core.types.auth import Credentials
from gl_iam.providers.postgresql import PostgreSQLProvider, PostgreSQLConfig

logging.basicConfig(level=logging.INFO)

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/gliam"

app = FastAPI()
provider: PostgreSQLProvider
gateway: IAMGateway


@app.on_event("startup")
async def startup():
    global provider, gateway
    config = PostgreSQLConfig(database_url=DATABASE_URL)
    provider = PostgreSQLProvider(config)
    gateway = IAMGateway(
        auth_provider=provider,
        user_store=provider,
        session_provider=provider,
        audit_handlers=[ConsoleAuditHandler()],
    )


@app.on_event("shutdown")
async def shutdown():
    await provider.close()


@app.middleware("http")
async def audit_context_middleware(request, call_next):
    set_audit_context(
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent"),
    )
    try:
        return await call_next(request)
    finally:
        clear_audit_context()


@app.post("/login")
async def login(username: str, password: str):
    result = await gateway.authenticate(
        credentials=Credentials(username=username, password=password),
        organization_id="default",
    )
    if result.is_ok:
        return {"user_id": result.user.id, "token": result.token}
    return {"error": result.error.message}
```

Run it:

```bash
uvicorn fastapi_audit:app --reload
```

## API Reference

| Function | Description |
| --- | --- |
| `set_audit_context(ip_address=None, user_agent=None)` | Set context for the current request/task |
| `get_audit_context()` | Get the current `AuditContext` or `None` |
| `clear_audit_context()` | Clear context (call in middleware `finally` block) |

## Common Pitfalls

| Pitfall | Solution |
| --- | --- |
| Missing `clear_audit_context()` in `finally` | Context can leak to the next request in the same async task |
| Using raw `X-Forwarded-For` | Parse the first IP from the comma-separated list |
| Context not in background tasks | `contextvars` does not auto-propagate to `asyncio.create_task()` — set context explicitly |

---

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Faudit-trail%2Frequest-context).
{% endhint %}
