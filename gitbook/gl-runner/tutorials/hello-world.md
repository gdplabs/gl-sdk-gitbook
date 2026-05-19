# Hello World

Deploy the Hello World bundle and run it.

```bash
python ./scripts/deploy.py --key hello-world --bundle-path ./examples/bundles/hello-world
python ./scripts/run.py --runnable-key hello-world --payload '{"question":"status"}' --wait
```

If you prefer Python:

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
