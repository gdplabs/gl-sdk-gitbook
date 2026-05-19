# Text-to-Speech

## Text-to-Speech (TTS) API Contract

### Overview

The Text-to-Speech API provides endpoints for converting text to speech audio. It supports multiple voices, audio formats, and customization options like pitch and tempo.

**Base URL:** `https://tts-api.stg.prosa.ai/v2/speech/tts`

**Authentication:** All endpoints require the `x-api-key` header with your API key.

***

### List Models (GET /tts/models)

List all available TTS (Text-to-Speech) voices/models.

**Authentication:** API key required

**Request:**

```bash
curl -X GET 'https://tts-api.stg.prosa.ai/v2/speech/tts/models' \
  -H 'x-api-key: your-api-key'
```

**Response (200 OK):**

```json
[
  {
    "name": "tts-dimas-formal",
    "label": "TTS Dimas Formal",
    "language": "Bahasa Indonesia",
    "domain": "formal",
    "voice": "Dimas",
    "gender": "male",
    "channels": 1,
    "samplerate": 48000
  },
  {
    "name": "tts-sinta-casual",
    "label": "TTS Sinta Casual",
    "language": "Bahasa Indonesia",
    "domain": "casual",
    "voice": "Sinta",
    "gender": "female",
    "channels": 1,
    "samplerate": 48000
  }
]
```

**Response Fields:**

| Field        | Type    | Description                                        |
| ------------ | ------- | -------------------------------------------------- |
| `name`       | string  | Model identifier (use this in synthesize requests) |
| `label`      | string  | Human-readable model name                          |
| `language`   | string  | Supported language                                 |
| `domain`     | string  | Voice style (formal, casual, etc.)                 |
| `voice`      | string  | Voice character name                               |
| `gender`     | string  | Voice gender (male/female)                         |
| `channels`   | integer | Number of audio channels                           |
| `samplerate` | integer | Audio sample rate in Hz                            |

**Error Responses:**

* **401 Unauthorized:** Invalid or missing API key

```json
{
  "status": "unauthorized",
  "message": "Invalid API key"
}
```

***

### Synthesize Speech (POST /tts)

Convert text to speech audio. Supports both synchronous and asynchronous modes.

**Authentication:** API key required

**Request:**

```bash
curl -X POST 'https://tts-api.stg.prosa.ai/v2/speech/tts' \
  -H 'x-api-key: your-api-key' \
  -H 'Content-Type: application/json' \
  -d '{
    "config": {
      "model": "tts-dimas-formal",
      "wait": true,
      "audio_format": "mp3",
      "pitch": 0.0,
      "tempo": 1.0
    },
    "request": {
      "text": "Selamat pagi, apa kabar?",
      "label": "Greeting audio"
    }
  }'
```

**Request Body - Config:**

| Field          | Type    | Required | Default | Description                         |
| -------------- | ------- | -------- | ------- | ----------------------------------- |
| `model`        | string  | ✅ Yes    | -       | TTS model name (from list models)   |
| `wait`         | boolean | No       | `false` | `true` for sync, `false` for async  |
| `audio_format` | string  | No       | `opus`  | Output format: `opus`, `mp3`, `wav` |
| `pitch`        | number  | No       | `0.0`   | Pitch adjustment (-1.0 to 1.0)      |
| `tempo`        | number  | No       | `1.0`   | Speed adjustment (0.5 to 2.0)       |
| `sample_rate`  | integer | No       | -       | Output sample rate                  |

**Request Body - Request:**

| Field   | Type   | Required    | Description                                      |
| ------- | ------ | ----------- | ------------------------------------------------ |
| `text`  | string | Conditional | Plain text to synthesize (required if no `ssml`) |
| `ssml`  | string | Conditional | SSML markup (required if no `text`)              |
| `label` | string | No          | Optional label for the job                       |

> ⚠️ **Important:** Either `text` or `ssml` must be provided, but not both.

**Response (200 OK) - Synchronous with Base64:**

