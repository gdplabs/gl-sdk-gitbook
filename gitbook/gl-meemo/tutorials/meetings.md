# Meetings

Access meeting data including details, transcripts, summaries, participants, recordings, and topics through `client.meetings`.

### 1. List Meetings

Returns a paginated list of meetings for your accessible organization(s), ordered by start time descending.

```python
list_meetings(
    organization_id: int | None = None,
    title: str | None = None,
    participants: str | None = None,
    created_after: str | None = None,
    created_before: str | None = None,
    summary_complete: bool | None = None,
    from_calendar: bool | None = None,
    page: int | None = None,
    size: int | None = None,
    extra_headers: dict | None = None,
) -> MeetingListResponse
```

**Parameters**

| Parameter          | Type   | Description                                                    |
| ------------------ | ------ | -------------------------------------------------------------- |
| `organization_id`  | `int`  | Filter to a specific organization.                             |
| `title`            | `str`  | Filter by title (case-insensitive, contains match).            |
| `participants`     | `str`  | Filter by participant user IDs (comma-separated, matches ANY). |
| `created_after`    | `str`  | Filter meetings created on or after this date (`YYYY-MM-DD`).  |
| `created_before`   | `str`  | Filter meetings created on or before this date (`YYYY-MM-DD`). |
| `summary_complete` | `bool` | Filter by summary completion status.                           |
| `from_calendar`    | `bool` | `True` = calendar integration, `False` = manually created.     |
| `page`             | `int`  | Page number for pagination.                                    |
| `size`             | `int`  | Number of results per page (default: 10).                      |
| `extra_headers`    | `dict` | Additional HTTP headers for this request.                      |

All parameters are optional.

**Sync Example**

```python
from meemo import MeemoClient

client = MeemoClient(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    base_url="https://your-meemo-instance.com",
)

# List all meetings
response = client.meetings.list_meetings()
print(f"Total meetings: {response.count}")
for meeting in response.results:
    print(f"  [{meeting.id}] {meeting.title} - {meeting.status}")

# Filter by organization and date range
response = client.meetings.list_meetings(
    organization_id=1,
    created_after="2024-01-01",
    created_before="2024-01-31",
    summary_complete=True,
)
```

**Async Example**

```python
from meemo import AsyncMeemoClient

client = AsyncMeemoClient(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    base_url="https://your-meemo-instance.com",
)

response = await client.meetings.list_meetings(organization_id=1)
for meeting in response.results:
    print(f"  [{meeting.id}] {meeting.title}")
```

**Returns** `MeetingListResponse` with fields: `count`, `next`, `previous`, `results` (list of `MeetingListItem`).

***

### 2. Get Meeting Details

Returns detailed information about a specific meeting.

```python
get_meeting(
    meeting_id: int,
    extra_headers: dict | None = None,
) -> MeetingDetail
```

**Parameters**

| Parameter    | Type  | Description                   |
| ------------ | ----- | ----------------------------- |
| `meeting_id` | `int` | **Required**. The meeting ID. |

**Sync Example**

```python
meeting = client.meetings.get_meeting(meeting_id=123)
print(f"Title: {meeting.title}")
print(f"Duration: {meeting.duration_seconds}s")
print(f"Participants: {meeting.participant_count}")
print(f"Host: {meeting.host.name} ({meeting.host.email})")
```

**Async Example**

```python
meeting = await client.meetings.get_meeting(meeting_id=123)
print(f"Title: {meeting.title}")
```

**Returns** `MeetingDetail` with fields: `id`, `title`, `start_time`, `end_time`, `created_at`, `location`, `status`, `summary_complete`, `host` (`MeetingHost`), `language`, `keywords`, `participant_count`, `duration_seconds`, `num_cluster`, `calendar_event` (`CalendarEvent | None`).

***

### 3. Create Meeting

Create a new meeting. Supports standard meetings, bot-joined meetings (via URL), or file imports (via URL).

```python
create_meeting(
    organization_id: int,
    title: str,
    start_time: str | None = None,
    user_token: str | None = None,
    topic_id: int | None = None,
    participants: list[str] | None = None,
    bot_meeting_url: str | None = None,
    bot_join_at: str | None = None,
    file_url: str | None = None,
    speaker_count: int | None = None,
    calendar_event: CreateMeetingCalendarEvent | None = None,
    extra_headers: dict | None = None,
) -> MeetingDetail
```

**Parameters**

