# Webhooks

## Webhooks API

Manage webhooks to receive real-time notifications about meeting events.

### List Available Organizations

Returns a list of organizations accessible to your external application. Use these IDs when creating webhooks.

#### Request

```
GET /api/v1/external/webhooks/available-organizations/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

#### Response

```json
[
  {
    "id": 1,
    "name": "Organization A"
  },
  {
    "id": 2,
    "name": "Organization B"
  }
]
```

### Create Webhook

Register a new webhook to receive events for one or more organizations.

#### Request

```
POST /api/v1/external/webhooks/
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json
```

**Body**

```json
{
  "target_url": "https://your-domain.com/webhook-handler",
  "events": [
    "meeting.created",
    "meeting.transcription_completed"
  ],
  "organization_ids": [1, 2],
  "description": "Integration Webhook"
}
```

**Parameters**

| Parameter         | Type   | Description                                    |
| ----------------- | ------ | ---------------------------------------------- |
| target\_url       | string | Required. HTTPS URL where events will be sent. |
| events            | array  | Required. List of events to subscribe to.      |
| organization\_ids | array  | Required. List of organization IDs to monitor. |
| description       | string | Optional. Description of the webhook.          |

**Available Events**

* meeting.created
* meeting.deleted
* meeting.transcription\_completed
* meeting.transcription\_failed
* meeting.summarization\_completed

#### Response

Returns an array of created webhook objects (one per organization).

```json
[
  {
    "id": 101,
    "target_url": "https://your-domain.com/webhook-handler",
    "secret_key": "whsec_...",
    "events": ["meeting.created"],
    "is_active": true,
    "description": "Integration Webhook",
    "created_at": "2024-02-04T10:00:00Z",
    "organization_id": 1
  },
  {
    "id": 102,
    "target_url": "https://your-domain.com/webhook-handler",
    "secret_key": "whsec_...",
    "events": ["meeting.created"],
    "is_active": true,
    "description": "Integration Webhook",
    "created_at": "2024-02-04T10:00:00Z",
    "organization_id": 2
  }
]
```

### List Webhooks

Returns a list of all webhooks registered for your accessible organizations.

#### Request

```
GET /api/v1/external/webhooks/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

#### Response

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 101,
      "target_url": "https://your-domain.com/webhook-handler",
      "secret_key": "whsec_...",
      "events": ["meeting.created"],
      "is_active": true,
      "description": "Integration Webhook",
      "created_at": "2024-02-04T10:00:00Z",
      "organization_id": 1
    }
  ]
}
```

### Get Webhook Details

#### Request

```
GET /api/v1/external/webhooks/{id}/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

#### Response

```json
{
  "id": 101,
  "target_url": "https://your-domain.com/webhook-handler",
  "secret_key": "whsec_...",
  "events": ["meeting.created"],
  "is_active": true,
  "description": "Integration Webhook",
  "created_at": "2024-02-04T10:00:00Z",
  "failure_count": 0,
  "last_failure_reason": "",
  "organization_id": 1
}
```

### Delete Webhook

#### Request

```
DELETE /api/v1/external/webhooks/{id}/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

#### Response

204 No Content

### List Webhook Events (Logs)

View delivery logs for your webhooks.

#### Request

```
GET /api/v1/external/webhook-events/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Query Parameters**

| Parameter   | Type    | Description                              |
| ----------- | ------- | ---------------------------------------- |
| webhook\_id | integer | Optional. Filter by specific webhook ID. |

#### Response

```json
{
  "count": 5,
  "results": [
    {
      "id": 501,
      "webhook_id": 101,
      "event_uuid": "evt_...",
      "event_type": "meeting.created",
      "status": "SUCCESS",
      "response_status": 200,
      "attempt_count": 1,
      "created_at": "2024-02-04T10:05:00Z"
    }
  ]
}
```

### Get Webhook Event Details

#### Request

```
GET /api/v1/external/webhook-events/{id}/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

#### Response

```json
{
  "id": 501,
  "webhook_id": 101,
  "event_uuid": "evt_...",
  "event_type": "meeting.created",
  "status": "SUCCESS",
  "response_status": 200,
  "attempt_count": 1,
  "created_at": "2024-02-04T10:05:00Z"
}
```
