# Streaming and History

The SDK exposes streaming and history helpers when the server provides
the endpoints.

## Stream (SSE)

`runnable.stream(run_id)` opens an SSE connection and yields raw
[OpenAI Responses API](https://platform.openai.com/docs/api-reference/responses-streaming)
payloads. Each event dict has a `type` field you can inspect:

```python
import json

for event in runnable.stream(run_id):
    print(event["type"], json.dumps(event, indent=2))
    if event.get("type") in ("response.completed", "response.failed", "response.incomplete"):
        break
```

Use `runnable.run(stream=True)` to consume the stream in real time, then
access the final result after iteration:

```python
stream = runnable.run(payload={"question": "status"}, stream=True)
for event in stream:
    print(event["type"], json.dumps(event))
print(f"Final result: {stream.result}")
```

The returned `RunStream` object is iterable — it yields raw
[OpenAI Responses API](https://platform.openai.com/docs/api-reference/responses-streaming)
events as they arrive. After all events are consumed the stream calls
`wait()` internally and makes the completed result available via
`.result`.

## History (REST)

`runnable.events(run_id)` returns raw event dicts from the server:

```python
run = runnable.trigger(payload={"question": "status"})
history = runnable.events(run.id)
for event in history:
    print(event["event_type"], event.get("payload"))
```

Notes:

- `stream()` connects to `GET /v1/runs/{run_id}/stream` (SSE) and yields OpenAI-compatible payloads.
- `events()` connects to `GET /v1/runs/{run_id}/events` and returns the raw server response.
- `run(stream=True)` returns a `RunStream` iterable; iterate to consume events, then access `.result` for the completed output.
