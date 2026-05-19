## GET /agents/

**Summary:** List all agents with optional filtering

Retrieve a filtered list of agents for display in cards/grids. Supports filtering by type, framework, name (partial match), version, and metadata fields.

Use metadata.{key} syntax for JSON metadata filtering (e.g., metadata.environment=production).

When sync_langflow_agents=true is specified, automatically fetches and syncs all available flows from the configured LangFlow server.

This uses the LANGFLOW_BASE_URL and LANGFLOW_API_KEY environment variables and creates new agents for any flows that don't already exist in the database.

**Authentication:** API key (`X-API-Key` header)

### Query Parameters

| Name                   | Type    | Required | Description                                                                                                                                                             |
| ---------------------- | ------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `agent_type`           | —       | No       | Filter by agent type (config, code, a2a, langflow)                                                                                                                      |
| `framework`            | —       | No       | Filter by framework (langchain, langgraph, google_adk)                                                                                                                  |
| `name`                 | —       | No       | Filter by partial name match (case-insensitive)                                                                                                                         |
| `version`              | —       | No       | Filter by exact version match                                                                                                                                           |
| `sync_langflow_agents` | boolean | No       | If true, fetches and syncs all available flows from LangFlow server before returning the agent list. Uses LANGFLOW_BASE_URL and LANGFLOW_API_KEY environment variables. |
|                        |         |          | Creates new agents for any flows that don't exist in the database.                                                                                                      |

**Request Body:** None

### Responses

| Status | Description                           | Schema                                                   |
| ------ | ------------------------------------- | -------------------------------------------------------- |
| `200`  | List of agents retrieved successfully | `application/json` — BaseResponse_list_AgentListItem\_\_ |
| `422`  | Validation Error                      | `application/json` — HTTPValidationError                 |
| `500`  | Internal server error                 | `application/json` — ErrorResponse                       |

## POST /agents/

**Summary:** Create new agent

Create a new config-based agent with optional tools, sub-agents, and MCP configurations

**Authentication:** API key (`X-API-Key` header)

**Parameters:** None

### Request Body

_Required._

