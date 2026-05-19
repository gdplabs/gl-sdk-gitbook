---
icon: file-import
---

Attach files to agent runs, reuse artifacts from prior attachments, and manage chunk IDs for
long-form analysis. Reach for this guide when agents need to consume documents,
transcripts, or datasets with the Python SDK. CLI support exists for common flows. REST is reference-only.

{% hint style="info" %}
File-handling support is summarised in the [AIP capability matrix](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/introduction-to-gl-aip#platform-capabilities-at-a-glance).
The main limitation today is regenerating presigned URLs. Use the REST reference endpoint when a URL expires.
{% endhint %}

{% hint style="info" %}
`aip agents run` accepts either an agent ID or a unique name. Use `--select` to
pick from partial name matches or provide the ID directly when scripting.
{% endhint %}

## Attach Files to an Agent Run

_When to use:_ Collect fresh documents from users or pipelines and supply them during execution.

{% hint style="info" %}
**Local Document Processing:** For local execution, you can use document loader tools like `PDFReaderTool`, `DocxReaderTool`, and `ExcelReaderTool` from `aip-agents` to read files directly from disk without uploading to the server. Attach the file in the same run so the tool has access to it. See the [Local vs Remote guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/getting-started/local-vs-remote) for the document loader tools quickstart and example (`main_with_docproc_pdf.py`).
{% endhint %}

#### Python SDK

```python
from glaip_sdk import Agent

agent = Agent(name="analysis-agent", instruction="You analyze documents.")

response = agent.run(
    "Summarise the document and extract key metrics",
    files=["./reports/q1.pdf", "./reports/q2.pdf"],
)
print(response)
```

#### CLI

```bash
aip agents run analysis-agent \
  --input "Summarise these reports" \
  --file reports/q1.pdf \
  --file reports/q2.pdf \
  --view json > summary.json
```

### Common attachment errors

| Symptom                         | Likely cause                                      | Fix                                                                                     |
| ------------------------------- | ------------------------------------------------- | --------------------------------------------------------------------------------------- |
| `413 Payload Too Large`         | File exceeds backend attachment/upload limits.    | Compress the file or split it into smaller chunks.                                      |
| Missing file in run logs        | File path incorrect or permissions denied.        | Double-check the path, ensure the process can read the file, or use absolute paths.     |
| Duplicate chunks created        | Run attaches files without reusing `artifact_id`. | Pass the stored chunk IDs using the reuse workflows in the next section.                |
| `Unsupported media type` errors | File type not allowed for ingestion.              | Convert to a supported format (PDF, TXT, DOCX) or register a custom ingestion pipeline. |

## Reuse Chunk IDs from Prior Attachments

_When to use:_ Avoid re-ingesting the same files while keeping chunk IDs stable across runs.

When the backend returns `chunk_ids`, store them for later runs:

```python
chunk_ids = ["chunk-abc", "chunk-def"]
agent.run(
    "Compare the latest reports with previous attachments",
    chunk_ids=chunk_ids,
)
```

{% hint style="info" %}
CLI support for passing `chunk_ids` is coming soon. Use the SDK today to avoid re-attaching large files (REST is reference-only).
{% endhint %}

## Retrieve Artifacts and Output

_When to use:_ Capture the processed results, enriched files, or generated reports after execution.

1. Capture the run ID from the streaming response (`X-Run-ID`).

1. List run history with the SDK:

   ```python
   from glaip_sdk import Client

   client = Client()
   runs = client.agents.runs.list_runs(agent_id="agent-id", limit=20, page=1)
   print([r.id for r in runs.data])
   ```

1. Download artifacts directly from the presigned URLs in the response. If a URL
   has expired, regenerate it using the REST reference utilities (internal integrations only):
   [Utilities](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/rest-api/utilities).

## Best Practices

_When to use:_ Create organisation-wide guardrails for storage, retention, and compliance.

- **Compress large files** — keep attachments efficient and within allowable limits.
- **Track chunk IDs** — store them alongside run metadata so you can reference
  prior attachments without retransmitting data.
- **Sanitise inputs** — redaction or PII masking should occur before attaching
  sensitive documents; see the [Security & privacy guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/security-and-privacy).
- **Automate clean-up** — if you are storing artifacts locally for auditing,
  ensure rotation policies are in place.

## Related Documentation

- [Local vs Remote](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/getting-started/local-vs-remote) — local vs remote file processing comparison and built-in tools overview.
- [Agents guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/agents) — streaming behaviour and runtime overrides.
- [Automation & scripting](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/automation-and-scripting) — capture outputs in CI
  pipelines.
- [Configuration management](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/configuration-management) — export/import
  agents that rely on file workflows.
