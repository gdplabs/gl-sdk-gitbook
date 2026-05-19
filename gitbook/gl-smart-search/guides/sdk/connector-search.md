# Connector Search

The **Connector** capability lets GL Smart Search access third-party data sources such as **Google Drive**, **Google Mail**, **Google Calendar**, **GitHub**, and **Microsoft 365** (**Outlook** mail, **OneDrive** files, and **Microsoft Calendar**).\
It enables searching, connecting, and disconnecting these integrations from your application through a single, consistent interface.

***

### Setup

Define the following environment variables:

```bash
SMARTSEARCH_BASE_URL=https://search.glair.ai/
SMARTSEARCH_TOKEN=<your-smartsearch-auth-token>
gl_token=<optional-gl-token>
```

Then in your Python environment:

```python
import os
from dotenv import load_dotenv

from smart_search_sdk.connector.client import ConnectorClient

load_dotenv()

client = ConnectorClient(base_url=os.getenv("SMARTSEARCH_BASE_URL"))
await client.authenticate(token=os.getenv("SMARTSEARCH_TOKEN"))
```

***

### GL Connectors Token Authentication

Connector access requires a **GL Connectors token** for secure authorization.

You have **two options**:

1. **Use the GL Connectors Token provided by GL Smart Search**
   * This token is handled automatically based on the authentication used in GL Smart Search.
   * You can simply omit the `gl_token` environment variable.
2. **Bring your own GL Connectors Token**
   * If you generate and pass your own token, it **must be created using the same registered Client GL Connectors API Key** that GL Smart Search recognizes for that user.
   * If the key differs, GL Smart Search will reject connector authentication.

> ⚠️ **Important:**
>
> * The only registered Client GL Connectors API Key currently recognized by GL Smart Search is **GLChat**.
> * The GL Connectors API Key used in GL Smart Search is the same as the one registered for GLChat.
> * Therefore, if you bring your own token, ensure it was generated under the GLChat GL Connectors API Key; otherwise connector calls will fail.

Example:

```python
gl_token = os.getenv("GL_CONNECTORS_USER_TOKEN", "")  # Leave empty to use Smart Search’s token
```

***

### 1.  Connector Search

Performs a search across a specific connector (for example Google Drive, Gmail, Calendar, GitHub, or Microsoft Outlook / OneDrive / Microsoft Calendar).

```python
import json
import os
from smart_search_sdk.connector.models import ConnectorRequest, AppName

request = ConnectorRequest(query="List all my upcoming meetings today")

result = await client.search_connector(
    app_name=AppName.GOOGLE_CALENDAR,
    gl_token=os.getenv("GL_CONNECTORS_USER_TOKEN", ""),
    request=request,
)

print(json.dumps(result, indent=4))
```

| Parameter    | Type      | Description                                                             |
| ------------ | --------- | ----------------------------------------------------------------------- |
| `query`      | `str`     | The search query text.                                                  |
| `app_name`   | `AppName` | Target connector (for example `AppName.GOOGLE_MAIL`, `AppName.MICROSOFT_OUTLOOK`). |
| `gl_token` | `str`     | Optional; omit to use Smart Search’s managed token.                     |

***

### 2.  Connector Connect

Starts a connection (OAuth or similar) to a third-party app.

```python
import json
import os
from smart_search_sdk.connector.models import ConnectorConnectRequest, AppName

request = ConnectorConnectRequest(
    callback_url="https://search.glair.ai/health-check"
)

result = await client.connect_connector(
    app_name=AppName.GOOGLE_CALENDAR,
    gl_token=os.getenv("GL_CONNECTORS_USER_TOKEN", ""),
    request=request,
)

print(json.dumps(result, indent=4))
```

| Parameter      | Type      | Description                                |
| -------------- | --------- | ------------------------------------------ |
| `callback_url` | `str`     | URL to receive the authorization callback. |
| `app_name`     | `AppName` | The connector to connect.                  |
| `gl_token`   | `str`     | Optional; token for authorization.         |

***

### 3.  Connector Disconnect

Disconnects a connector previously linked to GL Smart Search.

```python
import json
import os
from smart_search_sdk.connector.models import AppName

result = await client.disconnect_connector(
    app_name=AppName.GOOGLE_CALENDAR,
    gl_token=os.getenv("GL_CONNECTORS_USER_TOKEN", "")
)

print(json.dumps(result, indent=4))
```

