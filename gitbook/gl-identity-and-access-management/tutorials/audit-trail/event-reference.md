---
icon: list-check
---

# Event Reference

Complete reference of all audit event types, severities, and factory functions.

## AuditEvent Model

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `event_type` | `AuditEventType` | (required) | The type of audit event |
| `severity` | `AuditSeverity` | `info` | Severity level |
| `timestamp` | `datetime` | UTC now | When the event occurred |
| `user_id` | `str \| None` | `None` | Actor user ID |
| `organization_id` | `str \| None` | `None` | Organization context |
| `provider_type` | `str \| None` | `None` | Provider that generated the event |
| `provider_id` | `str \| None` | `None` | Provider instance ID |
| `ip_address` | `str \| None` | `None` | Client IP address |
| `user_agent` | `str \| None` | `None` | Client user agent |
| `resource_id` | `str \| None` | `None` | Affected resource |
| `details` | `dict` | `{}` | Event-specific data |
| `error_code` | `str \| None` | `None` | Error identifier |
| `message` | `str \| None` | `None` | Human-readable description |
| `trace_id` | `str \| None` | `None` | OpenTelemetry trace ID |
| `span_id` | `str \| None` | `None` | OpenTelemetry span ID |

## Severity Levels

| Severity | Python Log Level | When to Use |
| --- | --- | --- |
| `debug` | `DEBUG` | Debug information, not typically logged in production |
| `info` | `INFO` | Normal operation (login success, session created) |
| `warning` | `WARNING` | Potential security concern (login failure, permission denied) |
| `error` | `ERROR` | Operation failed (validation failure, account locked) |
| `critical` | `CRITICAL` | Immediate attention required |

## Event Types by Category

### Authentication Events

| Enum Value | String Value | Default Severity | Auto-Emitted | Description |
| --- | --- | --- | --- | --- |
| `LOGIN_SUCCESS` | `login_success` | info | Yes | User successfully authenticated |
| `LOGIN_ERROR` | `login_error` | warning | Yes | Authentication failed |
| `LOGIN_ERROR_LIMIT_EXCEED` | `login_error_limit_exceed` | warning | Yes | Account locked due to too many failed attempts |
| `LOGOUT` | `logout` | info | Yes | User logged out |
| `TOKEN_ISSUED` | `token_issued` | info | No | Access/refresh tokens were issued |
| `TOKEN_REFRESHED` | `token_refreshed` | info | No | Tokens were refreshed |
| `TOKEN_REVOKED` | `token_revoked` | info | No | Token was revoked |
| `TOKEN_VALIDATION_FAILED` | `token_validation_failed` | warning | No | Token validation failed |

### Session Events

| Enum Value | String Value | Default Severity | Auto-Emitted | Description |
| --- | --- | --- | --- | --- |
| `SESSION_CREATED` | `session_created` | info | Yes | New session was created |
| `SESSION_VALIDATED` | `session_validated` | debug | No | Session was validated successfully |
| `SESSION_EXPIRED` | `session_expired` | info | No | Session expired |
| `SESSION_REVOKED` | `session_revoked` | info | No | Session was explicitly revoked |
| `SESSION_REVOKED_ALL` | `session_revoked_all` | info | Yes | All sessions for a user were revoked |

### MFA Events

| Enum Value | String Value | Default Severity | Auto-Emitted | Description |
| --- | --- | --- | --- | --- |
| `MFA_CHALLENGE_CREATED` | `mfa_challenge_created` | info | No | MFA challenge was initiated |
| `MFA_SUCCESS` | `mfa_success` | info | No | MFA verification succeeded |
| `MFA_ERROR` | `mfa_error` | warning | No | MFA verification failed |
| `MFA_ERROR_LIMIT_EXCEED` | `mfa_error_limit_exceed` | warning | No | MFA locked due to too many failed attempts |
| `MFA_ENROLLED` | `mfa_enrolled` | info | No | User enrolled in MFA |
| `MFA_UNENROLLED` | `mfa_unenrolled` | info | No | User unenrolled from MFA |
| `MFA_BACKUP_CODE_USED` | `mfa_backup_code_used` | warning | No | Backup code was used for MFA |

### API Key Events

| Enum Value | String Value | Default Severity | Auto-Emitted | Description |
| --- | --- | --- | --- | --- |
| `API_KEY_CREATED` | `api_key_created` | info | No | New API key was created |
| `API_KEY_VALIDATED` | `api_key_validated` | debug | No | API key was validated successfully |
| `API_KEY_VALIDATION_FAILED` | `api_key_validation_failed` | warning | No | API key validation failed |
| `API_KEY_REVOKED` | `api_key_revoked` | info | No | API key was revoked |
| `API_KEY_ROTATED` | `api_key_rotated` | info | No | API key was rotated |
| `API_KEY_EXPIRED` | `api_key_expired` | info | No | API key expired |

