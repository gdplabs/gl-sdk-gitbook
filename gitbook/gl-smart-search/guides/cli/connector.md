# CLI Connector Commands

The GL Smart Search SDK provides CLI commands to interact with third-party connectors such as GitHub, Google Drive, Google Calendar, Google Mail, and **Microsoft 365** (Outlook mail, OneDrive, and Microsoft Calendar).

## Overview

Connector commands allow you to:
- **Connect** to third-party services
- **Disconnect** from third-party services
- **Search** within connected services using natural language queries

## Prerequisites

Before using connector commands, ensure you have:
- GL Smart Search SDK installed (`pip install smart-search-sdk`)
- `SMARTSEARCH_BASE_URL` environment variable set to `https://search.glair.ai/`
- Valid GL Smart Search Token (set via `SMARTSEARCH_TOKEN` environment variable)

## Available Commands

### Connector - Connect

Initiate integration with a third-party connector.

#### Usage

```bash
smart-search connector connect --app-name <APP_NAME> [OPTIONS]
```

#### Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `--app-name` | Yes | String | App name to connect to. Options: `github`, `google_mail`, `google_calendar`, `google_drive`, `microsoft_outlook`, `microsoft_onedrive`, `microsoft_calendar` |
| `--gl-token` | No | String | GL Connectors token for authentication (optional) |
| `--callback-url` | No | String | OAuth callback URL (defaults to GL Smart Search's URL) |
| `--view` | No | String | Output format: `pretty` or `json` (default: `pretty`) |

#### Examples

**Interactive mode:**
```bash
smart-search connector connect
```

**Connect to GitHub:**
```bash
smart-search connector connect --app-name github --gl-token "your-token"
```

**Connect to Google Drive with custom callback:**
```bash
smart-search connector connect \
  --app-name google_drive \
  --callback-url "https://your-app.com/callback"
```

#### Response

When OAuth setup is required:
```json
{
  "status": "setup_required",
  "message": "Please authenticate with the service",
  "setup_url": "https://oauth.provider.com/authorize?..."
}
```

When already connected:
```json
{
  "status": "connected",
  "message": "Successfully connected to GitHub"
}
```

---

### Connector - Disconnect

Remove integration with a third-party connector.

#### Usage

```bash
smart-search connector disconnect --app-name <APP_NAME> [OPTIONS]
```

#### Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `--app-name` | Yes | String | App name to disconnect from. Options: `github`, `google_mail`, `google_calendar`, `google_drive`, `microsoft_outlook`, `microsoft_onedrive`, `microsoft_calendar` |
| `--gl-token` | No | String | GL Connectors token for authentication (optional) |
| `--view` | No | String | Output format: `pretty` or `json` (default: `pretty`) |

#### Examples

**Disconnect from GitHub:**
```bash
smart-search connector disconnect --app-name github
```

**Disconnect with GL Connectors token:**
```bash
smart-search connector disconnect \
  --app-name google_calendar \
  --gl-token "your-token"
```

#### Response

```json
{
  "status": "disconnected",
  "message": "Successfully disconnected from GitHub"
}
```

---

### Connector - Search

Search a connected third-party service using natural language queries.

#### Usage

```bash
smart-search connector search --query "<QUERY>" --app-name <APP_NAME> [OPTIONS]
```

#### Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `--query` | Yes | String | Natural language search query |
| `--app-name` | Yes | String | App name to search. Options: `github`, `google_mail`, `google_calendar`, `google_drive`, `microsoft_outlook`, `microsoft_onedrive`, `microsoft_calendar` |
| `--gl-token` | No | String | GL Connectors token for authentication (optional) |
| `--view` | No | String | Output format: `table` or `json` (default: `table`) |
| `--stream` | No | Boolean | Enable streaming response (default: `false`) |

#### Examples

**Search GitHub issues:**
```bash
smart-search connector search \
  --query "open issues about authentication" \
  --app-name github
```

**Search Google Calendar:**
```bash
smart-search connector search \
  --query "meetings with Alice next week" \
  --app-name google_calendar \
  --view json
```

**Search Google Drive with streaming:**
```bash
smart-search connector search \
  --query "Q2 financial reports" \
  --app-name google_drive \
  --stream true
```

#### Response (Table View)

```
┏━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ No ┃ Title       ┃ Content Preview ┃ Source        ┃
┡━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ 1  │ Issue #123  │ Authentication… │ github.com/…  │
│ 2  │ PR #456     │ Fix auth flow…  │ github.com/…  │
└────┴─────────────┴─────────────────┴───────────────┘
✓ Found 2 results.
```

#### Response (JSON View)

```json
{
  "data": [
    {
      "id": "…",
      "content": "Authentication issue in OAuth flow...",
      "metadata": {
        "title": "Issue #123: Fix OAuth authentication",
        "source": "https://github.com/user/repo/issues/123"
      }
    }
  ]
}
```

## Authentication

The connector commands support two authentication modes:

1. **Default Mode**: Uses GL Smart Search's internal GL Connectors credentials
   ```bash
   smart-search connector connect --app-name github
   ```

2. **GL Connectors Token Mode**: Uses provided GL Connectors token
   ```bash
   smart-search connector connect \
     --app-name github \
     --gl-token "your-token"
   ```

## Error Handling

All commands provide clear error messages:

```bash
❌ Error occurred during connector connection
Details: Connection timeout - please check your network
```

## Best Practices

1. **Use appropriate app names**: Ensure the app name matches exactly (case-sensitive)
2. **Handle setup URLs**: For OAuth connectors, visit the setup URL to complete authentication
3. **Stream large results**: Use `--stream true` for better performance with large result sets
4. **JSON for automation**: Use `--view json` when integrating with scripts or CI/CD pipelines
5. **Secure tokens**: Never hardcode GL Connectors tokens in scripts; use environment variables

## Common Use Cases

### Searching GitHub Issues
```bash
smart-search connector search \
  --query "bugs related to payment processing" \
  --app-name github \
  --view table
```

### Finding Email Threads
```bash
smart-search connector search \
  --query "emails from john about project alpha" \
  --app-name google_mail
```

### Locating Calendar Events
```bash
smart-search connector search \
  --query "meetings scheduled for tomorrow" \
  --app-name google_calendar
```

### Searching Documents
```bash
smart-search connector search \
  --query "design documents from last quarter" \
  --app-name google_drive
```

### Microsoft Outlook (mail)
```bash
smart-search connector search \
  --query "emails from finance about Q3 budget" \
  --app-name microsoft_outlook
```

### Microsoft OneDrive
```bash
smart-search connector search \
  --query "budget spreadsheet xlsx" \
  --app-name microsoft_onedrive
```

### Microsoft Calendar (Outlook / Microsoft 365)
```bash
smart-search connector search \
  --query "meetings tomorrow where I accepted" \
  --app-name microsoft_calendar
```
