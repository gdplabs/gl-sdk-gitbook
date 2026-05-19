---
icon: database
---

# Database Storage

Persist audit events to PostgreSQL for compliance and querying.

{% hint style="info" %}
**When to use**: When you need queryable, persistent audit logs — compliance requirements, security investigations, or reporting.
{% endhint %}

<details>

<summary>Prerequisites</summary>

* Completed [Console Logging](console-logging.md)
* A running PostgreSQL instance with GL IAM configured

</details>

## 5-Line Core

```python
from gl_iam import IAMGateway, ConsoleAuditHandler
from gl_iam.providers.postgresql import PostgreSQLProvider, PostgreSQLConfig

config = PostgreSQLConfig(database_url=DATABASE_URL, enable_audit_log=True)
provider = PostgreSQLProvider(config)
db_handler = provider.create_audit_handler()  # DatabaseAuditHandler
gateway = IAMGateway(
    auth_provider=provider, user_store=provider, session_provider=provider,
    audit_handlers=[ConsoleAuditHandler(), db_handler],
)
```

## Configuration

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `enable_audit_log` | `bool` | `False` | Enable persistent audit logging to the database |
| `audit_batch_size` | `int` | `50` | Number of events to buffer before flushing |
| `audit_flush_interval_seconds` | `float` | `5.0` | Maximum seconds to buffer before flushing |
| `audit_table_name` | `str` | `"audit_events"` | Table name in the `gl_iam` schema |

## Step-by-Step

{% stepper %}
{% step %}
#### Enable Audit Logging

```python
from gl_iam.providers.postgresql import PostgreSQLProvider, PostgreSQLConfig

config = PostgreSQLConfig(
    database_url="postgresql+asyncpg://postgres:postgres@localhost:5432/gliam",
    enable_audit_log=True,        # Required — False by default
    audit_batch_size=50,          # Flush every 50 events
    audit_flush_interval_seconds=5.0,  # Or every 5 seconds
)
provider = PostgreSQLProvider(config)
```
{% endstep %}

{% step %}
#### Run Migrations

The `audit_events` table is created by migration v009 automatically:

```python
# Option 1: Auto-create tables on startup (default)
config = PostgreSQLConfig(
    database_url=DATABASE_URL,
    enable_audit_log=True,
    auto_create_tables=True,  # Default
)

# Option 2: Run migrations via CLI
# gliam db upgrade
```

The migration runs regardless of `enable_audit_log` — the table is always available.
{% endstep %}

{% step %}
#### Get the DatabaseAuditHandler

```python
db_handler = provider.create_audit_handler()
# Returns DatabaseAuditHandler if enable_audit_log=True, else None
```
{% endstep %}

{% step %}
#### Combine with Console Handler

```python
from gl_iam import IAMGateway, ConsoleAuditHandler

gateway = IAMGateway(
    auth_provider=provider,
    user_store=provider,
    session_provider=provider,
    audit_handlers=[ConsoleAuditHandler(), db_handler],
)
```

Use both handlers in production — console for real-time monitoring, database for querying.
{% endstep %}

{% step %}
#### Query Audit Events

```sql
-- All login failures for a user
SELECT event_type, timestamp, ip_address, error_code, message
FROM gl_iam.audit_events
WHERE user_id = 'usr_abc123'
  AND event_type = 'login_error'
ORDER BY timestamp DESC;

-- Permission denied events in the last 24 hours
SELECT user_id, resource_id, message, ip_address
FROM gl_iam.audit_events
WHERE event_type = 'permission_denied'
  AND timestamp > NOW() - INTERVAL '24 hours'
ORDER BY timestamp DESC;

-- All events for an organization in a time range
SELECT event_type, severity, user_id, timestamp, message
FROM gl_iam.audit_events
WHERE organization_id = 'org_456'
  AND timestamp BETWEEN '2026-04-01' AND '2026-04-07'
ORDER BY timestamp DESC;
```
{% endstep %}

{% step %}
#### Expected Output

Query result:

```
 event_type  |       timestamp        |  ip_address   | error_code            | message
-------------+------------------------+---------------+-----------------------+----------------------------------
 login_error | 2026-04-06 10:30:05+00 | 192.168.1.42  | authentication_failed | Login failed: authentication_failed
 login_error | 2026-04-06 10:29:58+00 | 192.168.1.42  | authentication_failed | Login failed: authentication_failed
```
{% endstep %}
{% endstepper %}

