# User Management

The User Management page lets you view existing users and register new users under a fixed client (as configured in the environment variables).

### 🔍 Viewing Users

You can view all registered users at:

📍 Go to the \[Users List]\(/admin/admin-cpdb-user/list)

From this page, you can:

* See all users and their associated metadata
* Click into a user to view details such as identifier and creation timestamp

<figure><img src="../../../../.gitbook/assets/User List.png" alt=""><figcaption><p>User List</p></figcaption></figure>

<figure><img src="../../../../.gitbook/assets/User Details.png" alt=""><figcaption><p>User Details</p></figcaption></figure>

***

### ➕ Creating a New User

To create a user:

1. Go to the \[Users List]\(/admin/admin-cpdb-user/list)
2. Click **"New User"**
3. Fill in the following field:
   * **Identifier**: A unique identifier for the user (e.g., `glchat_user`, `catapa_user`)
4. Submit the form to register the user

📌 **Note:**\
Users created via the AdminCP are automatically linked to a pre-configured client using the `CLIENT_API_KEY` environment variable. This differs from the API endpoint (`POST /user`), which accepts any valid client API key via the `x-api-key` header, allowing users to be created for different clients.

<figure><img src="../../../../.gitbook/assets/User Create.png" alt=""><figcaption><p>Create new User</p></figcaption></figure>

***

### 📋 Retrieving User List via API

You can programmatically retrieve a paginated list of users for a specific client using the API endpoint.

**Endpoint:**

```
GET /users
```

**Headers:**

```
x-api-key: <CLIENT_API_KEY>
```

**Query Parameters:**

* `page` (optional): Page number (1-indexed). Defaults to 1
* `page_size` (optional): Number of users per page. Defaults to 20

**Example Request:**

```bash
curl --location 'http://127.0.0.1:8003/users?page=1&page_size=20' \
--header 'x-api-key: <CLIENT_API_KEY>'
```

**Sample Response:**

```json
{
  "users": [
    {
      "user_id": "a169451c-8525-4352-b8ca-070dd449a1a5",
      "username": "glchat_user",
      "token_value": "eyJ****xyz",
      "expired_at": "2026-05-01T10:30:00Z",
      "created_by_username": "admin_user"
    },
    {
      "user_id": "b279562d-9636-5463-cffc-64dccbba7g19",
      "username": "catapa_user",
      "token_value": "abc****nop",
      "expired_at": "2026-04-15T08:20:00Z",
      "created_by_username": null
    }
  ],
  "total": 2,
  "page": 1,
  "page_size": 20
}
```

**Response Fields:**

* `users`: Array of user objects with their latest token metadata
  * `user_id`: Unique identifier of the user
  * `username`: User's identifier
  * `token_value`: Obfuscated token value (first 3 and last 3 characters visible)
  * `expired_at`: Token expiration timestamp (null if no token exists)
  * `created_by_username`: Username of admin who refreshed the token (null if user-created or no token)
* `total`: Total number of users for the client
* `page`: Current page number
* `page_size`: Number of users per page

**Use Cases:**

* Monitoring user token status across your client
* Building admin dashboards to track token expiration
* Auditing which tokens were manually refreshed by administrators
* Implementing pagination for large user bases

📌 **Note:**\
This endpoint uses database-level pagination for optimal performance, even with large numbers of users. Token metadata is retrieved in batch for all users on the current page to minimize database queries.
