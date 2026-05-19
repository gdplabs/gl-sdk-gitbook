---
icon: conveyor-belt-boxes
---

# Response Synthesizer

[**`gllm-generation`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-generation/gllm_generation/response_synthesizer) | [<mark style="background-color:yellow;">Involves LM</mark>](#user-content-fn-1)[^1] | **Tutorial**: [response-synthesizer.md](response-synthesizer.md "mention") | **Use Case:** [#create-the-response-synthesizer](../../guides/build-end-to-end-rag-pipeline/your-first-rag-pipeline.md#create-the-response-synthesizer "mention") | [API Reference](http://api.python.docs.gdplabs.id/gen-ai/library/gllm_generation/api/response_synthesizer.html)

## What’s a Response Synthesizer?

The **response synthesizer** is a utility module designed to synthesize the final response of an RAG pipeline based on the provided inputs and contexts. It can be executed with various strategy, such as `stuff`, `static list`, etc.

In this tutorial, you'll learn how to use the `ResponseSynthesizer` with `stuff` strategy in **just a few lines of code**. You can also explore other types of strategies, available [here](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_generation/api/response_synthesizer.html).

<details>

<summary>Prerequisites</summary>

This example specifically requires completion of all setup steps listed on the [prerequisites.md](../../prerequisites.md "mention") page.

You should be familiar with these concepts:

1. [lm-invoker](../inference/lm-invoker/ "mention")
2. [lm-request-processor.md](../inference/lm-request-processor.md "mention")

</details>

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}

```bash
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-generation"
```

{% endtab %}

{% tab title="Windows Powershell" %}

```powershell
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-generation"
```

{% endtab %}

{% tab title="Windows Command Prompt" %}

```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/"  "gllm-generation"
```

{% endtab %}
{% endtabs %}

## Available Strategies

The Response Synthesizer supports multiple synthesis strategies, each designed for different use cases and content processing needs. Choose the strategy that best fits your requirements:

<table><thead><tr><th width="151">Strategy</th><th width="382">When to Use</th><th>Link to Section</th></tr></thead><tbody><tr><td><strong>Stuff</strong></td><td>When <strong>all context fits within the model's token limit</strong>. Simple, single-pass processing.</td><td><a data-mention href="response-synthesizer.md#quickstart">#quickstart</a></td></tr><tr><td><strong>Map Reduce</strong></td><td>When dealing with <strong>large amounts of content</strong> that need <strong>hierarchical</strong> and <strong>parallel</strong> processing and combining.</td><td><a data-mention href="response-synthesizer.md#id-1.-map-reduce">#id-1.-map-reduce</a></td></tr><tr><td><strong>Refine</strong></td><td>When you need iterative refinement, <strong>processing chunks sequentially</strong> to build up an answer.</td><td><a data-mention href="response-synthesizer.md#id-2.-refine">#id-2.-refine</a></td></tr><tr><td><strong>Static List</strong></td><td>When you want to <strong>return a formatted list</strong> without LM processing. No model calls needed.</td><td><a data-mention href="response-synthesizer.md#id-3.-static-list">#id-3.-static-list</a></td></tr></tbody></table>

**Note:** The examples in this tutorial will use the `stuff` strategy, as it is the most common and basic strategy for RAG applications.

## Quickstart

Let’s jump into a basic example using `ResponseSynthesizer` with `stuff` strategy.

Here, we're going to use a preset that contains a predefined prompt templates with the following keys:

1. `query`: Will be filled with the `query` parameter passed to the `synthesize()` method.
2. `context`: Will be filled with the list of chunks passed to the `chunks` parameter passed to the `synthesize()` method. These chunks will be repacked (stuffed together) into a context string before being passed to the prompt template.

This preset is particularly useful for an RAG pipeline where we want to use a list of retrieved chunks as context to answer a user query. It can be instantiated through `ResponseSynthesizer.preset.stuff()` by providing the desired `model_id`.

```python
import asyncio
from gllm_core.schema import Chunk
from gllm_generation.response_synthesizer import ResponseSynthesizer

query = "How old is Alex?"
chunks = [Chunk(content="Alex is 25 years old."), Chunk(content="Bob is 30 years old.")]

synthesizer = ResponseSynthesizer.preset.stuff(model_id="openai/gpt-5-nano")
response = asyncio.run(synthesizer.synthesize(query=query, chunks=chunks))
print(f"Response: {response}")
```

**Expected Output**

```
Response: Alex is 25 years old.
```

## Customizing Language Model

We can also customize the language model related config, such as the prompt templates. In the example below, we create a prompt template that has no key, and therefore we dont need to pass any param to the `synthesize()` method.

