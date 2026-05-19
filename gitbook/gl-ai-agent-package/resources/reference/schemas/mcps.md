Field-by-field specification for Model Context Protocol (MCP) configurations derived from the backend Pydantic models.

{% hint style="info" %}
**Looking for operational guidance?** This page is a technical reference focused on field specifications. For endpoint usage, see the [REST API: MCPs](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/rest-api/mcps) and SDK usage patterns in the [Python SDK Reference](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/python-sdk#model-context-protocol-mcp).
{% endhint %}

## Schema: MCPCreate

Used when creating a new MCP configuration via `POST /mcps`.

### Required Fields

| Field                                | Type            | Constraints                             | Description                                 |
| ------------------------------------ | --------------- | --------------------------------------- | ------------------------------------------- |
| `name`                               | `string`        | Max 255 chars, unique per account       | Name of the MCP configuration               |
| [`transport`](#transport-types)      | `string` (enum) | `http` or `sse`                         | Transport protocol for the MCP connection   |
| [`config`](#config-object-structure) | `object`        | Must include `url` for `http` and `sse` | Connection details (e.g., `command`, `url`) |

### Optional Fields

| Field                                     | Type     | Constraints                                       | Description                                  |
| ----------------------------------------- | -------- | ------------------------------------------------- | -------------------------------------------- |
| [`authentication`](#authentication-types) | `object` | See [Authentication Types](#authentication-types) | Authentication credentials                   |
| `description`                             | `string` | Max 1000 chars                                    | Human-readable description                   |
| [`mcp_metadata`](#mcp-metadata-structure) | `object` | Additional properties allowed                     | Organizational metadata (informational only) |
| `account_id`                              | `string` | UUID format                                       | Account ID (auto-assigned)                   |

## Transport Types

Defined by `TransportType` enum:

| Value  | Description                                          |
| ------ | ---------------------------------------------------- |
| `http` | Streaming HTTP transport (requires `config.url`)     |
| `sse`  | Server-Sent Events transport (requires `config.url`) |

## Config Object Structure

The `config` field is a flexible JSON object that contains connection details for the MCP server. The only enforced requirement today is that `http` and `sse` transports must include a valid URL.

### HTTP config

| Field | Type     | Description                                |
| ----- | -------- | ------------------------------------------ |
| `url` | `string` | HTTPS endpoint that exposes the MCP server |

```json
{
  "url": "https://api.example.com/mcp"
}
```

#### Future Fields

The following fields are planned to be supported in the future:

| Field            | Type            | Description                                   |
| ---------------- | --------------- | --------------------------------------------- |
| `disabled_tools` | `array<string>` | List of tools to disable access to for agents |
| `enabled_tools`  | `array<string>` | List of tools to enable access to for agents  |

### SSE config

SSE transports reuse the same shape as HTTP and still require a `url`.

```json
{
  "url": "https://legacy.example.com/mcp-stream"
}
```

Additional fields are allowed and passed through to the MCP connector. Common optional keys include tool allow/deny lists and per-transport tuning parameters.

## MCP Metadata Structure

The `mcp_metadata` field is a flexible JSON object for storing organizational information about the MCP configuration. This metadata is informational only and does not affect runtime behavior.

```json
{
  "mcp_metadata": {
    "total_tools": 15,
    "environment": "production"
  }
}
```

## Authentication Types

The `authentication` object must include a `type` field with one of the following values. Responses redact sensitive values unless `return_full` serialization is requested internally.

### `no-auth`

```json
{
  "type": "no-auth"
}
```

### `bearer-token`

Provide a bearer token either directly or via headers.

```json
{
  "type": "bearer-token",
  "token": "your-bearer-token"
}
```

**Header format (mutually exclusive with `token`)**

```json
{
  "type": "bearer-token",
  "headers": {
    "Authorization": "Bearer your-bearer-token"
  }
}
```

### `api-key`

Supply the API key name and value, or precomputed headers.

```json
{
  "type": "api-key",
  "key": "X-API-Key",
  "value": "your-secret"
}
```

**Header format (mutually exclusive with `value`)**

```json
{
  "type": "api-key",
  "headers": {
    "X-API-Key": "your-secret"
  }
}
```

### `custom-header`

```json
{
  "type": "custom-header",
  "headers": {
    "X-API-Key": "secret",
    "X-Client-ID": "client123"
  }
}
```

## Schema: MCPPatch

Used for partial updates via `PATCH /mcps/{mcp_id}`. All fields are optional.

| Field                                     | Type            | Constraints                                   | Description              |
| ----------------------------------------- | --------------- | --------------------------------------------- | ------------------------ |
| `name`                                    | `string`        | Max 255 chars                                 | Update the MCP name      |
| `description`                             | `string`        | Max 1000 chars                                | Update description       |
| [`transport`](#transport-types)           | `string` (enum) | `http` or `sse`                               | Update transport type    |
| [`config`](#config-object-structure)      | `object`        | Must include `url` when transport is provided | Update connection config |
| [`authentication`](#authentication-types) | `object`        | See authentication rules                      | Update credentials       |
| [`mcp_metadata`](#mcp-metadata-structure) | `object`        | Additional properties allowed                 | Update metadata          |

## Schema: MCPResponse

Returned by `GET /mcps/{mcp_id}` and other read operations. Authentication fields are sanitized in responses (only non-sensitive keys are returned by default).

| Field            | Type                | Description                                        |
| ---------------- | ------------------- | -------------------------------------------------- |
| `id`             | `string` (UUID)     | Unique MCP identifier                              |
| `name`           | `string`            | MCP name                                           |
| `description`    | `string`            | Description                                        |
| `transport`      | `string`            | Transport type (`http` or `sse`)                   |
| `config`         | `object`            | Connection configuration                           |
| `authentication` | `object`            | Authentication details (sensitive values redacted) |
| `mcp_metadata`   | `object`            | Metadata                                           |
| `account_id`     | `string`            | Associated account ID                              |
| `created_at`     | `string` (datetime) | Creation timestamp                                 |
| `updated_at`     | `string` (datetime) | Last update timestamp                              |
| `deleted_at`     | `string` (datetime) | Soft-delete timestamp                              |

## Schema: MCPToolDefinition

Represents a tool exposed by an MCP server, returned by `GET /mcps/{mcp_id}/tools` and `POST /mcps/connect/tools`.

| Field         | Type     | Required | Description                          |
| ------------- | -------- | -------- | ------------------------------------ |
| `name`        | `string` | Yes      | Unique tool name                     |
| `description` | `string` | Yes      | What the tool does                   |
| `args_schema` | `object` | No       | JSON schema for tool input arguments |

## Validation Rules

### On Create (POST /mcps)

- `name` must be unique within the account.
- `transport` must be `http` or `sse`.
- `config` must be a JSON object that includes a valid URL when the transport is `http` or `sse`.
- If `authentication` is provided, it must include a valid `type` and satisfy the per-type requirements.

### On Update (PUT /mcps/{mcp_id})

- Full replacement: all required fields must be present.
- Same validation as create.

### On Partial Update (PATCH /mcps/{mcp_id})

- Only provided fields are updated.
- Validation applies only to fields being changed.

## Common Validation Errors

| Status | Error                        | Cause                                            |
| ------ | ---------------------------- | ------------------------------------------------ |
| `400`  | Invalid input data           | Malformed JSON or invalid field types            |
| `400`  | Invalid URL format           | `config.url` missing or fails URL validation     |
| `409`  | MCP with name already exists | Duplicate `name` in the same account             |
| `422`  | Validation error             | Missing required fields or constraint violations |

## Connection Test Schemas

### MCPConnectionTestRequest

Used by `POST /mcps/connect` and `POST /mcps/connect/tools` to test configurations without saving. Has the same structure as `MCPCreate` but does not persist the configuration.

## Minimal Example

```json
{
  "name": "minimal-mcp",
  "transport": "http",
  "config": {
    "url": "https://api.example.com/mcp"
  }
}
```

## Full Example

```json
{
  "name": "production-analytics",
  "description": "Analytics MCP for production environment",
  "transport": "http",
  "config": {
    "url": "https://analytics.example.com/mcp"
  },
  "authentication": {
    "type": "api-key",
    "key": "X-API-Key",
    "value": "analytics-secret"
  },
  "mcp_metadata": {
    "environment": "production",
    "team": "data-science",
    "cost_center": "analytics"
  }
}
```

## Related Documentation

- [REST API: MCPs](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/rest-api/mcps) — Endpoint reference
- [Python SDK Reference](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/python-sdk#model-context-protocol-mcp) — Method signatures and usage
- [MCPs Guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/mcps) — Lifecycle operations
