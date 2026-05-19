---
icon: shield-quartered
---

Protect sensitive data while using the AIP SDK and CLI. This guide covers PII
masking, tool-output controls, memory scoping, and API key hygiene.

> **Success**
>
> **When to use this guide:** You handle regulated data, govern tooling access, or perform privacy reviews on agent configurations.
>
> **Who benefits:** Security engineers, PMs overseeing compliance, and data developers stewarding user content.

{% hint style="info" %}
Security features by surface are tracked in the [AIP capability matrix](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/introduction-to-gl-aip#platform-capabilities-at-a-glance).
Key gaps today: CLI still relies on export/import for `pii_mapping`, memory, and tool-output toggles. Presigned URL regeneration and some auditing workflows use REST reference endpoints.
{% endhint %}

## Mask PII During Runs

_When to use:_ Redact sensitive inputs or outputs before sharing transcripts or artifacts.

{% hint style="warning" %}
**Prerequisites:** To use PII masking features, install the privacy extra:

```bash
pip install --upgrade "glaip-sdk[privacy]"
```

**Installation options:**

- **Remote mode only:** `glaip-sdk[privacy]` - Privacy features work with remote API calls
- **Local mode only:** `glaip-sdk[local]` - For local agent execution without privacy
- **Local mode with privacy:** `glaip-sdk[local,privacy]` - For local execution with PII masking
- **All features:** `glaip-sdk[local,privacy,memory]` - Local execution with privacy and memory features
{% endhint %}

```python
from glaip_sdk import Agent

agent = Agent(name="secure-processor", instruction="Process sensitive inputs.")
response = agent.run(
    "Process <EMAIL_1> order",
    pii_mapping={
        "<EMAIL_1>": "customer@example.com",
        "<NAME_1>": "Alex Taylor",
    },
)
print(response)
```

{% hint style="info" %}
Until CLI flags ship, export the agent JSON, add a `pii_mapping` example, and
re-import for automation scenarios.
{% endhint %}

### Common security gaps

| Symptom                                      | Likely cause                                                    | Fix                                                                |
| -------------------------------------------- | --------------------------------------------------------------- | ------------------------------------------------------------------ |
| PII still appears in outputs                 | Redaction rules incomplete or mismatch between SDK and backend. | Expand `pii_mapping` entries and test with sample payloads.        |
| Shared artifacts visible to unintended teams | `agent_config.tool_output_sharing` left enabled.                | Disable sharing or scope agents per team.                          |
| Keys leaked in repos                         | Credentials stored in `.env` committed accidentally.            | Add `.env` to `.gitignore`, rotate keys, and use secrets managers. |
| Expired presigned URLs break workflows       | Long-running jobs using stale download links.                   | Regenerate URLs via the REST Utilities reference (internal integrations). |

## Control Tool Output Sharing

_When to use:_ Limit which agents or collaborators can see tool artifacts.

```python
agent.update(agent_config={"tool_output_sharing": False})
```

- `True` — downstream agents can reuse artifacts and tables produced by the
  agent.
- `False` — artifacts stay isolated to the producing agent.

Configure the field through agent payloads; the CLI will expose a dedicated flag
in a future release.

## Manage Memory Scope

_When to use:_ Keep conversation history compliant while preserving useful context.

Use `agent_config["memory"] = "mem0"` to persist conversation state between
runs. Share memory only when agents belong to the same account and should retain
context; otherwise leave memory unset for stateless behaviour.

## API Key Hygiene

_When to use:_ Rotate, scope, and store credentials safely across teams.

1. Issue separate keys per environment (dev/staging/production).
1. Store keys in environment variables or secure stores (`aip accounts add` saves
   them locally under `~/.aip/config.yaml`).
1. Rotate keys regularly and revoke unused values after testing.

## Presigned Artifact Management

_When to use:_ Secure file downloads and prevent stale links from leaking data.

- Each run response may include presigned URLs for attached artifacts.
- If a URL expires and you need to regenerate it from an internal integration, use the REST reference only:
- REST reference: [Utilities](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/rest-api/utilities)
- Keep regenerated URLs short-lived and avoid sharing them broadly.

## Audit Trails

_When to use:_ Document who changed what and when for compliance or incident response.

Use run history to trace PII usage, artifact creation, and tool activity.

Python SDK:

```python
from glaip_sdk import Client

client = Client()
runs = client.agents.runs.list_runs(agent_id="<AGENT_ID>", limit=20, page=1)
for run in runs.data:
    print(run.id, run.created_at)
```

CLI (saved locally):

```bash
/transcripts
```

## Related Documentation

- [Agents guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/agents) — configure `pii_mapping`, `tool_configs`, and
  memory alongside other agent features.
- [File processing](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/file-processing) — handle attached artifacts and chunk
  reuse securely.
- [Automation & scripting](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/automation-and-scripting) — integrate security checks
  into CI pipelines.
