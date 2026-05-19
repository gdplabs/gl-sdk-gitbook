Field-by-field specification for agent resources derived from the backend Pydantic models.

{% hint style="info" %}
**Looking for operational guidance?** This page is a technical reference focused on field specifications. For endpoint usage, see the [REST API: Agents](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/rest-api/agents) and SDK usage patterns in the [Python SDK Reference](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/python-sdk#agents).
{% endhint %}

## Schema: AgentCreate

Used when creating a new agent via `POST /agents`.

### Core Requirements

| Field       | Type            | Constraints / Notes                                                                                                                           |
| ----------- | --------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`      | `string` (enum) | Required. One of \[`config`, `a2a`, `langflow`\].                                                                                             |
| `name`      | `string`        | Required for all types except `a2a` when `a2a_profile` is provided. Max 255 chars.                                                            |
| `framework` | `string` (enum) | Required for `config` agents (`langchain`, `langgraph`, or `google_adk`). Optional for other types; `a2a` defaults to `langchain` if omitted. |

All other fields are optional, but `config` agents **must** specify a language model using exactly one of the mechanisms described in [Language Model Selection](#language-model-selection).

### Optional Fields

| Field                                     | Type            | Constraints / Notes                                                             |
| ----------------------------------------- | --------------- | ------------------------------------------------------------------------------- |
| `account_id`                              | `string`        | Account UUID (auto-assigned when omitted).                                      |
| `instruction`                             | `string`        | Agent instruction prompt. Optional but recommended.                             |
| `version`                                 | `string`        | Max 255 chars.                                                                  |
| `description`                             | `string`        | Free-form description.                                                          |
| [`a2a_profile`](#a2a-profile-structure)   | `object`        | Required for `a2a` agents if `name` is omitted.                                 |
| [`agent_config`](#agent-config-structure) | `object`        | Framework-specific configuration. Additional properties allowed.                |
| `agents`                                  | `array<string>` | Optional list of sub-agent UUIDs.                                               |
| `tools`                                   | `array<string>` | Optional list of tool UUIDs.                                                    |
| `mcps`                                    | `array<string>` | Optional list of MCP configuration UUIDs.                                       |
| [`tool_configs`](#tool-configs-structure) | `object`        | Keys must match entries in `tools`. Extra configs are ignored.                  |
| `metadata`                                | `object`        | Application-defined metadata. Additional properties allowed.                    |
| `language_model_id`                       | `string`        | Mutually exclusive with `provider`/`model_name` and `agent_config.lm_provider`. |
| `provider`                                | `string`        | Legacy language model provider. Must be supplied together with `model_name`.    |
| `model_name`                              | `string`        | Legacy language model name. Must be supplied together with `provider`.          |

On create, supply UUID references in `tools`, `agents`, and `mcps`. Read responses expand those references into detailed objects.

### Language Model Selection

`config` agents must specify a language model exactly once using one of the following options:

1. `language_model_id`
1. `provider` **and** `model_name`
1. `agent_config.lm_provider` (legacy) with accompanying `agent_config.lm_name`

If multiple mechanisms are provided, validation fails. `a2a` and `langflow` agents may omit language model information.

### Agent Types

Defined by `AgentType` enum:

| Value      | Description                          |
| ---------- | ------------------------------------ |
| `config`   | Standard configuration-based agent   |
| `a2a`      | Agent-to-agent communication profile |
| `langflow` | Agent sourced from LangFlow flows    |

### Agent Frameworks

Defined by `AgentFramework` enum:

| Value        | Description          |
| ------------ | -------------------- |
| `langchain`  | LangChain framework  |
| `langgraph`  | LangGraph framework  |
| `google_adk` | Google ADK framework |
| `langflow`   | LangFlow framework   |

### Tool Configs Structure

The `tool_configs` field is a JSON object keyed by tool UUID. Each entry supplies configuration for the referenced tool. Keys that are not present in the `tools` list are ignored automatically.

```json
{
  "tool_configs": {
    "tool-uuid-1": {
      "parameter1": "value1",
      "parameter2": 42
    },
    "tool-uuid-2": {
      "custom_setting": true
    }
  }
}
```

### Agent Config Structure

The `agent_config` field contains framework-specific settings. Common keys include recursion limits, memory bindings, or LangFlow metadata.

```json
{
  "agent_config": {
    "max_recursion_limit": 10,
    "memory": "mem0",
    "planning": true,
    "tool_output_sharing": true
  }
}
```

No default values are enforced by the API; populate only the settings your runtime understands.

**Available Configuration Options:**

| Field                 | Type      | Default | Description                                                                                                                                                                                                                |
| --------------------- | --------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `max_recursion_limit` | `integer` | 100     | Maximum number of recursive calls the agent can make. Prevents infinite loops in agent reasoning chains. This setting is especially important for complex agents that may call themselves or create circular dependencies. |
| `memory`              | `string`  | `null`  | Memory system identifier to use for persistent conversation context. Common values include `"mem0"` for Mem0 integration.                                                                                                  |
| `planning`            | `boolean` | `false` | Whether to enable planning mode for the agent. When enabled, the agent will first create a structured plan before executing tasks, improving reasoning and task decomposition for complex queries.                         |
| `tool_output_sharing` | `boolean` | `false` | Whether tool outputs are shared across different tool calls within the same agent execution session. When enabled, tools can access outputs from previous tool calls in the execution chain.                               |

### Metadata Structure

The `metadata` field can be used by applications such as GLChat to store UI and behavior configuration. Common fields include:

```json
{
  "metadata": {
    "type": "custom",
    "timeout": 60,
    "is_shown": true,
    "agent_source": "form",
    "display_name": "Display agent name",
    "chat_history_limit": 20,
    "svg_icon": "<svg>...</svg>"
  }
}
```

**Common Fields:**

| Field                | Type      | Description                             |
| -------------------- | --------- | --------------------------------------- |
| `type`               | `string`  | Agent type: `native` or `custom`        |
| `display_name`       | `string`  | Display name shown in GLChat UI         |
| `is_shown`           | `boolean` | Whether agent is visible in UI          |
| `timeout`            | `number`  | Request timeout in seconds              |
| `chat_history_limit` | `number`  | Maximum chat history messages           |
| `agent_source`       | `string`  | Source of agent creation (e.g., `form`) |
| `svg_icon`           | `string`  | SVG markup for agent icon               |

### A2A Profile Structure

The `a2a_profile` field configures agent-to-agent communication profiles. It is required for `a2a` agents unless a `name` is provided.

```json
{
  "a2a_profile": {
    "url": "https://remote-agent-server.com/api"
  }
}
```

`url` is required and validated for proper scheme and host.

## Schema: AgentResponse

Returned by `GET /agents/{agent_id}` and other read operations.

| Field                                     | Type                    | Description                                              |
| ----------------------------------------- | ----------------------- | -------------------------------------------------------- |
| `id`                                      | `string` (UUID)         | Unique agent identifier                                  |
| `name`                                    | `string`                | Agent name                                               |
| [`type`](#agent-types)                    | `string` (enum)         | Agent type classification                                |
| `description`                             | `string`                | Detailed description                                     |
| `instruction`                             | `string`                | Agent instructions                                       |
| [`framework`](#agent-frameworks)          | `string` (enum)         | Framework used by agent                                  |
| `version`                                 | `string`                | Agent version                                            |
| [`metadata`](#metadata-structure)         | `object`                | Agent metadata                                           |
| `tools`                                   | `array<ToolReference>`  | List of tool references with `id`, `name`, `description` |
| `agents`                                  | `array<AgentReference>` | List of sub-agent references                             |
| `mcps`                                    | `array<MCPConfig>`      | List of MCP configurations                               |
| [`tool_configs`](#tool-configs-structure) | `object`                | Tool configuration keyed by tool UUID                    |
| `language_model_id`                       | `string`                | Resolved language model configuration ID                 |
| `provider`                                | `string`                | Legacy language model provider (deprecated)              |
| `model_name`                              | `string`                | Legacy language model name (deprecated)                  |
| [`agent_config`](#agent-config-structure) | `object`                | Agent-specific config                                    |
| [`a2a_profile`](#a2a-profile-structure)   | `object`                | Agent-to-agent communication profile                     |
| `account_id`                              | `string`                | Account ID associated with the agent                     |
| `created_at`                              | `string` (datetime)     | Creation timestamp                                       |
| `updated_at`                              | `string` (datetime)     | Last update timestamp                                    |

## Schema: AgentListItem

Returned by `GET /agents` list operations.

| Field                            | Type                | Description                      |
| -------------------------------- | ------------------- | -------------------------------- |
| `id`                             | `string` (UUID)     | Unique agent identifier          |
| `name`                           | `string`            | Agent name                       |
| [`type`](#agent-types)           | `string` (enum)     | Agent type classification        |
| [`framework`](#agent-frameworks) | `string` (enum)     | Framework used by agent          |
| `version`                        | `string`            | Agent version                    |
| `description`                    | `string`            | Detailed description             |
| `metadata`                       | `object`            | Agent metadata                   |
| `created_at`                     | `string` (datetime) | Creation timestamp               |
| `updated_at`                     | `string` (datetime) | Last update timestamp            |
| `deleted_at`                     | `string` (datetime) | Soft-delete timestamp (nullable) |

## Validation Rules

### On Create (POST /agents)

- `type` must be one of `config`, `a2a`, `langflow`.
- `name` is required for all non-`a2a` agents. `a2a` agents must provide either `name` or a populated `a2a_profile`.
- `framework` is required for `config` agents. When omitted for `a2a` agents it defaults to `langchain`. `langflow` agents expect `agent_config.langflow.flow_id` instead.
- `config` agents must specify a language model using exactly one supported method.
- String fields respect their max length constraints.
- `tools`, `agents`, and `mcps` arrays must contain valid UUID strings when provided. Extra entries in `tool_configs` that do not correspond to the `tools` list are ignored.

### On Update (PUT /agents/{agent_id})

- Full replacement: all required fields must be present and follow create rules.
- Language model selectors remain mutually exclusive.

### On Partial Update (PATCH /agents/{agent_id})

- Only provided fields are validated and updated.
- Language model selectors remain mutually exclusive.

## Common Validation Errors

| Status | Error                          | Cause                                            |
| ------ | ------------------------------ | ------------------------------------------------ |
| `400`  | Invalid input data             | Malformed JSON or invalid field types            |
| `409`  | Agent with name already exists | Duplicate `name` in the same account             |
| `422`  | Validation error               | Missing required fields or constraint violations |

## Minimal Example

```json
{
  "name": "basic-agent",
  "type": "config",
  "framework": "langchain",
  "instruction": "You are a helpful assistant that provides clear and accurate responses.",
  "language_model_id": "model-uuid"
}
```

## Full Example

```json
{
  "name": "data-analyst",
  "type": "config",
  "framework": "langchain",
  "version": "1.0.0",
  "description": "Analyzes data and generates reports",
  "instruction": "You are a data analyst. Analyze the provided data and generate comprehensive reports with visualizations.",
  "metadata": {
    "team": "analytics",
    "environment": "production"
  },
  "tools": ["tool-uuid-1", "tool-uuid-2"],
  "agents": ["sub-agent-uuid"],
  "mcps": ["mcp-config-uuid"],
  "tool_configs": {
    "tool-uuid-1": {
      "api_key": "analytics-api-key",
      "timeout": 30
    }
  },
  "language_model_id": "model-uuid",
  "agent_config": {
    "max_recursion_limit": 10,
    "memory": "mem0",
    "planning": true,
    "tool_output_sharing": true
  }
}
```

## Related Documentation

- [REST API: Agents](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/rest-api/agents) — Endpoint reference
- [Python SDK Reference](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/python-sdk#agents) — Method signatures and usage
- [Agents Guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/agents) — Lifecycle operations
