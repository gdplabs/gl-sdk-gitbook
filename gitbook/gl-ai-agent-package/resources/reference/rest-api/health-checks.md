## GET /health-check

**Summary:** Health Check

Health check endpoint.

Returns:
HealthCheckResponse: Status and message indicating service health.

**Authentication:** None

**Parameters:** None

**Request Body:** None

### Responses

| Status | Description         | Schema                                   |
| ------ | ------------------- | ---------------------------------------- |
| `200`  | Successful Response | `application/json` — HealthCheckResponse |

## GET /health-check/auth-test

**Summary:** Test Authentication

Test authentication endpoint.

This endpoint requires a valid API key to access and can be used to test
that authentication is working correctly.

Args:
account_id: The verified API key from the request header

Returns:
HealthCheckResponse: Status confirming authentication works

**Authentication:** API key (`X-API-Key` header)

**Parameters:** None

**Request Body:** None

### Responses

| Status | Description         | Schema                                   |
| ------ | ------------------- | ---------------------------------------- |
| `200`  | Successful Response | `application/json` — HealthCheckResponse |

## GET /health-check/database

**Summary:** Database Health Check

Database health check endpoint.

Returns:
HealthCheckResponse: Status and message indicating database health.

Raises:
HTTPException: If database health check fails.

**Authentication:** None

**Parameters:** None

**Request Body:** None

### Responses

| Status | Description         | Schema                                   |
| ------ | ------------------- | ---------------------------------------- |
| `200`  | Successful Response | `application/json` — HealthCheckResponse |
