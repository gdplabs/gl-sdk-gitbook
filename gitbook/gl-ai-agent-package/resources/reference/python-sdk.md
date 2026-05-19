Official Python client for GL AIP (GDP Labs AI Agents Package). Typed, session-aware, and aligned with the live FastAPI backend.

This document is the authoritative guide to the `glaip-sdk` package. Every
method, payload, and return type documented here is derived from the code in
`python/glaip-sdk/glaip_sdk` and mirrors the behaviour used by the CLI and the
end-to-end test suite.

The content is organised by resource category so you can quickly locate the
operation you need—agents, tools, MCP connections, language models, and utility
helpers.

> **Success**
>
> **Quickstart (SDK, Agent-first)** — `pip install glaip-sdk` (or
> `glaip-sdk[local]`) → create `Agent(...)` → `agent.run(...)` locally →
> optionally `agent.deploy()` for remote execution.

{% hint style="info" %}
`Client` remains available as a low-level/advanced API for workspace-wide admin
operations (bulk list/filter, migration/import pipelines, and governance).
{% endhint %}

______________________________________________________________________

## Installation & SDK Basics

```bash
pip install glaip-sdk
```

```python
from glaip_sdk import Agent

agent = Agent(
    name="hello-agent",
    instruction="You are a helpful assistant.",
)

print(agent.run("Hello"))
```

Use the low-level `Client` API when you need workspace-wide administrative
operations:

```python
from glaip_sdk import Client

# Read configuration from environment variables (AIP_API_URL, AIP_API_KEY)
client = Client()

# Explicit configuration
client = Client(
    api_url="https://aip.example.com",
    api_key="sk-your-api-key",
    timeout=60.0,
)
```

{% hint style="info" %}
**Environment variables:** The client reads `AIP_API_URL` and `AIP_API_KEY` by default when arguments are omitted.
{% endhint %}

### Session lifecycle

| Action                     | Behaviour                                                                                    |
| -------------------------- | -------------------------------------------------------------------------------------------- |
| `with Client() as client:` | Opens and automatically closes the underlying `httpx.Client`.                                |
| `client.timeout = 90`      | Rebuilds the shared HTTP client and propagates the session to `agents`, `tools`, and `mcps`. |
| `client.close()`           | Manual teardown when not using a context manager.                                            |

```python
with Client(timeout=45) as client:
    client.timeout = 90  # propagates to sub-clients
    print(client.agents.list_agents())
```

______________________________________________________________________

## Client API Surface

The `Client` class exposes convenience methods that delegate to the specialised
sub-clients under the hood. This section documents every public method grouped
by resource.

Each signature is shown exactly as implemented. Optional parameters list their
Python default values.

### Agents

#### `client.create_agent(...) -> Agent`

```python
client.create_agent(
    name=None,
    instruction=None,
    model=None,
    tools=None,
    agents=None,
    timeout=None,
    *,
    file=None,
    **kwargs,
) -> Agent
```

Create an agent with the supplied configuration. When `file` is provided, the SDK
loads the agent definition from a JSON or YAML document, merges any keyword
overrides you pass, and submits the combined payload.

Parameters:
- `name` (`str`, required unless `file` is provided, default: none): human-readable agent name (must be unique per account). Loaded from file when omitted.
- `instruction` (`str`, required unless `file` is provided, default: none): system prompt / operating instructions. Pulled from file when omitted.
- `model` (`str`, optional, default: `openai/gpt-5-nano`): language model name when not using `language_model_id`.
- `tools` (`list[str | Tool] | None`, optional, default: `None`): tool IDs or `Tool` objects to attach.
- `agents` (`list[str | Agent] | None`, optional, default: `None`): sub-agent IDs or `Agent` objects for delegation.
- `timeout` (`int`, optional): Execution timeout in seconds. Recommended way to set agent runtime timeout. Internally normalized to `agent_config["timeout_seconds"]`.
- `file` (`str | Path`, optional, default: `None`): load base configuration from JSON/YAML; merge overrides.
- `**kwargs` (optional): forwarded fields such as `language_model_id`, `agent_config`, `metadata`, and `mcps`.

