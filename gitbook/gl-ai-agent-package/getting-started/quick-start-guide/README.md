---
icon: bolt-lightning
---

# Quick Start

Go from zero to your first successful agent run.

If you have not installed and configured the SDK yet, start with
[Install & Configure](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/prerequisites).

> **Success**
>
> **When to use this guide:** Choose it when you need a reproducible walkthrough to prove connectivity, create an agent, and observe responses without diving into advanced configuration.
>
> **Audience:** Developers, PMs running acceptance demos, and data developers validating prompt baselines.

{% hint style="info" %}
If you need a deeper comparison before choosing, read
[Local vs Remote](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/getting-started/local-vs-remote).
{% endhint %}

## Default Path: Python SDK

Follow the [Python SDK](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/getting-started/quick-start-guide/python-sdk) page for step-by-step installation, a default local agent run, and optional setup when you want to target a remote AIP server with API credentials and deployment.

> **Info**
>
> If you prefer a low-code workflow (operators, demos, CI smoke tests), use the CLI section:
>
> - CLI entry: [CLI](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/tutorials/cli)
> - Quick start (CLI): [CLI Quick Start](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/getting-started/quick-start-guide/cli)

## Troubleshooting

| Issue                | Solution                                                         |
| -------------------- | ---------------------------------------------------------------- |
| `command not found`  | Ensure pip's script directory is on `PATH`, or reinstall with uv |
| `401 Unauthorized`   | Run `aip accounts add <name>` and `aip accounts use <name>`, or update your environment variables |
| `404 Not Found`      | Check your API URL with `aip accounts show <name>`               |
| `Connection refused` | Confirm the remote AIP server is reachable                       |
| `uv not found`       | Install uv: `curl -LsSf https://astral.sh/uv/install.sh \| sh`   |

## Next Steps

## Suggested Sequence

1. Complete either the
   [Python SDK quick start](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/getting-started/quick-start-guide/python-sdk)
   or
   [CLI quick start](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/getting-started/quick-start-guide/cli).
1. Confirm at least one successful response from your agent.
1. Move to the corresponding guide track:
   [Agents](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/agents),
   [Tools](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/tools),
   [MCPs](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/mcps).

## Troubleshooting Quick Checks

| Issue | Fast fix |
| --- | --- |
| `command not found` (`aip`) | Ensure pip's script directory is on `PATH`, or reinstall using `uv tool install glaip-sdk` |
| `401 Unauthorized` | Run `aip accounts add <name>` and `aip accounts use <name>`, or update environment variables |
| `404 Not Found` | Verify API URL with `aip accounts show <name>` |
| `Connection refused` | Confirm AIP server reachability and network/proxy settings |
| `uv not found` | Install uv: `curl -LsSf https://astral.sh/uv/install.sh \| sh` |

## What to Read Next

1. [Hands-on examples](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/tutorials/hands-on-examples) for runnable patterns.
1. [Agents](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/agents) for lifecycle and runtime controls.
1. [Configuration management](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/configuration-management) for export/import promotion loops.
1. [CLI reference](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/cli-commands) for flags and automation.
