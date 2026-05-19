Reference notes for HITL audit visibility.

This page documents how to capture operator decisions and approval history when
using Human-in-the-Loop (HITL) workflows.

## Scope

Use this page with the core HITL endpoints in:

- [HITL REST Workflow](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/rest-api/hitl)

## Audit Data to Persist

For each HITL request, persist at least:

- `request_id`
- `agent_id`
- `run_id`
- `decision` (`approved`, `rejected`, `skipped`, `timeout_skip`)
- `operator_input`
- `created_at`
- `resolved_at`
- `timeout_at`
- tool context (`tool_name`, arguments snapshot)

## Recommended Pattern

1. Stream run events and capture `metadata.hitl.*` fields.
2. On operator action, submit decision via the HITL decision endpoint.
3. Store both pending snapshot and final decision record in your audit store.
4. Correlate with your own user/session identifiers for compliance reporting.

## Notes

- The pending HITL endpoint is an operational inbox, not a durable audit store.
- Persist audit records in your own system of record.
