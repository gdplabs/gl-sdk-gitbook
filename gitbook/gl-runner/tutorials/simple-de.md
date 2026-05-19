# Simple DE

Deploy the simple decision engine bundle.

```bash
python ./scripts/deploy.py --key simple-de --bundle-path ./examples/bundles/simple-de
python ./scripts/run.py --runnable-key simple-de --payload '{"message":"Hello, what can you do?"}' --wait
```

Python version:

```python
from gl_runner_sdk import Runnable

runnable = Runnable.from_key(
    "simple-de",
    base_url="http://localhost:4200",
    api_key="glr_...",
)
result = runnable.run(payload={"message": "Hello, what can you do?"})
print(result)
```
