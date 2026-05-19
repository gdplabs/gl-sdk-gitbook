---
icon: diagram-predecessor
---

Operationalise LangFlow boards inside AIP so you can run and manage them
alongside native agents. This guide is for teams prototyping visually who are
ready to sync flows into the wider automation platform without rewriting them by
hand.

## Overview

_When to use:_ Understand the sync pipeline before wiring automation.

LangFlow lets you design complex agent workflows visually. The GL AIP package can
sync those flows and expose them as agents of type `langflow`, ready to run via
the Python SDK or CLI. Use LangFlow for rapid prototyping, then promote the
result into your wider automation pipelines.

## Configure Access

_When to use:_ Connect LangFlow to AIP with the right credentials and endpoints.

Set the LangFlow connection once via environment variables or CLI flags:

```bash
export LANGFLOW_BASE_URL="https://your-langflow.example.com"
export LANGFLOW_API_KEY="super-secret"
```

## Sync Flows from LangFlow

_When to use:_ Promote a visual flow into an AIP agent for the first time or after edits.

#### Python SDK

```python
from glaip_sdk import Client

client = Client()

client.sync_langflow_agents()

# Inspect LangFlow-based agents
langflow_agents = client.agents.list_agents(agent_type="langflow")
for agent in langflow_agents:
    print(agent.name)
```

#### CLI

```bash
# Pull all flows and create/update matching AIP agents
aip agents sync-langflow

# Provide explicit connection details if you do not use env vars
aip agents sync-langflow \
  --base-url "https://your-langflow.example.com" \
  --api-key "super-secret"

# List the imported agents (type=langflow)
aip agents list --type langflow
```

{% hint style="info" %}
`aip agents sync-langflow` references agents by their underlying LangFlow IDs,
but follow-up commands like `aip agents run` accept either the synced agent ID
or its unique name. Use `--select` if multiple agents share a similar name.
{% endhint %}

The sync operation fetches every published flow, creating new agents or updating
existing ones if the LangFlow ID already exists in AIP.

### Common sync issues

| Symptom                            | Likely cause                                               | Fix                                                                                                 |
| ---------------------------------- | ---------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| Flow not listed in CLI after sync  | Sync command failed silently or wrong workspace connected. | Re-run the sync with verbose logging and confirm API keys reference the correct LangFlow workspace. |
| Tool references missing            | Tool IDs in the flow do not exist in the target account.   | Import or recreate the tools first, then resync the flow.                                           |
| Runtime errors about unknown nodes | Custom components unsupported in AIP runtime.              | Replace custom nodes with supported blocks before syncing.                                          |
| Flow changes not reflected         | Cached agent still running previous version.               | Use `--force` sync options or delete/recreate the agent before syncing.                             |

## Run LangFlow Agents

_When to use:_ Execute, monitor, and validate converted flows inside AIP.

#### Python SDK

```python
from glaip_sdk import Client

client = Client()

agent = client.find_agents(name="marketing-flow")[0]
response = agent.run("Create a campaign brief for the autumn launch")
print(response)
```

#### CLI

```bash
aip agents list --type langflow
aip agents run <LANGFLOW_AGENT_REF> --input "Summarise the Q4 roadmap"
```

Replace `<LANGFLOW_AGENT_REF>` with the agent ID or name from the list output.

## Best Practices

_When to use:_ Keep flows consistent between design and production environments.

- **Version in LangFlow**: Tag releases in LangFlow so you can track which build
  is currently synced. The sync output returns counts for created, updated, and
  skipped flows.
- **Modular boards**: Break large chains into reusable sub-flows to keep agent
  responses predictable and easier to debug.
- **Tool parity**: Ensure any tools referenced in the LangFlow board exist in the
  target AIP account; missing tools will surface as execution errors.
- **Scheduled syncs**: Use CI or scheduled jobs to call `aip agents sync-langflow`
  so your AIP account always mirrors the latest published boards.

## Troubleshooting

_When to use:_ Resolve sync or runtime failures before filing an issue.

| Symptom                                | Likely Cause                                  | Fix                                                                  |
| -------------------------------------- | --------------------------------------------- | -------------------------------------------------------------------- |
| `Missing LangFlow configuration` error | No base URL/API key configured                | Set `LANGFLOW_BASE_URL` and `LANGFLOW_API_KEY` or pass flags         |
| Agents not appearing after sync        | Flow is disabled or missing required metadata | Publish/enable the flow in LangFlow and re-run sync                  |
| Execution errors at runtime            | Referenced tools/models unavailable in AIP    | Provision the same tools/models in the target account before running |

## Related Documentation

- **[Agents guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/agents)**: Operate LangFlow and native agents side by side.
- **[Automation & scripting](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/automation-and-scripting)**: Schedule sync jobs or
  integrate with CI pipelines.
- **[Configuration management](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/configuration-management)**: Export agent
  configurations after syncing for review or promotion.
- **[REST API reference](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/rest-api)**: Reference-only endpoints for LangFlow sync.

______________________________________________________________________

_Design visually in LangFlow, sync into AIP, and run those flows anywhere you use
the SDK or CLI._
