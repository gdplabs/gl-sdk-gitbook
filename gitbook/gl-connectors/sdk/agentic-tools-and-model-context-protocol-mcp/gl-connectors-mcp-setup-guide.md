---
icon: mcp
---

# GL Connectors MCP Setup Guide

## Cookbook

The best way to get started is by checking the [connector-mcp-cookbook.md](connector-mcp-cookbook.md "mention") page, to see how to set up Connector MCP programmatically.

## Authentication Types

To access an MCP Server, there are two types of authentication available. The method you choose depends on your client type and use case.

| Method         | Best For                                              | User Interaction Required |
| -------------- | ----------------------------------------------------- | ------------------------- |
| Token-based    | Headless clients, CI/CD, scripts, programmatic access | No                        |
| OAuth 2.1 Flow | Interactive clients (Claude Desktop, Cursor, etc.)    | Yes                       |

### Token-based Authentication

Token-based authentication is designed for **headless clients** and scenarios where user interaction is not possible or is detrimental. This includes CI/CD pipelines, automated scripts, server-to-server communication, and any client that cannot open a browser for OAuth consent.

While headless clients _can_ technically present an OAuth authorization link to users, the OAuth 2.1 Flow introduces significant operational challenges in non-interactive environments:

* **Server stall** — The MCP connection blocks while waiting for the OAuth callback to complete
* **Timeout risks** — Long waits for user interaction can cause connection timeouts or process hangs

Token-based authentication avoids these issues entirely by using pre-generated credentials that require no runtime user interaction.

#### Headers Required

{% hint style="warning" %}
Do not omit the `Bearer` prefix. `Authorization: eyJ...` will fail—it must be `Authorization: Bearer eyJ...`
{% endhint %}

| Header          | Description                                                                                                   |
| --------------- | ------------------------------------------------------------------------------------------------------------- |
| `X-Api-Key`     | Your Client API Key as listed above.                                                                          |
| `Authorization` | <p>Your User Token (JWT). <strong>Must include <code>Bearer</code></strong></p><p><strong>prefix</strong></p> |

#### Headers Optional

| Header          | Description                              |
| --------------- | ---------------------------------------- |
| `X-Integration` | Specifies which user integration to use. |

#### Creating Your Tokens

Before using Token-based authentication, you must create your credentials separately. These are **not** automatically provisioned.

There are multiple ways to create the tokens required:

1. The easiest way utilizes [connectors-console.md](../api/tools-and-interfaces/connectors-console.md "mention"), but it requires you to have @gdplabs.id email.
2. Via the CLI, you can authenticate following this guide [credentials.md](../api/credentials.md "mention"). You can then retrieve the values via these two commands (on \*Nix based systems):
   1. **Client API Key**: `jq -r '.client_api_key' ~/.connector/config.json`
   2. **User Token**: `jq -r '.token' ~/.connector/config.json`
