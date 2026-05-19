# Speech-to-Text

## Speech-to-Text (STT) API

### Overview

The Speech-to-Text API provides endpoints for converting audio to text transcriptions. It supports both synchronous (real-time) and asynchronous (batch) processing modes.

**Base URL:** `https://asr-api.stg.prosa.ai/v2/speech/stt`

**Authentication:** All endpoints require the `x-api-key` header with your API key.

***

### List Models (GET /stt/models)

List all available ASR (Automatic Speech Recognition) models.

**Authentication:** API key required

**Request:**

```bash
curl -X GET 'https://asr-api.stg.prosa.ai/v2/speech/stt/models' \
  -H 'x-api-key: your-api-key'
```

**Response (200 OK):**

```json
[
  {
    "name": "stt-general",
    "label": "ASR General",
    "language": "Bahasa Indonesia",
    "domain": "general",
    "acoustic": "recording",
    "channels": 1,
    "samplerate": 16000
  }
]
```

**Response Fields:**

| Field        | Type    | Description                                        |
| ------------ | ------- | -------------------------------------------------- |
| `name`       | string  | Model identifier (use this in transcribe requests) |
| `label`      | string  | Human-readable model name                          |
| `language`   | string  | Supported language                                 |
| `domain`     | string  | Model specialization domain                        |
| `acoustic`   | string  | Optimal audio source type                          |
| `channels`   | integer | Optimal number of audio channels                   |
| `samplerate` | integer | Optimal sample rate in Hz                          |

**Error Responses:**

* **401 Unauthorized:** Invalid or missing API key

```json
{
  "status": "unauthorized",
  "message": "Invalid API key"
}
```

***

### Transcribe Audio (POST /stt)

Submit an audio file for transcription. Supports both synchronous and asynchronous modes.

**Input (data vs URI):** For small amounts of audio (e.g. below one minute; the threshold may vary by configuration), include base64-encoded audio in the request body. For larger audio, provide a publicly accessible URI to the audio file instead.

**Currently supported URI:**

* HTTP URL that returns the audio file, e.g. `https://storage.example.com/file.wav`
* Google Drive: URL to a Google Drive audio file or a Google Drive file ID, e.g. `googledrive://file_id`

**Processing behavior:**

* **Short ASR requests:** The job is processed on the fly and the client is expected to wait for the result in the response. If the job cannot be completed within the allotted time, it is queued and only the job ID is returned.
* **Long ASR requests:** The job is always queued. Poll for results using the job endpoints, or set up a webhook endpoint to receive notifications. See Receiving Webhook.

**Authentication:** API key required

**Request:**

```bash
curl -X POST 'https://asr-api.stg.prosa.ai/v2/speech/stt' \
  -H 'x-api-key: your-api-key' \
  -H 'Content-Type: application/json' \
  -d '{
    "config": {
      "engine": "stt-general",
      "wait": true,
      "speaker_count": 1,
      "include_filler": false,
      "auto_punctuation": true
    },
    "request": {
      "data": "<base64-encoded-audio>",
      "label": "My audio file"
    }
  }'
```

**Request Body - Config:**

| Field                     | Type    | Required | Default | Description                        |
| ------------------------- | ------- | -------- | ------- | ---------------------------------- |
| `engine`                  | string  | ✅ Yes    | -       | ASR model name (from list models)  |
| `wait`                    | boolean | No       | `false` | `true` for sync, `false` for async |
| `speaker_count`           | integer | No       | `1`     | Expected number of speakers        |
| `include_filler`          | boolean | No       | `false` | Include filler words (um, uh)      |
| `include_partial_results` | boolean | No       | `false` | Include partial transcriptions     |
| `auto_punctuation`        | boolean | No       | `false` | Auto-add punctuation               |
| `enable_spoken_numerals`  | boolean | No       | `false` | Convert "one" to "1"               |
| `enable_speech_insights`  | boolean | No       | `false` | Enable speech analytics            |
| `enable_voice_insights`   | boolean | No       | `false` | Enable voice analytics             |

**Request Body - Request:**