Common values:
- `name`: `"pipeline-runner"`
- `instruction`: `"Coordinate ETL tasks..."`
- `model`: `"openai/gpt-5-nano"`
- `tools`: `["tool-uuid"]`
- `agents`: `["delegate-id"]`
- `file`: `"configs/agent.yaml"`
- `**kwargs`: `language_model_id="models/vertex"`

When `file` is used you may specify tools/agents/MCPs by **name** instead of ID;
the SDK resolves them against the current workspace before submitting the
payload (mirroring the CLI’s `--import` behaviour).

Returns the created `Agent` with all persisted fields populated. Raises
`ValueError` if neither runtime arguments nor the file payload provide `name`
and `instruction`.

{% hint style="info" %}
**Complete field specifications:** See [Agents Schema Reference](schemas/agents)
for all available fields, validation rules, and constraints.
Additional fields can be passed via `**kwargs`.
{% endhint %}

```python
agent = client.create_agent(
    name="pipeline-runner",
    instruction="Coordinate ETL tasks and report results",
    tools=["tool-uuid"],
    metadata={"team": "ml"},
    agent_config={"memory": "mem0", "tool_output_sharing": True},
)
```

```python
agent = client.create_agent(
    file="configs/sentiment.yaml",
    metadata={"environment": "prod"},
    tools=["tool-uuid-extra"],
)
```

#### `client.list_agents(...) -> AgentListResult`

```python
client.list_agents(
    agent_type=None,
    framework=None,
    name=None,
    version=None,
    sync_langflow_agents=False,
    *,
    limit=None,
    page=None,
    include_deleted=None,
    created_at_start=None,
    created_at_end=None,
    updated_at_start=None,
    updated_at_end=None,
    metadata=None,
    query=None,
) -> AgentListResult
```

Fetch agents with optional filtering and pagination metadata. The returned
`AgentListResult` is iterable like a list of `Agent` models and also exposes
`total`, `page`, `limit`, `has_next`, and `has_prev`.

Filters:
- `agent_type` (`str`, optional, default: `None`): `config`, `code`, `a2a`, or `langflow`.
- `framework` (`str`, optional, default: `None`): filter by orchestration framework.
- `name` (`str`, optional, default: `None`): case-insensitive substring match.
- `version` (`str`, optional, default: `None`): exact version.
- `sync_langflow_agents` (`bool`, optional, default: `False`): sync LangFlow before listing.
- `limit` (`int`, optional, default: `None`): page size (1-100).
- `page` (`int`, optional, default: `None`): 1-based page number.
- `include_deleted` (`bool`, optional, default: `None`): include soft-deleted agents.
- `created_at_start` / `created_at_end` (`str`, optional, default: `None`): creation timestamp range (ISO 8601).
- `updated_at_start` / `updated_at_end` (`str`, optional, default: `None`): update timestamp range (ISO 8601).
- `metadata` (`dict[str, str]`, optional, default: `None`): metadata filters (for example `metadata.environment=prod`).
- `query` (`AgentListParams`, optional, default: `None`): pass a pre-built parameter object.

Common values:
- `agent_type`: `"langflow"`
- `framework`: `"langgraph"`
- `name`: `"pipeline"`
- `version`: `"1.2.0"`
- `limit`: `20`
- `page`: `2`
- `created_at_start`: `"2024-01-01T00:00:00Z"`
- `metadata`: `{"environment": "prod"}`

Returns an empty result set if no agents match (`len(result) == 0`).

#### `client.get_agent_by_id(agent_id) -> Agent`

Retrieve an agent by UUID. Raises `NotFoundError` if the agent does not exist or
belongs to another account.

`client.get_agent(agent_id)` is an alias.

