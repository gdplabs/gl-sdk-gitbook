---
icon: people-roof
---

Enable manual checkpoints for high-risk actions by routing agent decisions
through an operator before execution. This guide outlines the end-to-end flow,
where it fits in existing automation, and how to combine it with the SDK and
CLI.

{% hint style="warning" %}
HITL runtime examples should stay Agent-first where possible. `Client` examples
in this page are advanced integrations for remote handler customization and
workspace-level approval orchestration.
{% endhint %}

## When to Use HITL

- You need an audit trail for outbound actions (email, ticketing, CRM updates).
- Teams want live visibility into agent decisions without disabling automation.
- Regulatory or compliance policies require operator approval on sensitive steps.

## Quick Start

### Auto-Approval (Local Testing/CI)

```python
import os
os.environ["GLAIP_HITL_AUTO_APPROVE"] = "true"

from glaip_sdk.agents import Agent
from tools import CalculatorTool  # Any LangChain BaseTool subclass.

# Local auto-approval uses LocalPromptHandler, injected when hitl_enabled is True.
agent = Agent(
    name="hitl_local_agent",
    instruction="Use the calculator tool when needed.",
    tools=[CalculatorTool],
    tool_configs={CalculatorTool: {"hitl": {"timeout_seconds": 30}}},
    agent_config={"hitl_enabled": True},
)

response = agent.run("Calculate 2 + 2", local=True)
# All HITL requests auto-approved.
```

**Note:** Local HITL prompts do not enforce timeouts; approval waits indefinitely.

### Auto-Approval (Remote Testing/CI)

For remote runs, the env var is only read by `RemoteHITLHandler`. Make sure you
pass one so HITL requests are actually resolved.

```python
import os
os.environ["GLAIP_HITL_AUTO_APPROVE"] = "true"

from glaip_sdk import Client
from glaip_sdk.hitl.remote import RemoteHITLHandler

client = Client(api_url="...", api_key="...")
handler = RemoteHITLHandler(client=client)  # Reads env var.
response = client.agents.run_agent(
    agent_id,
    "Run with auto-approval",
    hitl_handler=handler,
)
```

### Custom Approval Logic

```python
from glaip_sdk import Client
from glaip_sdk.hitl.remote import RemoteHITLHandler
from glaip_sdk.hitl.base import HITLRequest, HITLResponse, HITLDecision

def approver(request: HITLRequest) -> HITLResponse:
    # Auto-approve safe tools
    if request.tool_name in ["read_file", "search"]:
        return HITLResponse(decision=HITLDecision.APPROVED)

    # Auto-reject dangerous tools
    if "delete" in request.tool_name.lower():
        return HITLResponse(
            decision=HITLDecision.REJECTED,
            operator_input="Dangerous operation blocked"
        )

    # Interactive prompt for others
    choice = input(f"Approve {request.tool_name}? (y/n/s): ")
    if choice == 'y':
        return HITLResponse(decision=HITLDecision.APPROVED)
    elif choice == 'n':
        return HITLResponse(decision=HITLDecision.REJECTED)
    else:
        return HITLResponse(decision=HITLDecision.SKIPPED)

client = Client(api_url="...", api_key="...")
handler = RemoteHITLHandler(callback=approver, client=client)

response = client.agents.run_agent(
    agent_id,
    "Perform actions requiring approval",
    hitl_handler=handler,
)
```

**Note:** Keep callbacks short and handle timeouts; for longer approvals, use the manual approval flow (`hitl.list_pending` + approve/reject) from another process. Log errors for operational visibility.

### Manual Approval (Separate Process)

```python
from glaip_sdk import Client

client = Client(api_url="...", api_key="...")

# In monitoring dashboard/script
pending = client.hitl.list_pending()
for req in pending:
    print(f"Tool: {req['tool']}, Args: {req['arguments']}")
    decision = input("Approve? (y/n): ")

    if decision == 'y':
        client.hitl.approve(req['request_id'], operator_input="Approved")
    else:
        client.hitl.reject(req['request_id'], operator_input="Rejected")
```

## Components

