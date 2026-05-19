---
icon: lightbulb-on
---

# Introduction to GL Runner

GL Runner lets you deploy and run runnable bundles over HTTP. The Lite SDK
uses a runnable-first interface (`from gl_runner_sdk import Runnable`) so you
can deploy, trigger, and wait without wiring raw HTTP calls.

Setup:

```bash
pip install -e python/gl-runner-sdk
export GL_RUNNER_BASE_URL="http://localhost:4200"
export GL_RUNNER_API_KEY="glr_..."
```

## Stage 1: Create the runnable file structure

Create a minimal bundle directory:

```text
hello-world/
  __init__.py
  entrypoint.py
  runnables.yaml
```

```bash
mkdir -p hello-world
touch hello-world/__init__.py
```

## Stage 2: Add runnable file contents

`entrypoint.py`:

```python
def handler(payload: dict | None = None, context: dict | None = None) -> dict:
    payload = payload or {}
    question = payload.get("question", "hello")
    return {"answer": f"You asked: {question}", "context": context or {}}
```

`runnables.yaml`:

```yaml
entrypoint: entrypoint.py:handler
metadata:
  name: hello-world
  description: Simple hello world runnable.
```

Note: GL Runner manages the Prefect `@flow` wrapper for runnable entrypoints.

## Stage 3: Use separate deploy, run, and trigger scripts

Create a `scripts/` directory with separate actions.

`scripts/deploy.py`:

```python
from gl_runner_sdk import Runnable

runnable = Runnable(
    base_url="http://localhost:4200",
    api_key="glr_...",
    key="hello-world",
    bundle_path="./hello-world",
    version="v1.0.0",
)

deployment = runnable.deploy()
print(deployment.id)
```

`scripts/run.py`:

```python
from gl_runner_sdk import Runnable

runnable = Runnable.from_key(
    "hello-world",
    base_url="http://localhost:4200",
    api_key="glr_...",
)

result = runnable.run(payload={"question": "status"})
print(result)
```

Advanced / direct ID lookup:

```python
from gl_runner_sdk import Runnable

runnable = Runnable.from_id(
    "<runnable-id>",
    base_url="http://localhost:4200",
    api_key="glr_...",
)

result = runnable.run(payload={"question": "status"})
print(result)
```

`scripts/trigger.py` (optional non-waiting start):

```python
from gl_runner_sdk import Runnable

runnable = Runnable.from_key(
    "hello-world",
    base_url="http://localhost:4200",
    api_key="glr_...",
)

run = runnable.trigger(payload={"question": "status"})
print(run.id, run.status)
```

Scope notes:

- `run()` waits by default using polling.
- `trigger()` returns the run record immediately.
- Stream/history helpers are available when those endpoints are exposed.
