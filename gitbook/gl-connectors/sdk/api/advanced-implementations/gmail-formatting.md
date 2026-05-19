---
icon: envelope-open-text
---

# Gmail Formatting

This guide shows how to use the Gmail MCP connector to send an HTML-formatted email through an agent. We'll build a small script that composes a styled daily schedule email and sends it via `google_mail_send_email`. You should check [mcp-tool-filtration.md](mcp-tool-filtration.md "mention") for how to filter tools, because we filter only the single tool needed to send the email.

## Case Study: Email Formatting

Gmail Connector supports sending formatted email via HTML. We will show you how to provide the template for the LLM to fill without overfilling the context with tokens.

### Installation

```shellscript
uv init --bare
uv add glaip-sdk[local] gllm-tools-binary
```

### Source Code

```python
import asyncio
import os

from glaip_sdk import Agent
from gllm_tools.mcp.client.langchain import LangchainMCPClient

DESIRED_TOOLS = {"google_mail_send_email"}

client = LangchainMCPClient({
    "google_mail": {
        "url": "https://connectors.gdplabs.id/google_mail/mcp",
        "headers": {"Authorization": f"Bearer {os.getenv('GL_CONNECTORS_USER_TOKEN')}"},
    }
})

EMAIL_FORMAT = """
THIS IS A TEST EMAIL. PLEASE IGNORE.
<div style="font-family: Helvetica, Arial, sans-serif; max-width: 600px; margin: 0 auto; color: #333;">
    <h2 style="border-bottom: 2px solid #0066cc; padding-bottom: 10px;">📅 Today's Schedule</h2>

    <!-- REPEAT FOR EACH MEETING -->
    <div style="padding: 15px 0; border-bottom: 1px solid #eee;">
        <div style="font-size: 14px; font-weight: bold; color: #0066cc; margin-bottom: 4px;">
            [START_TIME] - [END_TIME]
        </div>
        <div style="font-size: 18px; font-weight: bold; margin-bottom: 4px;">
            [MEETING_TITLE]
        </div>
        <div style="font-size: 14px; color: #666;">
            📍 [LOCATION_OR_LINK] <br>
            📝 [DESCRIPTION]
        </div>
    </div>
    <!-- END REPEAT -->

    <p style="margin-top: 20px; font-size: 14px; color: #888;">
        Have a productive day!
    </p>
</div>
"""


def extract_content(chunk) -> str | None:
    if isinstance(chunk, str):
        return chunk
    if isinstance(chunk, dict):
        return chunk.get("content")
    return getattr(chunk, "content", None)


async def main():
    all_tools = await client.get_tools("google_mail")
    tools = [t for t in all_tools if t.name in DESIRED_TOOLS]

    agent = Agent(
        name="gmail_agent",
        instruction="You are a helpful assistant.",
        tools=tools,
        model="gpt-4.1",
    )

    prompt = (
        "Send an email to myself about my schedule for today. "
        "Use the following HTML format for the body, filling in the blanks "
        f"with the schedule (make it up if needed): {EMAIL_FORMAT}"
    )

    async for chunk in agent.arun(prompt):
        if content := extract_content(chunk):
            print(content)


asyncio.run(main())
```

### How It Works

{% stepper %}
{% step %}
#### Connect to the Gmail MCP server

The `LangchainMCPClient` takes a server config dictionary. For Gmail, point it at the `google_mail` connector endpoint and authenticate with your user token.

```python
client = LangchainMCPClient({
    "google_mail": {
        "url": "https://connectors.gdplabs.id/google_mail/mcp",
        "headers": {"Authorization": f"Bearer {os.getenv('GL_CONNECTORS_USER_TOKEN')}"},
    }
})
```
{% endstep %}

{% step %}
**Filter to only the tools you need**

The Gmail connector exposes several tools (sending, reading, searching, etc.). This example only needs `google_mail_send_email`, so we filter the rest out before handing tools to the agent.

```python
DESIRED_TOOLS = {"google_mail_send_email"}

all_tools = await client.get_tools("google_mail")
tools = [t for t in all_tools if t.name in DESIRED_TOOLS]
```

For a deeper look at filtering strategies (allow-lists, deny-lists, pattern matching), see [mcp-tool-filtration.md](mcp-tool-filtration.md "mention").
{% endstep %}

{% step %}
#### Define your email format

The `EMAIL_FORMAT` constant is an HTML template with placeholder brackets. The agent receives this template as part of its prompt and fills in the blanks when composing the email body.

You can swap this template for anything — plain text, a different HTML layout, or a format pulled from a file. The agent will adapt as long as the prompt makes the expected structure clear.
{% endstep %}

{% step %}
#### Run the agent

The agent streams its response as chunks. The `extract_content` helper normalizes the different chunk types (`str`, `dict`, or object with a `.content` attribute) so we can print them uniformly.

```python
async for chunk in agent.arun(prompt):
    if content := extract_content(chunk):
        print(content)
```
{% endstep %}
{% endstepper %}

### Prerequisites

* A valid `GL_CONNECTORS_USER_TOKEN` environment variable (see the [connectors-console.md](../tools-and-interfaces/connectors-console.md "mention") or [credentials.md](../credentials.md "mention") for how to obtain one).
* An active Google Mail integration configured through GL Connectors (see [agentic-tools-and-model-context-protocol-mcp](../../agentic-tools-and-model-context-protocol-mcp/ "mention")). The MCP server does not handle a one-shot authentication setup — this must be done beforehand via the API, SDK, or CLI.
