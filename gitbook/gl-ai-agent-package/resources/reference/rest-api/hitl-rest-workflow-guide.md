Step-by-step reference for Human-in-the-Loop (HITL) REST orchestration.

## Primary Workflow

Use the canonical workflow page:

- [HITL](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/rest-api/hitl)

That page covers:

1. Agent creation with HITL enabled.
2. Streaming execution and pause detection.
3. Decision submission (`approved`, `rejected`, `skipped`).
4. Pending request listing.

## Integration Checklist

- Keep SSE connection active while waiting for operator decisions.
- Surface `request_id` and timeout metadata in operator UI.
- Handle timeout paths explicitly (`timeout_skip`).
- Persist operator rationale for post-run audit and review.

## Related

- [HITL Audit Log](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/rest-api/hitl-audit-log)
- [Agents REST Reference](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/rest-api/agents)
