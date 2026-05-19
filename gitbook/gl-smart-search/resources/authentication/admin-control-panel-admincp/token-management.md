# Token Management

The Token Management page allows you to view and generate authentication tokens tied to specific users. These tokens are used for accessing protected API endpoints.

### 🔍 Viewing Tokens

You can see all issued tokens at:

📍 Go to the \[Tokens List]\(/admin/admin-cpdb-token/list)

From this page, you can:

* View a list of all tokens
* Inspect token details such as the associated user, creation date, and token string (if visible)

<figure><img src="../../../../.gitbook/assets/Token List.png" alt=""><figcaption><p>Token List</p></figcaption></figure>

<figure><img src="../../../../.gitbook/assets/Token Details.png" alt=""><figcaption><p>Token Details</p></figcaption></figure>

***

### ➕ Creating a New Token

To create a token:

1. Go to the \[Tokens List]\(/admin/admin-cpdb-token/list)
2. Click **"New Token"**
3. Fill in the following fields:
   * **User Identifier**: The identifier of the user the token should belong to
   * **Secret**: The secret associated with that user (used for token generation)
4. Submit the form to generate and store the token

The newly created token will now be visible in the list and available for immediate use with the API.

📌 **Note:**\
Tokens created via the AdminCP use the `CLIENT_API_KEY` environment variable for backward compatibility. This is the same behavior as calling the API endpoint (`POST /token`) without providing the `x-api-key` header. For more details on token creation options, see the [Token Generation](../authentication/token-generation.md) documentation.

<figure><img src="../../../../.gitbook/assets/Token Create.png" alt=""><figcaption><p>Create new Token</p></figcaption></figure>