### Credential Events

| Enum Value | String Value | Default Severity | Auto-Emitted | Description |
| --- | --- | --- | --- | --- |
| `CREDENTIAL_CREATED` | `credential_created` | info | No | New credential was created |
| `CREDENTIAL_AUTH_SUCCESS` | `credential_auth_success` | info | No | Credential authentication succeeded |
| `CREDENTIAL_AUTH_FAILED` | `credential_auth_failed` | warning | No | Credential authentication failed |
| `CREDENTIAL_PASSWORD_UPDATED` | `credential_password_updated` | info | No | User password was updated |
| `CREDENTIAL_PASSWORD_RESET_REQUESTED` | `credential_password_reset_requested` | info | No | Password reset was requested |
| `CREDENTIAL_PASSWORD_RESET_COMPLETED` | `credential_password_reset_completed` | info | No | Password reset was completed |

### User Events

| Enum Value | String Value | Default Severity | Auto-Emitted | Description |
| --- | --- | --- | --- | --- |
| `USER_CREATED` | `user_created` | info | Yes | New user was created |
| `USER_UPDATED` | `user_updated` | info | Yes | User profile was updated |
| `USER_DELETED` | `user_deleted` | info | Yes | User was deleted |
| `USER_ACTIVATED` | `user_activated` | info | No | User account was activated |
| `USER_DEACTIVATED` | `user_deactivated` | info | No | User account was deactivated |
| `USER_EMAIL_VERIFIED` | `user_email_verified` | info | No | User email was verified |

### Authorization Events

| Enum Value | String Value | Default Severity | Auto-Emitted | Description |
| --- | --- | --- | --- | --- |
| `PERMISSION_GRANTED` | `permission_granted` | info | Yes | Permission was granted to a user |
| `PERMISSION_REVOKED` | `permission_revoked` | info | Yes | Permission was revoked from a user |
| `PERMISSION_DENIED` | `permission_denied` | warning | Yes | Access denied due to missing permission |
| `ROLE_ASSIGNED` | `role_assigned` | info | Yes | Role was assigned to a user |
| `ROLE_REMOVED` | `role_removed` | info | Yes | Role was removed from a user |

### Organization Events

| Enum Value | String Value | Default Severity | Auto-Emitted | Description |
| --- | --- | --- | --- | --- |
| `ORG_USER_ADDED` | `org_user_added` | info | No | User was added to an organization |
| `ORG_USER_REMOVED` | `org_user_removed` | info | No | User was removed from an organization |
| `ORG_USER_ROLE_CHANGED` | `org_user_role_changed` | info | No | User's role in organization was changed |

### Integration Events

| Enum Value | String Value | Default Severity | Auto-Emitted | Description |
| --- | --- | --- | --- | --- |
| `INTEGRATION_STORED` | `integration_stored` | info | No | External integration was stored |
| `INTEGRATION_RETRIEVED` | `integration_retrieved` | debug | No | External integration was retrieved |
| `INTEGRATION_UPDATED` | `integration_updated` | info | No | External integration was updated |
| `INTEGRATION_DELETED` | `integration_deleted` | info | No | External integration was deleted |

### JIT Provisioning Events

| Enum Value | String Value | Default Severity | Auto-Emitted | Description |
| --- | --- | --- | --- | --- |
| `JIT_PROVISION` | `jit_provision` | info | No | User was provisioned via JIT |
| `IDENTITY_LINKED` | `identity_linked` | info | No | External identity was linked to a user |
| `IDENTITY_UNLINKED` | `identity_unlinked` | info | No | External identity was unlinked from a user |

### Agent Events

| Enum Value | String Value | Default Severity | Auto-Emitted | Description |
| --- | --- | --- | --- | --- |
| `AGENT_REGISTERED` | `agent_registered` | info | Yes | New agent identity was registered |
| `AGENT_REVOKED` | `agent_revoked` | warning | No | Agent was permanently revoked |
| `AGENT_SUSPENDED` | `agent_suspended` | warning | No | Agent was temporarily suspended |
| `AGENT_REACTIVATED` | `agent_reactivated` | info | No | Suspended agent was reactivated |

### Delegation Events

