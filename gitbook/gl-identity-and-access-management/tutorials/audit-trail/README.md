---
icon: clipboard-list
---

# Audit Trail

Track every authentication, authorization, and identity event in your GL IAM application.

{% hint style="info" %}
Learn the concepts first? See [Introduction to GL IAM](../../introduction-to-gl-iam.md).
{% endhint %}

## How It Works

The `IAMGateway` automatically emits `AuditEvent` objects for security-relevant operations — login attempts, permission changes, agent delegations, and more. You don't modify your auth logic. You just attach **handlers** that decide where events go.

```
Gateway Method Call
       │
       ▼
  AuditEvent created automatically
       │
       ▼
  Enriched with request context (ip_address, user_agent)
       │
       ▼
  Dispatched to all registered AuditHandlers
       │
       ├──► ConsoleAuditHandler  → Python logger (JSON)
       ├──► DatabaseAuditHandler → PostgreSQL table
       ├──► OpenTelemetryAuditHandler → OTel span events
       └──► Your custom handler  → Slack, SIEM, queue, etc.
```

## Core Concepts

| Concept | Description |
| --- | --- |
| `AuditEvent` | Pydantic model with event\_type, severity, user\_id, ip\_address, details, trace context |
| `AuditHandler` | Base class: `handle(event)`, `handle_batch(events)`, `close()` |
| `AuditEventType` | 60+ standardized event types across 13 categories |
| `AuditSeverity` | `debug`, `info`, `warning`, `error`, `critical` |
| Request Context | Per-request `ip_address` / `user_agent` via `contextvars` |

## Handler Comparison

| Handler | Destination | Async | Use Case |
| --- | --- | --- | --- |
| `ConsoleAuditHandler` | Python logger (JSON) | No | Development, log aggregation |
| `DatabaseAuditHandler` | PostgreSQL table | Yes (batch) | Compliance, queryable audit |
| `OpenTelemetryAuditHandler` | OTel span events | No | Distributed tracing |
| `CompositeAuditHandler` | Multiple handlers | Delegates | Production (combine above) |
| `CallbackAuditHandler` | Custom function | No | Legacy / simple callbacks |

{% hint style="warning" %}
**Important**: `from_fullstack_provider()` does **not** configure audit handlers. You must pass `audit_handlers` to the `IAMGateway()` constructor directly:

```python
gateway = IAMGateway(
    auth_provider=provider,
    user_store=provider,
    session_provider=provider,
    audit_handlers=[handler],
)
```
{% endhint %}

## Auto-Emitted Events

The gateway automatically emits audit events for these operations (no extra code needed):

| Category | Events |
| --- | --- |
| Authentication | `login_success`, `login_error`, `login_error_limit_exceed`, `logout` |
| Sessions | `session_created`, `session_revoked_all` |
| Users | `user_created`, `user_updated`, `user_deleted` |
| Authorization | `permission_granted`, `permission_revoked`, `permission_denied`, `role_assigned`, `role_removed` |
| Agents | `agent_registered` |
| Delegation | `delegation_created`, `delegation_validation_failed`, `delegation_scope_escalation_denied`, `delegation_depth_exceeded`, `delegation_resource_constraint_denied` |

See [Event Reference](event-reference.md) for the complete list of 60+ event types.

## Tutorials

{% stepper %}
{% step %}
#### Console Logging

[Console Logging](console-logging.md)

What You'll Learn: Log audit events as structured JSON to stdout
{% endstep %}

{% step %}
#### Request Context

[Request Context](request-context.md)

What You'll Learn: Attach IP address and user agent to every event automatically
{% endstep %}

{% step %}
#### Database Storage

[Database Storage](database-storage.md)

What You'll Learn: Persist audit events to PostgreSQL for compliance and querying
{% endstep %}

{% step %}
#### Custom Handler

[Custom Handler](custom-handler.md)

What You'll Learn: Build your own handler and combine multiple handlers
{% endstep %}

{% step %}
#### OpenTelemetry Integration

[OpenTelemetry](opentelemetry.md)

What You'll Learn: Correlate audit events with distributed traces
{% endstep %}

{% step %}
#### Event Reference

[Event Reference](event-reference.md)

What You'll Learn: Complete reference of all event types, severities, and factory functions
{% endstep %}
{% endstepper %}

---

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Faudit-trail).
{% endhint %}
