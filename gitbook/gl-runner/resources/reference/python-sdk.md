# Python SDK Reference

## Public Exports

```python
from gl_runner_sdk import (
    Client,
    Runnable,
    Runs,
    RunnableRecord,
    RunDetailResponse,
    RunResponse,
)
```

## `Runnable` (recommended)

```python
from gl_runner_sdk import Runnable

runnable = Runnable(
    base_url="http://localhost:4200",
    api_key="glr_...",
    key="hello-world",
    bundle_path="./hello-world",
)
```

Constructor:

- `Runnable(client=None, base_url=None, api_key=None, key=None, kind="code", bundle_path=None, version=None, entrypoint=None)`
- `api_key` defaults to `GL_RUNNER_API_KEY`; `base_url` defaults to `GL_RUNNER_BASE_URL` or `http://localhost:4200`.
- If no `client` is supplied, `Runnable` creates an internal transport `Client`.

Deployment methods:

- `deploy(key=None, kind=None, bundle_zip=None, include_sensitive_files=None, version=None, entrypoint=None, wait_for_active=True, activation_timeout=120.0, activation_poll_interval=5.0) -> RunnableRecord`
  - When `_deployment` is already tracked (after `from_id`/`load_from_id` or a prior `deploy`) this posts to the update endpoint.
- `set_bundle_path(bundle_path) -> Runnable`
- `deployment` property returns the tracked deployed `Runnable` or `None`.

Execution methods:

- `trigger(payload=None, context=None) -> RunResponse`
- `run(payload=None, context=None, timeout=120.0, poll_interval=2.0, stream=False) -> dict | None | RunStream`
  - `stream=True` returns a `RunStream` iterable that yields raw OpenAI-compatible events. Access the final result via `.result` after iteration.
- `wait(run_id, timeout=120.0, poll_interval=2.0) -> RunDetailResponse`
- `get_run(run_id) -> RunDetailResponse`
- `stream(run_id, deadline=None) -> Iterator[dict]`
- `events(run_id, event_type=None, limit=100) -> list[dict]`

Lookup/delete methods:

- `from_key(key, *, client=None, base_url=None, api_key=None) -> Runnable` (classmethod constructor-style loader, key-first)
- `load_from_key(key) -> Runnable` (instance loader, key-first)
- `from_id(runnable_id, *, client=None, base_url=None, api_key=None) -> Runnable` (classmethod constructor-style loader, direct ID lookup)
- `load_from_id(runnable_id) -> Runnable` (instance loader, direct ID lookup)
- `delete() -> None`
- `sync() -> RunnableRecord` - Refresh the tracked deployment record from the server in-place.

`include_sensitive_files` is an explicit opt-in for bundle-relative files such
as `.env`. The SDK excludes `.env`, `.env.*`, caches, virtualenvs, build
outputs, and VCS metadata by default.

When `deploy()` receives metadata overrides (`key`, `kind`,
`version`, `entrypoint`), the facade state is updated first and top-level
`runnables.yaml` fields are synchronized before bundle packaging.

## `Runs` Helper

Use this when you need direct run-history/stream operations without going
through `Runnable` convenience methods.

```python
from gl_runner_sdk import Client, Runs

client = Client.from_api_key(base_url="http://localhost:4200", api_key="glr_...")
runs = Runs(client)
```

Methods:

- `get(run_id) -> RunDetailResponse`
- `list(runnable_key=None, limit=100, cursor=None) -> list[RunDetailResponse]`
- `wait(run_id, timeout=120.0, poll_interval=2.0) -> RunDetailResponse`
- `stream(run_id, deadline=None) -> Iterator[dict]`
- `events(run_id, event_type=None, limit=100) -> list[dict]`
- `cancel(run_id)` is currently not implemented and raises `NotImplementedError`.

## `Client.runnables` Collection

Use this for server-scoped runnable collection operations.

```python
from gl_runner_sdk import Client

client = Client.from_api_key(base_url="http://localhost:4200", api_key="glr_...")
items = client.runnables.list(limit=10)
target = client.runnables.get_by_id_or_key("hello-world")
```

Methods:

- `get(runnable_id) -> RunnableRecord`
- `list(limit=100, offset=0) -> list[RunnableRecord]`
- `get_by_key(key) -> RunnableRecord | None`
- `get_by_id_or_key(runnable_id_or_key) -> RunnableRecord | None`
- `delete(runnable_id) -> None`

## Data Types

- `RunnableRecord`: runnable entity (`id`, `key`, `entrypoint`, `kind`, `version`, `status`, `metadata`, `config`, timestamps).
- `RunResponse`: trigger response entity (`id`, `runnable_id`, `status`, `payload`, `context`, `result`, `error`, timestamps). Returned by `trigger()`.
- `RunDetailResponse`: run detail entity (`id`, `runnable_id`, `status`, `payload`, `context`, `result`, `error`, timestamps). Returned by `get()`, `list()`, and `wait()`.
- `RunnableRecord`, `RunDetailResponse`, `RunRequest`, and `RunResponse` are available from `gl_runner_sdk.types`.

## Errors and Timeouts

- API errors raise `RuntimeError` with HTTP status and server response text.
- `wait()` raises `TimeoutError` if terminal status is not reached in time.
- `stream()` with a passed `deadline` raises `TimeoutError` when the deadline is exceeded.
- Missing API key in constructor paths raises `ValueError`/`SystemExit` depending on call path.

## Transport Compatibility

`Client.from_api_key(base_url, api_key)` remains available for compatibility
and lower-level transport-style usage.
