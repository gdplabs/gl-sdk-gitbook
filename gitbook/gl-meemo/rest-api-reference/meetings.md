# Meetings

Access meeting data including details, transcripts, summaries, participants, and recordings.

### 1. List Meetings

Returns a paginated list of meetings for your accessible organization(s). Meetings are ordered by start time descending (newest first).

**Request**

```http
GET /api/v1/external/meeting/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Query Parameters**

| Parameter          | Type    | Description                                                                                                                         |
| ------------------ | ------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `organization_id`  | integer | **Optional**. Filter to a specific organization. If not provided, returns meetings from all accessible organizations.               |
| `title`            | string  | **Optional**. Filter by title (case-insensitive, contains match).                                                                   |
| `participants`     | string  | **Optional**. Filter by participant user IDs (comma-separated, matches ANY).                                                        |
| `created_after`    | date    | **Optional**. Filter meetings created on or after this date (YYYY-MM-DD).                                                           |
| `created_before`   | date    | **Optional**. Filter meetings created on or before this date (YYYY-MM-DD).                                                          |
| `summary_complete` | boolean | **Optional**. Filter by summary completion status (`true`/`false`). If not provided, returns both complete and incomplete meetings. |
| `from_calendar`    | boolean | **Optional**. Filter by meeting source. `true`=calendar integration, `false`=manually created.                                      |
| `page`             | integer | **Optional**. Page number for pagination.                                                                                           |
| `size`             | integer | **Optional**. Number of results per page (default: 10).                                                                             |

**Response**

```json
{
  "count": 45,
  "next": "https://your-meemo-instance.com/api/v1/external/meeting/?page=2",
  "previous": null,
  "results": [
    {
      "id": 123,
      "title": "Daily Standup",
      "start_time": "2024-01-15T09:00:00Z",
      "end_time": "2024-01-15T09:30:00Z",
      "created_at": "2024-01-15T08:55:00Z",
      "status": "past",
      "summary_complete": true,
      "host_name": "John Doe",
      "calendar_event": null
    }
  ]
}
```

***

### 2. Get Meeting Details

Returns detailed information about a specific meeting. The meeting must belong to one of your accessible organizations.

**Request**

```http
GET /api/v1/external/meeting/{id}/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Response**

```json
{
  "id": 123,
  "title": "Q1 Planning Meeting",
  "start_time": "2024-01-15T09:00:00Z",
  "end_time": "2024-01-15T11:00:00Z",
  "created_at": "2024-01-14T16:30:00Z",
  "location": "Conference Room A",
  "status": "past",
  "summary_complete": true,
  "host": {
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com"
  },
  "language": "id",
  "keywords": ["planning", "q1", "budget"],
  "participant_count": 5,
  "duration_seconds": 7200.0,
  "num_cluster": 5,
  "calendar_event": {
    "event_id": "abc123xyz789",
    "summary": "Q1 Planning Meeting",
    "organizer_email": "admin@example.com",
    "attendees": [
      {
        "email": "john.doe@example.com",
        "display_name": "John Doe",
        "response_status": "accepted"
      }
    ],
    "meeting_link": "https://meet.google.com/xyz-abcd-efg",
    "start_time": "2024-01-15T09:00:00Z",
    "end_time": "2024-01-15T11:00:00Z"
  }
}
```

***

### 3. Create Meeting

Create a new meeting. Supports creating standard meetings, bot-joined meetings (via URL), or file imports (via URL).

**Request**

