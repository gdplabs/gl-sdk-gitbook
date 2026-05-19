## GET /mcps/

**Summary:** List all MCPs

Retrieve a list of all MCP configurations, optionally including related resources (e.g., tools).

Args:
mcp_service: Injected MCP service dependency.
account_id: Account ID from API key (None for master API key)
include: If set to 'tools', include tools for each MCP
validate_mcp_params: Injected MCP query parameter validator dependency.

Returns:
MCPWithToolsListResponse | MCPListResponse:
Response containing a list of MCPs, each with an optional tools field.

Raises:
StandardHTTPException: If a database error occurs.

**Authentication:** API key (`X-API-Key` header)

### Query Parameters

| Name      | Type   | Required | Description                                                                                 |
| --------- | ------ | -------- | ------------------------------------------------------------------------------------------- |
| `include` | string | No       | Comma-separated list of related resources to include. Currently, only 'tools' is supported. |

**Request Body:** None

### Responses

| Status | Description                         | Schema                                   |
| ------ | ----------------------------------- | ---------------------------------------- |
| `200`  | List of MCPs retrieved successfully | `application/json` — —                   |
| `422`  | Validation Error                    | `application/json` — HTTPValidationError |
| `500`  | Internal server error               | `application/json` — ErrorResponse       |

## POST /mcps/

**Summary:** Create a new MCP

Create a new MCP configuration.

Args:
mcp: The MCP configuration data.
mcp_service: Injected MCP service dependency.
account_id: Account ID from API key (None for master API key)

Returns:
MCPCreateResponse: Response containing the ID of the created MCP.

Raises:
StandardHTTPException: If an MCP with the same name already exists (409)
or if another database error occurs.

**Authentication:** API key (`X-API-Key` header)

**Parameters:** None

### Request Body

_Required._

