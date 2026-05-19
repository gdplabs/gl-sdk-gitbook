# Usage

Retrieve aggregated usage data with quota information for your accessible organization(s) through `client.usage`.

### Get Usage

Returns usage per capability for each accessible organization.

```python
get_usage(
    organization_id: int | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    extra_headers: dict | None = None,
) -> UsageResponse
```

**Parameters**

| Parameter         | Type   | Description                                                                |
| ----------------- | ------ | -------------------------------------------------------------------------- |
| `organization_id` | `int`  | Filter to a specific organization. Must be accessible to your application. |
| `start_date`      | `str`  | Filter usage on or after this date (`YYYY-MM-DD`).                         |
| `end_date`        | `str`  | Filter usage on or before this date (`YYYY-MM-DD`).                        |
| `extra_headers`   | `dict` | Additional HTTP headers for this request.                                  |

All parameters are optional.

**Sync Example**

```python
from meemo import MeemoClient

client = MeemoClient(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    base_url="https://your-meemo-instance.com",
)

# Get all usage
response = client.usage.get_usage()
for item in response.results:
    print(f"  {item.organization_name} | {item.capability_name}: {item.usage} / {item.quota}")
```

**Async Example**

```python
from meemo import AsyncMeemoClient

client = AsyncMeemoClient(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    base_url="https://your-meemo-instance.com",
)

response = await client.usage.get_usage()
for item in response.results:
    print(f"  {item.capability_name}: {item.usage}")
```

**Returns** `UsageResponse` with field `results` (list of `UsageItem`).

Each `UsageItem` has fields:

| Field               | Type  | Description                                                                     |
| ------------------- | ----- | ------------------------------------------------------------------------------- |
| `organization_id`   | `int` | The organization's ID.                                                          |
| `organization_name` | `str` | The organization's name.                                                        |
| `capability_name`   | `str` | The capability identifier (see table below).                                    |
| `usage`             | `int` | Total usage. Unit depends on capability type (seconds for STT, tokens for LLM). |
| `quota`             | `int` | Allocated quota. `-1` if no quota is configured (unlimited).                    |

***

### Capability Names

| Capability                 | Description                                 | Usage Unit |
| -------------------------- | ------------------------------------------- | ---------- |
| `speech-to-text`           | Speech-to-text transcription                | seconds    |
| `summarization:input`      | LLM input tokens for meeting summarization  | tokens     |
| `summarization:output`     | LLM output tokens for meeting summarization | tokens     |
| `keyword-detection:input`  | LLM input tokens for keyword extraction     | tokens     |
| `keyword-detection:output` | LLM output tokens for keyword extraction    | tokens     |
| `ai-chat:input`            | LLM input tokens for AI chat                | tokens     |
| `ai-chat:output`           | LLM output tokens for AI chat               | tokens     |

***

### Filter Examples

#### Filter by Organization

```python
response = client.usage.get_usage(organization_id=1)
```

#### Filter by Date Range

```python
response = client.usage.get_usage(
    start_date="2024-01-01",
    end_date="2024-01-31",
)
```

#### Combine Filters

```python
response = client.usage.get_usage(
    organization_id=1,
    start_date="2024-01-01",
    end_date="2024-01-31",
)
```

***

### Error Responses

| Status | Condition                                                                        |
| ------ | -------------------------------------------------------------------------------- |
| `400`  | Invalid `organization_id` (not an integer).                                      |
| `401`  | Missing or invalid access token.                                                 |
| `403`  | Application has no linked organizations, or `organization_id` is not accessible. |
