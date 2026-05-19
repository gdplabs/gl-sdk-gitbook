Backend API for the GL AIP (GDP Labs AI Agents Package) covering agents, tools, MCP connections, language models, accounts, and utilities. The canonical OpenAPI document is published at [https://aip.glair.ai/docs](https://aip.glair.ai/docs) and is updated alongside every GL AIP package release.

## Base URLs

| Environment       | Base URL                 | Notes                 |
| ----------------- | ------------------------ | --------------------- |
| Production        | `https://aip.glair.ai`   | Use issued API key.   |
| Local development | `http://localhost:8000`  | Default FastAPI port. |

All paths documented below are relative to the chosen base URL.

## Authentication

Unless noted, endpoints require an API key presented in the `X-API-Key` header. The specification defines the `APIKeyHeader` security scheme.

{% hint style="info" %}
Include your API key in requests using the `X-API-Key` header:

```http
X-API-Key: <your-api-key>
```

Endpoints marked with `Authentication: None` are publicly accessible (for example, `POST /accounts`).
{% endhint %}

## Response Envelope

Most JSON responses follow this envelope (streaming endpoints return SSE events instead):

```json
{
  "success": true,
  "data": { ... },
  "message": "Operation successful",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

Error responses set `success` to `false` and include an `error` payload with diagnostic context.

## Endpoint Index

- [Health Checks](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/rest-api/health-checks)
- [Accounts](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/rest-api/accounts)
- [Agents](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/rest-api/agents)
- [Tools](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/rest-api/tools)
- [Model Context Protocol (MCP)](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/rest-api/mcps)
- [Language Models](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/rest-api/language-models)
- [Utilities](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/rest-api/utilities)
- [Schema Components](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/rest-api/schemas)
- [Human-in-the-Loop Workflow](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/rest-api/hitl)
- [HITL Audit Log](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/rest-api/hitl-audit-log)
- [HITL REST Workflow Guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/rest-api/hitl-rest-workflow-guide)
