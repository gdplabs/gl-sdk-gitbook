# Webhooks

## Webhooks API Contract

### Overview

The Webhooks API allows you to receive real-time notifications when STT or TTS jobs complete or fail. Instead of polling for job status, webhooks push events to your server automatically.

**Base URL:** `https://tts-api.stg.prosa.ai/v2/speech/webhooks`

**Authentication:** All endpoints require the `x-api-key` header with your API key.

***

### Webhook Event Types

| Event               | Description                                  |
| ------------------- | -------------------------------------------- |
| `stt.job.completed` | STT transcription job completed successfully |
| `stt.job.failed`    | STT transcription job failed                 |
| `tts.job.completed` | TTS synthesis job completed successfully     |
| `tts.job.failed`    | TTS synthesis job failed                     |
| `webhook.ping`      | Test event for endpoint verification         |

***

### Endpoint Management

#### Create Endpoint (POST /webhooks/endpoints)

Register a new webhook endpoint to receive events.

**Authentication:** API key required

**Request:**

```bash
curl -X POST 'https://tts-api.stg.prosa.ai/v2/speech/webhooks/endpoints' \
  -H 'x-api-key: your-api-key' \
  -H 'Content-Type: application/json' \
  -d '{
    "url": "https://your-server.com/webhook",
    "event_filters": ["stt.job.completed", "tts.job.completed"],
    "ssl_verification": true
  }'
```

**Request Body:**

| Field              | Type    | Required | Default        | Description                                 |
| ------------------ | ------- | -------- | -------------- | ------------------------------------------- |
| `url`              | string  | ✅ Yes    | -              | Your webhook endpoint URL (must be HTTPS)   |
| `event_filters`    | array   | No       | `[]`           | Events to subscribe to (empty = all events) |
| `ssl_verification` | boolean | No       | `true`         | Verify SSL certificate                      |
| `secret_key`       | string  | No       | Auto-generated | Custom secret key for signing               |

**Response (201 Created):**

```json
{
  "id": "endpoint-123e4567-e89b-12d3-a456-426614174000",
  "url": "https://your-server.com/webhook",
  "secrets": [
    {
      "id": "secret-abc123",
      "key": "whsec_abc123xyz789def456ghi",
      "expired_at": null
    }
  ],
  "event_filters": ["stt.job.completed", "tts.job.completed"],
  "ssl_verification": true
}
```

**Response Fields:**

| Field                  | Type    | Description                      |
| ---------------------- | ------- | -------------------------------- |
| `id`                   | string  | Unique endpoint identifier       |
| `url`                  | string  | Registered webhook URL           |
| `secrets`              | array   | Signing secrets for verification |
| `secrets[].key`        | string  | Secret key for HMAC signature    |
| `secrets[].expired_at` | string  | Expiration date (null = never)   |
| `event_filters`        | array   | Subscribed event types           |
| `ssl_verification`     | boolean | SSL verification enabled         |

> ⚠️ **Important:** Save the `secrets[0].key` immediately - you'll need it to verify webhook signatures!

**Error Responses:**

* **400 Bad Request:** Invalid URL

```json
{
  "status": "invalid_url",
  "message": "URL must be a valid HTTPS endpoint"
}
```

* **401 Unauthorized:** Invalid API key

```json
{
  "status": "unauthorized",
  "message": "Invalid API key"
}
```

***

#### List Endpoints (GET /webhooks/endpoints)

List all registered webhook endpoints.

**Authentication:** API key required

**Request:**

```bash
curl -X GET 'https://tts-api.stg.prosa.ai/v2/speech/webhooks/endpoints' \
  -H 'x-api-key: your-api-key'
```

**Response (200 OK):**

```json
[
  {
    "id": "endpoint-123e4567-e89b-12d3-a456-426614174000",
    "url": "https://your-server.com/webhook",
    "event_filters": ["stt.job.completed"],
    "ssl_verification": true
  },
  {
    "id": "endpoint-789xyz",
    "url": "https://backup-server.com/webhook",
    "event_filters": [],
    "ssl_verification": true
  }
]
```

