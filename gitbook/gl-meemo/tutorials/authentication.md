# Authentication

The Meemo Python library provides both synchronous (`MeemoClient`) and asynchronous (`AsyncMeemoClient`) clients that handle OAuth2 Client Credentials authentication automatically.

### Installation

```bash
pip install meemo
```

### Prerequisites

1. An **ExternalApplication** must be created by a Meemo administrator
2. You will receive a `client_id` and `client_secret`
3. The ExternalApplication links your credentials to one or more organizations

### Client Initialization

#### Sync Client

```python
from meemo import MeemoClient

client = MeemoClient(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    base_url="https://your-meemo-instance.com",
)
```

#### Async Client

```python
from meemo import AsyncMeemoClient

client = AsyncMeemoClient(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    base_url="https://your-meemo-instance.com",
)
```

#### Constructor Parameters

| Parameter         | Type    | Description                                                                    |
| ----------------- | ------- | ------------------------------------------------------------------------------ |
| `client_id`       | `str`   | Your application's client ID. Falls back to `MEEMO_CLIENT_ID` env var.         |
| `client_secret`   | `str`   | Your application's client secret. Falls back to `MEEMO_CLIENT_SECRET` env var. |
| `base_url`        | `str`   | Base URL of the Meemo instance. Falls back to `MEEMO_BASE_URL` env var.        |
| `timeout`         | `float` | Request timeout in seconds. Default: `60.0`.                                   |
| `default_headers` | `dict`  | Additional headers to include in every request.                                |

#### Environment Variables

Instead of passing credentials directly, you can set environment variables:

```bash
export MEEMO_CLIENT_ID="YOUR_CLIENT_ID"
export MEEMO_CLIENT_SECRET="YOUR_CLIENT_SECRET"
export MEEMO_BASE_URL="https://your-meemo-instance.com"
```

```python
from meemo import MeemoClient

# Credentials are read from environment variables
client = MeemoClient()
```

***

### Token Management

The library manages access tokens automatically. When you call any API method, the client obtains a token if needed and refreshes it before expiry (with a 60-second buffer).

#### Explicit Token Operations

You can also manage tokens explicitly if needed.

**Get Access Token**

```python
# Sync
token = client.get_access_token()
print(token)  # "eyJ0eXAiOiJKV1Qi..."
```

```python
# Async
token = await client.get_access_token()
print(token)
```

Returns the current access token as a `str`, requesting a new one if the cached token has expired.

**Revoke Token**

```python
# Sync
client.revoke_token()
```

```python
# Async
await client.revoke_token()
```

Revokes the current access token. After revocation, the next API call will automatically obtain a new token.

***

### API Services

Once initialized, the client exposes three API service objects:

| Service           | Access                       | Description                                                            |
| ----------------- | ---------------------------- | ---------------------------------------------------------------------- |
| `client.meetings` | `Meetings` / `AsyncMeetings` | Meeting CRUD, transcripts, summaries, participants, recordings, topics |
| `client.webhooks` | `Webhooks` / `AsyncWebhooks` | Webhook management and event logs                                      |
| `client.usage`    | `Usage` / `AsyncUsage`       | Usage and quota data                                                   |

See the dedicated documentation pages for each service:

* Meetings
* Webhooks
* Usage

***

### Error Handling

The SDK raises `httpx.HTTPStatusError` for non-2xx responses. You can catch these to handle errors:

```python
import httpx
from meemo import MeemoClient

client = MeemoClient(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    base_url="https://your-meemo-instance.com",
)

try:
    meetings = client.meetings.list_meetings()
except httpx.HTTPStatusError as e:
    print(f"HTTP {e.response.status_code}: {e.response.text}")
```

| Status | Condition                                                   |
| ------ | ----------------------------------------------------------- |
| `400`  | Invalid request parameters.                                 |
| `401`  | Invalid or expired credentials.                             |
| `403`  | Application does not have access to the requested resource. |
| `404`  | Resource not found.                                         |
