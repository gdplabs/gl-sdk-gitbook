{% hint style="info" %}
**Looking for operational guidance?** This page is a technical reference focused on field specifications. For endpoint usage, see the [REST API: Tools](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/rest-api/tools) and SDK usage patterns in the [Python SDK Reference](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/python-sdk#tools).
{% endhint %}

## Schema: ToolBase

Used when creating or updating a tool via `POST /tools/` or `PUT /tools/{id}`.

### Required Fields

| Field                           | Type            | Constraints                | Description                |
| ------------------------------- | --------------- | -------------------------- | -------------------------- |
| `name`                          | `string`        | Must be unique per account | Tool name                  |
| [`framework`](#framework-types) | `string` (enum) | Must be valid framework    | Framework used by the tool |
| [`tool_type`](#tool-types)      | `string` (enum) | Must be valid tool type    | Type of the tool           |

### Optional Fields

| Field         | Type           | Constraints                  | Description                |
| ------------- | -------------- | ---------------------------- | -------------------------- |
| `account_id`  | `string`       | UUID format                  | Account ID (auto-assigned) |
| `description` | `string`       | Max length varies by backend | Tool description           |
| `tags`        | `list[string]` | Optional                     | Tags for search/filtering  |
| `version`     | `string`       | Default: `"1.0.0"`           | Tool version identifier    |

### Framework Types

Defined by `ToolFramework` enum:

| Value        | Description          |
| ------------ | -------------------- |
| `langchain`  | LangChain framework  |
| `langgraph`  | LangGraph framework  |
| `google_adk` | Google ADK framework |

### Tool Types

Defined by `ToolType` enum:

| Value    | Description                |
| -------- | -------------------------- |
| `native` | Pre-built native tools     |
| `custom` | User-uploaded custom tools |

## Schema: ToolListItem

Returned by `GET /tools/` and other list operations. Includes additional runtime fields.

| Field                           | Type            | Required | Description                                                                  |
| ------------------------------- | --------------- | -------- | ---------------------------------------------------------------------------- |
| `id`                            | `string` (UUID) | Yes      | Unique tool identifier                                                       |
| `name`                          | `string`        | Yes      | Tool name                                                                    |
| [`framework`](#framework-types) | `string` (enum) | Yes      | Framework type                                                               |
| [`tool_type`](#tool-types)      | `string` (enum) | Yes      | Tool type                                                                    |
| `description`                   | `string`        | No       | Tool description                                                             |
| `version`                       | `string`        | No       | Tool version                                                                 |
| `account_id`                    | `string`        | No       | Associated account ID                                                        |
| `plugin_class_name`             | `string`        | No       | Name of the plugin class (for custom tools)                                  |
| `module_name`                   | `string`        | No       | Python module name                                                           |
| `script_content`                | `string`        | No       | Source code (redacted by default; use `/tools/{id}/source` for full content) |

## File Upload Requirements

For custom tools uploaded via `POST /tools/upload` and `PUT /tools/{tool_id}/upload`:

### File Format

- Format: Python source file (`.py`)
- Encoding: UTF-8
- Size limits: Varies by backend configuration

### Plugin Requirements

On older servers (< v0.1.85), the Python file must export a `tool_plugin` entry point with the following structure:

```python
def tool_plugin():
    return YourToolClass()
```

On newer servers (v0.1.85+), this entry point is optional as long as the file defines a valid tool class. The Python SDK injects the entry point automatically when needed for compatibility.

### Plugin Class Requirements

- Must inherit from the appropriate base class for the specified framework.
- Should implement the required interface methods for the framework.
- Include proper metadata and documentation.

## Validation Rules

### On Create (POST /tools/ or POST /tools/upload)

- `name` must be unique within the account.
- `framework` must be one of `langchain`, `langgraph`, `google_adk`.
- `tool_type` must be one of `native`, `custom`.
- On older servers (< v0.1.85), custom tool uploads must include a valid `tool_plugin` function. On newer servers, a valid tool class is sufficient (the Python SDK injects the entry point when needed).

### On Update (PUT /tools/{id})

- Full replacement: all required fields must be present.
- Same validation as create.
- For code updates, use `PUT /tools/{tool_id}/upload` instead.

### On Metadata Update (PUT /tools/{id})

- Only metadata fields are updated (`name`, `description`, `version`, etc.).
- Plugin code remains unchanged.
- Validation applies only to provided fields.

## Common Validation Errors

| Status | Error                         | Cause                                                                   |
| ------ | ----------------------------- | ----------------------------------------------------------------------- |
| `400`  | Invalid plugin file           | Malformed Python code or missing `tool_plugin` function (older servers) |
| `404`  | Tool not found                | Tool ID does not exist or is soft-deleted                               |
| `409`  | Tool with name already exists | Duplicate `name` in the same account                                    |
| `422`  | Validation error              | Missing required fields or constraint violations                        |
| `500`  | Failed to register plugin     | Runtime error during plugin validation                                  |

## Minimal Example

**Minimal example (JSON)**

```json
{
  "name": "basic-calculator",
  "framework": "langchain",
  "tool_type": "custom"
}
```

## Full Example

**Full example (JSON)**

```json
{
  "name": "advanced-analytics-tool",
  "description": "Performs complex statistical analysis and data visualization",
  "framework": "langgraph",
  "tool_type": "custom",
  "version": "2.1.0"
}
```

## File Upload Example

**cURL file upload example**

```bash
curl -X POST "$AIP_API_URL/tools/upload" \
  -H "X-API-Key: $AIP_API_KEY" \
  -F name="analytics-tool" \
  -F description="Statistical analysis tool" \
  -F framework="langchain" \
  -F tool_type="custom" \
  -F file=@analytics_tool.py
```

## Security Considerations

- Keep credentials for custom tools in an external secret manager instead of embedding raw keys in tool metadata.
- Redacted fields (`script_content`, secrets) only surface in targeted endpoints; avoid logging them downstream.

## Related Documentation

- [REST API: Tools](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/rest-api/tools) — Endpoint reference
- [Python SDK Reference](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/python-sdk#tools) — Method signatures and usage
- [Tools Guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/tools) — Lifecycle operations and file upload workflows
