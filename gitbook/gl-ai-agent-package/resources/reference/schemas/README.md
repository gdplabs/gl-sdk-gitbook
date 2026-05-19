---
icon: book-open
---

Field-by-field specification for runtime configuration used in multi-agent execution, derived from the backend runtime models.

{% hint style="info" %}
**Looking for operational guidance?** This page is a technical reference focused on field specifications. For endpoint usage, see the [REST API: Agents](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/rest-api/agents) and SDK usage patterns in the [Python SDK Reference](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/python-sdk#agents).
{% endhint %}

## Schema: RuntimeConfig

Runtime configuration for multi-agent execution. Supports global configurations and agent-specific overrides keyed directly by agent UUID. Runtime merges are shallow: agent-level overrides replace entire sibling objects rather than deep-merging nested structures.

### Supported Fields

| Field                           | Type                                                 | Constraints / Notes                                                  |
| ------------------------------- | ---------------------------------------------------- | -------------------------------------------------------------------- |
| [`tool_configs`](#tool-configs) | `object`                                             | Optional. Keys must be tool UUIDs; values must be objects.           |
| [`mcp_configs`](#mcp-configs)   | `object`                                             | Optional. Keys must be MCP UUIDs; values must be objects.             |
| [`agent_config`](#agent-config) | `object`                                             | Optional. Top-level agent configuration.                             |
| `<agent_uuid>`                  | [`AgentSpecificConfig`](#schema-agentspecificconfig) | Optional. Each additional top-level key must be a valid UUID string. |

Unknown top-level keys that are not valid UUIDs raise a validation error. Agent IDs are validated for proper UUID format.

### Global Configuration Structures

#### MCP Configs

```json
{
  "mcp_configs": {
    "mcp-uuid-1": {
      "authentication": {
        "type": "custom-header",
        "headers": {
          "Authorization": "Bearer <token>"
        }
      }
    }
  }
}
```

#### Tool Configs

```json
{
  "tool_configs": {
    "tool-uuid-1": {
      "mode": "dry_run"
    },
    "tool-uuid-2": {
      "timeout": 30
    }
  }
}
```

#### Agent Config

```json
{
  "agent_config": {
    "tool_output_sharing": true,
    "max_recursion_limit": 10,
    "memory": "mem0"
  }
}
```

## Schema: AgentSpecificConfig

Configuration specific to an individual agent. These objects have the same shape as the global fields in `RuntimeConfig`. When supplied, they override the corresponding global settings for that agent.

| Field                           | Type     | Constraints                   | Description                                                                  |
| ------------------------------- | -------- | ----------------------------- | ---------------------------------------------------------------------------- |
| [`tool_configs`](#tool-configs) | `object` | Keys must be valid UUIDs      | Tool configurations keyed by tool UUID                                       |
| [`mcp_configs`](#mcp-configs)   | `object` | Keys must be valid UUIDs      | MCP configurations keyed by MCP UUID                                         |
| [`agent_config`](#agent-config) | `object` | Additional properties allowed | Agent-specific configuration (e.g., `tool_output_sharing`, recursion limits) |

## Validation Rules

### Structure Validation

- `tool_configs`, `mcp_configs`, and `agent_config` must be objects when provided.
- Additional top-level keys must be valid UUID strings. Their values must be objects conforming to `AgentSpecificConfig`.
- Unknown non-UUID keys raise `Unknown top-level key '<key>' in runtime_config`.
- Invalid UUID keys raise `Invalid UUID: <agent_id>`.

### Configuration Precedence

1. Agent-specific overrides (top-level UUID keys) take precedence over global configuration.
1. When an override omits a field, the global configuration is used.
1. Merges are shallow: overriding an object replaces the global object for that agent.

### Tool Config Filtering

Tool configuration dictionaries are validated so each value is an object. Additional filtering (e.g., matching `tool_configs` keys to stored agent tools) occurs during agent validation.

## Examples

### Global Configuration Only

```json
{
  "tool_configs": {
    "tool-uuid-1": {
      "mode": "dry_run"
    }
  }
}
```

### Global and Agent-Specific Overrides

```json
{
  "tool_configs": {
    "tool-uuid-1": {
      "mode": "production",
      "timeout": 30
    }
  },
  "mcp_configs": {
    "mcp-uuid-1": {
      "authentication": {
        "type": "bearer-token",
        "token": "global-token"
      }
    }
  },
  "agent_config": {
    "tool_output_sharing": true,
    "max_recursion_limit": 10
  },
  "agent-uuid-1": {
    "tool_configs": {
      "tool-uuid-1": {
        "mode": "dry_run"
      }
    },
    "agent_config": {
      "tool_output_sharing": false
    }
  },
  "agent-uuid-2": {
    "mcp_configs": {
      "mcp-uuid-1": {
        "authentication": {
          "type": "api-key",
          "key": "X-API-Key",
          "value": "agent-specific-key"
        }
      }
    }
  }
}
```

## Usage in AgentRunRequest

The `runtime_config` field in `AgentRunRequest` accepts this schema and automatically supplants legacy top-level `tool_configs` and `mcp_configs` fields.

```json
{
  "input": "Where is my order #123?",
  "chat_history": [
    {
      "role": "user",
      "content": "hi"
    },
    {
      "role": "assistant",
      "content": "Hello! How can I assist you today?"
    }
  ],
  "runtime_config": {
    "tool_configs": {
      "tool-uuid-1": {
        "mode": "dry_run"
      }
    },
    "mcp_configs": {
      "mcp-uuid-1": {
        "authentication": {
          "type": "bearer-token",
          "token": "<token>"
        }
      }
    }
  }
}
```

Legacy requests that still provide the deprecated top-level `tool_configs`/`mcp_configs` are automatically converted to `runtime_config` on ingest, but new integrations should send the new structure directly.

## Common Validation Errors

<details>

<summary>Common Validation Errors and Causes</summary>

| Error                                                  | Cause                                                          |
| ------------------------------------------------------ | -------------------------------------------------------------- |
| `Unknown top-level key '<key>' in runtime_config`      | Top-level key is neither a known global field nor a valid UUID |
| `Configuration must be a dictionary`                   | `tool_configs` or `mcp_configs` is not a dictionary            |
| `Configuration value for '<key>' must be a dictionary` | Value in `tool_configs` or `mcp_configs` is not a dictionary   |
| `Agent config for '<agent_id>' must be a dictionary`   | Agent-specific configuration is not a dictionary               |
| `Invalid UUID: <agent_id>`                             | Agent ID is not a valid UUID format                            |

</details>

## Migration from Legacy Format

{% hint style="warning" %}
The legacy `tool_configs` and `mcp_configs` fields at the top level of `AgentRunRequest` are deprecated. Use `runtime_config` instead.
{% endhint %}

### Legacy Format (Deprecated)

```json
{
  "input": "Where is my order?",
  "tool_configs": {
    "tool-uuid-1": {
      "mode": "dry_run"
    }
  },
  "mcp_configs": {
    "mcp-uuid-1": {
      "authentication": {
        "type": "bearer-token",
        "token": "<token>"
      }
    }
  }
}
```

### New Format (Recommended)

```json
{
  "input": "Where is my order?",
  "runtime_config": {
    "tool_configs": {
      "tool-uuid-1": {
        "mode": "dry_run"
      }
    },
    "mcp_configs": {
      "mcp-uuid-1": {
        "authentication": {
          "type": "bearer-token",
          "token": "<token>"
        }
      }
    }
  }
}
```

## Related Documentation

- [REST API: Agents](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/rest-api/agents) — Endpoint reference
- [Python SDK Reference](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/python-sdk#agents) — Method signatures and usage
- [Agents Schema](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/schemas/agents) — Agent configuration details
- [Tools Schema](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/schemas/tools) — Tool configuration details
- [MCPs Schema](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/schemas/mcps) — MCP configuration details
