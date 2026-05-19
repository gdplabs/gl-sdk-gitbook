---
icon: terminal
---

# Command Line Interface (CLI)

The GL Smart Search SDK provides CLI commands to interact with GL Smart Search capabilities directly from your terminal.

## Overview

The CLI allows you to:
- **Web Search** – Perform web searches and retrieve results
- **Connector Operations** – Connect, disconnect, and search within third-party services like GitHub, Google Drive, Google Calendar, Google Mail, and Microsoft 365 (Outlook, OneDrive, Microsoft Calendar)

## Prerequisites

Before using the CLI, ensure you have:
- GL Smart Search SDK installed (`pip install smart-search-sdk`)
- `SMARTSEARCH_BASE_URL` environment variable set to `https://search.glair.ai/`
- Valid GL Smart Search Token (set via `SMARTSEARCH_TOKEN` environment variable)

## Available Commands

* [**CLI Web Search**](web-search.md) — Perform web searches from the command line
* [**CLI Connector**](connector.md) — Manage connector connections and search within connected services
