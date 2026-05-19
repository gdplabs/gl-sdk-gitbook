---
icon: gear
---

# SDK Reference

This page summarizes the public GL Browser Use runtime contract.

## Package

Install the core package:

```bash
pip install gl-browser-use
```

Optional extras:

1. `gl-browser-use[steel]`: Steel browser infrastructure.
2. `gl-browser-use[infrastructure]`: all browser infrastructure providers.
3. `gl-browser-use[minio]`: MinIO/S3-compatible object storage.
4. `gl-browser-use[storage]`: all object storage providers.
5. `gl-browser-use[full]`: all infrastructure and storage providers.

## Public Classes

### **Client**

<table data-header-hidden><thead><tr><th width="197"></th><th></th></tr></thead><tbody>
<tr><td><strong>Class</strong></td><td><code>BrowserUseClient</code></td></tr>
<tr><td><strong>Purpose</strong></td><td>Runs browser automation tasks through <code>browser-use</code>.</td></tr>
<tr><td><strong>Constructor</strong></td><td><code>BrowserUseClient(*, config, infrastructure=None, storage=None)</code></td></tr>
<tr><td><strong>Run methods</strong></td><td><code>run(task)</code>, <code>run_once(task)</code>, <code>run_sync(task)</code></td></tr>
</tbody></table>

### **Configuration**

<table data-header-hidden><thead><tr><th width="197"></th><th></th></tr></thead><tbody>
<tr><td><strong>Class</strong></td><td><code>BrowserUseClientConfig</code></td></tr>
<tr><td><strong>Purpose</strong></td><td>Typed runtime configuration for model credentials, models, timeouts, logging, and retry behavior.</td></tr>
<tr><td><strong>Required credentials</strong></td><td><code>llm_openai_api_key</code> and <code>page_extraction_llm_openai_api_key</code>. Both default to <code>OPENAI_API_KEY</code> when omitted.</td></tr>
<tr><td><strong>Validation</strong></td><td>Raises <code>BrowserUseConfigurationError</code> when strict validation fails.</td></tr>
</tbody></table>

### **Infrastructure**

<table data-header-hidden><thead><tr><th width="197"></th><th></th></tr></thead><tbody>
<tr><td><strong>Base class</strong></td><td><code>BrowserInfrastructure</code></td></tr>
<tr><td><strong>Context</strong></td><td><code>BrowserInfrastructureContext</code></td></tr>
<tr><td><strong>Built-in implementation</strong></td><td><code>SteelBrowserInfrastructure</code></td></tr>
<tr><td><strong>Provider extra</strong></td><td><code>gl-browser-use[steel]</code></td></tr>
<tr><td><strong>Default credential source</strong></td><td><code>STEEL_API_KEY</code></td></tr>
</tbody></table>

### **Storage**

<table data-header-hidden><thead><tr><th width="197"></th><th></th></tr></thead><tbody>
<tr><td><strong>Base class</strong></td><td><code>ObjectStorage</code></td></tr>
<tr><td><strong>Built-in implementation</strong></td><td><code>MinIOS3CompatibleStorage</code></td></tr>
<tr><td><strong>Provider extra</strong></td><td><code>gl-browser-use[minio]</code></td></tr>
<tr><td><strong>Default credential source</strong></td><td><code>OBJECT_STORAGE_URL</code>, <code>OBJECT_STORAGE_USERNAME</code>, <code>OBJECT_STORAGE_PASSWORD</code>, and <code>OBJECT_STORAGE_BUCKET_NAME</code></td></tr>
<tr><td><strong>Default object prefix</strong></td><td><code>browser-recordings/</code>, optionally nested under <code>OBJECT_STORAGE_DIRECTORY_PREFIX</code></td></tr>
</tbody></table>

## Configuration Fields

| Field | Default | Description |
| ----- | ------- | ----------- |
| `llm_openai_api_key` | `OPENAI_API_KEY` | API key for the primary browser-control model. |
| `llm_openai_model` | `o3` | Primary browser-control model. |
| `llm_openai_temperature` | `None` | Primary model temperature when supported by the selected model. |
| `llm_openai_reasoning_effort` | `low` | Primary reasoning intensity. |
| `llm_openai_base_url` | `None` | Optional HTTP or HTTPS base URL override. |
| `page_extraction_llm_openai_api_key` | `OPENAI_API_KEY` | API key for page extraction. |
| `page_extraction_llm_openai_model` | `gpt-5-mini` | Page extraction model. |
| `page_extraction_llm_openai_temperature` | `None` | Extraction model temperature when supported by the selected model. |
| `page_extraction_llm_openai_reasoning_effort` | `minimal` | Extraction reasoning intensity. |
| `page_extraction_llm_openai_base_url` | `None` | Optional HTTP or HTTPS base URL override. |
| `extend_system_message` | `None` | Optional system prompt extension. |
| `vision_detail_level` | `auto` | Vision detail level: `auto`, `low`, or `high`. |
| `llm_timeout_in_s` | `None` | Optional LLM timeout in seconds. |
| `step_timeout_in_s` | `180` | Browser step timeout in seconds. |
| `enable_cloud_sync` | `False` | Whether `browser-use` cloud sync is enabled. |
| `logging_level` | `info` | Browser-use logging level: `debug`, `info`, `warning`, `error`, or `result`. |
| `max_session_retries` | `2` | Number of retries after recoverable session failures. |
| `session_retry_delay_in_s` | `3.0` | Delay between recoverable session retries. |

## Run Methods

1. `run(task)`: async generator that yields `BrowserUseStreamEvent` values as work progresses.
2. `run_once(task)`: async method that returns one `BrowserUseRunResult` and includes emitted events in `result.events`.
3. `run_sync(task)`: blocking wrapper around `run_once()` using `asyncio.run()`.

## Result Contract

`BrowserUseRunResult` contains:

1. `status`: `success`, `error`, or `cancelled`.
2. `task`: normalized task string.
3. `final_output`: final text extracted from the underlying agent, or `Task completed` when no final text is available.
4. `session_id`: infrastructure session ID when an external browser session was used.
5. `streaming_url`: browser debug or streaming URL when available.
6. `recording_url`: expected recording URL when recording is configured.
7. `steps`: number of browser-use steps executed.
8. `error`: terminal error message for error results.
9. `events`: collected stream events for `run_once()`.
10. `metadata`: attempt, retry, and recording metadata.

## Streaming Contract

`BrowserUseStreamEvent` contains:

1. `event_type`
2. `content`
3. `thinking_and_activity_info`
4. `is_final`
5. `tool_info`
6. `metadata`

Important event content values:

1. `Receive streaming URL`
2. `Receive recording URL`
3. `Task completed`

Step events include serialized tool calls in `tool_info["tool_calls"]`.

## Recording Metadata

Recording metadata may include these statuses:

1. `disabled`: infrastructure, storage, or browser context is not available.
2. `unsupported`: the selected infrastructure does not support recording.
3. `unavailable`: storage is configured but not available.
4. `scheduled`: a background recording upload has been scheduled.
5. `unknown`: recording may have started, but the terminal error did not include enough context to determine the final state.

## SDK Errors

1. `BrowserUseSDKError`: base exception for SDK errors.
2. `BrowserUseConfigurationError`: missing or invalid runtime configuration.
3. `BrowserUseDependencyError`: optional provider dependency problem.
4. `BrowserUseMissingDependencyError`: optional provider extra is not installed.
5. `BrowserUseExecutionError`: execution-time failure.
6. `BrowserUseRetryExhaustedError`: recoverable session retries were exhausted.
