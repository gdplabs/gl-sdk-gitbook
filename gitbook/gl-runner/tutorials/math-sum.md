# Math Sum

Deploy the Math Sum example and send inputs.

```bash
python ./scripts/deploy.py --key math-sum --bundle-path ./examples/bundles/math-sum
python ./scripts/run.py --runnable-key math-sum --payload '{"numbers":[3,5]}' --wait
```

Python version:

```python
from gl_runner_sdk import Runnable

runnable = Runnable.from_key(
    "math-sum",
    base_url="http://localhost:4200",
    api_key="glr_...",
)
result = runnable.run(payload={"numbers": [3, 5]})
print(result)
```