- **Approval-aware tool** — Exposes a tool that records pending actions instead of
  executing them immediately.
- **HITL-enabled agent** — Flags tools that require approval and pauses run
  execution until a decision arrives.
- **Operator console** — Any surface (custom UI, CLI, or scripts) that calls the
  HITL APIs (prefer the Python SDK; REST is reference-only for internal integrations).

## Detecting Pauses in a Run

- Remote runs stream Server-Sent Events. When an approval is required the chunk includes `metadata.hitl`.
- Capture the `metadata.hitl.request_id` and `metadata.tool_info` fields to
  populate the operator UI. `metadata.hitl.decision` moves from `pending` to
  `approved`, `rejected`, or `timeout_skip` once resolved.
- Keep the stream open so follow-up tokens deliver the agent's response after
  the decision lands.

## Typical Workflow

1. Upload or register a tool that surfaces actions for approval.
1. Create an agent with `hitl_enabled` set and map the tool to HITL settings and
   timeouts.
1. Start a run and watch the SSE stream for `metadata.hitl.decision == "pending"`
   to know when to open an approval card.
1. Let operators approve in your console using the SDK (`client.hitl.approve(...)` / `client.hitl.reject(...)`) with the streamed `request_id`.
1. Optionally monitor pending approvals via `client.hitl.list_pending()` for inbox-style dashboards or recovery from client restarts.
1. Remove temporary agents, tools, or runs when tests finish.

## Implementation Paths

### Python SDK - Remote HITL Handler (Recommended)

Use `RemoteHITLHandler` for programmatic approval workflows:

**Features:**

- Thread-based callback execution (non-blocking)
- Timeout enforcement (80% of backend timeout)
- Automatic retry on network/server errors
- Error recovery (callback exceptions handled gracefully)

**Patterns:**

1. **Auto-approval**: Set `GLAIP_HITL_AUTO_APPROVE=true` or `auto_approve=True`
1. **Conditional approval**: Callback with business logic (safe/dangerous tools)
1. **Interactive approval**: User prompts with timeout handling
1. **Logging-only**: Auto-approve but log all requests for audit
1. **Manual approval**: Separate process polling `client.hitl.list_pending()`

### REST API

Follow the detailed payloads in the
[HITL REST Workflow Guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/rest-api/hitl) for cURL-ready
examples and sample SSE payloads.

### CLI

Combine `aip agents run` with small scripts that invoke the HITL
endpoints for approvals. Perfect for demos or manual QA.

## Best Practices

- **Separate duties** — Store approval history outside the agent payload so you
  can report on reviewer actions.
- **Define timeouts** — Use `tool_configs[tool_id].hitl.timeout_seconds` to align
  with your SLA. Callbacks get 80% of this time (20% reserved for network).
- **Alerting** — Hook pending requests into chat or incident systems to avoid
  stalled workflows. Use `on_unrecoverable_error` callback for critical alerts.
- **Testing** — Include HITL runs in integration tests to ensure endpoints stay
  in sync across releases. Use auto-approval for CI/CD pipelines.
- **Error handling** — Callbacks should complete quickly and handle exceptions
  internally. Callback exceptions are logged and treated as REJECTED.
- **Thread safety** — If using custom `BaseClient`, ensure it's thread-safe or
  pass a dedicated client instance to `RemoteHITLHandler`.

## Testing & Examples

With these pieces in place you can ship agents that stay fast for low-risk
scenarios while keeping an operator in the loop for everything else.

______________________________________________________________________

## API Reference

### Decision Types

| Decision | Code                    | Behavior      |
| -------- | ----------------------- | ------------- |
| Approve  | `HITLDecision.APPROVED` | Tool executes |
| Reject   | `HITLDecision.REJECTED` | Tool blocked  |
| Skip     | `HITLDecision.SKIPPED`  | Tool skipped  |

### HITLRequest Fields

