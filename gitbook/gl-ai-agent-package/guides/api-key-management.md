---
icon: binary-lock
---


This guide covers how to integrate with GLAIR AIP Platform's multi-API key authentication system for remote server implementations.

## Overview

The AIP Platform supports multiple API keys per tenant account, enabling:

- Safe API key rotation without downtime
- Audit logging of all API key activities
- Key lifecycle management (create, list, update, revoke)
- 90-day expiration for newly created expiring keys

______________________________________________________________________

## Authentication

All protected endpoints require an API key in the `X-API-Key` header:

```
X-API-Key: <your-api-key>
```

### API Key Types

| Type                           | Description                                  | Expiration            |
| ------------------------------ | -------------------------------------------- | --------------------- |
| **Primary (Non-Expiring) Key** | Initial account key created at signup        | Never expires         |
| **Expiring Key**               | Additional keys created via `POST /api-keys` | Expires after 90 days |

______________________________________________________________________

## Response Format

All API responses use a consistent envelope format:

### Success Response

```json
{
  "success": true,
  "data": {},
  "message": "Operation completed successfully"
}
```

### Error Response

```json
{
  "success": false,
  "error": "Unauthorized|NotFound|Conflict|ValidationError|...",
  "message": "Human-readable error description",
  "details": null
}
```

______________________________________________________________________

## API Key Lifecycle Endpoints

### 1. Create Account (Public)

Creates a new tenant account with a primary non-expiring API key.

**Endpoint:** `POST /accounts/`

**Headers:**

- `Content-Type: application/json`
- No `X-API-Key` required (public endpoint)

**Request Body:**

```json
{
  "name": "my-organization"
}
```

**Success Response (201):**

```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "api_key": "aip_xxxxxxxxxxxxxxxxx"
  },
  "message": "Account created successfully"
}
```

**Error Codes:**

- `409` - Duplicate account name
- `422` - Validation error (missing/empty name)

> **Note:** The `api_key` is returned only once at creation. Store it securely.

______________________________________________________________________

### 2. List API Keys

List all API keys for your account.

**Endpoint:** `GET /api-keys`

**Headers:**

- `X-API-Key: <your-api-key>`

**Query Parameters:**

| Parameter          | Type     | Description                                                        |
| ------------------ | -------- | ------------------------------------------------------------------ |
| `status`           | string   | Comma-separated: `active,expired,revoked,deleted`                  |
| `created_at_start` | datetime | Filter by creation date (inclusive)                                |
| `created_at_end`   | datetime | Filter by creation date (inclusive)                                |
| `include_deleted`  | boolean  | Include soft-deleted keys (default: `false`)                       |
| `limit`            | integer  | Items per page (optional, `>=1`, currently no backend upper bound) |
| `page`             | integer  | Page number (optional, `>=1`)                                      |

**Success Response (200):**

```json
{
  "success": true,
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "prod-deployment-2026",
      "preview": "sk-1****COUA",
      "status": "active",
      "created_at": "2026-02-06T10:30:00Z",
      "expires_at": "2026-05-07T10:30:00Z",
      "last_used_at": "2026-02-07T09:12:00Z",
      "created_by_api_key_id": "<actor-key-id>",
      "created_by_name": "<actor-key-name>",
      "revoked_at": null,
      "revoked_by_api_key_id": null,
      "revoked_by_name": null
    }
  ],
  "message": "API keys retrieved successfully"
}
```

**Paginated Response (when `limit` and `page` provided):**

```json
{
  "success": true,
  "data": [...],
  "total": 5,
  "page": 1,
  "limit": 20,
  "has_next": true,
  "has_prev": false,
  "message": "API keys retrieved successfully"
}
```

**Error Codes:**

- `401` - Invalid or missing API key
- `422` - Invalid filter values

______________________________________________________________________

### 3. Create API Key

Create a new expiring API key (90-day expiration).

**Endpoint:** `POST /api-keys`

**Headers:**

- `X-API-Key: <your-api-key>`
- `Content-Type: application/json`

**Request Body:**

```json
{
  "name": "prod-deployment-2026"
}
```

> **Note:** `name` is optional.
> Duplicate names are allowed within the same account.

**Success Response (201):**

```json
{
  "success": true,
  "data": {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "api_key": "aip_yyyyyyyyyyyyyyyyy",
    "name": "prod-deployment-2026",
    "preview": "sk-y****9XYZ",
    "status": "active",
    "created_at": "2026-02-06T10:30:00Z",
    "expires_at": "2026-05-07T10:30:00Z",
    "last_used_at": null,
    "created_by_api_key_id": "<actor-key-id>",
    "created_by_name": "<actor-key-name>"
  },
  "message": "API key created successfully"
}
```

> **Important:** The `api_key` secret is returned only once at creation. Store it immediately.

______________________________________________________________________

### 4. Update API Key Name

Update the name of an existing API key.

**Endpoint:** `PATCH /api-keys/{key_id}`

**Headers:**

- `X-API-Key: <your-api-key>`
- `Content-Type: application/json`

**Request Body:**

```json
{
  "name": "updated-key-name"
}
```

**Success Response (200):**

```json
{
  "success": true,
  "data": {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "name": "updated-key-name",
    "preview": "sk-y****9XYZ",
    "status": "active",
    "created_at": "2026-02-06T10:30:00Z",
    "expires_at": "2026-05-07T10:30:00Z",
    "last_used_at": null,
    "created_by_api_key_id": "<actor-key-id>",
    "created_by_name": "<actor-key-name>",
    "revoked_at": null,
    "revoked_by_api_key_id": null,
    "revoked_by_name": null
  },
  "message": "API key updated successfully"
}
```

**Error Codes:**

- `401` - Invalid or missing API key
- `404` - Key not found
- `422` - Validation error