| Enum Value | String Value | Default Severity | Auto-Emitted | Description |
| --- | --- | --- | --- | --- |
| `DELEGATION_CREATED` | `delegation_created` | info | Yes | Delegation token was created |
| `DELEGATION_VALIDATED` | `delegation_validated` | debug | No | Delegation token was validated |
| `DELEGATION_VALIDATION_FAILED` | `delegation_validation_failed` | warning | Yes | Delegation token validation failed |
| `DELEGATION_SCOPE_ESCALATION_DENIED` | `delegation_scope_escalation_denied` | warning | Yes | Scope escalation was denied |
| `DELEGATION_DEPTH_EXCEEDED` | `delegation_depth_exceeded` | warning | Yes | Delegation depth limit was exceeded |
| `DELEGATION_RESOURCE_CONSTRAINT_DENIED` | `delegation_resource_constraint_denied` | warning | Yes | Resource constraint validation failed |

### SSO Partner Lifecycle Events

| Enum Value | String Value | Default Severity | Auto-Emitted | Description |
| --- | --- | --- | --- | --- |
| `PARTNER_REGISTERED` | `partner_registered` | info | No | New SSO partner was registered |
| `PARTNER_UPDATED` | `partner_updated` | info | No | Partner scope/policy fields were updated; `details` carries `changed_fields` plus `before`/`after` maps |
| `PARTNER_DEACTIVATED` | `partner_deactivated` | info | No | Partner was deactivated |
| `PARTNER_REACTIVATED` | `partner_reactivated` | info | No | Previously deactivated partner was reactivated |
| `PARTNER_SECRET_ROTATED` | `partner_secret_rotated` | info | No | Partner consumer secret was rotated |
| `PARTNER_SIGNATURE_VALIDATION_FAILED` | `partner_signature_validation_failed` | warning | No | HMAC signature validation failed for an SSO partner request |

{% hint style="info" %}
**Auto-Emitted: No** — the enum values exist in the SDK but the partner-registry mixin does not yet emit these events. Wiring is tracked as a follow-up (gateway wrapper methods that delegate to the partner registry and emit on success/failure, mirroring the delegation pattern). Until then, applications can emit these events manually from their own update paths if they need an audit trail today.
{% endhint %}

## Factory Functions

Helper functions for creating common audit events:

| Function | Creates | Default Severity |
| --- | --- | --- |
| `create_login_success_event(user_id, provider_type, ...)` | `LOGIN_SUCCESS` | info |
| `create_login_error_event(error_code, provider_type, ...)` | `LOGIN_ERROR` | warning |
| `create_account_locked_event(provider_type, ...)` | `LOGIN_ERROR_LIMIT_EXCEED` | warning |
| `create_permission_denied_event(user_id, permission, ...)` | `PERMISSION_DENIED` | warning |
| `create_agent_registered_event(agent_id, agent_name, owner_user_id, ...)` | `AGENT_REGISTERED` | info |
| `create_delegation_created_event(principal_id, agent_id, task_id, ...)` | `DELEGATION_CREATED` | info |
| `create_delegation_denied_event(reason, ...)` | `DELEGATION_SCOPE_ESCALATION_DENIED` | warning |
| `create_resource_constraint_denied_event(reason, ...)` | `DELEGATION_RESOURCE_CONSTRAINT_DENIED` | warning |

### Example: Using Factory Functions

```python
from gl_iam.core.types.audit import (
    create_login_success_event,
    create_permission_denied_event,
)

# Create a login success event
event = create_login_success_event(
    user_id="usr_abc123",
    provider_type="postgresql",
    ip_address="192.168.1.42",
)
# event.event_type == "login_success"
# event.severity == "info"
# event.message == "User usr_abc123 logged in successfully via postgresql"

# Create a permission denied event
event = create_permission_denied_event(
    user_id="usr_abc123",
    permission="admin:delete_user",
    resource_id="usr_target456",
)
# event.event_type == "permission_denied"
# event.severity == "warning"
# event.details == {"permission": "admin:delete_user"}
```

## Custom Events

You can create `AuditEvent` instances directly for application-specific events:

```python
from gl_iam.core.types.audit import AuditEvent, AuditEventType, AuditSeverity

event = AuditEvent(
    event_type=AuditEventType.PERMISSION_DENIED,
    severity=AuditSeverity.WARNING,
    user_id="usr_abc123",
    organization_id="org_456",
    resource_id="document_789",
    details={"attempted_action": "delete", "resource_type": "document"},
    message="User attempted to delete document without permission",
)
```

---

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Faudit-trail%2Fevent-reference).
{% endhint %}