***

#### Get Endpoint (GET /webhooks/endpoints/{endpoint\_id})

Get details of a specific webhook endpoint including secrets.

**Authentication:** API key required

**Request:**

```bash
curl -X GET 'https://tts-api.stg.prosa.ai/v2/speech/webhooks/endpoints/endpoint-123e4567' \
  -H 'x-api-key: your-api-key'
```

**Path Parameters:**

| Parameter     | Type   | Required | Description         |
| ------------- | ------ | -------- | ------------------- |
| `endpoint_id` | string | ✅ Yes    | Endpoint identifier |

**Response (200 OK):**

```json
{
  "id": "endpoint-123e4567-e89b-12d3-a456-426614174000",
  "url": "https://your-server.com/webhook",
  "secrets": [
    {
      "id": "secret-abc123",
      "key": "whsec_abc123xyz789def456ghi",
      "expired_at": null
    }
  ],
  "event_filters": ["stt.job.completed", "tts.job.completed"],
  "ssl_verification": true
}
```

**Error Responses:**

* **404 Not Found:** Endpoint not found

```json
{
  "status": "endpoint_not_found",
  "message": "Endpoint 'endpoint-123e4567' not found"
}
```

***

#### Update Endpoint (PUT /webhooks/endpoints/{endpoint\_id})

Update an existing webhook endpoint.

**Authentication:** API key required

**Request:**

```bash
curl -X PUT 'https://tts-api.stg.prosa.ai/v2/speech/webhooks/endpoints/endpoint-123e4567' \
  -H 'x-api-key: your-api-key' \
  -H 'Content-Type: application/json' \
  -d '{
    "url": "https://new-server.com/webhook",
    "event_filters": ["stt.job.completed", "stt.job.failed", "tts.job.completed", "tts.job.failed"],
    "ssl_verification": true
  }'
```

**Path Parameters:**

| Parameter     | Type   | Required | Description         |
| ------------- | ------ | -------- | ------------------- |
| `endpoint_id` | string | ✅ Yes    | Endpoint identifier |

**Request Body:**

| Field              | Type    | Required | Description                 |
| ------------------ | ------- | -------- | --------------------------- |
| `url`              | string  | No       | New webhook URL             |
| `event_filters`    | array   | No       | Updated event subscriptions |
| `ssl_verification` | boolean | No       | SSL verification setting    |

**Response (200 OK):**

```json
{
  "id": "endpoint-123e4567-e89b-12d3-a456-426614174000",
  "url": "https://new-server.com/webhook",
  "secrets": [
    {
      "id": "secret-abc123",
      "key": "whsec_abc123xyz789def456ghi",
      "expired_at": null
    }
  ],
  "event_filters": ["stt.job.completed", "stt.job.failed", "tts.job.completed", "tts.job.failed"],
  "ssl_verification": true
}
```

***

#### Delete Endpoint (DELETE /webhooks/endpoints/{endpoint\_id})

Delete a webhook endpoint.

**Authentication:** API key required

**Request:**

```bash
curl -X DELETE 'https://tts-api.stg.prosa.ai/v2/speech/webhooks/endpoints/endpoint-123e4567' \
  -H 'x-api-key: your-api-key'
```

**Path Parameters:**

| Parameter     | Type   | Required | Description         |
| ------------- | ------ | -------- | ------------------- |
| `endpoint_id` | string | ✅ Yes    | Endpoint identifier |

**Response (200 OK):**

```json
{
  "id": "endpoint-123e4567-e89b-12d3-a456-426614174000",
  "url": "https://your-server.com/webhook",
  "ssl_verification": true
}
```

**Error Responses:**

* **404 Not Found:** Endpoint not found

```json
{
  "status": "endpoint_not_found",
  "message": "Endpoint 'endpoint-123e4567' not found"
}
```

