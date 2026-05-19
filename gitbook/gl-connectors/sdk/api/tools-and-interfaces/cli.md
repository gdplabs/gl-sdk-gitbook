---
icon: terminal
---

# CLI

`gl-connectors-cli` is the official command-line tool designed to streamline operations, automation, and integrations within the GL Connectors ecosystem. It provides commands for authentication, service registration, project bootstrapping, plugin management, and more.

## Installation

From PyPi:

```
pip install gl-connectors-cli
```

## Quick Start

### Authentication

First, authenticate with your credentials:

```
glcon auth login
```

You'll be prompted for:

* **Client API Key**: Your client API key (input will be hidden)
* **Username**: Your user identifier
* **User Secret**: Your user secret (input will be hidden)

{% hint style="info" %}
By default, You will be log in to production https://connectors.gdplabs.id

For testing or custom URL, please use `--api-url` flag
{% endhint %}

Authentication with custom URL:

```
glcon auth login --api-url http://localhost:8000
```

Check authentication status:

```
glcon auth status
```

Logout and clear session:

```
glcon auth logout
```

## Commands

### Authentication

The `glcon auth` command manages your authentication credentials and session with the GL Connector's API Platform. All CLI operations require authentication, so this is typically the first command you'll use.

#### Login

Authenticate with your Connectors credentials to start using the CLI.

Usage:

```
glcon auth login [--api-url <url>]
```

Options:

* \--api-url \<url> - Custom Connectors API URL (default: https://connectors.gdplabs.id)

Interactive Prompts:

* Client API Key - Your client API key (format: sk-client-\*, input hidden)
* Username - Your user identifier
* User Secret - Your user secret (input hidden)

Examples:

```bash
# Login to production
glcon auth login

# Login to local development environment
glcon auth login --api-url http://localhost:8000

# Login to staging environment
glcon auth login --api-url https://stag-connector.obrol.id/
```

#### Status Check

Check your current authentication status and session information.

Usage:

```
glcon auth status
```

Examples:

```bash
glcon auth status

# Output:
# Authentication Status
# =====================
# Username: ..
# API URL: http://localhost:8000
```

#### Logout

Clear your stored authentication session and credentials.

Usage:

```
glcon auth logout
```

**Output:**

```bash
✓ Successfully logged out # Success
```

{% hint style="info" %}
Notes:

* API URL is stored with the session and used for all subsequent commands
* Always use `glcon auth logout` when switching between environments or when done working
{% endhint %}

***

### Integration Management

List all available connectors and their integration status:

```
glcon integrations
# or
glcon integrations list
```

This shows a simple table with:

* **Connector**: Name of each available connector
* **Integrated**: ✓ if you have integrated with that connector, ✗ if not

Add a new integration (initiates OAuth flow):

```
glcon integrations add github
glcon integrations add google
```

Show all accounts for a specific connector:

```
glcon integrations show google
glcon integrations show github
```

This displays:

* Number of integrations found
* Table showing account identifiers for each integration

Remove a specific integration:

```
glcon integrations remove github user@example.com
glcon integrations remove google john.doe@gmail.com
```

### User Management

Create a new user:

```
glcon users create john.doe@example.com
```

> **Important**: Save the user secret securely! It's only shown once.

## Configuration

The CLI stores configuration in `~/.connector/config.json`. This file contains:

* Authentication session (client key, user token, API URL)
* Session expiration information

The API URL is only configurable during authentication using the `--api-url` flag.