```python
import asyncio
from gllm_generation.response_synthesizer import ResponseSynthesizer

synthesizer = ResponseSynthesizer.preset.stuff(
    model_id="openai/gpt-5-nano",
    system_template="Talk like a pirate.",
    user_template="Name an animal that starts with the letter 'A'!",
)
response = asyncio.run(synthesizer.synthesize())
print(f"Response: {response}")
```

**Expected Output**

```
Response: Arrr, alligator, matey!
```

## Passing Custom LM Request Processor

Alternatively, we can also perform the customization by passing an `LMRequestProcessor` object to the `stuff()` method. This is particularly useful when we already have an `LMRequestProcessor` object, such as when we use the [`LMRequestProcessorCatalog`](../inference/catalog.md).

```python
import asyncio
from gllm_inference.request_processor import build_lm_request_processor
from gllm_generation.response_synthesizer import ResponseSynthesizer

lm_request_processor = build_lm_request_processor(
    model_id="openai/gpt-5-nano",
    system_template="Talk like a pirate.",
    user_template="Name an animal that starts with the letter 'A'!",
)

synthesizer = ResponseSynthesizer.stuff(lm_request_processor=lm_request_processor)
response = asyncio.run(synthesizer.synthesize())
print(f"Response: {response}")
```

**Expected Output**

```
Response: Arrr, an albatross, matey!
```

## Using Prompt Variables

`ResponseSynthesizer` with `stuff` strategy supports adding prompt variables to be injected to the prompt template.

```python
import asyncio
from gllm_generation.response_synthesizer import ResponseSynthesizer

synthesizer = ResponseSynthesizer.preset.stuff(
    model_id="openai/gpt-5-nano",
    system_template="Talk like a {role}.",
    user_template="Create a joke about {topic}.",
)
response = asyncio.run(synthesizer.synthesize(role="5 years old", topic="parrot"))
print(f"Response: {response}")
```

**Expected Output**

```
Response: Here's a silly parrot joke: What did the parrot say at the bakery? Polly wants a cracker!
```

## Adding History

`ResponseSynthesizer` with `stuff` strategy supports adding history as additional context for the language model.

```python
import asyncio
from gllm_inference.schema import Message
from gllm_generation.response_synthesizer import ResponseSynthesizer

history = [
    Message.user("Who is Charlie?"),
    Message.assistant("Charlie is a Golden Retriever."),
]
query = "What color is Charlie?"

synthesizer = ResponseSynthesizer.preset.stuff(
    model_id="openai/gpt-5-nano",
    system_template="You are a helpful assistant.",
    user_template="{query}",
)
response = asyncio.run(synthesizer.synthesize(query=query, history=history))
print(f"Response: {response}")
```

**Expected Output**

```
Response: Charlie's coat is golden.
```

## Adding Extra Contents

`ResponseSynthesizer` with `stuff` strategy supports adding extra contents — such as attachments — as additional context for the language model.

```python
import asyncio
from gllm_inference.schema import Attachment
from gllm_generation.response_synthesizer import ResponseSynthesizer

attachment = Attachment.from_path("path/to/tiger.jpg")
query = "What animal is this?"

synthesizer = ResponseSynthesizer.preset.stuff(
    model_id="openai/gpt-5-nano",
    system_template="You are a helpful assistant.",
    user_template="{query}",
)
response = asyncio.run(synthesizer.synthesize(query=query, extra_contents=[attachment]))
print(f"Response: {response}")
```

**Expected Output**

```
Response: Tiger.
```

## Customizing Extractor Function

By default, the `ResponseSynthesizer` with `stuff` strategy uses an extractor function that extracts only the `response` attribute of the language model's `LMOutput` schema. This ensures that the synthesized response will always be a string by default.

For example, let's try setting the `output_analytics` param to `True`, which will cause the internal `LMInvoker` to output an `LMOutput` objects with analytics information.

```python
import asyncio
from gllm_generation.response_synthesizer import ResponseSynthesizer

query = "Name an animal that starts with the letter 'A'!"

synthesizer = ResponseSynthesizer.preset.stuff(
    model_id="openai/gpt-5-nano",
    system_template="You are a helpful assistant.",
    user_template="{query}",
    config={"output_analytics": True},
)
response = asyncio.run(synthesizer.synthesize(query=query))
print(f"Response: {response}")
```

**Expected Output**

```
Response: Alligator.
```

As we can see, due to the default extractor function, the `ResponseSynthesizer` will always output just the response regardless of the `LMInvoker` output.

