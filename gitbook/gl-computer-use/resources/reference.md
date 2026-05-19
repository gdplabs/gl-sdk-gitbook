---
icon: gear
---

# SDK Reference

Complete GL Computer Use public API contract.

## Package

Install the core SDK:

```bash
pip install gl-computer-use
```

Optional extras:

| Extra | Installs | Purpose |
|---|---|---|
| `recording` | Playwright, Pillow | WebM session recording |
| `agents` | Simular-AI Agent-S, pyautogui | Agent-S provider |
| `opensandbox` | Alibaba OpenSandbox client | OpenSandbox provider |
| `minio` | aiobotocore | MinIO / S3-compatible artifact store |
| `retries` | tenacity | Retry logic |
| `observability` | gl-observability, tenacity | OTLP tracing, metrics, Sentry |
| `all` | All of the above | Full feature set |

## Public Classes

### Client

<table data-header-hidden><thead><tr><th width="180"></th><th></th></tr></thead><tbody>
<tr><td><strong>Class</strong></td><td><code>GLComputerUseClient</code></td></tr>
<tr><td><strong>Constructor</strong></td><td><code>GLComputerUseClient(config=None)</code></td></tr>
<tr><td><strong>Run methods</strong></td><td><code>run(prompt, ...)</code>, <code>run_once(prompt, ...)</code>, <code>run_sync(prompt, ...)</code></td></tr>
<tr><td><strong>Session (Layer 2)</strong></td><td><code>async with client.session() as s:</code></td></tr>
</tbody></table>

### Configuration

<table data-header-hidden><thead><tr><th width="180"></th><th></th></tr></thead><tbody>
<tr><td><strong>Class</strong></td><td><code>GLComputerUseConfig</code></td></tr>
<tr><td><strong>Loading</strong></td><td>Environment variables (<code>GLCU_*</code>), <code>.env</code> file, or explicit constructor fields</td></tr>
<tr><td><strong>Validation</strong></td><td>Raises <code>ConfigError</code> when required credentials are missing</td></tr>
</tbody></table>

### Provider Registration

| Function | Base class | Config key |
|---|---|---|
| `register_sandbox(name, cls)` | `BaseSandbox` | `GLComputerUseConfig(sandbox=name)` |
| `register_agent(name, cls)` | `BaseAgent` | `GLComputerUseConfig(agent=name)` |
| `register_artifact(name, cls)` | `BaseArtifact` | `GLComputerUseConfig(artifact=name)` |

## Configuration Variables

All fields are readable from environment variables with the `GLCU_` prefix.

### Core

| Variable | Default | Description |
|---|---|---|
| `GLCU_AGENT` | `"cua"` | Agent provider: `"cua"` or `"agents"` |
| `GLCU_SANDBOX` | `"e2b"` | Sandbox provider: `"e2b"` or `"opensandbox"` |
| `GLCU_ARTIFACT` | `"local"` | Artifact store: `"local"` or `"minio"` |
| `GLCU_MODEL` | `"anthropic/claude-sonnet-4-6"` | LLM in `provider/name` format |
| `GLCU_TIMEOUT` | `600` | Task timeout in seconds |
| `GLCU_MAX_STEPS` | `100` | Max agent loop iterations before policy takeover |
| `GLCU_STREAM_QUEUE_SIZE` | `64` | Max events buffered in the streaming queue |

### API Keys

| Variable | Default | Description |
|---|---|---|
| `GLCU_E2B_API_KEY` | `None` | E2B Desktop API key (required for `sandbox="e2b"`) |
| `GLCU_E2B_TIMEOUT` | `600` | Max E2B sandbox lifetime in seconds (capped at 3600) |
| `GLCU_ANTHROPIC_API_KEY` | `None` | Anthropic API key (required for `anthropic/*` models) |
| `GLCU_OPENAI_API_KEY` | `None` | OpenAI API key (required for `openai/*` models) |

### Artifact Storage