```json
{
  "job_id": "3abc45d2-1234-5678-abcd-ef1234567890",
  "status": "complete",
  "created_at": "2024-01-15T10:00:00Z",
  "modified_at": "2024-01-15T10:00:02Z",
  "request": {
    "text": "Selamat pagi, apa kabar?",
    "label": "Greeting audio"
  },
  "result": {
    "data": "<base64-encoded-audio>",
    "format": "mp3",
    "duration": 2.5,
    "samplerate": 48000,
    "channels": 1
  },
  "job_config": {
    "model": "tts-dimas-formal",
    "wait": true,
    "audio_format": "mp3"
  }
}
```

**Response (200 OK) - Asynchronous:**

```json
{
  "job_id": "3abc45d2-1234-5678-abcd-ef1234567890",
  "status": "queued",
  "created_at": "2024-01-15T10:00:00Z"
}
```

**Response Fields:**

| Field               | Type              | Description                          |
| ------------------- | ----------------- | ------------------------------------ |
| `job_id`            | string (UUID)     | Unique job identifier                |
| `status`            | string            | Job status (see status values below) |
| `created_at`        | string (datetime) | Job creation timestamp               |
| `modified_at`       | string (datetime) | Last modification timestamp          |
| `result.data`       | string            | Base64-encoded audio data            |
| `result.path`       | string            | Signed URL (if `as_signed_url=true`) |
| `result.format`     | string            | Audio format                         |
| `result.duration`   | number            | Audio duration in seconds            |
| `result.samplerate` | integer           | Sample rate in Hz                    |
| `result.channels`   | integer           | Number of audio channels             |

**Error Responses:**

* **400 Bad Request:** No text provided

```json
{
  "status": "no_text_provided",
  "message": "Either 'text' or 'ssml' must be provided"
}
```

* **400 Bad Request:** Model not found

```json
{
  "status": "tts_model_not_found",
  "message": "TTS model 'invalid-model' not found"
}
```

* **401 Unauthorized:** Invalid API key

```json
{
  "status": "unauthorized",
  "message": "Invalid API key"
}
```

***

### Synthesize with Signed URL (POST /tts?as\_signed\_url=true)

Get the synthesized audio as a downloadable URL instead of base64 data.

**Authentication:** API key required

**Request:**

```bash
curl -X POST 'https://tts-api.stg.prosa.ai/v2/speech/tts?as_signed_url=true' \
  -H 'x-api-key: your-api-key' \
  -H 'Content-Type: application/json' \
  -d '{
    "config": {
      "model": "tts-dimas-formal",
      "wait": true
    },
    "request": {
      "text": "Selamat pagi, apa kabar?"
    }
  }'
```

**Query Parameters:**

| Parameter       | Type    | Required | Description                       |
| --------------- | ------- | -------- | --------------------------------- |
| `as_signed_url` | boolean | No       | Return URL instead of base64 data |

**Response (200 OK):**

```json
{
  "job_id": "3abc45d2-1234-5678-abcd-ef1234567890",
  "status": "complete",
  "result": {
    "path": "https://storage.prosa.ai/tts/signed/abc123.mp3?expires=1705312800",
    "format": "mp3",
    "duration": 2.5
  }
}
```

> **Note:** Signed URLs are valid for a limited time. Download the audio promptly or regenerate the URL.

***

### List Jobs (GET /tts)

Retrieve all TTS jobs with optional filtering.

**Authentication:** API key required

**Request:**

```bash
curl -X GET 'https://tts-api.stg.prosa.ai/v2/speech/tts?page=1&per_page=10' \
  -H 'x-api-key: your-api-key'
```

**Query Parameters:**

| Parameter     | Type          | Required | Description                    |
| ------------- | ------------- | -------- | ------------------------------ |
| `page`        | integer       | No       | Page number (default: 1)       |
| `per_page`    | integer       | No       | Items per page (default: 10)   |
| `from_date`   | string (date) | No       | Filter from date (YYYY-MM-DD)  |
| `until_date`  | string (date) | No       | Filter until date (YYYY-MM-DD) |
| `sort_by`     | string        | No       | Sort field (`time` or `label`) |
| `sort_ascend` | boolean       | No       | Sort ascending                 |
| `query_text`  | string        | No       | Search in synthesis text       |

