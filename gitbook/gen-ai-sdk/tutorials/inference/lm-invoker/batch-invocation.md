---
icon: people-group
---

# Batch Invocation

[**`gllm-inference`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-inference/gllm_inference/catalog) | **Tutorial**: [batch-invocation.md](batch-invocation.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_inference/api/lm_invoker.html)

**Supported by:** `AnthropicLMInvoker`, `GoogleLMInvoker`, `OpenAILMInvoker`

## What is batch invocation?

Batch invocation is a feature that allows the language model to process multiple requests in a single cell. Batch invocation are generally **cheaper** that standard invocation, but are **slower** in exchange. Thus, it's suitable for **large amount of requests that does not concern latency**.

Batch invocation is only available for certain LM invokers. This feature can be accessed via the `batch` attribute of the LM invoker. As an example, let's try executing a batch invocation using the `AnthropicLMInvoker`:

```python
import asyncio
from gllm_core.utils import RetryConfig
from gllm_inference.lm_invoker import AnthropicLMInvoker

lm_invoker = AnthropicLMInvoker("claude-sonnet-4-20250514", retry_config=RetryConfig(timeout=360))

requests = {
    f"request_{letter}": f"Name an animal that starts with the letter '{letter}'"
    for letter in "ABCDE"
}

async def main():
    results = await lm_invoker.batch.invoke(requests)

    print("Results:")
    for result_id, result in results.items():
        print(f">> {result_id}: {result.text}")

if __name__ == "__main__":
    asyncio.run(main())
```

**Output:**

```
Results:
>> request_A: Alligator.
>> request_B: Bear.
>> request_C: Cat.
>> request_D: Dog.
>> request_E: Elephant.
```

Alternatively, the following standalone batch operations can also be executed separately:

### Create a Batch Job

We can create batch job by utilizing the `create()` method.

```python
requests = {
    "request_1": "What color is the sky?",
    "request_2": "What color is the grass?",
}
batch_id = await lm_invoker.batch.create(requests)
```

### Get a Batch Job Status

The status of a batch job can be checked via the `status()` method.

```python
status = await lm_invoker.batch.status(batch_id)
```

### Retrieve a Batch Job Results

Once a batch job is done, the results can be retrieved with the `retrieve()` method.

```python
results = await lm_invoker.batch.retrieve(batch_id)
```

### List Batch Jobs

The list of currently available batch jobs are accessible via the `list()` method.

```python
batch_jobs = await lm_invoker.batch.list()
```

### Cancel a Batch Job

If desired, a batch job can be cancelled using the `cancel()` method.

```python
await lm_invoker.batch.cancel(batch_id)
```