| Variable | Default | Description |
|---|---|---|
| `GLCU_LOCAL_ARTIFACT_DIR` | `"./artifacts"` | Directory for local screenshots and recordings |
| `GLCU_OBJECT_STORE_ENDPOINT` | `""` | MinIO/S3 host:port or full URL |
| `GLCU_OBJECT_STORE_ACCESS_KEY` | `""` | MinIO/S3 access key |
| `GLCU_OBJECT_STORE_SECRET_KEY` | `""` | MinIO/S3 secret key |
| `GLCU_OBJECT_STORE_BUCKET` | `"gl-computer-use"` | MinIO/S3 bucket name |
| `GLCU_PRESIGNED_URL_EXPIRY_SECONDS` | `3600` | Presigned URL TTL in seconds |

### Takeover

| Variable | Default | Description |
|---|---|---|
| `GLCU_REPEATED_NOOP_THRESHOLD` | `6` | Consecutive no-ops before policy takeover |
| `GLCU_AGENT_STUCK_PATTERNS` | `"i need help,i'm stuck,..."` | Comma-separated phrases that trigger agent-requested takeover |

### Agent-S Specific

| Variable | Default | Description |
|---|---|---|
| `GLCU_AGENTS_PLATFORM` | `"ubuntu"` | OS for Agent-S: `"ubuntu"`, `"macos"`, or `"windows"` |
| `GLCU_AGENTS_GROUNDING_MODEL` | `""` | Agent-S grounding model (empty = reuse main model) |
| `GLCU_AGENTS_ENABLE_REFLECTION` | `false` | Enable Agent-S ReflectionAgent |
| `GLCU_AGENTS_STEP_DELAY` | `0.5` | Seconds to sleep between Agent-S steps |
| `GLCU_AGENTS_MAX_STEPS` | `50` | Max Agent-S steps (independent of `GLCU_MAX_STEPS`) |

### OpenSandbox Specific

| Variable | Default | Description |
|---|---|---|
| `GLCU_OPENSANDBOX_API_KEY` | `None` | Alibaba OpenSandbox API key |
| `GLCU_OPENSANDBOX_DOMAIN` | `"localhost:8080"` | OpenSandbox host:port or URL |
| `GLCU_OPENSANDBOX_PROTOCOL` | `"http"` | Default scheme when domain has no prefix |
| `GLCU_OPENSANDBOX_SERVER_PROXY` | `false` | Use gateway/proxy mode (required on EC2) |

### Logging

| Variable | Default | Description |
|---|---|---|
| `GLCU_LOG_LEVEL` | `"INFO"` | `"DEBUG"`, `"INFO"`, `"WARNING"`, or `"ERROR"` |
| `GLCU_LOG_FORMAT` | `"json"` | `"json"` (structured) or `"console"` (human-readable) |

### Observability

| Variable | Default | Description |
|---|---|---|
| `GLCU_OTEL_ENABLED` | `false` | Enable OpenTelemetry tracing and metrics |
| `GLCU_OTEL_SERVICE_NAME` | `"gl-computer-use"` | OTel service name for trace attribution |
| `GLCU_OTEL_EXPORTER_ENDPOINT` | `None` | OTLP gRPC or HTTP endpoint URL |
| `GLCU_OTEL_USE_GRPC` | `true` | Use gRPC (`true`) or HTTP (`false`) for OTLP |
| `GLCU_OTEL_HEADERS` | `None` | Optional OTLP exporter headers (auth tokens) as JSON |
| `GLCU_PII_REDACTION_ENABLED` | `false` | Enable regex-based PII redaction on logs |
| `GLCU_SENTRY_ENABLED` | `false` | Enable Sentry error tracking |
| `GLCU_SENTRY_DSN` | `None` | Sentry project DSN |
| `GLCU_SENTRY_ENVIRONMENT` | `None` | Sentry environment tag (e.g. `production`) |
| `GLCU_SENTRY_RELEASE` | `None` | Sentry release string |

## Run Methods