| Parameter         | Type                         | Description                                                                                                                                                      |
| ----------------- | ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `organization_id` | `int`                        | **Required**. Organization ID where the meeting will be created. Must be > 0.                                                                                    |
| `title`           | `str`                        | **Required**. Meeting title.                                                                                                                                     |
| `start_time`      | `str`                        | Meeting start time (ISO 8601).                                                                                                                                   |
| `user_token`      | `str`                        | User Personal Token to attribute the meeting to a specific user.                                                                                                 |
| `topic_id`        | `int`                        | Topic ID to associate with the meeting (determines language/context).                                                                                            |
| `participants`    | `list[str]`                  | List of participant email addresses.                                                                                                                             |
| `bot_meeting_url` | `str`                        | URL of the meeting for the bot to join. **Mutually exclusive with `file_url`**.                                                                                  |
| `file_url`        | `str`                        | URL of an audio/video file to import. **Mutually exclusive with `bot_meeting_url`**.                                                                             |
| `bot_join_at`     | `str`                        | Schedule the bot to join at a future time (ISO 8601). If omitted or `None`, the bot joins immediately when `bot_meeting_url` is provided. Must be in the future. |
| `speaker_count`   | `int`                        | Estimated number of speakers (min: 1).                                                                                                                           |
| `calendar_event`  | `CreateMeetingCalendarEvent` | Calendar event metadata. Also accepts a `dict` (auto-coerced by Pydantic). See Calendar Event Object.                                                            |

#### Calendar Event Object

| Field             | Type         | Description                                                               |
| ----------------- | ------------ | ------------------------------------------------------------------------- |
| `event_id`        | `str`        | **Required**. Unique event ID from the external calendar.                 |
| `summary`         | `str`        | Event summary/title.                                                      |
| `organizer_email` | `str`        | Email of the event organizer.                                             |
| `attendees`       | `list[dict]` | List of attendee objects with `email`, `display_name`, `response_status`. |
| `meeting_link`    | `str`        | Video conference link.                                                    |
| `start_time`      | `str`        | Event start time (ISO 8601).                                              |
| `end_time`        | `str`        | Event end time (ISO 8601).                                                |

**Sync Example — Bot Meeting with Calendar Snapshot**

```python
meeting = client.meetings.create_meeting(
    organization_id=1,
    title="Project Sync",
    bot_meeting_url="https://meet.google.com/abc-defg-hij",
    calendar_event={
        "event_id": "google_event_id_123",
        "summary": "Project Sync",
        "organizer_email": "pm@example.com",
        "attendees": [
            {"email": "dev1@example.com", "response_status": "accepted"},
            {"email": "dev2@example.com", "response_status": "needsAction"},
        ],
        "meeting_link": "https://meet.google.com/abc-defg-hij",
        "start_time": "2024-02-10T10:00:00Z",
        "end_time": "2024-02-10T11:00:00Z",
    },
)
print(f"Created meeting: {meeting.id}")
```

**Sync Example — Scheduled Bot Meeting**

```python
meeting = client.meetings.create_meeting(
    organization_id=1,
    title="Scheduled Standup",
    bot_meeting_url="https://meet.google.com/abc-defg-hij",
    bot_join_at="2024-02-10T10:00:00Z",
)
print(f"Scheduled meeting: {meeting.id}")
```

> The bot will automatically join the meeting at the scheduled time. A periodic task checks every minute and dispatches bots up to 2 minutes before the scheduled time.

**Sync Example — File Import**

```python
meeting = client.meetings.create_meeting(
    organization_id=1,
    title="Uploaded Interview",
    file_url="https://example.com/recordings/interview-2024.mp3",
    speaker_count=2,
)
```

**Async Example**

```python
meeting = await client.meetings.create_meeting(
    organization_id=1,
    title="Async Bot Meeting",
    bot_meeting_url="https://meet.google.com/abc-defg-hij",
    user_token="pt_abc123...",
    topic_id=5,
    participants=["alice@example.com", "bob@external.com"],
)
print(f"Created meeting: {meeting.id}")
```

**Returns** `MeetingDetail`.

***

### 4. Get Meeting Transcript

Returns the meeting transcript as a list of timed segments.

```python
get_transcript(
    meeting_id: int,
    extra_headers: dict | None = None,
) -> TranscriptResponse
```

**Parameters**

| Parameter    | Type  | Description                   |
| ------------ | ----- | ----------------------------- |
| `meeting_id` | `int` | **Required**. The meeting ID. |

**Sync Example**

```python
transcript = client.meetings.get_transcript(meeting_id=123)
print(f"Total segments: {transcript.total_segments}")
for segment in transcript.transcripts:
    print(f"  [{segment.start_time:.1f}s] {segment.speaker}: {segment.text}")
```

