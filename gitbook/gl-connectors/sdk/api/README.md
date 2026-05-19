---
icon: trillium
---

# API

The GL Connectors API and all corresponding libraries are the primary way to integrate connectors into your application. All GL Connectors functionality — from authentication to executing connector actions — is accessible through it.

### What It Does

The SDK provides a unified interface to interact with all available GL Connectors. With it, you can:

* **Authenticate** and manage user tokens
* **Connect** to any supported connector (Google Drive, GitHub, and more)
* **Execute actions** on connectors such as searching files, fetching data, or triggering workflows
* **Handle responses** with structured data and status codes

The SDK supports two execution styles — a **fluent style** for readability and a **direct style** for brevity — so you can choose the approach that fits your codebase.

### Prerequisites

* Python 3.11+
* A Python package manager (we recommend [UV](https://docs.astral.sh/uv/))
* A **GL Connectors Client API Key** and **User Token**, obtainable via the Console

### Installation

```bash
uv add gl-connectors-sdk
```

To get quickly up to speed, please check [quickstart.md](quickstart.md "mention") to see the simple code to get things working.

### Next Steps

* [quickstart.md](quickstart.md "mention") — Get up and running with your first connector call
* [credentials.md](credentials.md "mention") — Learn how to obtain and manage your API Key and User Token
* [in-depth-setup](in-depth-setup/ "mention") — Explore authentication methods, advanced configuration, and more
* [sdk-method-api.md](sdk-method-api.md "mention") — Full reference for all available SDK methods

