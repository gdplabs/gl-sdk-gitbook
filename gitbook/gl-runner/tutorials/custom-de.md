# Custom DE

Deploy the custom decision engine bundle that uses tools.

```bash
python ./scripts/deploy.py --key custom-de --bundle-path ./examples/bundles/custom_de
python ./scripts/run.py --runnable-key custom-de --payload '{"message":"What is the weather in Tokyo?"}' --wait
```

Python version:

```python
from gl_runner_sdk import Runnable

runnable = Runnable.from_key(
    "custom-de",
    base_url="http://localhost:4200",
    api_key="glr_...",
)
result = runnable.run(payload={"message": "What is the weather in Tokyo?"})
print(result)
```