```http
POST /api/v1/external/meeting/
Content-Type: application/json
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Body Parameters**

| Parameter         | Type           | Description                                                                                                                                                                                                                |
| ----------------- | -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `organization_id` | integer        | **Required**. The ID of the organization where the meeting will be created.                                                                                                                                                |
| `title`           | string         | **Optional**. Meeting title. Defaults to "New External Meeting" or similar if not provided.                                                                                                                                |
| `start_time`      | datetime       | **Optional**. Meeting start time (ISO 8601). Defaults to current time.                                                                                                                                                     |
| `user_token`      | string         | **Optional**. A User Personal Token to attribute the meeting creation to a specific user. If omitted, the meeting is created by the organization admin. **Note**: The user must be a member of the specified organization. |
| `topic_id`        | integer        | **Optional**. The ID of the topic to associate with the meeting (determines language/context). See List Topics.                                                                                                            |
| `participants`    | array\[string] | **Optional**. List of participant email addresses to invite/associate with the meeting.                                                                                                                                    |
| `bot_meeting_url` | string         | **Optional**. URL of the meeting for the bot to join (e.g., Google Meet, Zoom). **Mutually exclusive with `file_url`.**                                                                                                    |
| `file_url`        | string         | **Optional**. URL of an audio/video file to import and transcribe. **Mutually exclusive with `bot_meeting_url`.**                                                                                                          |
| `bot_join_at`     | datetime       | **Optional**. Schedule the bot to join at a future time (ISO 8601). If omitted or `null`, the bot joins immediately when `bot_meeting_url` is provided. Must be in the future.                                             |
| `speaker_count`   | integer        | **Optional**. Estimated number of speakers (hints the diarization engine). Min: 1.                                                                                                                                         |
| `calendar_event`  | object         | **Optional**. Calendar event metadata to store as a snapshot. See Calendar Event Object below.                                                                                                                             |

#### Calendar Event Object

When providing `calendar_event`, the following fields are supported:

| Field             | Type     | Description                                                                                  |
| ----------------- | -------- | -------------------------------------------------------------------------------------------- |
| `event_id`        | string   | **Required**. The unique ID of the event from the external calendar (e.g., Google Event ID). |
| `summary`         | string   | **Optional**. The summary/title of the calendar event.                                       |
| `organizer_email` | string   | **Optional**. Email of the event organizer.                                                  |
| `attendees`       | array    | **Optional**. List of attendee objects.                                                      |
| `meeting_link`    | string   | **Optional**. Video conference link (Google Meet, Zoom, etc.).                               |
| `start_time`      | datetime | **Optional**. Event start time (ISO 8601).                                                   |
| `end_time`        | datetime | **Optional**. Event end time (ISO 8601).                                                     |

**Example: Create Bot Meeting with Calendar Snapshot**

```json
{
  "title": "Project Sync",
  "organization_id": 1,
  "bot_meeting_url": "https://meet.google.com/abc-defg-hij",
  "calendar_event": {
    "event_id": "google_event_id_123",
    "summary": "Project Sync",
    "organizer_email": "pm@example.com",
    "attendees": [
      {"email": "dev1@example.com", "response_status": "accepted"},
      {"email": "dev2@example.com", "response_status": "needsAction"}
    ],
    "meeting_link": "https://meet.google.com/abc-defg-hij",
    "start_time": "2024-02-10T10:00:00Z",
    "end_time": "2024-02-10T11:00:00Z"
  }
}
```

**Example: Create Bot Meeting with Personal Token**

```json
{
  "title": "Project Sync with External Team",
  "organization_id": 1,
  "start_time": "2024-02-10T10:00:00Z",
  "user_token": "pt_abc123...",
  "topic_id": 5,
  "participants": ["alice@example.com", "bob@external.com"],
  "bot_meeting_url": "https://meet.google.com/abc-defg-hij"
}
```

**Example: Scheduled Bot Meeting**

```json
{
  "title": "Scheduled Standup",
  "organization_id": 1,
  "bot_meeting_url": "https://meet.google.com/abc-defg-hij",
  "bot_join_at": "2024-02-10T10:00:00Z"
}
```

> The bot will automatically join the meeting at the scheduled time. A periodic task checks every minute and dispatches bots up to 2 minutes before the scheduled time.

**Example: Import File**

```json
{
  "title": "Uploaded Interview",
  "organization_id": 1,
  "file_url": "https://example.com/recordings/interview-2024.mp3",
  "speaker_count": 2
}
```

**Response**

Returns the created Meeting Details object.

```json
{
  "id": 124,
  "title": "Project Sync with External Team",
  "start_time": "2024-02-10T10:00:00Z",
  "status": "scheduled",
  ...
}
```

***

### 4. Get Meeting Transcript

Returns the meeting transcript as a JSON array of segments, ordered by start time.

**Request**

```http
GET /api/v1/external/meeting/{id}/transcript/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Response**

```json
{
  "meeting_id": 123,
  "title": "Q1 Planning Meeting",
  "total_segments": 45,
  "transcripts": [
    {
      "speaker": "John Doe",
      "text": "Selamat pagi semua. Mari kita mulai rapat hari ini.",
      "start_time": 0.0,
      "end_time": 4.5
    }
  ]
}
```

***

### 5. Get Meeting Summary

Returns the meeting summary, notes, and keywords.

**Request**

```http
GET /api/v1/external/meeting/{id}/summary/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Response**

```json
{
  "meeting_id": 123,
  "title": "Q1 Planning Meeting",
  "summary": "## Meeting Purpose\nThe meeting discussed...",
  "notes": "Additional meeting notes here",
  "keywords": ["planning", "q1", "budget"]
}
```

> **Note**: The `summary` field primarily returns a Markdown-formatted string.

***

### 6. Get Meeting Participants

Returns the list of meeting participants with their details.

**Request**

```http
GET /api/v1/external/meeting/{id}/participants/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Response**

```json
{
  "meeting_id": 123,
  "title": "Q1 Planning Meeting",
  "total_participants": 5,
  "participants": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john.doe@example.com",
      "position": "Director",
      "department": "Engineering"
    }
  ]
}
```

***

### 7. Get Meeting Recording

Returns the meeting recording URL, duration, and format.

**Request**

```http
GET /api/v1/external/meeting/{id}/recording/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Response**

```json
{
  "meeting_id": 123,
  "title": "Q1 Planning Meeting",
  "recording_url": "/media/meeting_records/123/recording.mp3",
  "duration": 7200.0,
  "format": "mp3"
}
```

***

### 8. List Topics

Returns a list of available topics (meeting contexts/languages) for your accessible organizations.

**Request**

```http
GET /api/v1/external/topics/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Query Parameters**

| Parameter         | Type    | Description                                                       |
| ----------------- | ------- | ----------------------------------------------------------------- |
| `organization_id` | integer | **Optional**. Filter topics available to a specific organization. |

**Response**

```json
[
  {
    "id": 1,
    "name": "General",
    "alias": "General Meeting",
    "language": "id"
  },
  {
    "id": 2,
    "name": "Engineering",
    "alias": "Tech Sync",
    "language": "en"
  }
]
```