***

#### Rotate Secret (POST /webhooks/endpoints/{endpoint\_id}/rotate)

Rotate the signing secret for an endpoint. The old secret remains valid for a grace period.

**Authentication:** API key required

**Request:**

```bash
curl -X POST 'https://tts-api.stg.prosa.ai/v2/speech/webhooks/endpoints/endpoint-123e4567/rotate' \
  -H 'x-api-key: your-api-key' \
  -H 'Content-Type: application/json' \
  -d '{
    "days": 3,
    "hours": 0
  }'
```

**Path Parameters:**

| Parameter     | Type   | Required | Description         |
| ------------- | ------ | -------- | ------------------- |
| `endpoint_id` | string | ✅ Yes    | Endpoint identifier |

**Request Body:**

| Field   | Type    | Required | Default | Description                    |
| ------- | ------- | -------- | ------- | ------------------------------ |
| `days`  | integer | No       | `0`     | Days until old secret expires  |
| `hours` | integer | No       | `0`     | Hours until old secret expires |

**Response (200 OK):**

```json
{
  "id": "endpoint-123e4567-e89b-12d3-a456-426614174000",
  "url": "https://your-server.com/webhook",
  "secrets": [
    {
      "id": "secret-new789",
      "key": "whsec_newkey123abc",
      "expired_at": null
    },
    {
      "id": "secret-abc123",
      "key": "whsec_abc123xyz789def456ghi",
      "expired_at": "2024-01-18T10:00:00Z"
    }
  ],
  "event_filters": ["stt.job.completed"],
  "ssl_verification": true
}
```

> **Note:** Both secrets are valid during the grace period. Update your server to use the new secret before the old one expires.

***

#### Test Endpoint (POST /webhooks/endpoints/{endpoint\_id}/test)

Send a test event to verify your endpoint is working.

**Authentication:** API key required

**Request:**

```bash
curl -X POST 'https://tts-api.stg.prosa.ai/v2/speech/webhooks/endpoints/endpoint-123e4567/test' \
  -H 'x-api-key: your-api-key'
```

**Path Parameters:**

| Parameter     | Type   | Required | Description         |
| ------------- | ------ | -------- | ------------------- |
| `endpoint_id` | string | ✅ Yes    | Endpoint identifier |

**Response (200 OK):**

```json
{
  "delivery_tag": "delivery-abc123",
  "endpoint_id": "endpoint-123e4567",
  "url": "https://your-server.com/webhook"
}
```

***

### Event Management

#### List Events (GET /webhooks/events)

List webhook events with optional filtering.

**Authentication:** API key required

**Request:**

```bash
curl -X GET 'https://tts-api.stg.prosa.ai/v2/speech/webhooks/events?from_date=2024-01-01' \
  -H 'x-api-key: your-api-key'
```

**Query Parameters:**

| Parameter    | Type          | Required | Description                    |
| ------------ | ------------- | -------- | ------------------------------ |
| `from_date`  | string (date) | No       | Filter from date (YYYY-MM-DD)  |
| `until_date` | string (date) | No       | Filter until date (YYYY-MM-DD) |

**Response (200 OK):**

```json
[
  {
    "id": "event-abc123",
    "event_type": "stt.job.completed",
    "created_at": "2024-01-15T10:00:00Z"
  },
  {
    "id": "event-def456",
    "event_type": "tts.job.completed",
    "created_at": "2024-01-15T10:05:00Z"
  }
]
```

***

#### Get Event (GET /webhooks/events/{event\_id})

Get details of a specific webhook event.

**Authentication:** API key required

**Request:**

```bash
curl -X GET 'https://tts-api.stg.prosa.ai/v2/speech/webhooks/events/event-abc123' \
  -H 'x-api-key: your-api-key'
```

**Path Parameters:**

| Parameter  | Type   | Required | Description      |
| ---------- | ------ | -------- | ---------------- |
| `event_id` | string | ✅ Yes    | Event identifier |

