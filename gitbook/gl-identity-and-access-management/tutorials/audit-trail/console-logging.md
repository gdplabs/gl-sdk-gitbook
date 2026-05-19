---
icon: terminal
---

# Console Logging

Log audit events as structured JSON to stdout.

{% hint style="info" %}
**When to use**: Start here — `ConsoleAuditHandler` works in all environments (async, sync, Django, FastAPI) with zero external dependencies.
{% endhint %}

<details>

<summary>Prerequisites</summary>

* Completed [Quickstart: PostgreSQL](../traditional-iam/quickstart/quickstart-postgresql.md)
* A running PostgreSQL instance with GL IAM configured

</details>

## 5-Line Core

```python
from gl_iam import IAMGateway, ConsoleAuditHandler

handler = ConsoleAuditHandler()
gateway = IAMGateway(
    auth_provider=provider, user_store=provider, session_provider=provider,
    audit_handlers=[handler],
)
```

## Step-by-Step

{% stepper %}
{% step %}
**Import and Create Handler**

```python
from gl_iam import ConsoleAuditHandler

# Default: logs to 'gl_iam.audit' logger, severity-based log levels
handler = ConsoleAuditHandler()

# Optional: custom logger name and fixed log level
import logging
handler = ConsoleAuditHandler(
    logger_name="my_app.audit",
    log_level=logging.INFO,  # None = maps from AuditSeverity
)
```

The handler logs to a dedicated Python logger so you can configure it independently (e.g., route to a separate file).
{% endstep %}

{% step %}
**Wire into IAMGateway**

```python
from gl_iam import IAMGateway
from gl_iam.providers.postgresql import PostgreSQLProvider, PostgreSQLConfig

config = PostgreSQLConfig(
    database_url="postgresql+asyncpg://postgres:postgres@localhost:5432/gliam",
)
provider = PostgreSQLProvider(config)

# Pass audit_handlers to the constructor (not from_fullstack_provider)
gateway = IAMGateway(
    auth_provider=provider,
    user_store=provider,
    session_provider=provider,
    audit_handlers=[handler],
)
```

{% hint style="warning" %}
`from_fullstack_provider()` does **not** wire audit handlers. Use the `IAMGateway()` constructor directly.
{% endhint %}
{% endstep %}

{% step %}
**Configure Python Logging**

```python
import logging

# Basic setup — see audit events in console
logging.basicConfig(level=logging.INFO)
```

For structured JSON output, configure `python-json-logger` (already a GL IAM dependency):

```python
import logging
from pythonjsonlogger import jsonlogger

handler = logging.StreamHandler()
handler.setFormatter(jsonlogger.JsonFormatter())
logging.getLogger("gl_iam.audit").addHandler(handler)
logging.getLogger("gl_iam.audit").setLevel(logging.DEBUG)
```
{% endstep %}

{% step %}
**Trigger an Event**

```python
from gl_iam.core.types.auth import Credentials

result = await gateway.authenticate(
    credentials=Credentials(username="alice", password="secret123"),
    organization_id="default",
)
# An audit event is emitted automatically!
```
{% endstep %}

{% step %}
**Expected Output**

```
INFO:gl_iam.audit:audit_event: login_success
  audit_event_type=login_success
  audit_severity=info
  audit_timestamp=2026-04-06T10:30:00+00:00
  audit_user_id=usr_abc123
  audit_provider_type=postgresql
  audit_message=User usr_abc123 logged in successfully via postgresql
```
{% endstep %}
{% endstepper %}

{% hint style="success" %}
You now have a full audit trail in your console logs.
{% endhint %}

## Complete Example

Create `console_audit.py`:

```python
"""GL IAM Console Audit Trail Example."""

import asyncio
import logging

from gl_iam import IAMGateway, ConsoleAuditHandler
from gl_iam.core.types.auth import Credentials
from gl_iam.providers.postgresql import PostgreSQLProvider, PostgreSQLConfig

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/gliam"

# Configure logging to see audit events
logging.basicConfig(level=logging.INFO)


async def main():
    # Step 1: Create audit handler
    handler = ConsoleAuditHandler()

    # Step 2: Setup provider and gateway with audit
    config = PostgreSQLConfig(database_url=DATABASE_URL)
    provider = PostgreSQLProvider(config)
    gateway = IAMGateway(
        auth_provider=provider,
        user_store=provider,
        session_provider=provider,
        audit_handlers=[handler],
    )

    # Step 3: Perform operations — audit events are emitted automatically
    result = await gateway.authenticate(
        credentials=Credentials(username="alice", password="secret123"),
        organization_id="default",
    )

    if result.is_ok:
        print(f"Login succeeded for {result.user.id}")
    else:
        print(f"Login failed: {result.error.message}")

    await provider.close()


if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
uv run console_audit.py
```

Expected output:

```
INFO:gl_iam.audit:audit_event: login_success
Login succeeded for usr_abc123
```

## Routing to a File

Route audit logs to a separate file while keeping other logs on console:

```python
import logging

# Dedicated file handler for audit events
file_handler = logging.FileHandler("audit.log")
file_handler.setLevel(logging.DEBUG)

audit_logger = logging.getLogger("gl_iam.audit")
audit_logger.addHandler(file_handler)
audit_logger.setLevel(logging.DEBUG)
```

## Common Pitfalls

| Pitfall                         | Solution                                                      |
| ------------------------------- | ------------------------------------------------------------- |
| No log output visible           | Set `logging.basicConfig(level=logging.INFO)`                 |
| Using `from_fullstack_provider` | Use `IAMGateway()` constructor directly with `audit_handlers` |
| Handler exceptions crash app    | They don't — the gateway wraps each handler in try/except     |

***

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url\&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Faudit-trail%2Fconsole-logging).
{% endhint %}