**Async Example**

```python
transcript = await client.meetings.get_transcript(meeting_id=123)
for segment in transcript.transcripts:
    print(f"  [{segment.start_time:.1f}s] {segment.speaker}: {segment.text}")
```

**Returns** `TranscriptResponse` with fields: `meeting_id`, `title`, `total_segments`, `transcripts` (list of `TranscriptSegment`).

***

### 5. Get Meeting Summary

Returns the meeting summary, notes, and keywords.

```python
get_summary(
    meeting_id: int,
    extra_headers: dict | None = None,
) -> SummaryResponse
```

**Parameters**

| Parameter    | Type  | Description                   |
| ------------ | ----- | ----------------------------- |
| `meeting_id` | `int` | **Required**. The meeting ID. |

**Sync Example**

```python
summary = client.meetings.get_summary(meeting_id=123)
print(f"Summary: {summary.summary}")
print(f"Keywords: {summary.keywords}")
```

**Async Example**

```python
summary = await client.meetings.get_summary(meeting_id=123)
print(f"Summary: {summary.summary}")
```

**Returns** `SummaryResponse` with fields: `meeting_id`, `title`, `summary` (`str | dict | None`), `notes`, `keywords`.

> **Note**: The `summary` field typically contains a Markdown-formatted string but may be a `dict` for legacy meetings.

***

### 6. Get Meeting Participants

Returns the list of meeting participants with their details.

```python
get_participants(
    meeting_id: int,
    extra_headers: dict | None = None,
) -> ParticipantsResponse
```

**Parameters**

| Parameter    | Type  | Description                   |
| ------------ | ----- | ----------------------------- |
| `meeting_id` | `int` | **Required**. The meeting ID. |

**Sync Example**

```python
result = client.meetings.get_participants(meeting_id=123)
print(f"Total participants: {result.total_participants}")
for p in result.participants:
    print(f"  {p.name} ({p.email}) - {p.position}, {p.department}")
```

**Async Example**

```python
result = await client.meetings.get_participants(meeting_id=123)
for p in result.participants:
    print(f"  {p.name} ({p.email})")
```

**Returns** `ParticipantsResponse` with fields: `meeting_id`, `title`, `total_participants`, `participants` (list of `Participant`).

***

### 7. Get Meeting Recording

Returns the meeting recording URL, duration, and format.

```python
get_recording(
    meeting_id: int,
    extra_headers: dict | None = None,
) -> RecordingResponse
```

**Parameters**

| Parameter    | Type  | Description                   |
| ------------ | ----- | ----------------------------- |
| `meeting_id` | `int` | **Required**. The meeting ID. |

**Sync Example**

```python
recording = client.meetings.get_recording(meeting_id=123)
print(f"URL: {recording.recording_url}")
print(f"Duration: {recording.duration}s ({recording.format})")
```

**Async Example**

```python
recording = await client.meetings.get_recording(meeting_id=123)
print(f"URL: {recording.recording_url}")
```

**Returns** `RecordingResponse` with fields: `meeting_id`, `title`, `recording_url`, `duration`, `format`.

***

### 8. List Topics

Returns a list of available topics (meeting contexts/languages) for your accessible organizations.

```python
list_topics(
    organization_id: int | None = None,
    extra_headers: dict | None = None,
) -> list[Topic]
```

**Parameters**

| Parameter         | Type  | Description                               |
| ----------------- | ----- | ----------------------------------------- |
| `organization_id` | `int` | Filter topics to a specific organization. |

**Sync Example**

```python
topics = client.meetings.list_topics(organization_id=1)
for topic in topics:
    print(f"  [{topic.id}] {topic.name} ({topic.language})")
```

**Async Example**

```python
topics = await client.meetings.list_topics(organization_id=1)
for topic in topics:
    print(f"  [{topic.id}] {topic.name} ({topic.language})")
```

**Returns** `list[Topic]`. Each `Topic` has fields: `id`, `name`, `alias`, `language`.

***

### Error Responses

| Status | Condition                                                                                                                         |
| ------ | --------------------------------------------------------------------------------------------------------------------------------- |
| `400`  | Invalid parameters (e.g., `organization_id` not an integer, `speaker_count` < 1, both `bot_meeting_url` and `file_url` provided). |
| `401`  | Missing or invalid access token.                                                                                                  |
| `403`  | Application does not have access to the requested organization or meeting.                                                        |
| `404`  | Meeting not found.                                                                                                                |