**Response (200 OK):**

```json
{
  "pagination": {
    "page": 1,
    "per_page": 10,
    "page_count": 3
  },
  "length": 25,
  "data": [
    {
      "job_id": "3abc45d2-1234-5678-abcd-ef1234567890",
      "status": "complete",
      "created_at": "2024-01-15T10:00:00Z",
      "modified_at": "2024-01-15T10:00:02Z",
      "request": {
        "text": "Selamat pagi",
        "label": "Greeting"
      },
      "job_config": {
        "model": "tts-dimas-formal",
        "wait": true
      }
    }
  ]
}
```

***

### Count Jobs (GET /tts/count)

Get the total count of TTS jobs matching filter criteria.

**Authentication:** API key required

**Request:**

```bash
curl -X GET 'https://tts-api.stg.prosa.ai/v2/speech/tts/count?from_date=2024-01-01' \
  -H 'x-api-key: your-api-key'
```

**Query Parameters:**

| Parameter    | Type          | Required | Description                    |
| ------------ | ------------- | -------- | ------------------------------ |
| `from_date`  | string (date) | No       | Filter from date (YYYY-MM-DD)  |
| `until_date` | string (date) | No       | Filter until date (YYYY-MM-DD) |
| `query_text` | string        | No       | Search in synthesis text       |

**Response (200 OK):**

```json
42
```

***

### Get Job (GET /tts/{job\_id})

Retrieve a specific TTS job with full results.

**Authentication:** API key required

**Request:**

```bash
curl -X GET 'https://tts-api.stg.prosa.ai/v2/speech/tts/3abc45d2-1234-5678-abcd-ef1234567890' \
  -H 'x-api-key: your-api-key'
```

**Path Parameters:**

| Parameter | Type          | Required | Description    |
| --------- | ------------- | -------- | -------------- |
| `job_id`  | string (UUID) | ✅ Yes    | Job identifier |

**Query Parameters:**

| Parameter       | Type    | Required | Description                       |
| --------------- | ------- | -------- | --------------------------------- |
| `as_signed_url` | boolean | No       | Return URL instead of base64 data |

**Response (200 OK):**

```json
{
  "job_id": "3abc45d2-1234-5678-abcd-ef1234567890",
  "status": "complete",
  "created_at": "2024-01-15T10:00:00Z",
  "modified_at": "2024-01-15T10:00:02Z",
  "request": {
    "text": "Selamat pagi, apa kabar?",
    "label": "Greeting audio"
  },
  "result": {
    "data": "<base64-encoded-audio>",
    "format": "mp3",
    "duration": 2.5,
    "samplerate": 48000,
    "channels": 1
  },
  "job_config": {
    "model": "tts-dimas-formal",
    "wait": true
  }
}
```

**Error Responses:**

* **404 Not Found:** Job not found

```json
{
  "status": "job_not_found",
  "message": "Job '3abc45d2-1234-5678-abcd-ef1234567890' not found"
}
```

***

### Get Job Status (GET /tts/{job\_id}/status)

Retrieve only the status of a job (lightweight endpoint).

**Authentication:** API key required

**Request:**

```bash
curl -X GET 'https://tts-api.stg.prosa.ai/v2/speech/tts/3abc45d2-1234-5678-abcd-ef1234567890/status' \
  -H 'x-api-key: your-api-key'
```

**Path Parameters:**

| Parameter | Type          | Required | Description    |
| --------- | ------------- | -------- | -------------- |
| `job_id`  | string (UUID) | ✅ Yes    | Job identifier |

**Response (200 OK):**

```json
{
  "job_id": "3abc45d2-1234-5678-abcd-ef1234567890",
  "status": "complete",
  "created_at": "2024-01-15T10:00:00Z",
  "modified_at": "2024-01-15T10:00:02Z"
}
```

