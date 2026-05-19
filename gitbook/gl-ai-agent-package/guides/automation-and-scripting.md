---
icon: terminal
---

Automate AIP workflows from Python scripts, shell pipelines, or CI jobs. Use
this guide when you need repeatable patterns for consistent output formats,
resource promotion, and scheduling hooks that teammates can reuse across
environments.

{% hint style="info" %}
For a full capability breakdown, refer to the [AIP matrix](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/introduction-to-gl-aip#platform-capabilities-at-a-glance).
Scheduling is available via the Python SDK. CLI scheduling commands are under development.
{% endhint %}

{% hint style="info" %}
CLI automations can target resources by ID or unique name. When scripting loops,
prefer IDs or add `--select` handling so partial name matches do not prompt for
input mid-run.
{% endhint %}

{% hint style="info" %}
This guide is SDK-first (Python). CLI equivalents are included when they add unique low-code value.
{% endhint %}

{% hint style="warning" %}
`Client` snippets in this guide are legacy/advanced automation paths. Prefer
Agent-first execution (`Agent(...)`, `agent.run(...)`, `agent.deploy()`) for
new scripts unless you need workspace-wide admin operations.
{% endhint %}

## Choose the Right Output Format

_When to use:_ Tailor CLI output for downstream systems, docs, or logs before integrating into scripts.

#### Python SDK

```python
from glaip_sdk import Client

client = Client()
agent = client.agents.get_agent_by_id("analytics-agent")

# Rich text (default renderer)
print(agent.run("Provide a concise summary"))

# Plain output for scripting
print(agent.run("List KPIs", renderer="plain"))
```

#### CLI

```bash
# JSON for automation
aip agents get analytics-agent --view json > agent.json

# Markdown for docs
aip agents run analytics-agent --input "Create summary" --view md > REPORT.md

# Plain text for logs
aip agents run analytics-agent --input "Quick check" --view plain
```

## Script Resource Promotion

_When to use:_ Promote agents and tools between sandboxes, staging, and production with audit trails.

Use the export/import workflows from the
[Configuration management guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/configuration-management)
as the source of truth. When you automate them, wrap the commands so your CI job
can back up or promote resources in one run:

```bash
#!/usr/bin/env bash
set -euo pipefail

mkdir -p exports

agents=(prod-research ops-analyst)
tools=(query-runner mcp-sync)

for agent in "${agents[@]}"; do
  aip agents get "$agent" --export "exports/agent-${agent}.json"
done

for tool in "${tools[@]}"; do
  aip tools get "$tool" --export "exports/tool-${tool}.json"
done

# Promote the JSON with the create/update commands from the configuration guide
# after your change review passes.
```

The script centralises resource selection for CI but defers ordering, validation,
and import strategy to the configuration guide’s checklist.

## Automate Prompt Iteration

_When to use:_ Batch-run prompts for evaluation, regression testing, or manual review.

Extend the configuration guide’s rapid-iteration loop with automation steps
that enforce reproducibility. Example nightly job:

```bash
#!/usr/bin/env bash
set -euo pipefail

AGENT_ID="prod-research"
EXPORT="exports/${AGENT_ID}.json"

aip agents get "${AGENT_ID}" --export "$EXPORT"

tmp=$(mktemp)
jq '.instruction = "Summarise latest earnings with KPIs"' "$EXPORT" > "$tmp"
mv "$tmp" "$EXPORT"

aip agents update "${AGENT_ID}" --import "$EXPORT"
aip agents run "${AGENT_ID}" --input "Smoke test" --view md > artifacts/${AGENT_ID}-smoke.md

git add "$EXPORT" artifacts/${AGENT_ID}-smoke.md
```

This focuses on the scripting concerns—file paths, idempotent edits, and
artifact capture—while the linked configuration guide covers the manual review
and promotion steps.

## Run Agents in CI

_When to use:_ Block deployments until sanity checks pass or surface usage metrics in pipelines.

```bash
#!/usr/bin/env bash
set -euo pipefail

: "${AIP_API_URL:?Missing AIP_API_URL}"
: "${AIP_API_KEY:?Missing AIP_API_KEY}"

aip agents run prod-research \
  --input "Generate daily summary" \
  --view json > artifacts/daily_summary.json
```

Store credentials in your CI secret manager and inject them as environment
variables before executing.

## Python Automation Pattern

_When to use:_ Embed agent calls inside existing Python services, notebooks, or ETL jobs.

```python
from glaip_sdk import Client

client = Client()

agent = client.agents.get_agent_by_id("prod-research")
result = agent.run(
    "Generate daily summary",
    runtime_config={
        "tool_configs": {
            "query-runner": {"dataset": "daily_metrics"}
        }
    },
    renderer="silent",
)
print(result)
```

The `renderer="silent"` option suppresses streaming UI output so your script can
capture the final text response directly.

## Schedule Runs

_When to use:_ Run the same agent input on a recurring timetable. Schedules execute automatically in the Asia/Jakarta (WIB) timezone.

Schedules require an `agent_id`, `input`, and a schedule. In the SDK you can pass either a cron string or a structured config. Cron strings use five fields: `minute hour day_of_month month day_of_week`. Each field supports `*`, ranges (e.g., `2-4`), lists (`0,6`), and steps (`*/N`).

```python
from glaip_sdk import Client
from glaip_sdk.models.schedule import ScheduleConfig

client = Client()

# Create a schedule for an agent
schedule = client.schedules.create(
    agent_id="agent-123",
    input="Generate daily summary report",
    schedule=ScheduleConfig(
        minute="0",
        hour="9",
        day_of_month="*",
        month="*",
        day_of_week="0-4",  # Monday to Friday
    ),
)

# Or use a cron string directly
schedule = client.schedules.create(
    agent_id="agent-123",
    input="Weekly status update",
    schedule="0 10 * * 0",  # Every Monday at 10am
)

# List all schedules
schedules = client.schedules.list()
for s in schedules:
    print(f"{s.id}: next run at {s.next_run_time}")

# List schedules for a specific agent
agent_schedules = client.schedules.list(agent_id="agent-123")

# Update a schedule
# Note: Omit schedule to keep the existing timing. Any provided schedule fills missing fields with "*".
updated = client.schedules.update(
    schedule.id,
    input="Updated daily report",
    schedule=ScheduleConfig(minute="30", hour="9"),
)

# Delete a schedule
client.schedules.delete(schedule.id)
```

You can also use the agent facade for schedule operations; it infers `agent_id` from the `Agent` instance:

```python
agent = client.agents.get_agent_by_id("agent-123")

# Create schedule via agent
schedule = agent.schedule.create(
    input="Daily task",
    schedule="0 8 * * *",
)

# List runs for this schedule
runs = schedule.list_runs(limit=10)
for run in runs:
    if run.status == "success":
        result = run.get_result()
        print(f"Run {run.id}: {run.duration}")
```

CLI commands for scheduling are under development. Use the SDK for now.

### Schedule Configuration

| Field          | Format                        | Examples          | Description                |
| -------------- | ----------------------------- | ----------------- | -------------------------- |
| `minute`       | 0-59, \*, \*/N, ranges, lists | `0`, `*/15`, `30` | Minute of the hour         |
| `hour`         | 0-23, \*, \*/N, ranges, lists | `9`, `*/2`, `0`   | Hour of the day (WIB)      |
| `day_of_month` | 1-31, \*, ranges, lists       | `1`, `15`, `*`    | Day of the month           |
| `month`        | 1-12, \*, \*/N, ranges, lists | `1`, `*/3`, `*`   | Month of the year          |
| `day_of_week`  | 0-6, \*, \*/N, ranges, lists  | `0-4`, `0,6`, `*` | Day of week (0=Mon, 6=Sun) |

{% hint style="info" %}
All schedules run in Asia/Jakarta (WIB) timezone. Plan your cron expressions accordingly.
{% endhint %}

### Schedule Run History

Retrieve execution history for scheduled runs, including status, duration, and output.
Run history is scoped to an agent; use `schedule_id` to narrow results, and a `run_id` to fetch output. These APIs return scheduled runs only.

List runs to filter by schedule, status, or paginate through history.

```python
# List all scheduled runs for an agent
runs = client.schedules.list_runs(agent_id="agent-123")

# Filter by specific schedule
runs = client.schedules.list_runs(
    agent_id="agent-123",
    schedule_id="schedule-abc",
    limit=10,
)

# Filter by status (started, success, failed, cancelled, aborted, unavailable)
successful_runs = client.schedules.list_runs(
    agent_id="agent-123",
    status="success",
)

# Via schedule instance
schedule = client.schedules.get("schedule-abc")
runs = schedule.list_runs(status="success", limit=20)
```

Get run results to fetch full output and metadata for a specific run.

```python
# From a ScheduleRun instance
for run in runs:
    print(f"Run ID: {run.id}")
    print(f"Status: {run.status}")
    print(f"Started: {run.started_at}")
    print(f"Duration: {run.duration}")

    # Get full output
    if run.status in ["success", "failed"]:
        result = run.get_result()
        # result.output contains the SSE output chunks
        # result.schedule_id links back to the schedule
```

Run status values:

| Status        | Description                |
| ------------- | -------------------------- |
| `started`     | Run has started execution  |
| `success`     | Run completed successfully |
| `failed`      | Run encountered an error   |
| `cancelled`   | Run was cancelled          |
| `aborted`     | Run was aborted            |
| `unavailable` | Run result is unavailable  |

### Common automation failures

| Symptom                                 | Likely cause                                          | Fix                                                                                                                               |
| --------------------------------------- | ----------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Cron job exits with `command not found` | `aip` not on the scheduler PATH.                      | Prefix with the full path or source the profile before invoking the CLI.                                                          |
| CI run fails with `401 Unauthorized`    | Expired or missing API key in the runner environment. | Rotate credentials and inject them via secrets or environment variables per job.                                                  |
| Scripts hang on interactive prompts     | CLI fuzzy search triggered by unfiltered lists.       | Pass IDs, use `--select`, add a filter flag (`--name`, `--type`, etc.), or force `--simple` when you need non-interactive output. |
| SDK automation times out intermittently | Backend slow or default timeout too low.              | Increase `Client(timeout=...)` or add retry logic with exponential backoff.                                                       |

## Automation Tips

_When to use:_ Sense-check your automation plan before scaling or handing it off to new team members.

1. **Use JSON everywhere** — it is the most resilient format for piping into
   tests or dashboards.
1. **Keep exports in Git** — treat agent/tool JSON like infrastructure-as-code
   and review changes via pull requests.
1. **Log run IDs** — responses include `X-Run-ID`; store it to trace streaming
   output later.
1. **Fail fast in CI** — run `set -euo pipefail` (Bash) or equivalent constructs
   to surface agent errors quickly.

## Related Documentation

- [Install & Configure](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/prerequisites) — bootstrap
  environments for automation servers.
- [Agents guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/agents) — full lifecycle and runtime overrides.
- [Configuration management](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/configuration-management) — promote resources
  between environments.
- [CLI commands reference](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/cli-commands) — explore automation
  flags in detail.
