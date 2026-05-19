# Schemas

Schema details are intentionally minimal in the Lite SDK. For now, use the SDK
types as the reference for fields returned by the endpoints.

Key response fields used by the SDK:

- `runnables: id, key, entrypoint, version, status, metadata, config`
- `runs: run_id, runnable_id, status, requested_payload, context_metadata, result, error_code`
