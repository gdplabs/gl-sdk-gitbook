Use these endpoints to orchestrate Human-in-the-Loop (HITL) pauses from a client
application: register a tool, create an agent, stream run updates, and resolve
approval requests.

## Prerequisites

- Backend service reachable at `$BACKEND_URL` (default: `http://localhost:8000`).
- API key with access to the HITL endpoints (`X-API-Key` header).

Examples below assume the API key is stored in `$AIP_MASTER_API_KEY`.

## 1. Create an Agent with HITL Enabled

```bash
curl -X POST "$BACKEND_URL/agents/" \
  -H "X-API-Key: $AIP_MASTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d @agent_payload.json
```

Sample `agent_payload.json`:

```json
{
  "name": "hitl_approval_agent",
  "instruction": "Whenever an action needs approval, call the custom_tool first.",
  "type": "config",
  "framework": "langchain",
  "version": "1.0",
  "tools": ["<TOOL_ID_FROM_UPLOAD>"],
  "agent_config": {
    "hitl_enabled": true,
    "lm_provider": "openai",
    "lm_name": "gpt-4.1"
  },
  "tool_configs": {
    "<TOOL_ID_FROM_UPLOAD>": {
      "hitl": {
        "timeout_seconds": 180
      }
    }
  }
}
```

The response JSON returns a new `agent_id`.

## 2. Run the Agent and Watch for HITL Pauses

```bash
curl -N -X POST "$BACKEND_URL/agents/<AGENT_ID>/run" \
  -H "X-API-Key: $AIP_MASTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "input": "Please send an offer email to jane.doe@example.com and update her ATS record."
      }'
```

The call returns an SSE stream. When a tool requires human approval the chunks
include a `metadata.hitl` object. Example payload captured from the integration
test (`notes/hitl_e2e_run_raw.log`):

```json
{
  "status": "success",
  "task_state": "working",
  "content": "Awaiting human approval for request 'bc4d0a77-7800-470e-a91c-7fd663a66b4d'. Invoke ApprovalManager.resolve_pending_request using this identifier to continue execution.",
  "metadata": {
    "kind": "agent_thinking_step",
    "status": "finished",
    "hitl": {
      "required": true,
      "decision": "pending",
      "request_id": "bc4d0a77-7800-470e-a91c-7fd663a66b4d",
      "timeout_at": "2025-10-14T01:56:22.464367+00:00",
      "timeout_seconds": 10
    },
    "tool_info": {
      "id": "call_UHU9hq7rfikCrTLhImGmRx37",
      "name": "custom_tool",
      "args": {},
      "output": "Awaiting human approval for request 'bc4d0a77-7800-470e-a91c-7fd663a66b4d'. Invoke ApprovalManager.resolve_pending_request using this identifier to continue execution.",
      "execution_time": null
    }
  }
}
```

Key fields to capture:

- `metadata.hitl.request_id` — unique identifier for the pending approval
  (UUID).
- `metadata.hitl.decision` — current state. Expect at least `pending`,
  `approved`, `rejected`, or `timeout_skip`.
- `metadata.hitl.timeout_at` — ISO 8601 timestamp when the HITL request will timeout if no decision is made (UTC+0 timezone)
- `metadata.hitl.timeout_seconds` — static value of timeout duration in seconds for the HITL request (configured per tool with tool config)
- `metadata.tool_info` — context about the tool invocation (call id, tool name,
  arguments, output) for use in operator UIs.

Maintain the SSE connection while the operator decides so your client receives
the resumed tokens once the request is resolved.

## 3. Resolve a HITL Request

Use the `request_id` from the stream (or from the pending inbox endpoint) when
calling the decision API.

```bash
curl -X POST "$BACKEND_URL/agents/hitl/decision" \
  -H "X-API-Key: $AIP_MASTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "request_id": "bc4d0a77-7800-470e-a91c-7fd663a66b4d",
        "decision": "approved",
        "operator_input": "Looks good",
        "run_id": "optional-client-tracker"
      }'
```

Required fields:

- `request_id` — matches the identifier from the SSE chunk.
- `decision` — one of `approved`, `rejected`, or `skipped`.

Optional fields:

- `operator_input` — free-form notes for audit trails (defaults to `""`).
- `run_id` — client-side correlation identifier if you track sessions.

The endpoint returns `{"status": "ok", "message": "Request <id> <decision>"}` on
success. The corresponding SSE stream delivers a new chunk reflecting the final
decision so your client can update local state.

## 4. Optional: List Pending HITL Requests

```bash
curl -X GET "$BACKEND_URL/agents/hitl/pending" \
  -H "X-API-Key: $AIP_MASTER_API_KEY"
```

Sample response:

```json
[
  {
    "request_id": "bc4d0a77-7800-470e-a91c-7fd663a66b4d",
    "tool": "custom_tool",
    "arguments": {
      "action": "Finalize Jane Doe's hiring decision in the ATS for the Senior Backend Engineer role, including score and recommendation to move forward with offer."
    },
    "created_at": "2025-10-08T14:41:01.553063+00:00",
    "agent_id": "hitl_approval_agent-a44ac39b",
    "run_id": null,
    "hitl_metadata": {
      "required": true,
      "decision": "pending",
      "timeout_at": "2025-10-08T15:41:01.553063+00:00",
      "timeout_seconds": 180
    },
    "additional_context": {
      "tool_name": "custom_tool",
      "arguments": {
        "action": "Finalize Jane Doe's hiring decision in the ATS for the Senior Backend Engineer role, including score and recommendation to move forward with offer."
      },
      "agent_id": "hitl_approval_agent-a44ac39b"
    }
  }
]
```

The runner tracks these requests in-memory, so restarts clear the list. Treat
this endpoint as a real-time inbox rather than an audit log.

## 5. Optional Cleanup

- Delete agent: `DELETE /agents/<AGENT_ID>`
- Delete tool: `DELETE /tools/<TOOL_ID>`

Keep cleanup scripts handy for integration tests so temporary resources do not
accumulate in your tenant.