| Parameter    | Type      | Description                                    |
| ------------ | --------- | ---------------------------------------------- |
| `app_name`   | `AppName` | The connector to disconnect.                   |
| `gl_token` | `str`     | Optional; token for authenticated disconnects. |

***

### Full Example

```python
import asyncio
import json
import os
from dotenv import load_dotenv

from smart_search_sdk.connector.client import ConnectorClient
from smart_search_sdk.connector.models import (
    ConnectorRequest,
    ConnectorConnectRequest,
    AppName,
)

load_dotenv()

async def main():
    client = ConnectorClient(base_url=os.getenv("SMARTSEARCH_BASE_URL"))
    await client.authenticate(token=os.getenv("SMARTSEARCH_TOKEN"))
    gl_token = os.getenv("GL_CONNECTORS_USER_TOKEN", "")

    # Search
    request = ConnectorRequest(query="List all my upcoming meetings today")
    result = await client.search_connector(
        app_name=AppName.GOOGLE_CALENDAR,
        gl_token=gl_token,
        request=request,
    )
    print("=== Connector Search ===")
    print(json.dumps(result, indent=4))

    # Connect
    connect_request = ConnectorConnectRequest(
        callback_url="https://search.glair.ai/health-check"
    )
    result = await client.connect_connector(
        app_name=AppName.GOOGLE_CALENDAR,
        gl_token=gl_token,
        request=connect_request,
    )
    print("\n=== Connector Connect ===")
    print(json.dumps(result, indent=4))

    # Disconnect
    result = await client.disconnect_connector(
        app_name=AppName.GOOGLE_CALENDAR,
        gl_token=gl_token
    )
    print("\n=== Connector Disconnect ===")
    print(json.dumps(result, indent=4))

asyncio.run(main())
```

***

### Supported Connectors

| App | Enum | Description |
| --- | --- | --- |
| Google Drive | `AppName.GOOGLE_DRIVE` | Search and manage files in Drive. |
| Google Mail | `AppName.GOOGLE_MAIL` | Search messages and attachments in Gmail. |
| Google Calendar | `AppName.GOOGLE_CALENDAR` | Search calendar events and schedules. |
| GitHub | `AppName.GITHUB` | Search repositories, issues, and pull requests. |
| Microsoft Outlook | `AppName.MICROSOFT_OUTLOOK` | Search email in Outlook and Microsoft 365. |
| Microsoft OneDrive | `AppName.MICROSOFT_ONEDRIVE` | Search files in OneDrive and libraries you can access. |
| Microsoft Calendar | `AppName.MICROSOFT_CALENDAR` | Search calendar events in Outlook and Microsoft 365. |

If your SDK build does not yet include every enum member, you can use the matching string for `app_name` (for example `microsoft_outlook`, `microsoft_onedrive`, `microsoft_calendar`).

The same connect, disconnect, and search actions are available through the Smart Search API and as MCP tools named `search_<app_name>`. For MCP setup and the full tool list, see [Model Context Protocol (MCP)](../mcp.md).

***

### Sample Queries by Connector

#### Google Drive (`AppName.GOOGLE_DRIVE`)
- "Find all documents about Q2 financial reports"
- "Show me all PDF files from last month"
- "List documents shared with the team"

#### Google Mail (`AppName.GOOGLE_MAIL`)
- "Find emails from john@example.com about project alpha"
- "Show me emails with attachments from this week"
- "Find emails about meeting schedule changes"

#### Google Calendar (`AppName.GOOGLE_CALENDAR`)
- "List all my upcoming meetings today"
- "Show me meetings with Alice next week"
- "What meetings are scheduled in the conference room tomorrow?"

#### GitHub (`AppName.GITHUB`)
- "Find open issues about authentication"
- "Show me pull requests related to bug fixes"
- "List repositories with recent commits"

#### Microsoft Outlook (`AppName.MICROSOFT_OUTLOOK`)
- "Emails from alice@contoso.com last week about the roadmap"
- "Messages in Sent Items with subject invoice"
- "Show me this message" (paste a link to the message from Outlook on the web if you have one)

#### Microsoft OneDrive (`AppName.MICROSOFT_ONEDRIVE`)
- "Q4 financial workbook xlsx"
- "Presentation shared with the marketing team"

#### Microsoft Calendar (`AppName.MICROSOFT_CALENDAR`)
- "Meetings tomorrow afternoon"
- "Events next week where I declined"
- "Team syncs with Project Phoenix in the title"