#### `client.find_agents(name=None) -> list[Agent]`

List agents and apply a case-insensitive name filter client-side. Returns an
empty list if nothing matches.

#### `client.update_agent(agent_id, name=None, instruction=None, model=None, skills=None, timeout=None, *, file=None, tools=None, agents=None, mcps=None, **kwargs) -> Agent`

Replace an agent's configuration.

- `name` (`str | None`): agent display name.
- `instruction` (`str | None`): system prompt/instructions.
- `model` (`str | None`): language model name.
- `skills` (`str | list | dict | None`): skills to attach.
- `timeout` (`int | None`): execution timeout in seconds.
- `file` (`str | Path`): load base configuration from JSON/YAML; merge overrides.
- `tools` (`list[str | Tool] | None`): tool IDs or objects to attach.
- `agents` (`list[str | Agent] | None`): sub-agent IDs or objects for delegation.
- `mcps` (`list[str | MCP] | None`): MCP configurations to attach.

- Unspecified parameters retain their stored values.
- Pass `language_model_id` via `**kwargs` to reference the shared model catalog.
- Provide `tools=[]` / `agents=[]` to clear associations.
- Supply `file` to load a JSON/YAML definition and merge overrides, matching the
  CLI's `--import` behaviour.

When updating from a file, the SDK also resolves tool/agent/MCP names to the
corresponding IDs in the current workspace so you can reuse CLI exports without
manual edits.

{% hint style="info" %}
**Complete field specifications:** See [Agents Schema Reference](schemas/agents)
for all available fields, validation rules, and constraints.
Additional fields can be passed via `**kwargs`.
{% endhint %}

```python
updated = client.update_agent(
    agent.id,
    instruction="Be precise and provide references",
    timeout=900,
    metadata={"environment": "prod"},
)
```

#### `client.delete_agent(agent_id) -> None`

Soft-delete the agent.

#### `client.run_agent(agent_id, message, files=None, tty=False, *, renderer="auto", runtime_config=None, gl_connectors_token=None, trace=False, **kwargs) -> str | AgentRunResult`

Execute an agent and stream results. Returns the final assistant response as a
string.

Parameters:
- `message` (`str`): prompt for the agent.
- `files` (`list[str | BinaryIO] | None`): optional file attachments (file paths as strings).
- `tty` (`bool`): enables the Rich TTY renderer (`auto` by default on the CLI).
- `runtime_config` (`dict[str, Any] | None`): optional runtime overrides for tools, MCPs, and agent behavior.
- `gl_connectors_token` (`str | None`): optional end-user GL Connectors token forwarded to `/agents/{agent_id}/run`.
- `trace` (`bool`): when `True`, returns an `AgentRunResult` with response metadata/events.
- `**kwargs`: additional forwarded fields such as `chat_history`, `pii_mapping`, and `timeout`.

Use `gl_connectors_token` when a run may require GL Connectors user-auth checks
for native tools/MCPs. The token is forwarded in both JSON and multipart (`files`)
request modes.

The SDK automatically handles SSE streaming, rich rendering, and error handling.
It mirrors [`POST /agents/{agent_id}/run`](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/rest-api/agents).

```python
response = client.run_agent(
    agent.id,
    "Summarise ticket INC-42",
    chat_history=[{"role": "user", "content": "Please continue"}],
    gl_connectors_token="<user-token>",
)
```

#### `client.sync_langflow_agents(base_url=None, api_key=None) -> dict`

Trigger LangFlow synchronization. Returns the backend JSON response containing
counts of created/updated flows. `base_url` and `api_key` override the
environment variables `LANGFLOW_BASE_URL` / `LANGFLOW_API_KEY` when set.
Pairs with [`POST /agents/langflow/sync`](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/rest-api/agents).

#### Async streaming – `client.agents.arun_agent(agent_id, message, files=None, *, request_timeout=None, runtime_config=None, gl_connectors_token=None, **kwargs)`