| Field         | Type    | Required    | Description                                 |
| ------------- | ------- | ----------- | ------------------------------------------- |
| `data`        | string  | Conditional | Base64-encoded audio (required if no `uri`) |
| `uri`         | string  | Conditional | URL to audio file (required if no `data`)   |
| `label`       | string  | No          | Optional label for the job                  |
| `duration`    | number  | No          | Audio duration in seconds                   |
| `mime_type`   | string  | No          | Audio MIME type                             |
| `sample_rate` | integer | No          | Audio sample rate                           |
| `channels`    | integer | No          | Number of audio channels                    |

> ⚠️ **Important:** Either `data` or `uri` must be provided, but not both. URI-based requests are only allowed for asynchronous requests (`wait: false`).

**Response (200 OK) - Synchronous:**

```json
{
  "job_id": "2fec34e1-efb1-46f7-a743-1cb35b64550d",
  "status": "complete",
  "created_at": "2024-01-15T10:00:00Z",
  "modified_at": "2024-01-15T10:00:05Z",
  "request": {
    "label": "My audio file"
  },
  "result": {
    "data": [
      {
        "transcript": "Hasil akhir dari pekerjaan ini cukup memuaskan",
        "final": true,
        "time_start": 0,
        "time_end": 3.6,
        "channel": 0
      }
    ]
  },
  "job_config": {
    "model": "stt-general",
    "wait": true
  }
}
```

**Response (200 OK) - Asynchronous:**

```json
{
  "job_id": "2fec34e1-efb1-46f7-a743-1cb35b64550d",
  "status": "queued",
  "created_at": "2024-01-15T10:00:00Z"
}
```

**Response Fields:**

| Field                      | Type              | Description                          |
| -------------------------- | ----------------- | ------------------------------------ |
| `job_id`                   | string (UUID)     | Unique job identifier                |
| `status`                   | string            | Job status (see status values below) |
| `created_at`               | string (datetime) | Job creation timestamp               |
| `modified_at`              | string (datetime) | Last modification timestamp          |
| `result.data`              | array             | Array of transcription segments      |
| `result.data[].transcript` | string            | Transcribed text                     |
| `result.data[].final`      | boolean           | Whether segment is complete          |
| `result.data[].time_start` | number            | Start time in seconds                |
| `result.data[].time_end`   | number            | End time in seconds                  |
| `result.data[].channel`    | integer           | Audio channel number                 |

**Error Responses:**

* **400 Bad Request:** Invalid audio data

```json
{
  "status": "asr_request_invalid_base64",
  "message": "Invalid base64 encoded audio data"
}
```

* **400 Bad Request:** Model not found

```json
{
  "status": "asr_model_not_found",
  "message": "ASR model 'invalid-model' not found"
}
```

* **400 Bad Request:** No audio provided

```json
{
  "status": "no_audio_provided",
  "message": "Either 'data' or 'uri' must be provided"
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

### List Jobs (GET /stt)

Retrieve all STT jobs with optional filtering.

**Authentication:** API key required

**Request:**

```bash
curl -X GET 'https://asr-api.stg.prosa.ai/v2/speech/stt?page=1&per_page=10' \
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
| `query_text`  | string        | No       | Search in transcription text   |

**Response (200 OK):**

```json
{
  "pagination": {
    "page": 1,
    "per_page": 10,
    "page_count": 5
  },
  "length": 50,
  "data": [
    {
      "job_id": "2fec34e1-efb1-46f7-a743-1cb35b64550d",
      "status": "complete",
      "created_at": "2024-01-15T10:00:00Z",
      "modified_at": "2024-01-15T10:00:05Z",
      "request": {
        "label": "My audio file"
      },
      "job_config": {
        "model": "stt-general",
        "wait": true
      }
    }
  ]
}
```

***

### Get Job (GET /stt/{job\_id})

Retrieve a specific STT job with full results.

**Authentication:** API key required

**Request:**

```bash
curl -X GET 'https://asr-api.stg.prosa.ai/v2/speech/stt/2fec34e1-efb1-46f7-a743-1cb35b64550d' \
  -H 'x-api-key: your-api-key'
```

**Path Parameters:**