If we want to get other attributes of the `LMOutput`, or even the whole `LMOutput`, we can define a custom extractor function as follows:

```python
import asyncio
from gllm_generation.response_synthesizer import ResponseSynthesizer

query = "Name an animal that starts with the letter 'A'!"

def custom_extractor(response):
    return response

synthesizer = ResponseSynthesizer.preset.stuff(
    model_id="openai/gpt-5-nano",
    system_template="You are a helpful assistant.",
    user_template="{query}",
    config={"output_analytics": True},
    extractor_func=custom_extractor,
)
response = asyncio.run(synthesizer.synthesize(query=query))
print(f"Response: {response}")
```

**Expected Output**

```
Response: LMOutput(
    response=Alligator,
    token_usage=input_tokens=28 output_tokens=200,
    duration=3.207796573638916,
    finish_details={'status': 'completed', 'incomplete_details': {'reason': None}}
)
```

## Other Strategies

### 1. Map Reduce

The **Map Reduce** strategy uses a two-phase approach to process large amounts of content in parallel and then combine the results. This is ideal for handling content that exceeds token limits.

#### When to Use

Use the Map Reduce strategy when:

- You have a large number of chunks that exceed the model's context window.
- You want to process chunks in parallel for better performance.
- Each chunk can be summarized independently before combining.
- You need to handle hundreds or thousands of documents.

#### How It Works

1. **Map Phase**: Each chunk (or batch of chunks) is processed individually to generate intermediate draft responses. This process repeats until the number of chunks fits the batch size in the reduce phase.
2. **Reduce Phase**: All draft responses are then combined into a final response.

{% hint style="info" %}
Note: you can specify which model to use for map and reduce phase (e.g., the map phase can use a smaller model, while the reduce phase can use a larger model). This is useful when you want to balance between performance and cost.
{% endhint %}

#### Prompt Template Variables

The required prompt keys are as follows:

1. For **Map Phase** prompts:
   1. `query`: The input query from user.
   2. `context`: The context(s) provided to the map phase.
2. For **Reduce Phase** prompts:
   1. `query`: The input query from user.
   2. `context`: The partial responses from the map phase.

#### Example: Using Preset

```python
import asyncio
from gllm_core.schema import Chunk
from gllm_generation.response_synthesizer import ResponseSynthesizer

query = "Summarize the key features of Python"
chunks = [
    Chunk(content="Python was created in 1991 by Guido van Rossum."),
    Chunk(content="Python 2.0 was released in 2000 with new features."),
    Chunk(content="Python 3.0 was released in 2008, breaking backward compatibility.")
]

# Using preset with default map-reduce configuration
synthesizer = ResponseSynthesizer.map_reduce_preset(
    map_model_id="openai/gpt-5-nano",  # Model for the map phase
    reduce_model_id="openai/gpt-5",  # Model for the reduce phase
    batch_size=2,  # Process 2 chunks at a time in map phase
    max_iterations=10 # Iterate max 10 times
)

response = asyncio.run(synthesizer.synthesize(query=query, chunks=chunks))
print(response)
```

#### Example: Custom Configuration

```python
from gllm_inference.request_processor import build_lm_request_processor
from gllm_generation.response_synthesizer.strategy import MapReduceSynthesisStrategy
from gllm_generation.response_synthesizer import ResponseSynthesizer

map_processor = build_lm_request_processor(
    model_id="openai/gpt-5",
    system_template="You are a helpful assistant that summarizes content related to user query.",
    user_template="Query: {query}\n Context: {context}"
)

reduce_processor = build_lm_request_processor(
    model_id="openai/gpt-5-nano",
    system_template="You are a helpful assistant that combines summaries.",
    user_template="Combine these summaries into a coherent response for: {query}\n\nSummaries:\n{context}"
)

synthesizer = ResponseSynthesizer.map_reduce(
    map_lm_request_processor = map_processor,
    reduce_lm_request_processor = reduce_processor,
    batch_size = 2,
    max_iterations = 10,
)

response = asyncio.run(synthesizer.synthesize(query=query, chunks=chunks))
print(response)
```

---

### 2. Refine

The **Refine** strategy iteratively refines an answer by processing chunks sequentially. It starts with an initial answer from the first chunk(s), then refines it based on subsequent chunks.

#### When to Use

Use the Refine strategy when:

1. You want to build up an answer incrementally.
2. The order of chunks matters (e.g., chronological events, step-by-step instructions).
3. You need to maintain context from previous chunks while adding new information.
4. You want to see how the answer evolves (you can do this by using `stream_drafts=True`).

#### How It Works