Asynchronous generator that yields parsed SSE JSON fragments. Useful for server
applications or custom renderers.

`gl_connectors_token` is also supported in async runs and is forwarded for both
JSON and multipart requests.

```python
async for event in client.agents.arun_agent(agent.id, "Status update"):
    print(event)
```

Example SSE payload emitted by the backend:

```text
event: token
data: {"text": "Working on it..."}

event: completed
data: {"output": "Final answer here"}
```

### Agent model helpers

Agents returned by the SDK are Pydantic models that keep a reference to the
originating client when fetched through the SDK.

| Method                                | Description                                                              |
| ------------------------------------- | ------------------------------------------------------------------------ |
| `agent.run(message, **kwargs) -> str` | Delegates to `client.run_agent`, injecting the agent name automatically. |
| `agent.update(**kwargs) -> Agent`     | Calls `client.update_agent` and refreshes model fields in-place.         |
| `agent.delete() -> None`              | Calls `client.delete_agent`.                                             |
| `agent.to_component() -> Component`   | Returns an `AgentComponent` for use in `gllm-pipeline`.                  |

```python
agent = client.get_agent_by_id(agent_id)
result = agent.run("Summarise ticket INC-42", timeout=120)
print(result)
```

______________________________________________________________________

### Tools

#### `client.create_tool(file_path, name=None, description=None, framework="langchain", **kwargs) -> Tool`

Upload a Python plugin packaged as a `.py` file.

| Parameter     | Type          | Description                                                               |
| ------------- | ------------- | ------------------------------------------------------------------------- |
| `file_path`   | `str`         | Path to the plugin file. Must exist locally.                              |
| `name`        | `str \| None` | Optional override; default is derived from the plugin’s `name` attribute. |
| `description` | `str \| None` | Stored description. Auto-generated if omitted.                            |
| `framework`   | `str`         | Tool framework identifier (`langchain` default).                          |
| `**kwargs`    | –             | Additional metadata (e.g. `tags`, `tool_type`).                           |

Returns the created `Tool` instance. Temporary files created during upload are
cleaned up automatically.

{% hint style="info" %}
**Complete field specifications:** See [Tools Schema Reference](schemas/tools)
for all available fields, validation rules, and constraints.
{% endhint %}

```python
tool = client.create_tool(
    file_path="calculator_tool.py",
    tags=["math", "utility"],
)
```

#### `client.list_tools(tool_type=None) -> list[Tool]`

List tool metadata. Optional `tool_type` filters by backend type (`custom`,
`native`).

#### `client.get_tool_by_id(tool_id) -> Tool`

Fetch a tool by UUID. Raises `NotFoundError` if missing.

`client.get_tool(tool_id)` is an alias.

#### `client.find_tools(name) -> list[Tool]`

Return tools whose names match the supplied string (case-insensitive, client-side filter).

#### `client.update_tool(tool_id, **kwargs) -> Tool`

Update tool metadata (e.g. `name`, `description`, `tags`). For custom tools that
need a code refresh, use `client.update_tool_via_file`.

#### `client.update_tool_via_file(tool_id, file_path, **kwargs) -> Tool`

Upload a new plugin file for an existing custom tool. Any `kwargs` provided are
forwarded as form fields (description, tags, etc.).

#### `client.get_tool_script(tool_id) -> str`

Return the stored plugin source. Useful for audits or version control.

#### `client.delete_tool(tool_id) -> None`

Soft-delete the tool.

### Tool model helpers

| Method                          | Description                                                               |
| ------------------------------- | ------------------------------------------------------------------------- |
| `tool.get_script() -> str`      | Returns cached `tool_script` or a placeholder when not available.         |
| `tool.update(**kwargs) -> Tool` | Delegates to the appropriate SDK update method (metadata vs file upload). |
| `tool.delete() -> None`         | Delegates to `client.delete_tool`.                                        |

______________________________________________________________________

### Model Context Protocol (MCP)

