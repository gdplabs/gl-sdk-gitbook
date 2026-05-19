## GET /tools/

**Summary:** Get list of tools

Retrieve a list of all tools available in the system. Returns an array of tool objects.

**Authentication:** API key (`X-API-Key` header)

### Query Parameters

| Name   | Type | Required | Description                            |
| ------ | ---- | -------- | -------------------------------------- |
| `type` | —    | No       | Filter by tool type (native or custom) |

**Request Body:** None

### Responses

| Status | Description                          | Schema                                                  |
| ------ | ------------------------------------ | ------------------------------------------------------- |
| `200`  | Successfully retrieved list of tools | `application/json` — BaseResponse_list_ToolListItem\_\_ |
| `422`  | Validation Error                     | `application/json` — HTTPValidationError                |

## POST /tools/

**Summary:** Create a new tool

Create a new tool entry by providing tool metadata. Returns the created tool object.

**Authentication:** API key (`X-API-Key` header)

**Parameters:** None

### Request Body

_Required._

- `application/json` — [ToolBase](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/schemas/tools#schema-toolbase)

For complete field specifications, constraints, and validation rules, see the [Tools Schema Reference](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/schemas/tools).

### Responses

| Status | Description               | Schema                                                |
| ------ | ------------------------- | ----------------------------------------------------- |
| `200`  | Tool created successfully | `application/json` — BaseResponse_dict_str\_\_Any\_\_ |
| `422`  | Validation Error          | —                                                     |

## POST /tools/upload

**Summary:** Upload and register a new tool plugin

This endpoint allows uploading a Python file containing a tool plugin class. The plugin will be validated, registered at runtime, and stored in the database.

This endpoint is for creating new tools only, not updating existing ones. For updates, use PUT /tools/{tool_id}/upload instead.

**Authentication:** API key (`X-API-Key` header)

**Parameters:** None

### Request Body

_Required._

- `multipart/form-data` — Body_upload_and_register_plugin_tools_upload_post

### Responses

| Status | Description                                      | Schema                                                |
| ------ | ------------------------------------------------ | ----------------------------------------------------- |
| `200`  | Tool plugin uploaded and registered successfully | `application/json` — BaseResponse_dict_str\_\_Any\_\_ |
| `400`  | Invalid plugin file                              | —                                                     |
| `409`  | Tool with the same name already exists           | —                                                     |
| `422`  | Validation Error                                 | `application/json` — HTTPValidationError              |
| `500`  | Failed to register plugin                        | —                                                     |

### Example upload

```bash
curl -X POST "$AIP_API_URL/tools/upload" \
  -H "X-API-Key: $AIP_API_KEY" \
  -F name=calculator \
  -F description="Performs basic arithmetic" \
  -F file=@calculator.py
```

The file `calculator.py` must export a `tool_plugin` entry point. See the
[Tools guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/tools#create-tools)
for a full walkthrough of packaging and re-uploading custom tools.

## PUT /tools/{id}

**Summary:** Update tool metadata

Update metadata for an existing tool by its ID. Returns the updated tool object.

**Authentication:** API key (`X-API-Key` header)

### Path Parameters

| Name | Type          | Required | Description |
| ---- | ------------- | -------- | ----------- |
| `id` | string (uuid) | Yes      | —           |

### Request Body

_Required._

- `application/json` — [ToolBase](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/schemas/tools#schema-toolbase)

For complete field specifications, constraints, and validation rules, see the [Tools Schema Reference](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/schemas/tools).

### Responses

| Status | Description               | Schema                                                |
| ------ | ------------------------- | ----------------------------------------------------- |
| `200`  | Tool updated successfully | `application/json` — BaseResponse_dict_str\_\_Any\_\_ |
| `404`  | Tool not found            | —                                                     |
| `422`  | Validation Error          | —                                                     |

## GET /tools/{id}

**Summary:** Get tool details by ID

Retrieve detailed information about a specific tool by its ID.

**Authentication:** API key (`X-API-Key` header)

### Path Parameters

| Name | Type          | Required | Description |
| ---- | ------------- | -------- | ----------- |
| `id` | string (uuid) | Yes      | —           |

**Request Body:** None

### Responses

| Status | Description                         | Schema                                                |
| ------ | ----------------------------------- | ----------------------------------------------------- |
| `200`  | Tool details retrieved successfully | `application/json` — BaseResponse_dict_str\_\_Any\_\_ |
| `404`  | Tool not found                      | —                                                     |
| `422`  | Validation Error                    | `application/json` — HTTPValidationError              |

## DELETE /tools/{id}

**Summary:** Delete a tool

Delete a specific tool by its ID. Returns a confirmation message upon successful deletion.

**Authentication:** API key (`X-API-Key` header)

### Path Parameters

| Name | Type          | Required | Description |
| ---- | ------------- | -------- | ----------- |
| `id` | string (uuid) | Yes      | —           |

**Request Body:** None

### Responses

| Status | Description               | Schema                                                |
| ------ | ------------------------- | ----------------------------------------------------- |
| `200`  | Tool deleted successfully | `application/json` — BaseResponse_dict_str\_\_str\_\_ |
| `404`  | Tool not found            | —                                                     |
| `422`  | Validation Error          | `application/json` — HTTPValidationError              |

## POST /tools/{id}/restore

**Summary:** Restore a soft-deleted tool

Restore a soft-deleted tool to an active state.

**Authentication:** API key (`X-API-Key` header)

### Path Parameters

| Name | Type          | Required | Description |
| ---- | ------------- | -------- | ----------- |
| `id` | string (uuid) | Yes      | —           |

**Request Body:** None

### Responses

| Status | Description                   | Schema                                                |
| ------ | ----------------------------- | ----------------------------------------------------- |
| `200`  | Tool restored successfully    | `application/json` — BaseResponse_dict_str\_\_str\_\_ |
| `404`  | Tool not found or not deleted | —                                                     |
| `422`  | Validation Error              | `application/json` — HTTPValidationError              |

## GET /tools/{tool_id}/script

**Summary:** Get the script content for a tool

Retrieve the Python script content for a specific tool by its ID.

**Authentication:** API key (`X-API-Key` header)

### Path Parameters

| Name      | Type   | Required | Description |
| --------- | ------ | -------- | ----------- |
| `tool_id` | string | Yes      | —           |

**Request Body:** None

### Responses

| Status | Description                        | Schema                                                |
| ------ | ---------------------------------- | ----------------------------------------------------- |
| `200`  | Tool script retrieved successfully | `application/json` — BaseResponse_dict_str\_\_Any\_\_ |
| `404`  | Tool or script not found           | —                                                     |
| `422`  | Validation Error                   | `application/json` — HTTPValidationError              |

## PUT /tools/{tool_id}/upload

**Summary:** Update a tool plugin via file upload

This endpoint allows updating an existing tool plugin by uploading a new Python file. The plugin will be validated, registered at runtime, and the database record will be updated.

**Authentication:** API key (`X-API-Key` header)

### Path Parameters

| Name      | Type          | Required | Description                  |
| --------- | ------------- | -------- | ---------------------------- |
| `tool_id` | string (uuid) | Yes      | The ID of the tool to update |

### Request Body

_Required._

- `multipart/form-data` — Body_update_tool_via_upload_tools\_\_tool_id\_\_upload_put

### Responses

| Status | Description                      | Schema                                                |
| ------ | -------------------------------- | ----------------------------------------------------- |
| `200`  | Tool plugin updated successfully | `application/json` — BaseResponse_dict_str\_\_Any\_\_ |
| `400`  | Invalid plugin file              | —                                                     |
| `404`  | Tool not found                   | —                                                     |
| `422`  | Validation Error                 | `application/json` — HTTPValidationError              |
| `500`  | Failed to update plugin          | —                                                     |
