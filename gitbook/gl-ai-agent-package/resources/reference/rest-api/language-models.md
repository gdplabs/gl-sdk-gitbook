## GET /language-models/

**Summary:** Get All Language Models

Get all language models.

Args:
lm_service (LanguageModelService, optional): The service to handle language model
operations. Defaults to Depends(get_language_model_service).
api_key (str, optional): The API key for authentication.
Defaults to Depends(verify_api_key).

Returns:
LanguageModelListResponse: A response object containing a list of all
language models.

**Authentication:** API key (`X-API-Key` header)

**Parameters:** None

**Request Body:** None

### Responses

| Status | Description         | Schema                                                           |
| ------ | ------------------- | ---------------------------------------------------------------- |
| `200`  | Successful Response | `application/json` — BaseResponse_list_LanguageModelResponse\_\_ |

## POST /language-models/

**Summary:** Create Language Model

Create a new language model.

Args:
lm_data (LanguageModelCreate): The data for creating the new language model.
lm_service (LanguageModelService, optional): The service to handle language model
operations. Defaults to Depends(get_language_model_service).
api_key (str, optional): The API key for authentication.
Defaults to Depends(verify_master_api_key).

Returns:
LanguageModelDetailResponse: A response object containing the newly
created language model's details.

Raises:
StandardHTTPException: If a language model with the same provider and name already exists.

**Authentication:** API key (`X-API-Key` header)

**Parameters:** None

### Request Body

_Required._

- `application/json` — LanguageModelCreate

### Responses

| Status | Description         | Schema                                                    |
| ------ | ------------------- | --------------------------------------------------------- |
| `201`  | Successful Response | `application/json` — BaseResponse_LanguageModelResponse\_ |
| `422`  | Validation Error    | `application/json` — HTTPValidationError                  |

## GET /language-models/{lm_id}

**Summary:** Get Language Model

Get a specific language model by its ID.

Args:
lm_id (UUID): The unique identifier of the language model to retrieve.
lm_service (LanguageModelService, optional): The service to handle language model
operations. Defaults to Depends(get_language_model_service).
api_key (str, optional): The API key for authentication.
Defaults to Depends(verify_api_key).

Returns:
LanguageModelDetailResponse: A response object containing the details
of the requested language model.

Raises:
StandardHTTPException: If no language model is found with the specified ID.

**Authentication:** API key (`X-API-Key` header)

### Path Parameters

| Name    | Type          | Required | Description |
| ------- | ------------- | -------- | ----------- |
| `lm_id` | string (uuid) | Yes      | —           |

**Request Body:** None

### Responses

| Status | Description         | Schema                                                    |
| ------ | ------------------- | --------------------------------------------------------- |
| `200`  | Successful Response | `application/json` — BaseResponse_LanguageModelResponse\_ |
| `422`  | Validation Error    | `application/json` — HTTPValidationError                  |

## PUT /language-models/{lm_id}

**Summary:** Update Language Model

Update a specific language model.

Args:
lm_id (UUID): The unique identifier of the language model to update.
lm_data (LanguageModelUpdate): The new data for updating the language
model.
lm_service (LanguageModelService, optional): The service to handle language model
operations. Defaults to Depends(get_language_model_service).
api_key (str, optional): The API key for authentication.
Defaults to Depends(verify_master_api_key).

Returns:
LanguageModelDetailResponse: A response object containing the updated
language model's details.

Raises:
StandardHTTPException: If no language model is found with the specified ID,
or if the update would violate the unique constraint.

**Authentication:** API key (`X-API-Key` header)

### Path Parameters

| Name    | Type          | Required | Description |
| ------- | ------------- | -------- | ----------- |
| `lm_id` | string (uuid) | Yes      | —           |

### Request Body

_Required._

- `application/json` — LanguageModelUpdate

### Responses

| Status | Description         | Schema                                                    |
| ------ | ------------------- | --------------------------------------------------------- |
| `200`  | Successful Response | `application/json` — BaseResponse_LanguageModelResponse\_ |
| `422`  | Validation Error    | `application/json` — HTTPValidationError                  |

## DELETE /language-models/{lm_id}

**Summary:** Delete Language Model

Delete a specific language model.

Args:
lm_id (UUID): The unique identifier of the language model to delete.
lm_service (LanguageModelService, optional): The service to handle language model
operations. Defaults to Depends(get_language_model_service).
api_key (str, optional): The API key for authentication.
Defaults to Depends(verify_master_api_key).

Returns:
LanguageModelDeleteResponse: A response object confirming the deletion.

Raises:
StandardHTTPException: If no language model is found with the specified ID.

**Authentication:** API key (`X-API-Key` header)

### Path Parameters

| Name    | Type          | Required | Description |
| ------- | ------------- | -------- | ----------- |
| `lm_id` | string (uuid) | Yes      | —           |

**Request Body:** None

### Responses

| Status | Description         | Schema                                                 |
| ------ | ------------------- | ------------------------------------------------------ |
| `200`  | Successful Response | `application/json` — BaseResponse_dict_str\_\_UUID\_\_ |
| `422`  | Validation Error    | `application/json` — HTTPValidationError               |
