---
icon: mcp
---

Model Context Protocol (MCP) connections let agents call external services while
keeping credentials and transport details centralized. Use this guide when you
need to create, manage, or validate MCP configurations with the Python SDK and
the CLI. REST is reference-only and intended for internal integrations.

{% hint style="info" %}
Compare SDK and CLI support in the [AIP capability matrix](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/introduction-to-gl-aip#platform-capabilities-at-a-glance). REST details live in Resources as reference only.
{% endhint %}

{% hint style="info" %}
`aip mcps` commands accept either the MCP ID or a unique name. If multiple
connections share similar names, prefer the explicit ID in scripts to avoid
updating the wrong record.
{% endhint %}

## MCP Patterns

### Recommended: MCP Object Pattern

Define MCPs directly using the `MCP` class and attach them to agents. This is
the preferred pattern for day-to-day application code.

```python
from glaip_sdk import Agent, MCP

# Define MCP inline
weather_mcp = MCP(
    name="weather",
    transport="http",
    config={"url": "https://weather.example.com/mcp"},
    authentication={
        "type": "api-key",
        "key": "X-API-Key",
        "value": "secret-key",
    }
)

# Attach to agent
agent = Agent(
    name="weather-bot",
    instruction="You help users check the weather",
    mcps=[weather_mcp]
)

# Run locally - no deploy() needed for local execution
agent.run("What's the weather in Jakarta?", local=True)
```

**Reference existing MCPs by name or ID:**

```python
from glaip_sdk import Agent, MCP

# Reference by name (requires deploy() for remote)
agent = Agent(
    name="agent",
    instruction="...",
    mcps=[MCP.from_native("mcp-name")]
)
agent.deploy()

# Reference by ID (requires deploy() for remote)
agent = Agent(
    name="agent",
    instruction="...",
    mcps=[MCP.from_id("mcp_abc123")]
)
agent.deploy()
```

**Conditional MCP inclusion:**

```python
from glaip_sdk import Agent, MCP
import os

# Only include MCP if environment variable is set
weather_mcp = MCP(
    name="weather",
    transport="http",
    config={"url": os.getenv("WEATHER_MCP_URL")},
) if os.getenv("WEATHER_MCP_URL") else None

agent = Agent(
    name="weather-agent",
    instruction="You help with weather",
    mcps=[weather_mcp] if weather_mcp else []
)
```

### HTTP/SSE Transport Examples

**HTTP transport:**

```python
from glaip_sdk import MCP

mcp = MCP(
    name="my-http-mcp",
    transport="http",
    config={"url": "https://api.example.com/mcp"},
    authentication={
        "type": "api-key",
        "key": "X-API-Key",
        "value": "your-api-key",
    }
)
```

**SSE transport:**

```python
from glaip_sdk import MCP

mcp = MCP(
    name="my-sse-mcp",
    transport="sse",
    config={"url": "https://mcp.example.com/sse"},
)
```

**Stdio transport:**

```python
from glaip_sdk import MCP

mcp = MCP(
    name="filesystem",
    transport="stdio",
    config={
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/files"],
    }
)
```

{% hint style="info" %}
Stdio transport only works in local mode. It is not supported for remote/deployed agents.
{% endhint %}

### Legacy: Client Pattern

> The `Client` API is kept for backward compatibility but new code should prefer
> the `MCP` object pattern above for a simpler, low-code workflow.

```python
# Legacy: prefer the MCP(...) pattern above
from glaip_sdk import Client

client = Client()

# Create MCP in registry
mcp = client.mcps.create_mcp(
    name="weather-service",
    transport="http",
    config={"url": "https://weather.example.com/mcp"},
    authentication={...}
)

# Use for registry management, listing, and governance
mcps = client.mcps.list_mcps()
```

**Use Client pattern only for:**

- Managing the MCP registry
- Listing and searching MCPs
- Testing MCP connections
- MCP governance across environments

______________________________________________________________________

## Create an MCP Configuration

_When to use:_ Establish a new integration endpoint or clone settings from staging to production.

#### Python SDK (Recommended: MCP Object)

```python
from glaip_sdk import MCP, Agent

# Define MCP with all configuration
weather_mcp = MCP(
    name="weather-service",
    description="HTTP weather API via MCP",
    transport="http",
    config={"url": "https://weather.example.com/mcp"},
    authentication={
        "type": "api-key",
        "key": "X-API-Key",
        "value": "secret-key",
    },
)

# Attach to agent and deploy for remote execution
agent = Agent(
    name="weather-agent",
    instruction="You provide weather information",
    mcps=[weather_mcp],
)
agent.deploy()
print(weather_mcp.id)  # Available after deploy()
```

#### CLI

```bash
aip mcps create \
  --name weather-service \
  --description "HTTP weather API via MCP" \
  --transport http \
  --config '{"url": "https://weather.example.com/mcp"}' \
  --authentication '{"type": "api-key", "key": "X-API-Key", "value": "secret-key"}'
```

Using file references:

```bash
aip mcps create \
  --name weather-service \
  --transport http \
  --config @weather-config.json \
  --auth @weather-auth.json
```

See [Using files with the CLI](#using-files-with-the-cli) for file-based workflows and import examples.

#### CLI (Import file)

```bash
aip mcps create --import weather-mcp.json
```

See [Using files with the CLI](#using-files-with-the-cli) for field details and override behaviour.

The CLI loads every supported field from the file, then applies any CLI flags you pass on top of that data. This lets you tweak a few values (for example a new name or transport) without editing the file:

```bash
aip mcps create \
  --import weather-mcp.json \
  --name weather-service-prod \
  --transport http
```

Merge rules:

- Values inside `weather-mcp.json` form the baseline request (name, transport, config, authentication, metadata, etc.).
- Flags you provide alongside `--import` override the file values one by one (e.g., `--transport http` replaces the file's transport).
- If the file already supplies required fields like `name` and `transport`, you can omit those flags entirely; the CLI falls back to the file contents.

Example `weather-mcp.json`:

```json
{
  "name": "weather-service",
  "transport": "http",
  "description": "HTTP weather API via MCP",
  "config": {
    "url": "https://weather.example.com/mcp"
  },
  "authentication": {
    "type": "api-key",
    "headers": {
      "X-API-Key": "secret-key"
    }
  },
  "mcp_metadata": {
    "environment": "staging",
    "owner": "platform-team"
  }
}
```

### Using files with the CLI

- **Inline vs file inputs:** Any JSON flag (e.g., `--config`, `--auth`) accepts either inline JSON or a file reference using `@path/to/file.json`. File inputs are parsed with the same validation as inline payloads.
- **Importing full definitions:** Supply `--import <file>` to recreate an MCP from an export. The CLI loads every supported field from the file (name, transport, config, authentication, `mcp_metadata`, etc.).
- **Flag overrides:** CLI flags provided alongside `--import` override the matching keys in the file. Leaving a flag out keeps the file's value. When the file already contains required fields like `name` and `transport`, those flags become optional.

Example config file:

```json
{
  "url": "https://weather.example.com/mcp"
}
```

Example auth file:

```json
{
  "type": "api-key",
  "key": "X-API-Key",
  "value": "secret-key"
}
```

Example import file:

```json
{
  "name": "weather-service",
  "transport": "http",
  "description": "HTTP weather API via MCP",
  "config": {
    "url": "https://weather.example.com/mcp"
  },
  "authentication": {
    "type": "api-key",
    "headers": {
      "X-API-Key": "secret-key"
    }
  },
  "mcp_metadata": {
    "environment": "staging",
    "owner": "platform-team"
  }
}
```

Command examples:

```bash
# Use dedicated config/auth files with @file syntax
aip mcps create \
  --name weather-service \
  --transport http \
  --config @weather-config.json \
  --auth @weather-auth.json

# Import and override selected fields
aip mcps create \
  --import weather-mcp.json \
  --name weather-service-prod \
  --transport http
```

## Rotate Credentials or Update Configs

_When to use:_ Refresh secrets before they expire or tweak transport parameters without downtime.

#### Python SDK (MCP Object)

After deploying an MCP, you can update it using the MCP object's methods:

```python
from glaip_sdk import Client, MCP

# First get the MCP from the platform
client = Client()
mcp = client.mcps.get_mcp_by_id("mcp-123")

# Update credentials - uses MCP object method
mcp.update(
    authentication={
        "type": "api-key",
        "key": "X-API-Key",
        "value": "new-secret",
    }
)
```

#### CLI

```bash
# Export current config, edit, then update
aip mcps get <MCP_REF> --export mcp-config.json
# Edit the JSON file to update credentials
aip mcps update <MCP_REF> --config @mcp-config.json
```

## Validate Connections Before Saving

_When to use:_ Confirm the connector responds and auth works before exposing it to agents.

#### Python SDK (MCP Object)

```python
from glaip_sdk import MCP, Client

# Test MCP config before using
mcp = MCP(
    name="weather-service",
    transport="http",
    config={"url": "https://weather.example.com/mcp"},
    authentication={
        "type": "api-key",
        "key": "X-API-Key",
        "value": "secret-key",
    }
)

client = Client()
result = client.mcps.test_mcp_connection_from_config(mcp.model_dump(exclude_none=True))
print(result)
```

CLI:

```bash
aip mcps connect --from-file weather-mcp.json
```

REST reference only (internal integrations):

- [REST: MCPs](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/rest-api/mcps)

### Common errors and fixes

| Symptom                                         | Likely cause                                                       | Fix                                                                                      |
| ----------------------------------------------- | ------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| `401 Unauthorized` when validating              | API key lacks MCP permissions or connector secrets expired.        | Issue a runner/creator key or rotate the provider secret under **Rotate Credentials**.   |
| `404` or `connection refused` during validation | Base URL incorrect or firewall blocking outbound traffic.          | Confirm the URL, allowlist the host, or test from a network that can reach the provider. |
| Connector saves but tools list is empty         | Provider exposes no MCP tools or scope is limited.                 | Run discovery with elevated scopes or confirm the provider exports MCP metadata.         |
| Agents timeout when calling the MCP             | Runtime overrides missing, or concurrency exceeds provider limits. | Use per-run overrides for busy periods and tune agent `timeout` settings.                |

## Discover MCP Tools

_When to use:_ Inspect which tool definitions become available once the connector is active.

#### Python SDK (MCP Object)

```python
from glaip_sdk import Client, MCP

# Get MCP from platform and discover tools
client = Client()
mcp = client.mcps.get_mcp_by_id("mcp-123")
tools = mcp.get_tools()

for tool in tools:
    print(f"{tool['name']}: {tool['description']}")
```

{% hint style="info" %}
`mcp.get_tools()` requires the MCP to be saved on the platform (has an ID). If you haven't saved the MCP yet or want to use an MCP directly without AIP, you can discover tools through the MCP provider directly (e.g., DeepWiki's API).
{% endhint %}

#### CLI

Get tools from a saved MCP:

```bash
aip mcps tools <MCP_ID>
```

Get tools from a config file (without saving to DB):

```bash
aip mcps tools --from-config mcp-config.json
```

Get just tool names for `allowed_tools` config:

```bash
# Simple list output - easy to copy-paste
aip mcps tools <MCP_ID> --names-only

# JSON array output - ready for config files
aip mcps tools <MCP_ID> --names-only --json
```

Example config file (`mcp-config.json`):

```json
{
  "transport": "sse",
  "config": {
    "url": "https://mcp.obrol.id/f/sse"
  }
}
```

#### Python SDK (Legacy: Client Pattern)

```python
# Legacy pattern
from glaip_sdk import Client

client = Client()

# From a saved MCP (stored in DB)
tools = client.mcps.get_mcp_tools(mcp_id)
for tool in tools:
    print(f"{tool['name']}: {tool['description']}")

# From a non-saved MCP config (not stored in DB)
config = {
    "transport": "sse",
    "config": {"url": "https://mcp.obrol.id/f/sse"},
}
tools = client.mcps.get_mcp_tools_from_config(config)
for tool in tools:
    print(f"{tool['name']}: {tool['description']}")
```

Attach discovered tool IDs to agents just like native or custom uploads.

## Restrict Agent Tool Access (Allow List)

_When to use:_ Limit which MCP tools an agent can access instead of allowing all tools from the MCP.

{% hint style="warning" %}
Tool names in `allowed_tools` must match exactly. Use [Discover MCP Tools](#discover-mcp-tools) to find the correct tool names before configuring the allow list.
{% endhint %}

### Configure Tool Filtering at Agent Level

#### Python SDK (Recommended: Agent + MCP Pattern)

```python
from glaip_sdk import Agent, MCP, Client

# First, get MCP from platform (client-connected)
client = Client()
mcp = client.mcps.get_mcp_by_id("mcp_abc123")

# Discover available tools using MCP object method
tools = mcp.get_tools()
print([t['name'] for t in tools])  # ['get_weather', 'get_forecast', 'get_alerts']

# Define MCP with tool restrictions
weather_mcp = MCP(
    name="weather-service",
    transport="http",
    config={"url": "https://weather.example.com/mcp"},
)

# Create agent with only specific tools allowed
agent = Agent(
    name="Weather Agent",
    instruction="Provide weather info",
    model_name="gpt-5",
    mcps=[weather_mcp],
    mcp_configs={
        weather_mcp: {
            "allowed_tools": ["get_weather", "get_forecast"]  # blocks get_alerts
        }
    }
)
```

**Configuration rules:**

- Omit `allowed_tools` or set to `null` or empty list `[]` — allows all MCP tools (default)
- Set to `["tool1", "tool2"]` — allows only listed tools

**Different ways to key `mcp_configs`:**

```python
# 1. MCP object (recommended)
mcp_configs={
    weather_mcp: {
        "allowed_tools": ["get_weather"]
    }
}

# 2. MCP name string
mcp_configs={
    "weather-service": {
        "allowed_tools": ["get_weather"]
    }
}

# 3. MCP ID string (remote only, requires saved MCP)
mcp_configs={
    "mcp_abc123": {
        "allowed_tools": ["get_weather"]
    }
}
```

**Combining with authentication:**

```python
agent = Agent(
    name="Weather Agent",
    instruction="Provide weather info",
    mcps=[weather_mcp],
    mcp_configs={
        weather_mcp: {
            "allowed_tools": ["read_data"],
            "authentication": {
                "type": "bearer-token",
                "token": "agent-specific-token"
            }
        }
    }
)
```

#### Python SDK (Legacy: Client Pattern)

```python
# Legacy pattern - prefer Agent + MCP pattern above
from glaip_sdk import Client

client = Client()

# First, discover available tools
tools = client.mcps.get_mcp_tools(mcp_id)
print([t['name'] for t in tools])  # ['get_weather', 'get_forecast', 'get_alerts']

# Create agent with only specific tools allowed
agent = client.agents.create_agent(
    name="Weather Agent",
    instruction="Provide weather info",
    model_name="gpt-5",
    mcps=[mcp_id],
    mcp_configs={
        mcp_id: {
            "allowed_tools": ["get_weather", "get_forecast"]  # blocks get_alerts
        }
    }
)
```

### Update Existing Agent Tool Access

#### Python SDK

```python
# Update agent's MCP config
agent.mcp_configs = {
    weather_mcp: {
        "allowed_tools": ["get_weather", "get_forecast", "get_alerts"]  # add get_alerts
    }
}
agent.update()
```

## Runtime Overrides During Agent Runs

_When to use:_ Supply per-run credentials, tool restrictions, or endpoints that differ from the stored defaults.

**Override authentication:**

```python
agent.run(
    "Summarise sales data",
    runtime_config={
        "mcp_configs": {
            weather_mcp: {
                "authentication": {
                    "type": "api-key",
                    "key": "X-API-Key",
                    "value": "temporary-override"
                }
            }
        }
    }
)
```

**Override allowed tools:**

```python
# Agent normally has access to ['get_weather', 'get_forecast']
# Restrict to only get_weather for this run
agent.run(
    "What's the current weather?",
    runtime_config={
        "mcp_configs": {
            weather_mcp: {
                "allowed_tools": ["get_weather"]  # temporary restriction
            }
        }
    }
)
```

**Configuration layers (resolution order):**

1. **Runtime config** (highest priority) — per-execution overrides
1. **Agent config** — stored in agent `mcp_configs`
1. **MCP config** (lowest priority) — base MCP settings

{% hint style="info" %}
Runtime overrides are processed in-memory for the run and do not modify stored
MCP or agent records. CLI support is under development; use the SDK for now (REST is reference-only).
{% endhint %}

## MCP Maintenance

_When to use:_ Audit or retire connectors after incidents, vendor changes, or environment migrations.

#### Python SDK

```python
from glaip_sdk import Client

client = Client()

# List MCPs
mcps = client.mcps.list_mcps()

# Get specific MCP and delete
mcp = client.mcps.get_mcp_by_id("mcp-123")
mcp.delete()
```

- List MCPs with `client.mcps.list_mcps()` or `aip mcps list` (see [CLI: MCPs](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/tutorials/cli/commands/mcps)).
- Delete MCPs from the registry with `mcp.delete()` or CLI equivalent.
- Combine MCP tooling with the [Tools guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/tools) when you want to import
  remote tools into agent definitions.

## Best Practices

_When to use:_ Align your organisation on safe defaults that reduce downtime and credential leaks.

1. **Store secrets securely** — use environment variables when invoking CLI or
   export/import workflows; avoid committing secrets to JSON.
1. **Validate before saving** — run `aip mcps connect --from-file ...` or
   the SDK connection test helpers to catch network or auth issues early.
1. **Document tool discovery** — record which MCP tool IDs power each agent so
   teammates can maintain the integration.
1. **Monitor timeouts** — many services expose their own rate or timeout limits;
   set `config.timeout` accordingly and surface errors in run logs.

## Related Documentation

- [Tools guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/tools) — attach native, custom, and MCP-discovered tools.
- [Agents guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/agents) — manage agent lifecycle and runtime overrides.
- [Automation & scripting](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/automation-and-scripting) — script MCP promotion in
  CI pipelines.