```python
@dataclass
class HITLRequest:
    request_id: str          # Unique ID for this request
    tool_name: str           # Name of tool requiring approval
    tool_args: dict          # Arguments being passed to tool
    timeout_at: str          # ISO 8601 deadline (authoritative)
    timeout_seconds: int     # Timeout in seconds (informational)
    hitl_metadata: dict      # Raw HITL metadata
    tool_metadata: dict      # Raw tool metadata
```

**Example:**

```python
request.request_id        # "bc4d0a77-7800-470e-a91c-7fd663a66b4d"
request.tool_name         # "send_email"
request.tool_args         # {"to": "user@example.com", "subject": "..."}
request.timeout_at        # "2026-01-05T10:30:00Z"
request.timeout_seconds   # 180
```

### HITLResponse Fields

```python
@dataclass
class HITLResponse:
    decision: HITLDecision            # APPROVED, REJECTED, or SKIPPED
    operator_input: str | None = None # Optional reason/notes
```

**Examples:**

```python
# Approve
HITLResponse(decision=HITLDecision.APPROVED)

# Reject with reason
HITLResponse(
    decision=HITLDecision.REJECTED,
    operator_input="Production writes not allowed"
)

# Skip with note
HITLResponse(
    decision=HITLDecision.SKIPPED,
    operator_input="Tool temporarily unavailable"
)
```

### RemoteHITLHandler Configuration

```python
RemoteHITLHandler(
    callback=your_callback,           # Approval function (optional)
    client=client,                     # BaseClient instance (required)
    auto_approve=None,                 # Override env var (optional)
    max_retries=3,                     # POST retries (default: 3)
    on_unrecoverable_error=handler,    # Error callback (optional)
)
```

**Parameters:**

- `callback`: Function `(HITLRequest) -> HITLResponse`
  - If `None` and `auto_approve=False`, requests will be rejected
- `client`: `BaseClient` instance for posting decisions
- `auto_approve`: Override `GLAIP_HITL_AUTO_APPROVE` env var
- `max_retries`: Max retries for POST errors (default: 3)
- `on_unrecoverable_error`: Called when both callback and POST fail

### Manual Approval API

**List Pending Requests:**

```python
pending = client.hitl.list_pending()
# Returns: [{"request_id": "...", "tool": "...", "arguments": {...}, ...}, ...]
```

**Approve a Request:**

```python
client.hitl.approve(
    request_id="bc4d0a77-...",
    operator_input="Verified and approved",  # Optional
    run_id="run-123",                        # Optional
)
```

**Reject a Request:**

```python
client.hitl.reject(
    request_id="bc4d0a77-...",
    operator_input="Policy violation",       # Optional
    run_id="run-123",                        # Optional
)
```

**Skip a Request:**

```python
client.hitl.skip(
    request_id="bc4d0a77-...",
    operator_input="Tool unavailable",       # Optional
    run_id="run-123",                        # Optional
)
```

## Common Patterns

### Conditional Approval

```python
def smart_approver(request: HITLRequest) -> HITLResponse:
    # Whitelist safe tools
    if request.tool_name in ["read_file", "search", "list"]:
        return HITLResponse(decision=HITLDecision.APPROVED)

    # Blacklist dangerous tools
    if "delete" in request.tool_name.lower():
        return HITLResponse(
            decision=HITLDecision.REJECTED,
            operator_input="Dangerous operation blocked"
        )

    # Check arguments
    if "production" in str(request.tool_args).lower():
        return HITLResponse(
            decision=HITLDecision.REJECTED,
            operator_input="No production modifications"
        )

    # Default: approve
    return HITLResponse(decision=HITLDecision.APPROVED)
```

### Interactive Approval

```python
def interactive_approver(request: HITLRequest) -> HITLResponse:
    print(f"Tool: {request.tool_name}")
    print(f"Args: {request.tool_args}")

    choice = input("Approve? [y/n/s]: ").lower()

    if choice == 'y':
        return HITLResponse(decision=HITLDecision.APPROVED)
    elif choice == 'n':
        reason = input("Reason: ")
        return HITLResponse(
            decision=HITLDecision.REJECTED,
            operator_input=reason
        )
    else:
        return HITLResponse(decision=HITLDecision.SKIPPED)
```

