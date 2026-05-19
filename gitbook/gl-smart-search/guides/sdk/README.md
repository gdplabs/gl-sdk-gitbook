---
description: >-
  Welcome to the GL Smart Search SDK documentation. This guide will help you
  understand how to use the various features of the SDK effectively.
icon: cube
---

# GL Smart Search SDK

### Overview

The **GL Smart Search SDK** provides a high-level interface for integrating GL Smart Search capabilities directly into your applications.\
It simplifies communication with the GL Smart Search API by managing authentication, requests, and responses automatically — allowing developers to focus on building functionality rather than handling raw HTTP calls.

The SDK enables unified access to **web search** and **connector** capabilities across both internal and external data sources such as websites, Google Drive, Gmail, Google Calendar, GitHub, and Microsoft 365 (Outlook, OneDrive, Microsoft Calendar).

---

### SDK Version

**v2 — Current**

The latest version of GL Smart Search SDK introduces a modular architecture with two primary capability groups:

* **Web Search Capabilities**
  * `get_web_search_results` — Retrieve search results with `snippets`, `keypoints`, or `summary`
  * `get_web_search_urls` — Return relevant URLs only
  * `get_web_search_map` — Map a website and discover its URL structure
  * `get_web_page` — Fetch web page content
  * `get_web_page_snippets` — Extract snippets (`paragraph` or `sentence` style)
  * `get_web_page_keypoints` — Generate key points from a web page
* **Connector Capabilities**
  * `search_github`
  * `search_google_calendar`
  * `search_google_drive`
  * `search_google_mail`
  * `search_microsoft_outlook`
  * `search_microsoft_onedrive`
  * `search_microsoft_calendar`

All v2 capabilities share a consistent authentication mechanism using the **GL Smart Search Token**.\
In v2, each functionality is also exposed through **MCP Tools**, allowing seamless integration with agentic or modular environments.

---

### Getting Started

Developers can utilize GL Smart Search SDK to build backend applications. You can use smart-search-sdk by adding `smart-search-sdk` in the development configuration.

<details>

<summary>Prerequisites</summary>

To add smart-search-sdk to your project, please ensure you already have:

* Python <3.13, >=3.11
* [uv](https://docs.astral.sh/uv/) (recommended) or [pip](https://pypi.org/project/pip/)

</details>

---

### Installation

Install the SDK using pip:

```bash
pip install smart-search-sdk
```

Once installed, you're ready to import GL Smart Search clients and start interacting with the platform.

The GL Smart Search SDK is organized into two main sections:

* [**Web Search SDK**](web-search.md) — Learn how to perform web searches, extract snippets, and summarize web pages.
* [**Connector SDK**](connector-search.md) — Learn how to connect and search within third-party apps like Google Drive, Gmail, Calendar, GitHub, and Microsoft 365.

Each section provides:

* Setup instructions
* Parameter references
* Full code examples for direct use in your application
