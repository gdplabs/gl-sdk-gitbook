# Building Bundles

This guide walks through creating a runnable bundle from scratch. A bundle is
just a folder with a runnable entrypoint plus optional configuration files.

## 1) Create a new bundle folder

Start with a simple folder structure.

```
hello-world/
  __init__.py
  entrypoint.py
  runnables.yaml
```

## 2) Implement the runnable

Create `entrypoint.py` with a handler function. The SDK expects the handler to
return a JSON-serializable payload. Use `@task` for internal steps if needed;
`@flow` is not required because the server manages the flow wrapper.

### Task state vs run state

- Task states (Prefect) are controlled inside your runnable with `@task` and
  return values like `Completed` or `Failed`.
- Run state (GL Runner) is controlled by the server: it marks `success` when
  the entrypoint returns and `failed` only when the entrypoint raises.

For the available Prefect state names, types, and terminal behavior, see the
[Prefect states documentation](https://docs.prefect.io/v3/concepts/states).

If you need the run to fail, raise an exception in the entrypoint (or let a
task exception propagate). Returning a Prefect `Failed` state from a task does
not change the GL Runner run status by itself.

### Minimum required files

The server validates that every bundle contains `__init__.py`, `entrypoint.py`,
and `runnables.yaml`. Include all three in the bundle folder.

```python
from prefect import task

@task(name="format-answer")
def format_answer(question: str) -> dict:
    return {"answer": f"You asked: {question}"}

def handler(payload: dict) -> dict:
    question = payload.get("question", "hello")
    return format_answer(question)
```

## 3) Define bundle metadata

Create `runnables.yaml` to describe the entrypoint and runnable metadata.

```yaml
entrypoint: entrypoint.py:handler
metadata:
  name: hello-world
  description: Simple hello world runnable.
```

## 4) Deploy the bundle

Point the SDK at the bundle folder.

```python
from gl_runner_sdk import Runnable

runnable = Runnable(
    base_url="http://localhost:4200",
    api_key="glr_...",
    key="hello-world",
    bundle_path="./hello-world",
)
runnable.deploy()
```

## 5) Run the runnable

```python
result = runnable.run(payload={"question": "status"})
print(result)
```

## Next steps

- Add environment variables in your runnable configuration when it needs secrets.
- Use the bundle examples for larger templates and patterns.
