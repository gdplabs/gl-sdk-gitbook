## POST /utils/regenerate_presigned_url

**Summary:** Regenerate presigned URL for any storage object

Generate a new presigned URL for any object in storage by providing its path in request body

**Authentication:** API key (`X-API-Key` header)

**Parameters:** None

### Request Body

_Required._

- `application/json` — PresignedUrlRequest

### Responses

| Status | Description                            | Schema                                    |
| ------ | -------------------------------------- | ----------------------------------------- |
| `200`  | Presigned URL regenerated successfully | `application/json` — PresignedUrlResponse |
| `400`  | Invalid object path                    | `application/json` — ErrorResponse        |
| `422`  | Validation Error                       | `application/json` — HTTPValidationError  |
| `500`  | Internal server error                  | `application/json` — ErrorResponse        |