**Response (200 OK):**

```json
{
  "id": "event-abc123",
  "event_type": "stt.job.completed",
  "data": {
    "job_id": "2fec34e1-efb1-46f7-a743-1cb35b64550d",
    "status": "complete",
    "created_at": "2024-01-15T10:00:00Z"
  },
  "created_at": "2024-01-15T10:00:05Z"
}
```

***

### Delivery Management

#### List Deliveries (GET /webhooks/endpoints/{endpoint\_id}/deliveries)

List webhook deliveries for an endpoint.

**Authentication:** API key required

**Request:**

```bash
curl -X GET 'https://tts-api.stg.prosa.ai/v2/speech/webhooks/endpoints/endpoint-123e4567/deliveries' \
  -H 'x-api-key: your-api-key'
```

**Path Parameters:**

| Parameter     | Type   | Required | Description         |
| ------------- | ------ | -------- | ------------------- |
| `endpoint_id` | string | ✅ Yes    | Endpoint identifier |

**Query Parameters:**

| Parameter    | Type          | Required | Description       |
| ------------ | ------------- | -------- | ----------------- |
| `from_date`  | string (date) | No       | Filter from date  |
| `until_date` | string (date) | No       | Filter until date |

**Response (200 OK):**

```json
[
  {
    "delivery_id": "delivery-abc123",
    "event_id": "event-abc123",
    "endpoint_id": "endpoint-123e4567",
    "delivery": "2024-01-15T10:00:05Z",
    "request_method": "POST",
    "request_headers": {
      "Content-Type": "application/json",
      "X-Prosa-Signature": "sha256=abc123..."
    },
    "request_body": {
      "job_id": "2fec34e1-efb1-46f7-a743-1cb35b64550d"
    },
    "response_status": 200,
    "response_headers": {},
    "response_body": "OK",
    "elapsed_time": 0.15
  }
]
```

**Response Fields:**

| Field             | Type              | Description                |
| ----------------- | ----------------- | -------------------------- |
| `delivery_id`     | string            | Unique delivery identifier |
| `event_id`        | string            | Associated event ID        |
| `endpoint_id`     | string            | Target endpoint ID         |
| `delivery`        | string (datetime) | Delivery timestamp         |
| `request_method`  | string            | HTTP method used           |
| `request_headers` | object            | Headers sent               |
| `request_body`    | object            | Body sent                  |
| `response_status` | integer           | HTTP response status       |
| `response_body`   | string            | Response received          |
| `elapsed_time`    | number            | Response time in seconds   |

***

#### Replay Delivery (POST /webhooks/deliveries/{delivery\_id}/replay)

Replay a specific webhook delivery.

**Authentication:** API key required

**Request:**

```bash
curl -X POST 'https://tts-api.stg.prosa.ai/v2/speech/webhooks/deliveries/delivery-abc123/replay' \
  -H 'x-api-key: your-api-key'
```

**Path Parameters:**

| Parameter     | Type   | Required | Description         |
| ------------- | ------ | -------- | ------------------- |
| `delivery_id` | string | ✅ Yes    | Delivery identifier |

**Response (200 OK):**

```json
{
  "delivery_tag": "delivery-new789",
  "endpoint_id": "endpoint-123e4567",
  "url": "https://your-server.com/webhook"
}
```

***

#### Replay Failed Deliveries (POST /webhooks/endpoints/{endpoint\_id}/replay-failed)

Replay all failed deliveries for an endpoint.

**Authentication:** API key required

**Request:**

```bash
curl -X POST 'https://tts-api.stg.prosa.ai/v2/speech/webhooks/endpoints/endpoint-123e4567/replay-failed' \
  -H 'x-api-key: your-api-key'
```

**Path Parameters:**

| Parameter     | Type   | Required | Description         |
| ------------- | ------ | -------- | ------------------- |
| `endpoint_id` | string | ✅ Yes    | Endpoint identifier |

