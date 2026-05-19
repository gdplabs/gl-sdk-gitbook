---
icon: flask-round-potion
---

# In-Depth Guide

This guide covers authentication methods for GL Connector MCP servers in detail, including when to use each method and how to work with the OAuth 2.1 flow.

{% hint style="info" %}
If you just want to get connected quickly, start with the [quickstart.md](quickstart.md "mention") — it uses token-based authentication and works reliably across all clients.
{% endhint %}

## Choosing an Authentication Method

|                           | Token-based                                                                      | OAuth 2.1                                                                                                          |
| ------------------------- | -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| **Best for**              | Headless clients, CI/CD, scripts, server-to-server, or when you need reliability | Interactive clients with a browser (IDEs, desktop apps)                                                            |
| **Credential management** | Manual — you create and manage tokens yourself                                   | Automatic — the client handles token exchange                                                                      |
| **Setup effort**          | Slightly more upfront (obtain keys, configure headers)                           | Minimal config, but may require troubleshooting                                                                    |
| **Reliability**           | Stable and predictable                                                           | Unstable — see [#current-state-of-oauth-2.1-in-mcp](in-depth-guide.md#current-state-of-oauth-2.1-in-mcp "mention") |
| **Works with**            | Any client that supports custom headers                                          | Only clients that implement the MCP OAuth 2.1 spec (and even then, not always)                                     |

{% hint style="info" %}
**Our recommendation:** Use token-based authentication unless you have a specific reason to use OAuth 2.1. It works everywhere and doesn't depend on client-side OAuth support. See the [quickstart.md](quickstart.md "mention") to get started with token-based auth.
{% endhint %}

## Token-based Authentication

Token-based auth is covered in detail in the [quickstart.md](quickstart.md "mention"). In short: you provide an `Authorization: Bearer ...` header (your User Token) with every request. These credentials can be obtained via the [connectors-console.md](../api/tools-and-interfaces/connectors-console.md "mention") or [cli.md](../api/tools-and-interfaces/cli.md "mention") to provision it.

For the full header reference, see [credentials.md](../api/credentials.md "mention").

### Headers

| Header          | Required | Description                                          |
| --------------- | -------- | ---------------------------------------------------- |
| `Authorization` | Yes      | Your User Token, prefixed with `Bearer`              |
| `X-Integration` | No       | Target a specific integration when you have multiple |

***

## OAuth 2.1 Flow

OAuth 2.1 lets your MCP client handle authentication automatically — no need to manually copy tokens. When it works, the experience is seamless: connect, authorize in your browser, and you're done.

### Current State of OAuth 2.1 in MCP

{% hint style="danger" %}
**⚠️ OAuth 2.1 in MCP is not yet stable. Read this before proceeding.**
{% endhint %}

The MCP specification's OAuth 2.1 support is still evolving, and the ecosystem has not settled. In practice, this means:

* **No client is reliably compatible with all servers.** Even clients with native OAuth 2.1 support (e.g., VSCode, Windsurf) frequently fail to complete the flow with certain servers. A client that connects to one server may silently fail on another.
* **No server is reliably compatible with all clients.** Even servers that correctly follow the specification encounter failures with certain clients. This includes our own servers — and even extends to first-party clients (Claude Web has inconsistent results connecting to its own ecosystem's servers).
* **Compatibility is a matrix, not a checklist.** Client A might connect to Servers B, C, and D, while Client B only connects to Servers A, B, and C. There is no "known good" combination that universally works. This is a known limitation of the current ecosystem, not a configuration error on your part.
* **Failures can be opaque.** Error messages are often unhelpful — you may see silent failures, hanging connections, or generic auth errors with no clear cause.

This is not specific to GL Connectors — it affects the MCP ecosystem broadly.

**If you need a connection that reliably works today, use** [#token-based-authentication](in-depth-guide.md#token-based-authentication "mention")**.**

### mcp-remote: A Pragmatic Workaround

Despite the instability of native OAuth 2.1 across clients, [`mcp-remote`](https://www.npmjs.com/package/mcp-remote) has proven to be a surprisingly stable bridge. It handles the OAuth browser flow externally and translates between STDIO and Streamable HTTP, bypassing many of the client-specific issues.

If native OAuth fails in your client — which is likely — **try `mcp-remote` before giving up on OAuth entirely.** It has successfully connected to all of our MCP servers in testing.

{% hint style="warning" %}
**Tradeoff:** `mcp-remote` requires **Node.js (v20+)** and **NPM** to be installed on your machine, since it runs via `npx`. If you don't have Node.js and aren't willing to install it, **use token-based auth instead.**
{% endhint %}

```json
{
  "mcpServers": {
    "gmail": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://connectors.gdplabs.id/google_mail/mcp"]
    }
  }
}
```

{% hint style="info" %}
For per-client configuration details (where to put this config, client-specific quirks), see the [mcp-clients.md](mcp-clients.md "mention") page.
{% endhint %}

### When OAuth 2.1 Makes Sense Despite the Caveats

OAuth 2.1 is still worth attempting if:

* You want to avoid managing tokens manually for interactive use
* You're comfortable falling back to token-based auth or `mcp-remote` if the native flow doesn't work
* You have a `@gdplabs.id` email (required for the OAuth flow)

### Configuration

For clients with native OAuth 2.1 support, configuration is minimal — just the server URL:

```json
{
  "mcpServers": {
    "gmail": {
      "serverUrl": "https://connectors.gdplabs.id/google_mail/mcp"
    }
  }
}
```

{% hint style="info" %}
**Note:** Config syntax varies by client. The above is a common format, but check your client's documentation or the [mcp-clients.md](mcp-clients.md "mention") page.
{% endhint %}

You can still use the `X-Integration` header with OAuth 2.1 to target a specific integration. See the [mcp-clients.md](mcp-clients.md "mention") page for how to add headers in each client's config format.

#### Authorization Steps

Once your client initiates the OAuth flow (either natively or via `mcp-remote`):

1. **Application Access Request** — You'll be prompted in your browser with an access request. Click **Allow Access** to continue.
2. **Google Authentication** — Sign in with your `@gdplabs.id` email. Other email domains will be rejected.
3. **Google Consent** — Authorize the application to access your Google profile (only the profile is requested at this stage).
4. **Done** — You should see an "Authorization Successful" screen. Your MCP tools are now available.

### After Authorization: Setting Up an Integration

Completing the OAuth flow authenticates you, but you will still need an **integration** to actually use connector tools. The MCP server provides tools that can generate integration setup URLs — your LLM client can guide you through this.

{% hint style="warning" %}
**⚠️ Warning:** Avoid creating integrations via LLM-driven tool calls if you're using a [Custom Configuration](https://gdplabs.gitbook.io/sdk/gl-connectors/plugin-concepts/custom-configurations), as this may leak your configuration to the model. In the future, this will be done via [URL Mode Elicitation](https://modelcontextprotocol.io/specification/2025-11-25/client/elicitation#url-mode-elicitation-requests) mode. But even that **isn't always supported by the client**.
{% endhint %}

### User Sync Caveat

The OAuth 2.1 flow uses a dedicated authentication tenant. If you created your user account directly via the API (outside of the [connectors-console.md](../api/tools-and-interfaces/connectors-console.md "mention") or OAuth flow), your integrations and secrets **will not be synced** across authentication methods. Accounts created through the Connectors Console do not have this issue.

#### Troubleshooting OAuth

If the OAuth flow fails:

1. **Try `mcp-remote`.** If you were using native OAuth, this is the single most effective fix. It bypasses most client-side OAuth issues.
2. **Try a different client.** Due to the compatibility matrix described above, this can help determine if the issue is client-specific.
3. **Try adding a trailing slash** to the MCP URL (e.g., `.../mcp/` instead of `.../mcp`).
4. **Check your email domain.** Only `@gdplabs.id` accounts are supported.
5. **Fall back to token-based auth.** It always works. See the [quickstart.md](quickstart.md "mention").

***

## Debugging with MCP Inspector

The [MCP Inspector](https://github.com/modelcontextprotocol/inspector) lets you explore what an MCP server offers and test tool calls outside of any IDE. This is useful for verifying your credentials work before debugging client-specific issues.

### Running the Inspector

```bash
DANGEROUSLY_OMIT_AUTH=true npx @modelcontextprotocol/inspector
```

Then open `http://localhost:6274` in your browser.

> `DANGEROUSLY_OMIT_AUTH=true` disables the inspector's own auth proxy. Only use this locally.

#### What You Can Inspect

* **Available Tools** — List all tools the connector exposes
* **Tool Schemas** — Understand required and optional parameters for each tool
* **Resources** — Check available resources and their types
* **Prompts** — View any pre-defined prompts

This is particularly helpful when a tool call fails in your IDE and you want to isolate whether the problem is the MCP server, your credentials, or the client.
