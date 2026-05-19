# Usage

## Usage API

Retrieve usage data with quota information for your accessible organization(s). This includes speech-to-text, enrollment, and LLM token usage capabilities.

### List Usage

Returns aggregated usage per capability for each accessible organization.

**Request**

```http
GET /api/v1/external/usage/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Query Parameters**

| Parameter         | Type    | Description                                                                                              |
| ----------------- | ------- | -------------------------------------------------------------------------------------------------------- |
| `organization_id` | integer | **Optional**. Filter to a specific organization. Must be an organization accessible to your application. |
| `start_date`      | date    | **Optional**. Filter usage created on or after this date (YYYY-MM-DD).                                   |
| `end_date`        | date    | **Optional**. Filter usage created on or before this date (YYYY-MM-DD).                                  |

**Response**

```json
{
  "results": [
    {
      "organization_id": 1,
      "organization_name": "Organization A",
      "capability_name": "speech-to-text",
      "usage": 3600.5,
      "quota": 36000
    },
{
      "organization_id": 1,
      "organization_name": "Organization A",
      "capability_name": "summarization:input",
      "usage": 50000.0,
      "quota": null
    },
    {
      "organization_id": 1,
      "organization_name": "Organization A",
      "capability_name": "summarization:output",
      "usage": 12000.0,
      "quota": null
    },
    {
      "organization_id": 1,
      "organization_name": "Organization A",
      "capability_name": "keyword-detection:input",
      "usage": 45000.0,
      "quota": null
    },
    {
      "organization_id": 1,
      "organization_name": "Organization A",
      "capability_name": "keyword-detection:output",
      "usage": 3000.0,
      "quota": null
    },
    {
      "organization_id": 1,
      "organization_name": "Organization A",
      "capability_name": "ai-chat:input",
      "usage": 20000.0,
      "quota": null
    },
    {
      "organization_id": 1,
      "organization_name": "Organization A",
      "capability_name": "ai-chat:output",
      "usage": 8000.0,
      "quota": null
    }
  ]
}
```

**Response Fields**

| Field               | Type          | Description                                                                                                               |
| ------------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `organization_id`   | integer       | The organization's ID.                                                                                                    |
| `organization_name` | string        | The organization's name.                                                                                                  |
| `capability_name`   | string        | The capability identifier (see table below).                                                                              |
| `usage`             | float         | Total usage for the capability. Unit depends on capability type: seconds for STT/enrollment, tokens for LLM capabilities. |
| `quota`             | float \| null | The allocated quota for the capability. `null` if no quota is configured.                                                 |

**Capability Names**

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

### Examples

#### Filter by Organization

```http
GET /api/v1/external/usage/?organization_id=1
Authorization: Bearer YOUR_ACCESS_TOKEN
```

#### Filter by Date Range

```http
GET /api/v1/external/usage/?start_date=2024-01-01&end_date=2024-01-31
Authorization: Bearer YOUR_ACCESS_TOKEN
```

#### Combine Filters

```http
GET /api/v1/external/usage/?organization_id=1&start_date=2024-01-01&end_date=2024-01-31
Authorization: Bearer YOUR_ACCESS_TOKEN
```

***

### Error Responses

| Status | Condition                                                                                                    |
| ------ | ------------------------------------------------------------------------------------------------------------ |
| `400`  | Invalid `organization_id` (not an integer).                                                                  |
| `401`  | Missing or invalid access token.                                                                             |
| `403`  | Token's application has no linked organizations, or `organization_id` is not accessible to your application. |