**Response (200 OK):**

```json
[
  {
    "delivery_tag": "delivery-replay1",
    "endpoint_id": "endpoint-123e4567",
    "url": "https://your-server.com/webhook"
  },
  {
    "delivery_tag": "delivery-replay2",
    "endpoint_id": "endpoint-123e4567",
    "url": "https://your-server.com/webhook"
  }
]
```

***

### Implementing Your Webhook Endpoint

#### Webhook Payload Format

Your endpoint will receive POST requests with the following format:

**Headers:**

| Header               | Description                            |
| -------------------- | -------------------------------------- |
| `Content-Type`       | `application/json`                     |
| `X-Prosa-Signature`  | HMAC-SHA256 signature                  |
| `X-Prosa-Event-UUID` | Unique event identifier                |
| `X-Prosa-Event`      | Event type (e.g., `stt.job.completed`) |

**Example Payload (STT Job Completed):**

```json
{
  "job_id": "2fec34e1-efb1-46f7-a743-1cb35b64550d",
  "created_at": "2024-01-15T10:00:00Z",
  "modified_at": "2024-01-15T10:00:05Z",
  "request": {
    "label": "My audio file"
  },
  "result": {
    "data": [
      {
        "transcript": "Hasil akhir dari pekerjaan ini",
        "final": true,
        "time_start": 0,
        "time_end": 3.6,
        "channel": 0
      }
    ]
  },
  "job_config": {
    "engine": "stt-general",
    "wait": false
  }
}
```

**Example Payload (TTS Job Completed):**

```json
{
  "job_id": "3abc45d2-1234-5678-abcd-ef1234567890",
  "created_at": "2024-01-15T10:00:00Z",
  "modified_at": "2024-01-15T10:00:02Z",
  "request": {
    "text": "Selamat pagi",
    "label": "Greeting"
  },
  "result": {
    "path": "https://storage.prosa.ai/tts/audio.mp3",
    "format": "mp3",
    "duration": 2.5
  },
  "job_config": {
    "model": "tts-dimas-formal",
    "wait": false
  }
}
```

***

#### Verifying Webhook Signatures

Always verify the `X-Prosa-Signature` header to ensure the webhook is authentic.

**Python Example:**

```python
import hmac
import hashlib

def verify_signature(payload: bytes, signature: str, secret: str) -> bool:
    """Verify webhook signature."""
    expected = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    received = signature.replace("sha256=", "")
    return hmac.compare_digest(expected, received)

# In your webhook handler:
@app.post("/webhook")
async def handle_webhook(request: Request):
    payload = await request.body()
    signature = request.headers.get("X-Prosa-Signature", "")
    
    if not verify_signature(payload, signature, "whsec_your_secret"):
        return Response(status_code=401, content="Invalid signature")
    
    # Process the webhook...
    return Response(status_code=200, content="OK")
```

**Node.js Example:**

```javascript
const crypto = require('crypto');

function verifySignature(payload, signature, secret) {
  const expected = crypto
    .createHmac('sha256', secret)
    .update(payload)
    .digest('hex');
  
  const received = signature.replace('sha256=', '');
  return crypto.timingSafeEqual(
    Buffer.from(expected),
    Buffer.from(received)
  );
}
```

***

#### Response Requirements

Your webhook endpoint should:

1. **Return 2xx status** within 30 seconds to acknowledge receipt
2. **Return 204 No Content** for successful processing (recommended)
3. **Return 4xx/5xx** if processing fails (will trigger retry)

**Example Response:**

```
HTTP/1.1 204 No Content
```

***

### Retry Policy

Failed webhook deliveries are retried with exponential backoff:

| Attempt | Delay                  |
| ------- | ---------------------- |
| 1       | Immediate              |
| 2       | 1 minute               |
| 3       | 5 minutes              |
| 4       | 30 minutes             |
| 5       | 2 hours                |
| 6+      | Manual replay required |