______________________________________________________________________

### 5. Revoke API Key

Revoke an API key. Revocation is permanent and irreversible.

**Endpoint:** `POST /api-keys/{key_id}/revoke`

**Headers:**

- `X-API-Key: <your-api-key>`

**Success Response (200):**

```json
{
  "success": true,
  "data": {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "status": "revoked",
    "revoked_at": "2026-02-06T12:00:00Z",
    "revoked_by_api_key_id": "<actor-key-id>",
    "revoked_by_name": "<actor-key-name>"
  },
  "message": "API key revoked successfully"
}
```

**Error Codes:**

- `401` - Invalid or missing API key
- `404` - Key not found
- `409` - Cannot revoke the last active non-expiring key

> **Note:** Revocation is idempotent. Revoking an already-revoked key returns success.

______________________________________________________________________

## Key Rotation Workflow

To rotate an expiring API key without downtime:

> **Important:** This flow works when revoking the old key keeps at least one active non-expiring key in the account.

```bash
# Prerequisite: set the old key id you want to revoke
# OLD_KEY_ID="<old-key-uuid>"

# Step 1: Create a new key
NEW_KEY_RESPONSE=$(curl -s -X POST "$AIP_BASE_URL/api-keys" \
  -H "X-API-Key: $OLD_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"rotation-2026-02"}')

NEW_KEY=$(echo "$NEW_KEY_RESPONSE" | jq -r '.data.api_key')

# Step 2: Deploy the new key to your application
# (Application-specific deployment steps)

# Step 3: Verify the new key works
curl -X GET "$AIP_BASE_URL/api-keys" \
  -H "X-API-Key: $NEW_KEY"

# Step 4: Revoke the old key
curl -X POST "$AIP_BASE_URL/api-keys/$OLD_KEY_ID/revoke" \
  -H "X-API-Key: $NEW_KEY"
```

______________________________________________________________________

## Activity Audit

### List Activity (Tenant)

Query API key activity logs for your account. This is useful for security auditing and tracking who performed what actions.

**Endpoint:** `GET /api-keys/activity`

**Headers:**

- `X-API-Key: <your-api-key>`

**Query Parameters:**

| Parameter       | Type     | Description                                                                                    |
| --------------- | -------- | ---------------------------------------------------------------------------------------------- |
| `resource_type` | string   | Comma-separated: `api_key,account,agent,agent_run,hitl,mcp,tool,schedule,utils,language_model` |
| `action`        | string   | Comma-separated: `create,read,update,delete,revoke,run,decision,timeout`                       |
| `api_key_id`    | UUID     | Filter by specific API key                                                                     |
| `status_code`   | string   | Comma-separated HTTP status codes (e.g., `200,401,500`)                                        |
| `start_date`    | datetime | Filter by event date (inclusive, `>=`)                                                         |
| `end_date`      | datetime | Filter by event date (inclusive, `<=`)                                                         |
| `limit`         | integer  | Items per page (default: `20`, range: `1-100`)                                                 |
| `page`          | integer  | Page number (default: `1`, `>=1`)                                                              |

**Success Response (200):**

```json
{
  "success": true,
  "data": [
    {
      "id": "770e8400-e29b-41d4-a716-446655440002",
      "account_id": "550e8400-e29b-41d4-a716-446655440000",
      "api_key_id": "660e8400-e29b-41d4-a716-446655440001",
      "resource_type": "agent",
      "action": "run",
      "http_method": "POST",
      "path_template": "/agents/{agent_id}/run",
      "resource_id": "880e8400-e29b-41d4-a716-446655440003",
      "status_code": 200,
      "duration_ms": 150,
      "metadata": {
        "request_id": "req_1234567890",
        "actor_type": "api_key",
        "actor_name_at_event": "prod-deployment-2026"
      },
      "created_at": "2026-02-10T09:18:00Z"
    }
  ],
  "total": 150,
  "page": 1,
  "limit": 20,
  "has_next": true,
  "has_prev": false,
  "message": "API key activity logs retrieved successfully"
}
```

**Error Codes:**

- `401` - Invalid or missing API key
- `422` - Invalid filter values

> **Note:** Sort order is `created_at DESC, id DESC` (newest first).

______________________________________________________________________

## Error Reference

### Common HTTP Status Codes

| Code  | Error Type        | Description                                            |
| ----- | ----------------- | ------------------------------------------------------ |
| `200` | -                 | Success (GET, PATCH, POST for revoke)                  |
| `201` | -                 | Created (POST for create)                              |
| `401` | `Unauthorized`    | Invalid, expired, or missing API key                   |
| `404` | `NotFound`        | Resource not found                                     |
| `409` | `Conflict`        | Business rule violation (e.g., cannot revoke last key) |
| `422` | `ValidationError` | Request validation failed                              |

### Specific Error Messages

| Scenario                    | HTTP | Error Type        | Message                                                                                     |
| --------------------------- | ---- | ----------------- | ------------------------------------------------------------------------------------------- |
| Missing `X-API-Key` header  | 401  | `Unauthorized`    | `API key is required. Please provide X-API-Key header`                                      |
| Invalid/expired/revoked key | 401  | `Unauthorized`    | `Invalid API key`                                                                           |
| Key not found               | 404  | `NotFound`        | `API key {key_id} not found`                                                                |
| Revoke last active key      | 409  | `Conflict`        | `Cannot revoke: account must retain at least one active non-expiring key`                   |
| Invalid date range          | 422  | `ValidationError` | `start_date must be less than or equal to end_date`                                         |
| Invalid limit/page          | 422  | `ValidationError` | `GET /api-keys`: `limit >= 1`, `page >= 1`; activity endpoints: `limit 1..100`, `page >= 1` |

______________________________________________________________________
