# Token Generation

Once a user has been created and issued an **identifier** and **secret**, they can generate an authentication token to access the GL Smart Search API. This token is required for all authorized API requests and serves as proof of identity.

**✅ Generate a Token**

To generate a token, send a `POST` request to the `/token` endpoint. The endpoint supports two authentication modes for backward compatibility.

**Endpoint:**

```
POST /token
```

**Option 1: With Client API Key (Recommended)**

**Headers:**

```
x-api-key: <CLIENT_API_KEY>
```

**Request Body (Form Data):**

```json
{
  "identifier": "glchat_user",
  "secret": "user_secret_here",
  "created_by_username": "admin_user"
}
```

* `x-api-key` (header, optional): The client API key for authentication. If not provided, falls back to `CLIENT_API_KEY` environment variable
* `identifier`: The unique identifier for the user (provided during creation)
* `secret`: The secret value assigned to the user
* `created_by_username` (optional): Username of the admin who is manually refreshing this token. Used for tracking token metadata. Leave empty if the user is creating their own token

**Option 2: Without API Key (Backward Compatible)**

For backward compatibility with existing integrations, you can omit the `x-api-key` header. The system will automatically use the `CLIENT_API_KEY` from environment variables.

**Request Body (Form Data):**

```json
{
  "identifier": "glchat_user",
  "secret": "user_secret_here",
  "created_by_username": ""
}
```

**Note:** The `created_by_username` field is optional. Leave it empty for user self-service token creation.

**Sample Response:**

```json
{
    "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_at": "2019-08-24T14:15:22Z",
    "is_revoked": false,
    "user_id": "a169451c-8525-4352-b8ca-070dd449a1a5",
    "client_id": "5b3fa7ba-57d3-4017-a65b-d57dcd2db643"
}
```

* `id`: Unique identifier for this token
* `token`: A valid JWT authentication token
* `token_type`: Token type (always "bearer")
* `expires_at`: Token expiration timestamp
* `is_revoked`: Whether the token has been revoked
* `user_id`: ID of the user who owns this token
* `client_id`: ID of the client associated with this user

***

**🔐 Using the Token**

Include the token in the `Authorization` header of every API request that requires authentication:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Example Request:**

```bash
curl -X GET "https://api.example.com/search" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

***

**👤 Get Authenticated User**

To fetch the current authenticated user's information (based on the token), send a `GET` request to the `/token` endpoint with the token included in the `Authorization` header.

**Endpoint:**

```
GET /token
```

**Headers:**

```
Authorization: Bearer <token>
```

**Sample Response:**

```json
{
  "user_id": "a169451c-8525-4352-b8ca-070dd449a1a5",
  "username": "glchat_user",
  "scopes": ["read:all"]
}
```

* `user_id`: The unique identifier of the authenticated user
* `username`: The user's identifier
* `scopes`: List of permissions/scopes granted to this user

This endpoint helps confirm the identity of the token holder and is useful for session validation or debugging purposes.

***

**🔒 Token Verification Process**

When you use a token to access protected endpoints, the system performs the following verification steps:

1. **JWT Decoding**: The token is decoded and validated using the secret key
2. **Expiration Check**: Ensures the token has not expired
3. **Database Validation**: Verifies the token exists in the database and has not been revoked
4. **User Retrieval**: Fetches the associated user information
5. **Scope Validation**: Checks if the user has the required permissions for the requested operation

This multi-layer verification ensures secure and reliable authentication for all API requests.
