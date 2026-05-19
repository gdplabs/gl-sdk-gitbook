---
icon: flag-checkered
---

# Getting Started

## Meemo SDK

A Python library for interacting with the Meemo External API, providing access to meeting data including details, transcripts, summaries, participants, and recordings.

### Getting Started

**Hello World:**

```python
from meemo_sdk import MeemoClient

client = MeemoClient(
    client_id="your-client-id",
    client_secret="your-client-secret",
    base_url="https://your-meemo-instance.com",
)

meetings = client.meetings.list_meetings()
for meeting in meetings.results:
    print(f"{meeting.id}: {meeting.title} ({meeting.status})")
```

For configuration, authentication, full Meetings API, and error handling, see [Cookbook](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/meemo-sdk/examples).
