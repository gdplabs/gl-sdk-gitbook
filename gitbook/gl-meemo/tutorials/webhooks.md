# Webhooks

Manage webhooks to receive real-time notifications about meeting events through `client.webhooks`.

### 1. List Available Organizations

Returns organizations accessible to your external application. Use these IDs when creating webhooks.

```python
list_available_organizations(
    extra_headers: dict | None = None,
) -> list[AvailableOrganization]
```

**Sync Example**

```python
from meemo import MeemoClient

client = MeemoClient(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    base_url="https://your-meemo-instance.com",
)

orgs = client.webhooks.list_available_organizations()
for org in orgs:
    print(f"  [{org.id}] {org.name}")
```

**Async Example**

```python
from meemo import AsyncMeemoClient

client = AsyncMeemoClient(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    base_url="https://your-meemo-instance.com",
)

orgs = await client.webhooks.list_available_organizations()
for org in orgs:
    print(f"  [{org.id}] {org.name}")
```

**Returns** `list[AvailableOrganization]`. Each item has fields: `id`, `name`.

***

### 2. Create Webhook

Register a new webhook to receive events for one or more organizations.

```python
create_webhook(
    target_url: str,
    events: list[str],
    organization_ids: list[int],
    description: str | None = None,
    extra_headers: dict | None = None,
) -> list[Webhook]
```

**Parameters**

| Parameter          | Type        | Description                                                          |
| ------------------ | ----------- | -------------------------------------------------------------------- |
| `target_url`       | `str`       | **Required**. HTTPS URL where events will be sent.                   |
| `events`           | `list[str]` | **Required**. List of events to subscribe to (see Available Events). |
| `organization_ids` | `list[int]` | **Required**. List of organization IDs to monitor.                   |
| `description`      | `str`       | Description of the webhook.                                          |

#### Available Events

* `meeting.created`
* `meeting.deleted`
* `meeting.transcription_completed`
* `meeting.transcription_failed`
* `meeting.summarization_completed`

**Sync Example**

```python
webhooks = client.webhooks.create_webhook(
    target_url="https://your-domain.com/webhook-handler",
    events=["meeting.created", "meeting.transcription_completed"],
    organization_ids=[1, 2],
    description="Integration Webhook",
)

for wh in webhooks:
    print(f"  Webhook {wh.id} for org {wh.organization_id}")
    print(f"  Secret: {wh.secret_key}")
```

**Async Example**

```python
webhooks = await client.webhooks.create_webhook(
    target_url="https://your-domain.com/webhook-handler",
    events=["meeting.created"],
    organization_ids=[1],
    description="My Webhook",
)
```

**Returns** `list[Webhook]` — one webhook object per organization. Each `Webhook` has fields: `id`, `target_url`, `secret_key`, `events`, `is_active`, `description`, `created_at`, `organization_id`, `failure_count`, `last_failure_reason`.

***

### 3. List Webhooks

Returns all webhooks registered for your accessible organizations.

```python
list_webhooks(
    extra_headers: dict | None = None,
) -> WebhookListResponse
```

**Sync Example**

```python
response = client.webhooks.list_webhooks()
print(f"Total webhooks: {response.count}")
for wh in response.results:
    print(f"  [{wh.id}] {wh.target_url} (org {wh.organization_id})")
```

**Async Example**

```python
response = await client.webhooks.list_webhooks()
for wh in response.results:
    print(f"  [{wh.id}] {wh.target_url}")
```

**Returns** `WebhookListResponse` with fields: `count`, `next`, `previous`, `results` (list of `Webhook`).

***

### 4. Get Webhook Details

```python
get_webhook(
    webhook_id: int,
    extra_headers: dict | None = None,
) -> Webhook
```

**Parameters**

| Parameter    | Type  | Description                   |
| ------------ | ----- | ----------------------------- |
| `webhook_id` | `int` | **Required**. The webhook ID. |

**Sync Example**

```python
webhook = client.webhooks.get_webhook(webhook_id=101)
print(f"URL: {webhook.target_url}")
print(f"Events: {webhook.events}")
print(f"Active: {webhook.is_active}")
print(f"Failures: {webhook.failure_count}")
```

**Async Example**

```python
webhook = await client.webhooks.get_webhook(webhook_id=101)
print(f"URL: {webhook.target_url}")
```

**Returns** `Webhook`.

***

### 5. Delete Webhook

```python
delete_webhook(
    webhook_id: int,
    extra_headers: dict | None = None,
) -> None
```

**Parameters**

| Parameter    | Type  | Description                             |
| ------------ | ----- | --------------------------------------- |
| `webhook_id` | `int` | **Required**. The webhook ID to delete. |

**Sync Example**

```python
client.webhooks.delete_webhook(webhook_id=101)
print("Webhook deleted")
```

**Async Example**

```python
await client.webhooks.delete_webhook(webhook_id=101)
print("Webhook deleted")
```

**Returns** `None`.

***

### 6. List Webhook Events (Logs)

View delivery logs for your webhooks.

```python
list_webhook_events(
    webhook_id: int | None = None,
    extra_headers: dict | None = None,
) -> WebhookEventListResponse
```

**Parameters**

| Parameter    | Type  | Description                           |
| ------------ | ----- | ------------------------------------- |
| `webhook_id` | `int` | Filter events by specific webhook ID. |

**Sync Example**

```python
response = client.webhooks.list_webhook_events(webhook_id=101)
print(f"Total events: {response.count}")
for event in response.results:
    print(f"  [{event.id}] {event.event_type} - {event.status} ({event.attempt_count} attempts)")
```

**Async Example**

```python
response = await client.webhooks.list_webhook_events(webhook_id=101)
for event in response.results:
    print(f"  [{event.id}] {event.event_type} - {event.status}")
```

**Returns** `WebhookEventListResponse` with fields: `count`, `results` (list of `WebhookEvent`).

***

### 7. Get Webhook Event Details

```python
get_webhook_event(
    event_id: int,
    extra_headers: dict | None = None,
) -> WebhookEvent
```

**Parameters**

| Parameter  | Type  | Description                         |
| ---------- | ----- | ----------------------------------- |
| `event_id` | `int` | **Required**. The webhook event ID. |

**Sync Example**

```python
event = client.webhooks.get_webhook_event(event_id=501)
print(f"Type: {event.event_type}")
print(f"Status: {event.status}")
print(f"Response: {event.response_status}")
```

**Async Example**

```python
event = await client.webhooks.get_webhook_event(event_id=501)
print(f"Type: {event.event_type}")
```

**Returns** `WebhookEvent` with fields: `id`, `webhook_id`, `event_uuid`, `event_type`, `status`, `response_status`, `attempt_count`, `created_at`.

***

### Error Responses

| Status | Condition                                                        |
| ------ | ---------------------------------------------------------------- |
| `400`  | Invalid parameters (e.g., missing required fields, invalid URL). |
| `401`  | Missing or invalid access token.                                 |
| `403`  | Application does not have access to the specified organizations. |
| `404`  | Webhook or event not found.                                      |
