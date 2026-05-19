The accounts API exposes a single public endpoint that allows new tenants to
provision themselves. All other account lifecycle operations are reserved for
platform operators and are intentionally omitted here.

## POST /accounts/

**Summary:** Create new account

Create a new account with a unique name and generate an API key. This is a public endpoint that does not require authentication.

**Authentication:** None

**Parameters:** None

### Request Body

_Required._

- `application/json` — AccountCreateRequest

### Responses

| Status | Description                      | Schema                                     |
| ------ | -------------------------------- | ------------------------------------------ |
| `201`  | Account created successfully     | `application/json` — AccountCreateResponse |
| `400`  | Invalid input data               | —                                          |
| `409`  | Account with name already exists | —                                          |
| `422`  | Validation Error                 | `application/json` — HTTPValidationError   |
| `500`  | Internal server error            | —                                          |