3.  Via the SDK, you can authenticate following [#authentication](../api/in-depth-setup/#authentication "mention") using the code programmatically.

    ```python
    from gl_connectors.connector import GLConnectors

    connectors = GLConnectors(api_key="YOUR_API_KEY")
    user = connectors.authenticate("username", "password")
    user_token = user.token  # Will resolve to `eyJ......` bearer token.
    ```

### OAuth 2.1 Flow

{% hint style="danger" %}
**It is important to note** that because we utilize a special Client (tenant) for this authentication method, if you have created a user directly outside of the Playground or using the API, this user **will not by synced** (integrations, secret, etc). This user is **synchronized with** [connectors-console.md](../api/tools-and-interfaces/connectors-console.md "mention"). If you've used Connector Console to get your account, you will not have any issues!
{% endhint %}

OAuth 2.1 Flow is the **preferred method for interactive clients** such as Claude Desktop, Cursor, and other MCP-compatible applications with a user interface. This flow handles all credential management automatically.

For users with GDP Labs email (@gdplabs.id), it's possible to directly authenticate into the MCP servers utilizing OAuth2 Flow:

* User creation, token exchange, and all authorization flows are managed automatically
* Simply connect your MCP client and authorize when prompted

This is **preferred** for you as an end-user as you do not need to deal with user creation and anything that entails. See [#supported-clients](gl-connectors-mcp-setup-guide.md#supported-clients "mention") clients below because not all clients are supported.

{% stepper %}
{% step %}
**Configuration**

{% hint style="info" %}
Note that even with this authentication method, you may still use the optional headers to determine which integration you want to use via `X-Integration` header. Simply add a new `headers` section and adding the `X-Integration` value!
{% endhint %}

The configuration, once you deal with OAuth2, becomes as simple and as short as (check your IDE since the syntax may differ):

```json
{
  "mcpServers": {
    "gmail": {
      "serverUrl": "https://connectors.gdplabs.id/google_mail/mcp"
    }
  }
}
```
{% endstep %}

{% step %}
**Authorization Step**

If all goes well, you should be prompted with an Application Access Request. To continue with the authentication, please click **Allow Access**.

<figure><img src="../../../.gitbook/assets/image (2) (1).png" alt=""><figcaption></figcaption></figure>
{% endstep %}

{% step %}
**Authenticate Google Email**

You need to then authenticate using your Google email. Please use your @gdplabs.id email, as you will be rejected access if you use other email domains.

<figure><img src="../../../.gitbook/assets/image (3) (1).png" alt=""><figcaption></figcaption></figure>

Like before, you will be asked to **authorize the application** to access your Google Account (only the profile is requested). To continue, please give it the access.
{% endstep %}

{% step %}
**You're done!**

You can now check your MCP once you get the "Authorization Successful" screen. Your tools can now be used.

<figure><img src="../../../.gitbook/assets/image (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>
{% endstep %}
{% endstepper %}

**Disclaimer**: You will still need to create an integration. However, we've made sure the MCP server now also provides tools that allow for easy URL generation for integration. Let the LLM decide for you when you need to do this! **However, it is&#x20;**_**highly discouraged**_**&#x20;to do this on Custom Configuration because you may leak your configuration to the LLM!**

### Supported Clients

Not all clients support OAuth2 Flow. It is important to know that **all headless clients** cannot utilize this OAuth2 Flow because the MCP Specification requires a browser interaction (and does not support client credentials officially in the base specification). As such, the following clients are known to be supported:

* VSCode
* Windsurf
* Cursor (via **MCP-Remote**)
* AntiGravity (via **MCP-Remote**)
* Kiro (via **MCP-Remote**)
* ChatGPT Web (requires **Plus** or higher subscription, or if **Business**, requires administrative access)

Some clients do not entirely support this flow, including **Claude Web** because it _sometimes_ works, and sometimes it doesn't. And clients like Cursor do not entirely support it because you are required to _manually_ access the authentication URL instead of the IDE opening the browser for you. To circumvent this, we can use an STDIO MCP Server called **MCP Remote** that does it all for you. The following is an example configuration (please check your IDE documentation to be sure!)

**Prerequisites**

1. To utilize MCP Remote, you need to have **NodeJS** and **NPM** installed (we will utilize `npx` as the command).
   1. We recommend using the latest LTS, but at the very least **NodeJS version 20** is recommended.

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

The full command is `npx -y mcp-remote {url}`, where the URL can be obtained from [.](./ "mention"). You will still need to follow the Authorization Step like above!

### IDE Setup

Various IDEs and clients support MCPs, so this won't be a comprehensive list. Having said that, we have curated ways to add MCP Servers to popular MCP Clients.

{% tabs %}
{% tab title="Claude Desktop" %}
**Adding a Single Connector**

{% hint style="warning" %}
You may need to restart your Claude client in order to load the changes in your MCP servers after editing the `claude_desktop_config.json`
{% endhint %}

Claude Desktop only supports STDIO-based MCP. Here is how you can do it:

1. **Settings > Developer**
2. Click `edit config`
3. You will be prompted to edit the file `claude_desktop_config.json`
4. After saving the file, you may need to restart Claude Desktop to load the changes to your MCP Servers list.

{% code fullWidth="true" %}
```json
{
  "mcpServers": {
    "gdrive_oauth2": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://connectors.gdplabs.id/google_drive/mcp"
      ]
    },
    "gdocs_token": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://connectors.gdplabs.id/google_docs/mcp",
        "--header",
        "X-Api-Key: sk-client-...",
        "--header",
        "Authorization: Bearer eyJ...",
        "--header",
        "X-Integration: user..."
      ]
    }
  }
}
```
{% endcode %}
{% endtab %}

{% tab title="Cursor" %}
1. Open Cursor
2. Go to **File** > **Preferences** > **Cursor Settings** > **Tools & MCP**
3. Click `New MCP Server`
4. Add the MCP configuration similar to this (do note that **because of Cursor's limitations, if you wish to use the OAuth2 Flow above, you need to use `mcp-remote`**). Below is an example of how to do both:

```json
{
  "mcpServers": {
    "gdrive_oauth2": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://connectors.gdplabs.id/google_drive/mcp"
      ]
    },
    "gmail_token": {
      "url": "https://connector.gdplabs.id/google_mail/mcp",
      "headers": {
        "X-Api-Key": "sk-client-...",
        "Authorization": "Bearer eyJ...",
        "X-Integration": "user..."
      }
    }
  }
}
```
{% endtab %}

{% tab title="Windsurf" %}
**Adding a Single Connector**

1. Open Windsurf
2. Go to **File** > **Preferences** > **Windsurf Settings** > **Cascade** > **Open MCP Marketplace > Click the Gear Icon** :gear: **on the right**.
3. Add the MCP configuration (Windsurf natively supports OAuth2, so it _should_ work for both authentication methods):

```json
{
  "mcpServers": {
    "gdrive_oauth2": {
      "serverUrl": "https://connectors.gdplabs.id/google_drive/mcp"
    },
    "gmail_token": {
      "serverUrl": "https://connectors.gdplabs.id/google_mail/mcp",
      "headers": {
        "X-Api-Key": "sk-client-...",
        "Authorization": "Bearer eyJ..."
      }
    }
  }
}

```
{% endtab %}

{% tab title="VSCode" %}
1. Open VSCode
2. Use the command `> Add MCP Server` to add the server via wizard, or:
3. Use the command `> MCP: Open User Configuration` to configure the file manually on `mcp.json`. This guide uses this method:

```json
{
  "mcp": {
    "servers": {
      "google": {
        "type": "http",
        "url": "https://connectors.gdplabs.id/google/mcp"
      },
      "gmail": {
        "type": "http",
        "url": "https://connectors.gdplabs.id/google_mail/mcp",
        "headers": {
          "X-Api-Key": "sk-client-...",
          "Authorization": "Bearer eyJ...",
          "X-Integration": "user..."
        }
      }
    }
  }
}
```
{% endtab %}
{% endtabs %}

## Using MCP Inspector

The MCP Inspector is a powerful tool that allows you to explore and understand the capabilities of each MCP server. You can use it to:

* List available tools for each connector
* Understand tool parameters and requirements
* Test tool functionality
* Debug connection issues

#### Installation and Usage

{% hint style="warning" %}
`DANGEROUSLY_OMIT_AUTH=true` is used to remove the need of proxies. Only to be used when you're doing things locally.
{% endhint %}

```bash
# Run mcp inspector
DANGEROUSLY_OMIT_AUTH=true npx @modelcontextprotocol/inspector

# after that you can open your localhost:6274
```

#### What You Can Inspect

* **Available Tools**: See all tools provided by the connector
* **Tool Schemas**: Understand required and optional parameters
* **Resources**: Check available resources and their types
* **Prompts**: View any pre-defined prompts

## Programmatic Usage

You can also use Connector MCP servers programmatically in your Python applications using [mcp-client.md](../../../common-modules/tutorials/tools/mcp-client.md "mention").