1. **Initial Response**: Generate an initial answer from the first chunk(s).
2. **Iterative Refinement**: For each subsequent chunk (or batch), refine the previous answer by incorporating new information.

#### Prompt Template Variables

The required prompt keys are as follows:

1. `query`: The input query.
2. `context`: The new context(s) to incorporate into the refined answer.
3. `draft_response`: The answer from the previous iteration that will be refined.

#### Example: Using Preset

```python
import asyncio
from gllm_core.schema import Chunk
from gllm_generation.response_synthesizer import ResponseSynthesizer

query = "What is the history of Python?"
chunks = [
    Chunk(content="Python was created in 1991 by Guido van Rossum."),
    Chunk(content="Python 2.0 was released in 2000 with new features."),
    Chunk(content="Python 3.0 was released in 2008, breaking backward compatibility.")
]

# Using preset with default refine configuration
synthesizer = ResponseSynthesizer.refine_preset(
    model_id="openai/gpt-5",
    batch_size=1,  # Process one chunk at a time
    stream_drafts=False  # Only stream the final response
)

response = asyncio.run(synthesizer.synthesize(query=query, chunks=chunks))
print(response)
```

#### Example: Custom Configuration

```python
from gllm_inference.request_processor import build_lm_request_processor
from gllm_generation.response_synthesizer.strategy import RefineSynthesisStrategy
from gllm_generation.response_synthesizer import ResponseSynthesizer

# Custom prompt for refinement
processor = build_lm_request_processor(
    model_id="openai/gpt-5",
    system_template="You are a helpful assistant that refines answers based on new information.",
    user_template="""Query: {query}

Current Answer:
{draft_response}

New Information:
{context}

Refine the current answer by incorporating the new information. If the new information contradicts the current answer, update it accordingly."""
)

strategy = RefineSynthesisStrategy(
    lm_request_processor=processor,
    batch_size=2,  # Process 2 chunks at a time
    stream_drafts=True  # Stream intermediate drafts
)

synthesizer = ResponseSynthesizer(strategy=strategy)
```

### 3. Static List

The **Static List** strategy generates responses by formatting a list of context items without using a language model. This is the most lightweight strategy as it doesn't require any LM calls. You can customize the formatter function by defining the `format_response_func` .

#### When to Use

Use the Static List strategy when:

1. You want to return retrieved chunks directly without LM processing.
2. You need fast responses without API costs.
3. Your use case requires only a simple list formatting (e.g., search results, document listings).
4. You want to display all retrieved context items to users.

#### Example: Using default configuration

```python
import asyncio
from gllm_core.schema import Chunk
from gllm_generation.response_synthesizer import ResponseSynthesizer
from gllm_generation.response_synthesizer.strategy import StaticListSynthesisStrategy

# Using default formatter
strategy = StaticListSynthesisStrategy()
synthesizer = ResponseSynthesizer(strategy=strategy)

chunks = [
    Chunk(content="Python is a high-level programming language."),
    Chunk(content="Python was created by Guido van Rossum."),
    Chunk(content="Python is known for its readability.")
]

response = asyncio.run(synthesizer.synthesize(chunks=chunks))

print(response)
```

**Expected Output:**

```
Here's what I found based on your query:
1. Python is a high-level programming language.
2. Python was created by Guido van Rossum.
3. Python is known for its readability.
```

---

#### Example: Using custom `format_response_func`

```python
import asyncio
from gllm_core.schema import Chunk
from gllm_generation.response_synthesizer import ResponseSynthesizer
from gllm_generation.response_synthesizer.strategy import StaticListSynthesisStrategy

# Using default formatter
strategy = StaticListSynthesisStrategy()
synthesizer = ResponseSynthesizer(strategy=strategy)

chunks = [
    Chunk(content="Python is a high-level programming language."),
    Chunk(content="Python was created by Guido van Rossum."),
    Chunk(content="Python is known for its readability.")
]

def format_chunks(items: list[str]) -> str:
    if not items:
        return "No content available."

    return "### Retrieved Information:\n" + "\n".join(f"- {item}" for item in items)


response = asyncio.run(synthesizer.synthesize(chunks=chunks, format_response_func=format_chunks))

print(response)
```

**Expected Output:**

```
#### Retrieved Information:
- Python is a high-level programming language.
- Python was created by Guido van Rossum.
- Python is known for its readability.
```

Congratulations! You've finished the tutorial to use the `ResponseSynthesizer`!

[^1]: This component may involve Language Model (LM). See tutorial about LM Request Processor or related [here](response-synthesizer.md#lm-request-processor)
