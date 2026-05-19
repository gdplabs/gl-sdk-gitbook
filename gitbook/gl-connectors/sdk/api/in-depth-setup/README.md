---
icon: screwdriver-wrench
---

# In-Depth Setup

Here's a detailed instructions on how to use the GL Connector SDK, starting to set up integrations and execute actions with the SDK.

## Initialization

Before using the connector, you need to initialize it with your Connector API base URL and API key.

```python
from gl_connectors_sdk.connector import GLConnectors

# Initialize the connector
connector = GLConnectors(api_base_url="https://connectors.gdplabs.id", api_key="YOUR_API_KEY")
```

### What's Next?

Once you've initialized the connector, you can proceed with either setup phase:

### [Integration Setup](integration-setup.md)

Learn how to:

* Create and authenticate users
* Set up OAuth2 integrations with third-party services (GitHub, Google Drive, etc.)
* Manage user integrations (check, select, remove)
* Retrieve user information and integration status

> **When to use:** Before executing any actions, you'll need to set up at least one integration for your user.

### [Execution](execution.md)

Learn how to:

* Execute actions using direct execution methods
* Use the fluent interface for complex scenarios
* Handle pagination for list responses
* Work with file uploads and downloads
* Filter response fields
* Configure retry attempts

> **When to use:** After setting up integrations, you can start executing actions against connected services.
