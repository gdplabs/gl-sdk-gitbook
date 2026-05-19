---
icon: user
---

# User Management API

## User Management API

This guide covers how to use user management functionality in the Connector platform. The user management system allows you to create users, authenticate them, and manage their third-party integrations.

### Prerequisites

Before using the user management APIs, you'll need:

* **API Client Key**: Your API client key for authentication
* **API URL**: The base URL for GL Connector API (e.g., https://connectors.gdplabs.id)

All API requests must include your API client key in the `x-api-key` header.

### Authentication Flow

The typical user management flow involves:

1. Creating a user account
2. Authenticating the user to get a Bearer token
3. Using the Bearer token for authenticated requests
4. Managing third-party integrations

***

### API Endpoints

#### 1. Create User

Creates a new user account in the GL Connectors system.

**Endpoint:** `POST /users`

**Headers:**

* `x-api-key`: Your GL Connectors API client key
* `Content-Type`: application/json

**Request Body:**

```json
{
    "identifier": "unique-user-identifier"
}
```

**Example Request:**

```bash
curl --location 'https://connectors.gdplabs.id/users' \
--header 'x-api-key: {your-api-key}' \
--header 'Content-Type: application/json' \
--data '{
    "identifier":"fahmi-armand"
}'
```

**Response:**

```json
{
    "data": {
        "id": "0bc2191c-4080-4521-b30d-6bb993840b82",
        "client_id": "7e285918-9174-4cdb-8c8e-8359d48562a7",
        "identifier": "fahmi-armand",
        "secret": "sk-user-MGJjMjE5MWMtNDA4MC00NTIxLWIzMGQtNmJiOTkzODQwYjgy.ZmFobWktYXJtYW5kMg.8yKGgbAXGfiPE-OvfLjk__fLF7FYx1cPt55RJ2d73Bc",
        "secret_preview": "sk-user-...RJ2d73Bc",
        "is_active": true,
        "integrations": []
    },
    "meta": null
}
```

> ⚠️ **Important**: Save the `secret` value immediately. GL Connectors will not provide it again and does not store this secret for security reasons.

#### 2. User Authentication (Login)

Authenticates a user and returns a Bearer token for subsequent API calls.

**Endpoint:** `POST /auth/tokens`

**Headers:**

* `x-api-key`: Your GL Connectors API client key
* `Content-Type`: application/json

**Request Body:**

```json
{
    "identifier": "user-identifier",
    "secret": "user-secret-from-registration"
}
```

**Example Request:**

```bash
curl --location 'https://connectors.gdplabs.id/auth/tokens' \
--header 'x-api-key: {your-api-key}' \
--header 'Content-Type: application/json' \
--data '{
    "identifier": "fahmi-armand",
    "secret": "sk-user-MjdiYTA5OTgtYmExMC00MDU2LTgzYTMtNmFjYThjZmFlODVk.ZmFobWktYXJtYW5k.UoNe8Ra08YIFsIsaaSdSFi3EIsdF9Q"
}'
```

**Response:**

```json
{
    "data": {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4MWY2YjA4OC1jMGZlLTQ1ZGMtYjM3ZC04YTc0OWViMjg2ZDIiLCJjbGllbnRfaWQiOiI4MWY2YjA4OC1jMGZlLTQ1ZGMtYjM3ZC04YTc0OWViMjg2ZDIiLCJpZGVudGlmaWVyIjoiZmFobWktYXJtYW5kIiwianRpIjoiMWQwMDM0MjItNzA0Ny00NmZhLTliM2MtYjgzMmI4NzdiZGQxIiwiZXhwIjoxNzUzOTkzMjAxfQ.uk0bE3qUVzslJqinMbwV5MMgpRu4fOC2oTnGcDW3628",
        "token_type": "Bearer",
        "expires_at": "2025-07-31T20:20:01.970582",
        "is_revoked": false,
        "user_id": "81f6b088-c0fe-45dc-b37d-8a749eb286d2",
        "client_id": "7e285918-9174-4cdb-8c8e-8359d48562a7"
    },
    "meta": null
}
```

Use the returned `token` as a Bearer token for authenticated requests.

⚠️ **Important**: you can reuse the bearer token until it's expired. Please reuse them if you can to prevent security risks due the previous token will not expired when you generate new bearer token.

#### 3. Get User Details

Retrieves detailed information about the authenticated user, including their integrations.

**Endpoint:** `GET /users/me`

**Headers:**

* `x-api-key`: Your GL Connectors API client key
* `Authorization`: Bearer {your-bearer-token}

**Example Request:**

```bash
curl --location 'https://connectors.gdplabs.id/users/me' \
--header 'x-api-key: {your-api-key}' \
--header 'Authorization: Bearer {your-bearer-token}'
```

**Response:**

```json
{
    "data": {
        "id": "81f6b088-c0fe-45dc-b37d-8a749eb286d2",
        "client_id": "7e285918-9174-4cdb-8c8e-8359d48562a7",
        "identifier": "fahmi-armand",
        "secret": null,
        "secret_preview": "sk-user-...ciC9nBMY",
        "is_active": true,
        "integrations": [
            {
                "id": "dcce2388-2b0c-4abf-adc0-f671ddfd1866",
                "client_id": "7e285918-9174-4cdb-8c8e-8359d48562a7",
                "user_id": "81f6b088-c0fe-45dc-b37d-8a749eb286d2",
                "connector": "google",
                "user_identifier": "fahmi.a.r.harahap@gdplabs.id"
            },
            {
                "id": "73e44eeb-d459-47b6-8171-ef8e5feb080b",
                "client_id": "7e285918-9174-4cdb-8c8e-8359d48562a7",
                "user_id": "81f6b088-c0fe-45dc-b37d-8a749eb286d2",
                "connector": "github",
                "user_identifier": "fahmi-armand"
            }
        ]
    },
    "meta": null
}
```

This endpoint returns the user's profile information and all active third-party integrations.

#### 4. Create Third-Party Integration

Initiates integration with third-party services like Google, GitHub, etc.

**Endpoint:** `POST /connectors/{third_party}/integrations`

**Available Third-Party Services:**

* `google` - Google services integration
* `github` - GitHub integration
* And more...

**Headers:**

* `x-api-key`: Your GL Connectors API client key
* `Content-Type`: application/json
* `Authorization`: Bearer {your-bearer-token}

**Request Body:**

```json
{
    "callback_url": "https://your-app.com/callback"
}
```

**Example Request (Google Integration):**

```bash
curl --location 'https://connectors.gdplabs.id/connectors/google/integrations' \
--header 'x-api-key: {your-api-key}' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer {your-bearer-token}' \
--data '{
    "callback_url":"https://google.com"
}'
```

The `callback_url` is where users will be redirected after successfully authenticating with the third-party service.

#### 5. Remove Third-Party Integration

Removes an existing integration with a third-party service.

**Endpoint:** `DELETE /connectors/{third_party}/integrations/{user_identifier}`

**Available Third-Party Services:**

* `google` - Google services integration
* `github` - GitHub integration
* And more...

**Headers:**

* `x-api-key`: Your GL Connectors API client key
* `Content-Type`: application/json
* `Authorization`: Bearer {your-bearer-token}

You can check all `user identifier` across all integrations via [`GET /clients/user`](user-management-api.md#id-3.-get-user-details)

**Example Request (Remove Github Integration):**

```bash
curl --location \
--request DELETE 'https://connectors.gdplabs.id/connectors/github/integrations/my-username' \
--header 'x-api-key: {your-api-key}' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer {your-bearer-token}'
```

This will remove the integration for the specified third-party service and account.

***

### Error Handling

All endpoints return standard HTTP status codes:

* `200` - Success
* `400` - Bad Request (invalid parameters)
* `401` - Unauthorized (invalid API key or Bearer token)
* `404` - Not Found
* `500` - Internal Server Error

Error responses will include details about what went wrong:

```json
{
    "error": {
        "message": "Description of the error",
        "code": "ERROR_CODE"
    }
}
```

***

### Best Practices

1. **Secure Secret Storage**: Always store user secrets securely and never log them
2. **Token Management**: Monitor token expiration times and refresh as needed
3. **Error Handling**: Implement proper error handling for all API calls

***

### Additional Resources

For more comprehensive API documentation and additional endpoints, visit our complete API documentation at [Broken link](/broken/pages/uwTaBgSFKYEUe0Ykv0ci "mention")

This interactive documentation provides detailed information about all available endpoints, request/response schemas, and testing capabilities.