- `application/json` — [AgentCreate](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/schemas/agents#agentcreate)

For complete field specifications, constraints, and validation rules, see the [Agents Schema Reference](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/schemas/agents).

### Responses

| Status | Description                                  | Schema                                                |
| ------ | -------------------------------------------- | ----------------------------------------------------- |
| `201`  | Agent created successfully                   | `application/json` — BaseResponse_dict_str\_\_str\_\_ |
| `400`  | Invalid input data                           | `application/json` — ErrorResponse                    |
| `409`  | Agent with name already exists               | `application/json` — ErrorResponse                    |
| `422`  | Validation error - missing or invalid fields | `application/json` — ErrorResponse                    |
| `500`  | Internal server error                        | `application/json` — ErrorResponse                    |

## POST /agents/langflow/sync

**Summary:** Sync LangFlow agents

Fetch available flows from LangFlow and create agents automatically.

Optionally accepts base_url and api_key in request body, with fallback to environment variables.

Can be called with no body to use environment variables only.

**Authentication:** API key (`X-API-Key` header)

**Parameters:** None

### Request Body

- `application/json` — —

### Responses

| Status | Description                                 | Schema                                    |
| ------ | ------------------------------------------- | ----------------------------------------- |
| `200`  | LangFlow agents synced successfully         | `application/json` — LangflowSyncResponse |
| `400`  | Invalid request data or missing credentials | —                                         |
| `422`  | Validation Error                            | `application/json` — HTTPValidationError  |
| `500`  | Internal server error                       | `application/json` — ErrorResponse        |

## GET /agents/schedules

**Summary:** Get schedules with optional filtering

Get paginated schedules with optional filtering

**Authentication:** API key (`X-API-Key` header)

### Query Parameters

| Name       | Type    | Required | Description                           |
| ---------- | ------- | -------- | ------------------------------------- |
| `limit`    | integer | No       | Maximum number of schedules to return |
| `page`     | integer | No       | Page number (1-based)                 |
| `agent_id` | —       | No       | Filter by agent ID                    |

**Request Body:** None

### Responses

| Status | Description                      | Schema                                                           |
| ------ | -------------------------------- | ---------------------------------------------------------------- |
| `200`  | Schedules retrieved successfully | `application/json` — PaginatedResponse_list_ScheduleResponse\_\_ |
| `404`  | Agent not found                  | `application/json` — ErrorResponse                               |
| `422`  | Validation Error                 | `application/json` — HTTPValidationError                         |
| `500`  | Internal server error            | `application/json` — ErrorResponse                               |

## GET /agents/schedules/{schedule_id}

**Summary:** Get specific schedule

Get a specific schedule by its ID

**Authentication:** API key (`X-API-Key` header)

### Path Parameters

| Name          | Type          | Required | Description |
| ------------- | ------------- | -------- | ----------- |
| `schedule_id` | string (uuid) | Yes      | —           |

**Request Body:** None

### Responses

| Status | Description                     | Schema                                               |
| ------ | ------------------------------- | ---------------------------------------------------- |
| `200`  | Schedule retrieved successfully | `application/json` — BaseResponse_ScheduleResponse\_ |
| `404`  | Schedule not found              | `application/json` — ErrorResponse                   |
| `422`  | Validation Error                | `application/json` — HTTPValidationError             |
| `500`  | Internal server error           | `application/json` — ErrorResponse                   |

## PUT /agents/schedules/{schedule_id}

**Summary:** Update schedule

Update an existing schedule

**Authentication:** API key (`X-API-Key` header)

### Path Parameters

| Name          | Type          | Required | Description |
| ------------- | ------------- | -------- | ----------- |
| `schedule_id` | string (uuid) | Yes      | —           |

### Request Body

_Required._

- `application/json` — ScheduleUpdateRequest

### Responses

| Status | Description                    | Schema                                               |
| ------ | ------------------------------ | ---------------------------------------------------- |
| `200`  | Schedule updated successfully  | `application/json` — BaseResponse_ScheduleResponse\_ |
| `400`  | Invalid schedule configuration | `application/json` — ErrorResponse                   |
| `404`  | Schedule not found             | `application/json` — ErrorResponse                   |
| `422`  | Invalid schedule format        | `application/json` — ErrorResponse                   |
| `500`  | Internal server error          | `application/json` — ErrorResponse                   |

## DELETE /agents/schedules/{schedule_id}

**Summary:** Delete schedule

Delete an existing schedule by its ID

**Authentication:** API key (`X-API-Key` header)

### Path Parameters

| Name          | Type          | Required | Description |
| ------------- | ------------- | -------- | ----------- |
| `schedule_id` | string (uuid) | Yes      | —           |

**Request Body:** None

### Responses

| Status | Description                   | Schema                                       |
| ------ | ----------------------------- | -------------------------------------------- |
| `200`  | Schedule deleted successfully | `application/json` — BaseResponse_NoneType\_ |
| `404`  | Schedule not found            | `application/json` — ErrorResponse           |
| `422`  | Invalid schedule ID format    | `application/json` — ErrorResponse           |
| `500`  | Internal server error         | `application/json` — ErrorResponse           |

## GET /agents/{agent_id}

**Summary:** Get agent details

Retrieve full agent configuration including tools, sub-agents, and MCP settings

**Authentication:** API key (`X-API-Key` header)

### Path Parameters

| Name       | Type          | Required | Description |
| ---------- | ------------- | -------- | ----------- |
| `agent_id` | string (uuid) | Yes      | —           |

**Request Body:** None

### Responses

| Status | Description                          | Schema                                            |
| ------ | ------------------------------------ | ------------------------------------------------- |
| `200`  | Agent details retrieved successfully | `application/json` — BaseResponse_AgentResponse\_ |
| `404`  | Agent not found                      | `application/json` — ErrorResponse                |
| `422`  | Invalid agent ID format              | `application/json` — ErrorResponse                |
| `500`  | Internal server error                | `application/json` — ErrorResponse                |

## PUT /agents/{agent_id}

**Summary:** Update agent (full replacement)

Replace an existing agent's configuration completely, including all relationships

**Authentication:** API key (`X-API-Key` header)

### Path Parameters

| Name       | Type          | Required | Description |
| ---------- | ------------- | -------- | ----------- |
| `agent_id` | string (uuid) | Yes      | —           |

### Request Body

_Required._

- `application/json` — [AgentCreate](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/schemas/agents#agentcreate)

For complete field specifications, constraints, and validation rules, see the [Agents Schema Reference](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/schemas/agents).

### Responses

| Status | Description                                                          | Schema                                            |
| ------ | -------------------------------------------------------------------- | ------------------------------------------------- |
| `200`  | Agent updated successfully                                           | `application/json` — BaseResponse_AgentResponse\_ |
| `400`  | Invalid input data                                                   | `application/json` — ErrorResponse                |
| `404`  | Agent not found                                                      | `application/json` — ErrorResponse                |
| `409`  | Agent name conflict                                                  | `application/json` — ErrorResponse                |
| `422`  | Validation error - missing/invalid fields or invalid agent ID format | `application/json` — ErrorResponse                |
| `500`  | Internal server error                                                | `application/json` — ErrorResponse                |

## DELETE /agents/{agent_id}

**Summary:** Soft delete agent

Soft delete an agent (marks as deleted but preserves data)

**Authentication:** API key (`X-API-Key` header)

### Path Parameters

| Name       | Type          | Required | Description |
| ---------- | ------------- | -------- | ----------- |
| `agent_id` | string (uuid) | Yes      | —           |

**Request Body:** None

### Responses

| Status | Description                | Schema                                                |
| ------ | -------------------------- | ----------------------------------------------------- |
| `200`  | Agent deleted successfully | `application/json` — BaseResponse_dict_str\_\_str\_\_ |
| `404`  | Agent not found            | `application/json` — ErrorResponse                    |
| `422`  | Invalid agent ID format    | `application/json` — ErrorResponse                    |
| `500`  | Internal server error      | `application/json` — ErrorResponse                    |

## POST /agents/{agent_id}/restore

**Summary:** Restore soft-deleted agent

Restore a soft-deleted agent to active state

**Authentication:** API key (`X-API-Key` header)

### Path Parameters

| Name       | Type          | Required | Description |
| ---------- | ------------- | -------- | ----------- |
| `agent_id` | string (uuid) | Yes      | —           |

**Request Body:** None

### Responses

| Status | Description                    | Schema                                                |
| ------ | ------------------------------ | ----------------------------------------------------- |
| `200`  | Agent restored successfully    | `application/json` — BaseResponse_dict_str\_\_str\_\_ |
| `404`  | Agent not found or not deleted | `application/json` — ErrorResponse                    |
| `422`  | Invalid agent ID format        | `application/json` — ErrorResponse                    |
| `500`  | Internal server error          | `application/json` — ErrorResponse                    |

## POST /agents/{agent_id}/run

**Summary:** Run agent and get streaming response

Execute an agent and stream the response back. Supports both JSON and form data with file attachments (multipart uploads).
When native tools/MCPs require user authentication, the backend may use
`gl_connectors_token` for GL Connectors prechecks and runtime propagation.

**Authentication:** API key (`X-API-Key` header)

### Path Parameters

| Name       | Type          | Required | Description |
| ---------- | ------------- | -------- | ----------- |
| `agent_id` | string (uuid) | Yes      | —           |

### Request Body

_Required._

Supported content types:

- `application/json`
- `multipart/form-data`

Common fields:

| Field                 | Type     | Required | Notes                                                                                     |
| --------------------- | -------- | -------- | ----------------------------------------------------------------------------------------- |
| `input`               | `string` | Yes      | User prompt sent to the agent.                                                           |
| `gl_connectors_token` | `string` | No       | Optional GL Connectors token for connector auth checks and runtime token propagation.    |
| `chat_history`        | `array`  | No       | Prior conversation turns.                                                                 |
| `pii_mapping`         | `object` | No       | Placeholder-to-PII mapping used by PII-aware workflows.                                  |
| `runtime_config`      | `object` | No       | Runtime overrides (`tool_configs`, `mcp_configs`, `agent_config`).                       |
| `files`               | `array`  | No       | Multipart only: uploaded files attached to the run request.                              |

### Responses

| Status | Description                                      | Schema                                   |
| ------ | ------------------------------------------------ | ---------------------------------------- |
| `200`  | Agent execution started, response is streaming.  | `text/event-stream` (SSE, each `data:` line contains JSON) |
| `400`  | Invalid request data or unsupported content type | `application/json` — ErrorResponse       |
| `403`  | GL Connectors token is invalid or forbidden      | `application/json` — ErrorResponse       |
| `404`  | Agent not found                                  | `application/json` — ErrorResponse       |
| `409`  | Run blocked by GL Connectors precheck            | `application/json` — ErrorResponse       |
| `422`  | Validation Error                                 | `application/json` — HTTPValidationError |
| `502`  | GL Connectors dependency failure                 | `application/json` — ErrorResponse       |
| `500`  | Internal server error                            | `application/json` — ErrorResponse       |

## GET /agents/{agent_id}/runs

**Summary:** Get runs for agent with optional filtering

Get paginated runs for a specific agent with optional filtering

**Authentication:** API key (`X-API-Key` header)

### Path Parameters

| Name       | Type          | Required | Description |
| ---------- | ------------- | -------- | ----------- |
| `agent_id` | string (uuid) | Yes      | —           |

### Query Parameters

| Name          | Type          | Required | Description                                           |
| ------------- | ------------- | -------- | ----------------------------------------------------- |
| `limit`       | integer       | No       | Maximum number of runs to return                      |
| `page`        | integer       | No       | Page number (1-based)                                 |
| `schedule_id` | string (uuid) | No       | Filter by schedule ID                                 |
| `run_type`    | string        | No       | Filter by run type (schedule)                         |
| `status`      | string        | No       | Filter by execution status (started, success, failed) |

**Request Body:** None

### Responses

| Status | Description                       | Schema                                                           |
| ------ | --------------------------------- | ---------------------------------------------------------------- |
| `200`  | Agent runs retrieved successfully | `application/json` — PaginatedResponse_list_AgentRunResponse\_\_ |
| `404`  | Agent not found                   | `application/json` — ErrorResponse                               |
| `422`  | Validation Error                  | `application/json` — HTTPValidationError                         |
| `500`  | Internal server error             | `application/json` — ErrorResponse                               |

## POST /agents/{agent_id}/schedule

**Summary:** Create schedule for agent

Create a new schedule for an agent with cron-like schedule configuration

**Authentication:** API key (`X-API-Key` header)

### Path Parameters

| Name       | Type          | Required | Description |
| ---------- | ------------- | -------- | ----------- |
| `agent_id` | string (uuid) | Yes      | —           |

### Request Body

_Required._

- `application/json` — ScheduleCreateRequest

### Responses

| Status | Description                    | Schema                                                 |
| ------ | ------------------------------ | ------------------------------------------------------ |
| `201`  | Schedule created successfully  | `application/json` — BaseResponse_ScheduleCreateData\_ |
| `400`  | Invalid schedule configuration | `application/json` — ErrorResponse                     |
| `404`  | Agent not found                | `application/json` — ErrorResponse                     |
| `422`  | Invalid schedule format        | `application/json` — ErrorResponse                     |
| `500`  | Internal server error          | `application/json` — ErrorResponse                     |