### Logging + Auto-Approve

```python
import json
from datetime import datetime

def logging_approver(request: HITLRequest) -> HITLResponse:
    # Log to audit trail
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "request_id": request.request_id,
        "tool_name": request.tool_name,
        "tool_args": request.tool_args,
        "decision": "approved",
    }

    with open("hitl_audit.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    # Auto-approve
    return HITLResponse(decision=HITLDecision.APPROVED)
```

### Error Handling

```python
def robust_approver(request: HITLRequest) -> HITLResponse:
    try:
        # Your approval logic
        return HITLResponse(decision=HITLDecision.APPROVED)

    except Exception as e:
        # Fallback: reject on error
        return HITLResponse(
            decision=HITLDecision.REJECTED,
            operator_input=f"Error: {str(e)[:100]}"
        )

def error_handler(request_id: str, error: Exception) -> None:
    # Handle unrecoverable errors (callback + POST both failed)
    print(f"CRITICAL: HITL request {request_id} failed: {error}")
    # Send alert to monitoring system

handler = RemoteHITLHandler(
    callback=robust_approver,
    client=client,
    on_unrecoverable_error=error_handler,
)
```

## Error Handling Details

### Callback Errors

| Error            | Behavior                    |
| ---------------- | --------------------------- |
| Callback raises  | Log error, reject request   |
| Callback timeout | Log timeout, reject request |
| Invalid response | Log error, reject request   |

### POST Errors

| Error                  | Behavior                          |
| ---------------------- | --------------------------------- |
| Network error          | Retry 3x with delays (1s, 2s, 3s) |
| 5xx server error       | Retry 3x with delays              |
| 4xx client error       | Fail immediately, no retry        |
| 404 (not found)        | Treated as resolved, no retry     |
| 409 (already resolved) | Treated as resolved, no retry     |

### Unrecoverable Errors

When both callback execution **and** fallback rejection POST fail:

1. Error is logged
1. `on_unrecoverable_error` callback is invoked (if provided)
1. Backend will eventually timeout the request

## Timeout Details

**Callback Timeout:**

- Callbacks get 80% of backend timeout
- 20% reserved for network/POST operations

**Example:**

- Backend timeout: 60 seconds
- Callback timeout: 48 seconds (80%)
- Network buffer: 12 seconds (20%)

**Source of truth:** `timeout_at` field (ISO 8601 deadline)
**Fallback:** `timeout_seconds` field (only if `timeout_at` parsing fails)

## Environment Variables

```bash
# Auto-approve all HITL requests
export GLAIP_HITL_AUTO_APPROVE=true

# Backend URL
export AIP_API_URL=http://localhost:8000

# API Key
export AIP_API_KEY=your-api-key
```

## Complete Example

```python
import os
from glaip_sdk import Client
from glaip_sdk.hitl.remote import RemoteHITLHandler
from glaip_sdk.hitl.base import HITLRequest, HITLResponse, HITLDecision

# Approval callback
def smart_approver(request: HITLRequest) -> HITLResponse:
    # Safe tools
    if request.tool_name in ["read_file", "search"]:
        return HITLResponse(decision=HITLDecision.APPROVED)

    # Dangerous tools
    if "delete" in request.tool_name.lower():
        return HITLResponse(
            decision=HITLDecision.REJECTED,
            operator_input="Dangerous operation blocked"
        )

    # Default
    return HITLResponse(decision=HITLDecision.APPROVED)

# Error handler
def on_error(request_id: str, error: Exception) -> None:
    print(f"CRITICAL ERROR: {request_id} - {error}")

# Setup
client = Client(
    api_url=os.getenv("AIP_API_URL"),
    api_key=os.getenv("AIP_API_KEY"),
)

handler = RemoteHITLHandler(
    callback=smart_approver,
    client=client,
    max_retries=3,
    on_unrecoverable_error=on_error,
)

# Run agent with HITL handler
response = client.agents.run_agent(
    agent_id="your-agent-id",
    message="Perform actions requiring approval",
    hitl_handler=handler,
)

print(f"Response: {response}")
```
