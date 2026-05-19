# Client and User Creation

In this system, both **clients** and **users** are created exclusively by the **Master** user. This ensures strict control over who can interact with the GL Smart Search API and under what context.

**✅ Creating a Client**

To create a new **client**, the Master user sends a `POST` request to the `/client` endpoint.

**Endpoint:**

```
POST /client
```

**Request Body:**

```json
{
  "username": "<MASTER_USERNAME>",
  "password": "<MASTER_PASSWORD>",
  "client_name": "example_company"
}
```

* `username`: Master username (from environment variable `MASTER_USERNAME`)
* `password`: Master password (from environment variable `MASTER_PASSWORD`)
* `client_name`: Desired name of the new client (e.g., company or application name)

**Sample Response:**

```json
{
  "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
  "name": "string",
  "api_key": "string",
  "is_active": true,
  "created_at": "2019-08-24T14:15:22Z"
}
```

***

**✅ Creating a User**

Users are tied to a **specific client** via the client's API key. To create a new user, you need the **client API key** obtained from the client creation step.

To create a new **user**, send a `POST` request to the `/user` endpoint with the client's API key.

**Endpoint:**

```
POST /user
```

**Headers:**

```
x-api-key: <CLIENT_API_KEY>
```

**Request Body (Form Data):**

```json
{
  "identifier": "glchat_user"
}
```

* `x-api-key` (header): The API key of the client to which this user will belong (obtained from client creation response)
* `identifier`: Unique string that will identify the user and be used for token generation

**Sample Response:**

```json
{
  "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
  "identifier": "glchat_user",
  "secret_preview": "string",
  "is_active": true,
  "client_id": "5b3fa7ba-57d3-4017-a65b-d57dcd2db643",
  "secret": "string"
}
```

**ℹ️ Important Notes:**

* Users are automatically associated with the client whose API key is provided in the `x-api-key` header
* The `x-api-key` header is **required** for user creation
* Each user receives a unique `secret` in the response, which must be securely stored for token generation
* The `secret` is only returned once during user creation and cannot be retrieved later
