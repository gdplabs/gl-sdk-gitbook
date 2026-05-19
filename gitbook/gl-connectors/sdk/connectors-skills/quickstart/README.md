---
icon: truck-fast
---

# Quickstart

## Prerequisites

As this guide utilizes a library published in Gen AI Google Cloud Repository, you will need to fulfill all the setup steps required in Gen AI's [prerequisites.md](../../../../gen-ai-sdk/prerequisites.md "mention"). To summarize, you need the following:

* Python 3.11 or higher
* [UV](https://docs.astral.sh/uv/) package manager

## Getting Started

{% stepper %}
{% step %}
**Installation**

Initialize a new project and add the GL Connectors Tools package.

{% code overflow="wrap" lineNumbers="true" %}
```bash
uv init --bare
uv add gl-connectors-tools-binary
```
{% endcode %}
{% endstep %}

{% step %}
**Code**

Create a `main.py` file with the following content:

{% code title="main.py" lineNumbers="true" %}
```python
from gl_connectors_tools.skills import SkillFactory
import asyncio

async def main():
    await SkillFactory.from_github(
        source="https://github.com/anthropics/skills/tree/main/skills/algorithmic-art",
        destination=[".agents/skills"],
    )

asyncio.run(main())
```
{% endcode %}

**Parameters**

| Parameter     | Description                                                                       |
| ------------- | --------------------------------------------------------------------------------- |
| `source`      | Any GitHub path containing a `SKILL.md` file. Can be https, can be ssh.           |
| `destination` | Local directory where the skill will be installed                                 |
| `token`       | _(Optional)_ GitHub token for private repository access or for higher rate limits |

**Common Destination Paths**

| Agent       | Path               |
| ----------- | ------------------ |
| General     | `.agents/skills`   |
| Claude Code | `.claude/skills`   |
| Copilot     | `.github/skills`   |
| Cursor      | `.cursor/skills`   |
| Windsurf    | `.windsurf/skills` |
| Codex       | `.codex/skills`    |
| Kimi Code   | `.kimi/skills`     |
{% endstep %}

{% step %}
**Run**

Execute the script to install the skill:

```bash
uv run main.py
```

The skill will be downloaded and placed in your `.agents/skills` directory, ready for your agent to use.
{% endstep %}

{% step %}
**What's Next?**

You have the following options:

* You can implement your own agents that supports Skills! You can see [implementing-with-agent.md](implementing-with-agent.md "mention") for an example using [LangChain's DeepAgents](https://docs.langchain.com/oss/python/deepagents/overview).
* You can now use the skills directly in your favorite Agentic Client such as Claude Code! For more information on how to install from private repositories, branches, etc. You can refer to the [sources](../sources/ "mention") to see what sources we currently support.
{% endstep %}
{% endstepper %}