{% hint style="success" %}
Audit events are now persisted to PostgreSQL and queryable with SQL.
{% endhint %}

## Database Schema

| Column | Type | Description |
| --- | --- | --- |
| `id` | `VARCHAR(36)` | UUID primary key |
| `event_type` | `VARCHAR(50)` | `AuditEventType` value |
| `severity` | `VARCHAR(10)` | `debug` / `info` / `warning` / `error` / `critical` |
| `timestamp` | `DATETIME` | When the event occurred |
| `user_id` | `VARCHAR(36)` | Actor user ID |
| `organization_id` | `VARCHAR(36)` | Organization context |
| `provider_type` | `VARCHAR(50)` | Provider that generated the event |
| `provider_id` | `VARCHAR(100)` | Provider instance ID |
| `ip_address` | `VARCHAR(45)` | Client IP address |
| `user_agent` | `VARCHAR(512)` | Client user agent |
| `resource_id` | `VARCHAR(255)` | Affected resource |
| `details_json` | `TEXT` | JSON blob with event-specific data |
| `error_code` | `VARCHAR(100)` | Error code if failed |
| `message` | `TEXT` | Human-readable description |
| `trace_id` | `VARCHAR(32)` | OpenTelemetry trace ID |
| `span_id` | `VARCHAR(16)` | OpenTelemetry span ID |
| `created_at` | `DATETIME` | Row creation timestamp |

## Indexes

| Index | Columns | Use Case |
| --- | --- | --- |
| `ix_audit_events_event_type` | `event_type` | Filter by event type |
| `ix_audit_events_timestamp` | `timestamp` | Time-range queries |
| `ix_audit_events_user_id` | `user_id` | User activity lookup |
| `ix_audit_events_organization_id` | `organization_id` | Org-scoped queries |
| `ix_audit_events_resource_id` | `resource_id` | Resource activity |
| `ix_audit_events_org_timestamp` | `organization_id, timestamp` | Org + time range |

## Architecture: Async Batch Writing

The `DatabaseAuditHandler` uses zero-latency-impact design:

1. `handle()` enqueues the event onto an `asyncio.Queue` (non-blocking)
2. A background task flushes the queue to PostgreSQL every `audit_flush_interval_seconds` or when `audit_batch_size` is reached
3. On database failure, the flush loop uses exponential backoff (up to 5 minutes, max 10 retries)
4. On shutdown, `provider.close()` flushes remaining events before closing the engine

{% hint style="info" %}
**No foreign keys**: The audit table has no FK constraints — audit events survive entity deletion (immutable log principle).
{% endhint %}

## Complete Example

Create `database_audit.py`:

```python
"""GL IAM Database Audit Trail Example."""

import asyncio
import logging

from gl_iam import IAMGateway, ConsoleAuditHandler
from gl_iam.core.types.auth import Credentials
from gl_iam.providers.postgresql import PostgreSQLProvider, PostgreSQLConfig

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/gliam"

logging.basicConfig(level=logging.INFO)


async def main():
    # Step 1: Enable audit log in config
    config = PostgreSQLConfig(
        database_url=DATABASE_URL,
        enable_audit_log=True,
    )
    provider = PostgreSQLProvider(config)

    # Step 2: Get database audit handler
    db_handler = provider.create_audit_handler()

    # Step 3: Create gateway with both handlers
    gateway = IAMGateway(
        auth_provider=provider,
        user_store=provider,
        session_provider=provider,
        audit_handlers=[ConsoleAuditHandler(), db_handler],
    )

    # Step 4: Perform operations — events go to console AND database
    result = await gateway.authenticate(
        credentials=Credentials(username="alice", password="secret123"),
        organization_id="default",
    )

    if result.is_ok:
        print(f"Login succeeded for {result.user.id}")
    else:
        print(f"Login failed: {result.error.message}")

    # Step 5: Close flushes remaining audit events
    await provider.close()


if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
uv run database_audit.py
```

## Common Pitfalls

| Pitfall | Solution |
| --- | --- |
| `enable_audit_log=False` (default) | Must explicitly set to `True` |
| No event loop (Django sync views) | `DatabaseAuditHandler` logs a warning; use `ConsoleAuditHandler` as primary |
| Table growth unbounded | Implement retention policy (partition by month, delete old data) |
| Not calling `provider.close()` | Remaining buffered events may be lost on shutdown |

---

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Faudit-trail%2Fdatabase-storage).
{% endhint %}
