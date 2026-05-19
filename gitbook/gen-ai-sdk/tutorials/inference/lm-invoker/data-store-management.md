---
icon: database
---

# Data Store Management

[**`gllm-inference`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-inference/gllm_inference/catalog) | **Tutorial**: [data-store-management.md](data-store-management.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_inference/api/lm_invoker.html)

**Supported by:** `GoogleLMInvoker`, `OpenAILMInvoker`

## What is data store management?

Data store management is a feature that allows the language model to **manage built-in data stores** to be used as **internal knowledge base**. This allows the LM invoker to **perform built-in RAG** (Retrieval-Augmented Generation).

Data store management is only available for certain LM invokers. This feature can be accessed via the `data_store` attribute of the LM invoker. As an example, let's try to perform a simple built-in RAG using the `GoogleLMInvoker`!

### Init an LM Invoker

First of all, let's create a `GoogleLMInvoker` that we will use to manage the data store:

```python
from dotenv import load_dotenv
load_dotenv()

from gllm_inference.lm_invoker import GoogleLMInvoker

lm_invoker = GoogleLMInvoker("gemini-2.5-flash-lite")
```

### Create a Data Store

Next, let's create a data store. The `create()` method will output an `AttachmentStore` object to be used in later operations.

```python
store = await lm_invoker.data_store.create()
```

### List the Data Stores

We can verify that the data store has been successfully created on the server side by using the `list()` method.

```python
stores = await lm_invoker.data_store.list()

if not stores:
    print("No stores found.")

for store in stores:
    print(f" - {store}")
```

### Add a File to the Data Store

Then, we can add a file to our newly created store using the `add_file()` method.

```python
from gllm_inference.schema import Attachment

file = Attachment.from_path('path/to/file.pdf')
await lm_invoker.data_store.add_file(store, file)
```

### Utilize the Data Store as a Native Tool

Then, we can wrap our store as a native tool and utilize it as an internal knowledge base for the LM invoker:

```python
from gllm_inference.schema import NativeTool, NativeToolType

# Option 1: as dictionary
data_store_tool = {"type": "data_store", "data_stores": [store], **kwargs}
# Option 2: as native tool object
data_store_tool = NativeTool.data_store(data_stores=[store], kwargs)

lm_invoker.set_tools([data_store_tool])
```

Alternatively, we can also directly assign it to a new LM invoker:

```python
lm_invoker = GoogleLMInvoker("gemini-2.5-flash-lite", tools=[data_store_tool])
```

During invocation, the LM invoker has the capability to retrieve knowledge from the stores that have been assigned to it, effectively enabling a **built-in RAG**.

```python
output = await lm_invoker.invoke("<question about the file>")
print(f"output:\n{output}")
```

### Delete the Data Store

Finally, if the store is no longer used, it can be deleted via the `delete()` method.

```python
await lm_invoker.data_store.delete(store)
```