- `application/json` — [MCPCreate](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/schemas/mcps#schema-mcpcreate)

For complete field specifications, constraints, and validation rules, see the [MCP Schema Reference](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/schemas/mcps).

### Responses

| Status | Description                                  | Schema                                                |
| ------ | -------------------------------------------- | ----------------------------------------------------- |
| `201`  | MCP created successfully                     | `application/json` — BaseResponse_dict_str\_\_str\_\_ |
| `400`  | Invalid input data                           | `application/json` — ErrorResponse                    |
| `422`  | Validation error - missing or invalid fields | `application/json` — ErrorResponse                    |
| `500`  | Internal server error                        | `application/json` — ErrorResponse                    |

## POST /mcps/connect

**Summary:** Test MCP Connection

Tests the connection to an MCP server using the provided configuration without saving it.

**Authentication:** API key (`X-API-Key` header)

**Parameters:** None

### Request Body

_Required._

- `application/json` — [MCPConnectionTestRequest](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/schemas/mcps#connection-test-schemas)

### Responses

| Status | Description                                    | Schema                                                |
| ------ | ---------------------------------------------- | ----------------------------------------------------- |
| `200`  | Connection successful                          | `application/json` — BaseResponse_dict_str\_\_str\_\_ |
| `400`  | Invalid input data                             | `application/json` — ErrorResponse                    |
| `422`  | Validation Error                               | `application/json` — HTTPValidationError              |
| `500`  | Internal server error                          | `application/json` — ErrorResponse                    |
| `503`  | Service unavailable (e.g., connection refused) | `application/json` — ErrorResponse                    |

## POST /mcps/connect/tools

**Summary:** Fetch tools from an MCP configuration

Fetches the list of tools from an MCP server using the provided configuration without saving it.

**Authentication:** API key (`X-API-Key` header)

**Parameters:** None

### Request Body

_Required._

- `application/json` — [MCPConnectionTestRequest](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/schemas/mcps#connection-test-schemas)

### Responses

| Status | Description                                    | Schema                                                  |
| ------ | ---------------------------------------------- | ------------------------------------------------------- |
| `200`  | Tools retrieved successfully                   | `application/json` — BaseResponse_MCPToolListResponse\_ |
| `400`  | Invalid input data                             | `application/json` — ErrorResponse                      |
| `422`  | Validation Error                               | `application/json` — HTTPValidationError                |
| `500`  | Internal server error                          | `application/json` — ErrorResponse                      |
| `503`  | Service unavailable (e.g., connection refused) | `application/json` — ErrorResponse                      |

## GET /mcps/{mcp_id}

**Summary:** Get MCP by ID

Retrieve a single MCP configuration by its unique ID, optionally including related resources (e.g., tools).

Args:
mcp_id: The unique identifier of the MCP.
mcp_service: Injected MCP service dependency.
account_id: Account ID from API key (None for master API key)
include: If set to 'tools', include tools for this MCP.
validate_mcp_params: Injected MCP query parameter validator dependency.

Returns:
MCPDetailResponse or MCPDetailWithToolsResponse: Response containing the MCP details.

Raises:
StandardHTTPException: If the MCP is not found (404) or a database error occurs.

**Authentication:** API key (`X-API-Key` header)

### Path Parameters

| Name     | Type          | Required | Description |
| -------- | ------------- | -------- | ----------- |
| `mcp_id` | string (uuid) | Yes      | —           |

### Query Parameters

| Name      | Type   | Required | Description                                                                                 |
| --------- | ------ | -------- | ------------------------------------------------------------------------------------------- |
| `include` | string | No       | Comma-separated list of related resources to include. Currently, only 'tools' is supported. |

**Request Body:** None

### Responses

| Status | Description                | Schema                             |
| ------ | -------------------------- | ---------------------------------- |
| `200`  | MCP retrieved successfully | `application/json` — —             |
| `404`  | MCP not found              | `application/json` — ErrorResponse |
| `422`  | Invalid MCP ID format      | `application/json` — ErrorResponse |
| `500`  | Internal server error      | `application/json` — ErrorResponse |

## PUT /mcps/{mcp_id}

**Summary:** Update an MCP

Update an existing MCP configuration.

Args:
mcp_id: The unique identifier of the MCP to update.
mcp: The updated MCP data.
mcp_service: Injected MCP service dependency.
account_id: Account ID from API key (None for master API key)

Returns:
MCPDetailResponse: Response containing the updated MCP details.

Raises:
StandardHTTPException: If the MCP is not found (404) or a database
error (e.g., unique constraint) occurs.

**Authentication:** API key (`X-API-Key` header)

### Path Parameters

| Name     | Type          | Required | Description |
| -------- | ------------- | -------- | ----------- |
| `mcp_id` | string (uuid) | Yes      | —           |

### Request Body

_Required._

- `application/json` — [MCPCreate](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/schemas/mcps#schema-mcpcreate)

### Responses

| Status | Description                                                        | Schema                                          |
| ------ | ------------------------------------------------------------------ | ----------------------------------------------- |
| `200`  | MCP updated successfully                                           | `application/json` — BaseResponse_MCPResponse\_ |
| `400`  | Invalid input data                                                 | `application/json` — ErrorResponse              |
| `404`  | MCP not found                                                      | `application/json` — ErrorResponse              |
| `422`  | Validation error - missing/invalid fields or invalid MCP ID format | `application/json` — ErrorResponse              |
| `500`  | Internal server error                                              | `application/json` — ErrorResponse              |

## PATCH /mcps/{mcp_id}

**Summary:** Update an MCP Partially

Update an existing MCP configuration partially.

Args:
mcp_id: The unique identifier of the MCP to update.
mcp: The updated MCP data (partial update).
mcp_service: Injected MCP service dependency.
account_id: Account ID from API key (None for master API key)

Returns:
MCPDetailResponse: Response containing the updated MCP details.

Raises:
StandardHTTPException: If the MCP is not found (404) or a database
error (e.g., unique constraint) occurs.

**Authentication:** API key (`X-API-Key` header)

### Path Parameters

| Name     | Type          | Required | Description |
| -------- | ------------- | -------- | ----------- |
| `mcp_id` | string (uuid) | Yes      | —           |

### Request Body

_Required._

- `application/json` — [MCPPatch](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/schemas/mcps#schema-mcppatch)

### Responses

| Status | Description                                                        | Schema                                          |
| ------ | ------------------------------------------------------------------ | ----------------------------------------------- |
| `200`  | MCP updated successfully                                           | `application/json` — BaseResponse_MCPResponse\_ |
| `400`  | Invalid input data                                                 | `application/json` — ErrorResponse              |
| `404`  | MCP not found                                                      | `application/json` — ErrorResponse              |
| `422`  | Validation error - missing/invalid fields or invalid MCP ID format | `application/json` — ErrorResponse              |
| `500`  | Internal server error                                              | `application/json` — ErrorResponse              |

## DELETE /mcps/{mcp_id}

**Summary:** Delete an MCP

Soft delete an MCP configuration by its ID.

Args:
mcp_id: The unique identifier of the MCP to delete.
mcp_service: Injected MCP service dependency.
account_id: Account ID from API key (None for master API key)

Returns:
MCPDeleteResponse: Response indicating successful deletion.

Raises:
StandardHTTPException: If the MCP is not found (404) or a database
error occurs.

**Authentication:** API key (`X-API-Key` header)

### Path Parameters

| Name     | Type          | Required | Description |
| -------- | ------------- | -------- | ----------- |
| `mcp_id` | string (uuid) | Yes      | —           |

**Request Body:** None

### Responses

| Status | Description              | Schema                                                |
| ------ | ------------------------ | ----------------------------------------------------- |
| `200`  | MCP deleted successfully | `application/json` — BaseResponse_dict_str\_\_str\_\_ |
| `404`  | MCP not found            | `application/json` — ErrorResponse                    |
| `422`  | Invalid MCP ID format    | `application/json` — ErrorResponse                    |
| `500`  | Internal server error    | `application/json` — ErrorResponse                    |

## POST /mcps/{mcp_id}/restore

**Summary:** Restore soft-deleted MCP

Restore a soft-deleted MCP to active state

**Authentication:** API key (`X-API-Key` header)

### Path Parameters

| Name     | Type          | Required | Description |
| -------- | ------------- | -------- | ----------- |
| `mcp_id` | string (uuid) | Yes      | —           |

**Request Body:** None

### Responses

| Status | Description               | Schema                                                |
| ------ | ------------------------- | ----------------------------------------------------- |
| `200`  | MCP restored successfully | `application/json` — BaseResponse_dict_str\_\_str\_\_ |
| `404`  | MCP not found             | `application/json` — ErrorResponse                    |
| `422`  | Invalid MCP ID format     | `application/json` — ErrorResponse                    |
| `500`  | Internal server error     | `application/json` — ErrorResponse                    |

## GET /mcps/{mcp_id}/tools

**Summary:** List tools from MCP

Retrieve a list of tools from a specific MCP server with proper session management.

Args:
mcp_id: The ID of the MCP to fetch tools from
mcp_service_factory: Factory for creating MCP service instances with proper session management
account_id: Account ID from API key (None for master API key)

Returns:
MCPToolListStandardResponse containing the list of tools available from the MCP

Raises:
HTTPException: If MCP is not found or tools cannot be fetched

**Authentication:** API key (`X-API-Key` header)

### Path Parameters

| Name     | Type          | Required | Description |
| -------- | ------------- | -------- | ----------- |
| `mcp_id` | string (uuid) | Yes      | —           |

**Request Body:** None

### Responses

| Status | Description                         | Schema                                                  |
| ------ | ----------------------------------- | ------------------------------------------------------- |
| `200`  | Tools retrieved successfully        | `application/json` — BaseResponse_MCPToolListResponse\_ |
| `404`  | MCP not found or URL not configured | `application/json` — ErrorResponse                      |
| `422`  | Invalid MCP ID format               | `application/json` — ErrorResponse                      |
| `500`  | Failed to fetch tools from MCP      | `application/json` — ErrorResponse                      |
