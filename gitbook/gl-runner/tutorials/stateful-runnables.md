# Stateful Runnables

Deploy the stateful runnable example to see how GL Runner handles Prefect task
states inside a runnable without requiring the bundle to define `@flow`.

```bash
python ./scripts/deploy.py --key stateful-runnables --bundle-path ./examples/bundles/stateful-runnables
python ./scripts/run.py --runnable-key stateful-runnables --payload '{"input":1}' --wait
```

Python version:

```python
from gl_runner_sdk import Runnable

runnable = Runnable.from_key(
    "stateful-runnables",
    base_url="http://localhost:4200",
    api_key="glr_...",
)
result = runnable.run(payload={"input": 1})
print(result)
```

The `input` value selects the Prefect state behavior used by the internal task:

| Input | Prefect behavior |
|-------|------------------|
| `1` | `Completed:Base` |
| `2` | Simulates `Running:InFlight` for 5 seconds, then returns `Running:InFlight:Terminated` |
| `3` | `Cancelled:User` |
| `4` | `Crashed:Runtime` |
| `5` | Raises transient task errors, retries at most 3 times, then returns `Retrying:Transient:Completed` |
| `6` | Simulates `AwaitingRetry:Backoff` for 3 seconds, then returns `AwaitingRetry:Backoff:Completed` |
| `7` | `Failed:InvalidInput` |
| `8` | Raises an intentional runtime error |

Notes:

- Non-terminal Prefect states are bounded in this example. `Running`,
  `Retrying`, and `AwaitingRetry` demonstrations always resolve to a terminal
  state so `python ./scripts/run.py --wait` can finish.
- GL Runner marks the run as `success` when the entrypoint returns, even if the
  returned Prefect task state is `Failed`.
- GL Runner marks the run as `failed` only when the entrypoint raises, as it
  does for `{"input":8}`.
- Use capability-focused examples as templates for documenting behavior beyond
  a basic request/response runnable.
