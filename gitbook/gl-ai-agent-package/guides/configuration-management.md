---
icon: sliders
---

Promote and back up AIP resources across environments. Use this guide
when you move configurations between sandboxes, staging, and production or need
repeatable backups for version control and peer review.

{% hint style="info" %}
Review export/import support in the [AIP capability matrix](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/introduction-to-gl-aip#platform-capabilities-at-a-glance).
Notable constraints: CLI edits to environment-specific overrides still require manual JSON tweaks, and automated backup tooling is driven through REST or custom scripts.
{% endhint %}

{% hint style="info" %}
In CLI snippets, resource arguments accept either the ID or a unique name. If a
name matches multiple records, use `--select` to choose the right one or provide
the full ID for deterministic promotion scripts.
{% endhint %}

{% hint style="info" %}
Data developers can focus on the CLI examples in this guide. Python samples are included for engineering teams that automate the same workflows in code.

**Example Configuration**: Start from an exported file generated with `aip agents get <agent_id> --export agent-config.yaml` or adapt the sample below.

```yaml
# agent-config.example.yaml
name: prod-research
instruction: >
  You are the production research agent. Act as a senior analyst and cite sources.
model: gpt-4o-mini
timeout: 450
mcps:
  - id: ${MCP_ID}
    description: Weather insights
tools:
  - id: ${TOOL_ID}
    config:
      region: us-east-1
metadata:
  team: insights
  environment: production
```
{% endhint %}

{% hint style="warning" %}
Configuration promotion should default to CLI export/import flows. Use `Client`
only for legacy/advanced automation where you need custom orchestration across
multiple resources.
{% endhint %}

## Export Resources

_When to use:_ Capture the current state before changes or to seed a new environment.

{% hint style="info" %}
**YAML Format Recommendation**: For better readability and version control compatibility, we recommend using YAML format (`.yaml` or `.yml` extension) for configuration files. YAML is more human-readable and handles complex nested structures better than JSON.

JSON exports/imports remain fully supported—simply switch the extension (for example, `aip agents get prod-research --export prod-research.json`). Choose JSON when you need strict tooling compatibility, and YAML when you want easier diffing of multiline prompts.
{% endhint %}

#### Agents

```bash
aip agents get prod-research --export prod-research.yaml
```

#### Tools

```bash
aip tools get query-runner --export query-runner.yaml
```

#### MCPs

```bash
aip mcps get weather-service --export weather-service.yaml
```

Add `--view md` if you need a human-readable snapshot alongside the JSON file.

## Import or Update from Files

_When to use:_ Apply reviewed configurations or roll back to a known-good version.

#### Create

```bash
aip agents create --import prod-research.yaml
```

#### Update

```bash
aip agents update prod-research --import prod-research.yaml
```

#### Python SDK

```python
from glaip_sdk import Client

client = Client()

# Create a new agent from an exported / hand-authored file
agent = client.agents.create_agent_from_file("agent-config.yaml")
print(f"Created agent {agent.name} ({agent.id}) from YAML definition.")

# Update an existing agent with the same file (supply the target agent ID)
updated = client.agents.update_agent_from_file(agent.id, "agent-config.yaml")
print(f"Updated agent {updated.name} ({updated.id}) from YAML definition.")
```

{% hint style="info" %}
File-based operations use the Client pattern since they require
bulk operations. For simple agent creation, prefer the
[Agent pattern](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/agents#agent-first-pattern-recommended).
{% endhint %}

Ensure referenced tools or MCPs exist in the target environment before creating
the agent. Export and import them in the same batch when promoting.

### Common import/export issues

| Symptom                                     | Likely cause                                             | Fix                                                                                      |
| ------------------------------------------- | -------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| JSON import fails with `schema mismatch`    | Outdated export or manual edits removed required fields. | Re-export from the latest environment and limit manual edits to sections you understand. |
| CLI prompts for confirmation mid-automation | `--force` flag omitted on destructive updates.           | Add `--force` when running non-interactive scripts.                                      |
| Tool import missing code bundle             | Referenced file path invalid or not checked into repo.   | Store zip packages alongside configs and double-check relative paths before import.      |
| Differences lost between environments       | Imports overwrite without diffing.                       | Run `git diff` or compare exports before applying and track changes in version control.  |

## Rapid Iteration Loop (CLI)

_When to use:_ Share quick adjustments with teammates or iterate during workshops.

1. **Export the current definition**

   ```bash
   aip agents get <agent_id> --export prod-research.yaml
   ```

1. **Edit the file locally** — tweak `instruction`, `language_model_id`, or
   nested `tool_configs` as needed. Keep the file under version control so you
   can diff changes between runs.

1. **Re-import immediately**

   ```bash
   aip agents update prod-research --import prod-research.yaml
   ```

1. **Validate the result** — use `aip agents run prod-research --view md` (or
   `--view json` for automation) to confirm the change behaved as expected.

Repeat the cycle until the prompt or configuration meets your needs, then commit
the JSON to your repository for peer review or promotion.

## Promotion Checklist

_When to use:_ Gate deployments with an explicit review and testing routine.

1. **Export from source environment** — pull agents, tools, MCPs, and schedules
   if applicable.
1. **Commit to version control** — store JSON files in Git for peer review.
1. **Apply environment overrides** — adjust API keys, dataset names, or tool
   configs before import.
1. **Import into target environment** — start with tools/MCPs, then agents.
1. **Smoke test** — run quick scenarios to verify connectivity and credentials.

## Validation Tips

_When to use:_ Confirm imported resources behave as expected before promoting.

- Use `aip agents run … --view json` after import to confirm the agent behaves as
  expected.
- For MCPs, run `aip mcps test-connection --from-file` prior to saving new
  credentials.
- Watch for `language_model_id` differences between environments—exported files
  retain the original ID, so adjust if the target closes over a different label.

## Automating Backups

_When to use:_ Schedule recurring exports for compliance or DR planning.

- Cron job / CI step: `aip agents list --view json | jq '.[].id'` then loop over
  IDs and export each agent nightly.
- Store artifacts in object storage with versioning (S3, GCS) for quick rollback.
- Use the [Automation & scripting guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/automation-and-scripting) for shell
  and Python templates.

## Related Documentation

- [Agents guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/agents) — understand payload structure and runtime
  overrides.
- [Tools guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/tools) — capture custom tool source alongside exports.
- [Automation & scripting](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/automation-and-scripting) — run exports in CI or
  scheduled jobs.