***

### Archive Job (DELETE /tts/{job\_id})

Soft delete a job. Archived jobs are retained for audit purposes.

**Authentication:** API key required

**Request:**

```bash
curl -X DELETE 'https://tts-api.stg.prosa.ai/v2/speech/tts/3abc45d2-1234-5678-abcd-ef1234567890' \
  -H 'x-api-key: your-api-key'
```

**Path Parameters:**

| Parameter | Type          | Required | Description    |
| --------- | ------------- | -------- | -------------- |
| `job_id`  | string (UUID) | ✅ Yes    | Job identifier |

**Response (200 OK):**

```json
{
  "job_id": "3abc45d2-1234-5678-abcd-ef1234567890",
  "status": "archived",
  "created_at": "2024-01-15T10:00:00Z",
  "modified_at": "2024-01-15T10:05:00Z"
}
```

**Error Responses:**

* **403 Forbidden:** Job is in progress

```json
{
  "status": "job_cancellation_error",
  "message": "Cannot archive job while in progress"
}
```

* **404 Not Found:** Job not found or already archived

```json
{
  "status": "job_not_found",
  "message": "Job not found or already archived"
}
```

> **Note:** This performs a soft delete - the job is marked as archived but data is retained for audit purposes.

***

### Job Status Values

| Status        | Description                    |
| ------------- | ------------------------------ |
| `created`     | Job has been created           |
| `queued`      | Job is waiting to be processed |
| `in_progress` | Job is being processed         |
| `complete`    | Job completed successfully     |
| `failed`      | Job failed due to an error     |
| `cancelled`   | Job was cancelled              |

***

### Supported Audio Formats

| Format | Description               | Use Case           |
| ------ | ------------------------- | ------------------ |
| `opus` | Default, high compression | Web streaming      |
| `mp3`  | Wide compatibility        | General use        |
| `wav`  | Uncompressed              | Professional audio |

***

### SSML Support

TTS supports Speech Synthesis Markup Language (SSML) for advanced control:

```bash
curl -X POST 'https://tts-api.stg.prosa.ai/v2/speech/tts' \
  -H 'x-api-key: your-api-key' \
  -H 'Content-Type: application/json' \
  -d '{
    "config": {
      "model": "tts-dimas-formal",
      "wait": true
    },
    "request": {
      "ssml": "<speak>Selamat <break time=\"500ms\"/> pagi!</speak>"
    }
  }'
```

**Common SSML Tags:**

| Tag          | Description        | Example                              |
| ------------ | ------------------ | ------------------------------------ |
| `<speak>`    | Root element       | `<speak>Hello</speak>`               |
| `<break>`    | Insert pause       | `<break time="500ms"/>`              |
| `<emphasis>` | Add emphasis       | `<emphasis>important</emphasis>`     |
| `<prosody>`  | Control pitch/rate | `<prosody rate="slow">...</prosody>` |

***

### Limits

| Limit               | Value             |
| ------------------- | ----------------- |
| Max text length     | 5,000 characters  |
| Max SSML length     | 10,000 characters |
| Max audio duration  | 10 minutes        |
| Max concurrent jobs | Contact support   |

***

### Voice Customization

#### Pitch Adjustment

| Value  | Effect                 |
| ------ | ---------------------- |
| `-1.0` | Lowest pitch           |
| `0.0`  | Normal pitch (default) |
| `1.0`  | Highest pitch          |

#### Tempo Adjustment

| Value | Effect                 |
| ----- | ---------------------- |
| `0.5` | Half speed (slowest)   |
| `1.0` | Normal speed (default) |
| `2.0` | Double speed (fastest) |

***

### Webhooks

Instead of polling for job status, you can receive real-time notifications when jobs complete or fail.

See [Webhooks](webhooks.md) for:

* Creating webhook endpoints
* Event types (`tts.job.completed`, `tts.job.failed`)
* Verifying webhook signatures
* Managing deliveries