| Method | Signature | Returns | Raises |
|---|---|---|---|
| `run` | `async (prompt, *, config, timeout, files, retrieve_files, on_takeover_needed)` | `StreamClient` | `ConfigError`, `SandboxProvisionError` |
| `run_once` | `async (prompt, ...)` | `TaskResult` | `TaskFailedError`, `TaskCancelledError`, `GLTimeoutError` |
| `run_sync` | `(prompt, ...)` | `TaskResult` | Same as `run_once` |

## Event Types

| Event | Payload fields |
|---|---|
| `SANDBOX_READY` | `stream_url` |
| `TASK_STARTED` | `prompt` |
| `STEP_COMPLETED` | `step_index`, `action` (ActionDetail), `reasoning`, `message`, `screenshot_b64` |
| `TASK_COMPLETED` | `result` (TaskResult) |
| `TASK_FAILED` | `error`, `result` |
| `TASK_CANCELLED` | — |
| `TAKEOVER_STARTED` | `reason`, `stream_url` |
| `TAKEOVER_RESUMED` | `message` |

## TaskResult Fields

| Field | Type | Description |
|---|---|---|
| `task_id` | `str` | Unique task identifier |
| `status` | `"COMPLETED" \| "FAILED" \| "CANCELLED"` | Terminal status |
| `output` | `str \| None` | Agent's final textual answer |
| `steps` | `list[TaskEvent]` | All `STEP_COMPLETED` events in order |
| `error` | `str \| None` | Error message when status is `FAILED` |
| `stream_url` | `str \| None` | noVNC URL active during this task |
| `screenshot_urls` | `list[str]` | Presigned URLs for per-step screenshots |
| `file_urls` | `dict[str, str]` | Sandbox path → presigned URL for retrieved files |
| `recording_url` | `str \| None` | Presigned URL for the session recording |
| `recording_status` | `"UPLOADED" \| "PARTIAL" \| "FAILED"` | Recording upload status |
| `metadata` | `dict[str, Any]` | Timing, model, and provider diagnostics |

## ActionDetail Fields

| Field | Type | Description |
|---|---|---|
| `type` | `str` | Action kind: `click`, `type`, `key`, `scroll`, `screenshot`, `move`, etc. |
| `coordinate` | `tuple[int, int] \| None` | `(x, y)` pixel coordinate for pointer actions |
| `text` | `str \| None` | Text for `type` actions |
| `key` | `str \| None` | Key combo for `key` actions |
| `direction` | `str \| None` | Scroll direction |
| `amount` | `int \| None` | Scroll amount |
| `raw` | `dict \| None` | Original provider-specific payload |

## Exception Hierarchy

| Exception | Extends | When raised |
|---|---|---|
| `GLComputerUseError` | `Exception` | Base for all SDK errors |
| `ConfigError` | `GLComputerUseError` | Missing or invalid credentials/config |
| `GLConnectionError` | `GLComputerUseError` | Cannot reach sandbox backend or object store |
| `SandboxProvisionError` | `GLComputerUseError` | Sandbox allocation failed |
| `SandboxError` | `GLComputerUseError` | General sandbox error |
| `AgentError` | `GLComputerUseError` | Agent encountered unrecoverable error |
| `DesktopError` | `GLComputerUseError` | Desktop interaction operation failed |
| `TaskFailedError` | `GLComputerUseError` | Agent loop terminated with `TASK_FAILED` |
| `TaskCancelledError` | `GLComputerUseError` | Task cancelled before completion |
| `TakeoverRequiredError` | `GLComputerUseError` | Takeover triggered but no callback supplied |
| `TakeoverInProgressError` | `GLComputerUseError` | Takeover already active |
| `TakeoverNotActiveError` | `GLComputerUseError` | Resume called without an active takeover |
| `SessionBusyError` | `GLComputerUseError` | Operation on an already-executing task |
| `SessionNotReadyError` | `GLComputerUseError` | Operation requires `sandbox.prepare()` first |
| `ArtifactStoreError` | `GLComputerUseError` | Artifact storage operation failed |
| `GLTimeoutError` | `GLComputerUseError` | Task exceeded configured timeout |