| Parameter | Type          | Required | Description    |
| --------- | ------------- | -------- | -------------- |
| `job_id`  | string (UUID) | ✅ Yes    | Job identifier |

**Response (200 OK):**

```json
{
  "job_id": "2fec34e1-efb1-46f7-a743-1cb35b64550d",
  "status": "complete",
  "created_at": "2024-01-15T10:00:00Z",
  "modified_at": "2024-01-15T10:00:05Z",
  "request": {
    "label": "My audio file"
  },
  "result": {
    "data": [
      {
        "transcript": "Hasil akhir dari pekerjaan ini cukup memuaskan",
        "final": true,
        "time_start": 0,
        "time_end": 3.6,
        "channel": 0
      }
    ]
  },
  "job_config": {
    "model": "stt-general",
    "wait": true
  }
}
```

**Error Responses:**

* **404 Not Found:** Job not found

```json
{
  "status": "job_not_found",
  "message": "Job '2fec34e1-efb1-46f7-a743-1cb35b64550d' not found"
}
```

***

### Get Job Status (GET /stt/{job\_id}/status)

Retrieve only the status of a job (lightweight endpoint).

**Authentication:** API key required

**Request:**

```bash
curl -X GET 'https://asr-api.stg.prosa.ai/v2/speech/stt/2fec34e1-efb1-46f7-a743-1cb35b64550d/status' \
  -H 'x-api-key: your-api-key'
```

**Path Parameters:**

| Parameter | Type          | Required | Description    |
| --------- | ------------- | -------- | -------------- |
| `job_id`  | string (UUID) | ✅ Yes    | Job identifier |

**Response (200 OK):**

```json
{
  "job_id": "2fec34e1-efb1-46f7-a743-1cb35b64550d",
  "status": "in_progress",
  "created_at": "2024-01-15T10:00:00Z",
  "modified_at": "2024-01-15T10:00:10Z",
  "progress": {
    "total": 50,
    "details": {
      "transfer": 100,
      "transcribe": 50
    }
  }
}
```

**Response Fields:**

| Field                         | Type          | Description                 |
| ----------------------------- | ------------- | --------------------------- |
| `job_id`                      | string (UUID) | Job identifier              |
| `status`                      | string        | Current job status          |
| `progress.total`              | number        | Overall progress percentage |
| `progress.details.transfer`   | number        | Transfer progress %         |
| `progress.details.transcribe` | number        | Transcription progress %    |

***

### Archive Job (DELETE /stt/{job\_id})

Soft delete a job. Archived jobs are retained for audit purposes.

**Authentication:** API key required

**Request:**

```bash
curl -X DELETE 'https://asr-api.stg.prosa.ai/v2/speech/stt/2fec34e1-efb1-46f7-a743-1cb35b64550d' \
  -H 'x-api-key: your-api-key'
```

**Path Parameters:**

| Parameter | Type          | Required | Description    |
| --------- | ------------- | -------- | -------------- |
| `job_id`  | string (UUID) | ✅ Yes    | Job identifier |

**Response (200 OK):**

```json
{
  "job_id": "2fec34e1-efb1-46f7-a743-1cb35b64550d",
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

| Format | Extensions                                                                |
| ------ | ------------------------------------------------------------------------- |
| Audio  | `.wav`, `.mp3`, `.m4a`, `.ogg`, `.weba`, `.webm`, `.flac`, `.gsm`, `.wma` |
| Video  | `.mp4`, `.webm`, `.mov`, `.avi`, `.wmv`, `.mpg`                           |

***

### Limits

| Limit                      | Value           |
| -------------------------- | --------------- |
| Max audio duration (sync)  | 60 seconds      |
| Max audio duration (async) | 4 hours         |
| Max request size           | 10 MB           |
| Max concurrent jobs        | Contact support |

***

### Webhooks

Instead of polling for job status, you can receive real-time notifications when jobs complete or fail.

See [Webhooks](webhooks.md) for:

* Creating webhook endpoints
* Event types (`stt.job.completed`, `stt.job.failed`)
* Verifying webhook signatures
* Managing deliveries
