# Python SDK Quick Start

Use the Lite SDK to deploy and run a runnable. `run()` waits by default and
returns the completed result.

## Blank-folder setup

```bash
mkdir lite-sdk-quickstart && cd lite-sdk-quickstart
python3 -m venv .venv
source .venv/bin/activate
pip install gl-runner-sdk python-dotenv
export GL_RUNNER_BASE_URL="http://localhost:4200"
export GL_RUNNER_API_KEY="glr_..."
mkdir -p bundles/hello-world
```

Create:

```text
lite-sdk-quickstart/
  deploy_and_run.py
  bundles/hello-world/
    runnables.yaml
    entrypoint.py
```

`bundles/hello-world/runnables.yaml`

```yaml
entrypoint: entrypoint.py:handler
kind: code
```

`bundles/hello-world/entrypoint.py`

```python
def handler(payload=None, context=None):
    payload = payload or {}
    return {"ok": True, "echo": payload}
```

### Deploy and run

The following script combines deploy, run, trigger, and history in one file:

```python
from gl_runner_sdk import Runnable

runnable = Runnable(
    base_url="http://localhost:4200",
    api_key="glr_...",
    key="hello-world",
    bundle_path="./bundles/hello-world",
)

runnable.deploy()
result = runnable.run(payload={"question": "status"})
print(result)
```

Use `trigger()` when you need the run record without waiting:

```python
run = runnable.trigger(payload={"question": "status"})
print(run.id, run.status)
```

Notes:

- `run()` polls `GET /v1/runs/{run_id}` until `success`, `failed`, or `cancelled`.
- Streaming and history helpers are available when the server exposes the endpoints.
- You can create a `Runnable` object per local bundle.
- Bundle `.env` files are excluded by default. Include explicitly only for trusted
  environments (`include_sensitive_files=[".env"]`) or set variables on the runner.
- Expected output includes a deployment id and a result like
  `{"ok": True, "echo": {"question": "status"}}`.