#### `client.create_mcp(**kwargs) -> MCP`

Create an MCP configuration. Accepts the same payload shape as the REST API
(`/mcps` POST) including `name`, `description`, `transport`, `config`, and
`authentication` dictionaries.

{% hint style="info" %}
**Complete field specifications:** See [MCP Schema Reference](schemas/mcps)
for all available fields, validation rules, and constraints.
{% endhint %}

```python
mcp = client.create_mcp(
    name="vector-db",
    transport="http",
    config={"url": "https://mcp.example.com"},
    authentication={"type": "api-key", "key": "X-API-Key", "value": "secret"},
)
```

#### `client.list_mcps() -> list[MCP]`

Return all stored MCP configurations for the account.

#### `client.get_mcp_by_id(mcp_id) -> MCP`

Retrieve an MCP by UUID. `client.get_mcp(mcp_id)` is an alias.

#### `client.find_mcps(name) -> list[MCP]`

Client-side name filtering across MCP configurations.

#### `client.update_mcp(mcp_id, **kwargs) -> MCP`

Update an MCP configuration. The SDK chooses between PUT or PATCH depending on
whether you provide a full payload (`name`, `config`, `transport`).

{% hint style="info" %}
**Complete field specifications:** See [MCP Schema Reference](schemas/mcps)
for all available fields, validation rules, and constraints.
{% endhint %}

#### `client.delete_mcp(mcp_id) -> None`

Soft-delete an MCP.

#### `client.test_mcp_connection(config: dict) -> dict`

Call `/mcps/connect` to validate credentials or connectivity without persisting
the configuration.

`client.test_mcp_connection_from_config(config)` is an alias.

#### `client.get_mcp_tools_from_config(config: dict) -> list[dict]`

Call `/mcps/connect/tools` to fetch tool metadata from an MCP without storing it.
Useful for validating available actions before creation.

### MCP model helpers

| Method                        | Description                       |
| ----------------------------- | --------------------------------- |
| `mcp.update(**kwargs) -> MCP` | Delegates to `client.update_mcp`. |
| `mcp.delete() -> None`        | Delegates to `client.delete_mcp`. |

______________________________________________________________________

### Schedules

#### `client.schedules.create(*, agent_id, input, schedule) -> Schedule`

Create a schedule for recurring agent execution.

Parameters:
- `agent_id` (`str`, required): agent ID to schedule runs for.
- `input` (`str`, required): input text for each scheduled execution.
- `schedule` (`ScheduleConfig | dict | str`, required): cron config as object, dict, or string.

Common values:
- `agent_id`: `"agent-123"`
- `input`: `"Generate daily report"`
- `schedule`: `"0 9 * * 0-4"`

Cron strings use five fields: `minute hour day_of_month month day_of_week`.
Fields accept `*`, ranges (e.g., `2-4`), lists (`0,6`), and steps (`*/N`).
Day-of-week uses APScheduler numbering (`0` = Monday, `6` = Sunday).
All schedules run in Asia/Jakarta (WIB).

Returns the created `Schedule` instance.

```python
from glaip_sdk.models.schedule import ScheduleConfig

schedule = client.schedules.create(
    agent_id="agent-123",
    input="Generate daily summary",
    schedule=ScheduleConfig(
        minute="0",
        hour="9",
        day_of_week="0-4",  # Weekdays (Mon-Fri)
    ),
)

# Or use a cron string directly
schedule = client.schedules.create(
    agent_id="agent-123",
    input="Weekly update",
    schedule="0 10 * * 0",  # Every Monday at 10am
)
```

#### `client.schedules.list(*, limit=None, page=None, agent_id=None) -> ScheduleListResult`

List schedules with optional filtering and pagination.

| Parameter  | Type  | Required | Default | Description                   |
| ---------- | ----- | -------- | ------- | ----------------------------- |
| `limit`    | `int` | No       | `None`  | Page size (1-100).            |
| `page`     | `int` | No       | `None`  | Page number for pagination.   |
| `agent_id` | `str` | No       | `None`  | Filter schedules by agent ID. |

Returns `ScheduleListResult` with `items`, `total`, `page`, `limit`, `has_next`, `has_prev`.

```python
# List all schedules
schedules = client.schedules.list()

# Filter by agent
agent_schedules = client.schedules.list(agent_id="agent-123")

# Paginate
page1 = client.schedules.list(limit=10, page=1)
```

#### `client.schedules.get(schedule_id) -> Schedule`

Retrieve a schedule by UUID.

Raises `NotFoundError` if the schedule does not exist.

```python
from glaip_sdk.exceptions import NotFoundError

try:
    schedule = client.schedules.get("schedule-abc")
    print(schedule.next_run_time)
except NotFoundError:
    print("Schedule not found")
```

#### `client.schedules.update(schedule_id, *, input=None, schedule=None) -> Schedule`

Update an existing schedule. Unspecified parameters retain their values.

**Update Behavior (Explicit, Not Merge):**

- Omit `schedule` to keep the existing timing unchanged
- Providing a partial schedule dict (e.g., `{"hour": "10"}`) will fill missing fields with `"*"`
- This is intentional for predictability: what you provide is what you get, plus wildcard defaults
- To preserve existing values, fetch the current schedule first and modify only what you need

| Parameter     | Type                            | Required | Default | Description                             |
| ------------- | ------------------------------- | -------- | ------- | --------------------------------------- |
| `schedule_id` | `str`                           | Yes      | —       | Schedule ID to update.                  |
| `input`       | `str`                           | No       | `None`  | New input text for scheduled execution. |
| `schedule`    | `ScheduleConfig \| dict \| str` | No       | `None`  | New schedule configuration.             |

```python
updated = client.schedules.update(
    "schedule-abc",
    input="Updated daily report",
    schedule="0 8 * * *",  # Change to 8am
)
```

#### `client.schedules.delete(schedule_id) -> None`

Delete a schedule by ID.

```python
client.schedules.delete("schedule-abc")
```

#### `client.schedules.list_runs(agent_id, *, schedule_id=None, status=None, limit=None, page=None) -> ScheduleRunListResult`

List execution runs for an agent, optionally filtered by schedule and status.
Only returns schedule runs (equivalent to `run_type=schedule`).

Parameters:
- `agent_id` (`str`, required): agent ID to list runs for.
- `schedule_id` (`str`, optional, default: `None`): filter by specific schedule ID.
- `status` (`RunStatus`, optional, default: `None`): `started`, `success`, `failed`, `cancelled`, `aborted`, or `unavailable`.
- `limit` (`int`, optional, default: `None`): page size (1-100).
- `page` (`int`, optional, default: `None`): page number.

```python
# List all scheduled runs for an agent
runs = client.schedules.list_runs("agent-123")

# Filter by schedule and status
successful_runs = client.schedules.list_runs(
    "agent-123",
    schedule_id="schedule-abc",
    status="success",
)
```

### Schedule model helpers

| Method                                                  | Description                      |
| ------------------------------------------------------- | -------------------------------- |
| `schedule.update(**kwargs) -> Schedule`                 | Update schedule config or input. |
| `schedule.delete() -> None`                             | Delete the schedule.             |
| `schedule.list_runs(**params) -> ScheduleRunListResult` | List runs for this schedule.     |
| `run.get_result() -> ScheduleRunResult`                 | Fetch full output for a run.     |
| `schedule_run.duration -> str \| None`                  | Formatted duration (HH:MM:SS).   |

### Schedule run fields

Schedule run list items (`ScheduleRun`) expose run metadata:

| Field          | Description                                                                                    |
| -------------- | ---------------------------------------------------------------------------------------------- |
| `id`           | Run ID.                                                                                        |
| `agent_id`     | Agent ID associated with the run.                                                              |
| `schedule_id`  | Schedule ID for scheduled runs.                                                                |
| `run_type`     | Run type, usually `schedule`.                                                                  |
| `status`       | Run status (lowercase): `started`, `success`, `failed`, `cancelled`, `aborted`, `unavailable`. |
| `started_at`   | Execution start timestamp.                                                                     |
| `completed_at` | Execution end timestamp.                                                                       |
| `input`        | Input used for the run, when provided by the backend.                                          |
| `config`       | Schedule config used for the run, when provided by the backend.                                |

### Schedule run results

`run.get_result()` returns a `ScheduleRunResult` with the stored output payload.
The `output` field is a list of backend-defined event dictionaries and is not
guaranteed to match a fixed schema.

### Agent schedule facade

Access `agent.schedule` for scoped operations:

```python
agent = client.get_agent_by_id("agent-123")

# Create schedule via agent
schedule = agent.schedule.create(
    input="Daily task",
    schedule="0 9 * * 0-4",
)

# List this agent's schedules
for s in agent.schedule.list():
    print(s.id)

# List runs for a schedule
runs = agent.schedule.list_runs(schedule.id)
```

______________________________________________________________________

### Language Models & Utilities

#### `client.list_language_models() -> list[dict]`

Returns the language model catalogue visible to the current API key. Each entry
contains provider metadata, model identifiers, and optional base URLs.

#### `client.ping() -> bool`

Calls `/health-check`. Returns `True` when the API responds successfully,
otherwise `False`.

#### `client.timeout`

Property exposing the current timeout (seconds). Assigning a new value rebuilds
the shared `httpx.Client` instance.

______________________________________________________________________

## Error Handling

All network operations raise typed exceptions from `glaip_sdk.exceptions` when
the backend responds with an error status.

| Exception                            | Trigger                                                                 |
| ------------------------------------ | ----------------------------------------------------------------------- |
| `AuthenticationError`                | Missing/invalid `X-API-Key` (401).                                      |
| `ForbiddenError`                     | Attempt to access a master-key-only endpoint with an account key (403). |
| `NotFoundError`                      | Resource does not exist or is soft-deleted (404).                       |
| `ValidationError`                    | Payload failed validation (400/422).                                    |
| `ConflictError`                      | Duplicate names or incompatible state (409).                            |
| `RateLimitError`                     | Too many requests (429).                                                |
| `TimeoutError` / `AgentTimeoutError` | Request or streaming timeout.                                           |
| `ServerError`                        | Backend 5xx responses.                                                  |

Example pattern:

```python
from glaip_sdk import Client
from glaip_sdk.exceptions import AuthenticationError, ValidationError

client = Client()

try:
    agent = client.create_agent(name="demo", instruction="Be helpful")
except AuthenticationError:
    print("Invalid API key")
except ValidationError as exc:
    print("Payload rejected", exc.payload)
```

## Troubleshooting & FAQ

- **401 Invalid API key** — Refresh credentials from the AIP console and confirm `AIP_API_KEY` is set.
- **404 Not found** — Resources are soft-deleted; call `client.list_*` to confirm IDs before retrying.
- **409 Conflict** — Resolve duplicate names or finish outstanding runs before retrying the write.
- **429 Rate limited** — Catch `RateLimitError` and back off using the `Retry-After` header from the REST response.
- **Streaming stalls** — Increase `timeout`; SSE connections idle for 5 minutes are closed server-side.

______________________________________________________________________

## Related Documentation

- [CLI Commands Reference](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/cli-commands)
- [REST API Reference](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/rest-api)
- [Hands-on examples](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/tutorials/hands-on-examples) for curated, runnable projects
- [GL SDK Cookbook](https://github.com/gl-sdk/gen-ai-sdk-cookbook/tree/main/gl-aip) for advanced patterns and integrations

Keep this page in sync whenever you add new client methods, adjust signatures, or
expand the backend payloads consumed by the SDK.
